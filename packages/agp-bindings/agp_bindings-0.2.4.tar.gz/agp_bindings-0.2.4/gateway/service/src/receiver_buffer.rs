// SPDX-FileCopyrightText: Copyright (c) 2025 Cisco and/or its affiliates.
// SPDX-License-Identifier: Apache-2.0

use std::collections::HashSet;

use agp_datapath::pubsub::proto::pubsub::v1::Message;

use thiserror::Error;
use tracing::{debug, error, info, trace};

#[derive(Error, Debug, PartialEq)]
pub enum ReceiverBufferError {
    #[error("Error processing received message: {0}")]
    ProcessingError(String),
}

pub(crate) struct ReceiverBuffer {
    // ID of the last packet sent to the application
    // Init to usize max and it takes the values of the first
    // packet received in the buffer
    last_sent: usize,
    // First valid entry in the buffer. Packets may be
    // removed from the front of the buffer and we want to
    // avoid copies. This pointer keeps track of the valid entries
    first_entry: usize,
    // set of messages definitely lost that cannot be recoverd
    // anymore using RTX messages
    lost_msgs: HashSet<usize>,
    // Buffer of valid messages received Out-of-Order (OOO)
    // waiting to be delivered to the application
    // The first valid entry of the buffer always corresponds to
    // last_sent + 1
    buffer: Vec<Option<Message>>,
}

impl Default for ReceiverBuffer {
    fn default() -> Self {
        ReceiverBuffer {
            last_sent: usize::MAX,
            first_entry: 0,
            lost_msgs: HashSet::new(),
            buffer: vec![],
        }
    }
}

impl ReceiverBuffer {
    // returns a vec of messages to send to the application
    // in case the vector contains a None it means that the packet is lost
    // and cannot be recovered. the second vector contains the ids of the
    // packets lost that requires an RTX. If both vectors are empty the
    // caller has nothing to do
    pub fn on_received_message(
        &mut self,
        msg: Message,
    ) -> Result<(Vec<Option<Message>>, Vec<u32>), ReceiverBufferError> {
        let msg_id = msg.get_id() as usize;

        debug!("Received message id {}", msg_id);
        // no loss detected, return message
        // if this is the first packet received (case last_sent == usize::MAX) we consider it
        // valid one and the buffer is initialized accordingly. in this way a stream can start from
        // a random number or it can be joined at any time
        if self.last_sent == usize::MAX
            || (msg_id == (self.last_sent + 1)) && (self.buffer.is_empty())
        {
            debug!("No loss detected, return message {}", msg_id);
            self.last_sent = msg_id;
            return Ok((vec![Some(msg)], vec![]));
        }

        // the message is an OOO check what to do with the message
        if msg_id <= self.last_sent {
            // this message is not useful anymore because we have already sent
            // content for this ID to the application. It can be a duplicated
            // msg or a message that arrived too late. Log and drop
            info!("Received possibly DUP message, drop it");
            return Ok((vec![], vec![]));
        }

        if self.buffer.is_empty() {
            // init the buffer and send required rtx
            self.first_entry = 0;
            // fill the buffer with an empty entry for each hole
            // detected in the message stream
            self.buffer = vec![None; msg_id - (self.last_sent + 1)];
            debug!("Losses found, missing {} packets", self.buffer.len());
            self.buffer.push(Some(msg));
            let mut rtx: Vec<u32> = Vec::new();
            for i in (self.last_sent + 1)..(msg_id) {
                trace!("add {} to rtx vector", i);
                rtx.push(i as u32);
            }

            Ok((vec![], rtx))
        } else {
            debug!(
                "buffer is not empty and received OOO packet {}, process it",
                msg_id
            );
            trace!(
                "buffer status: last sent {}, first entry {}, len {}",
                self.last_sent,
                self.first_entry,
                self.buffer.len()
            );
            // check if the msg_id fits inside the buffer range
            if msg_id <= (self.last_sent + (self.buffer.len() - self.first_entry)) {
                debug!(
                    "message {} is inside the buffer range {} - {}",
                    msg_id,
                    (self.last_sent + 1),
                    (self.buffer.len() - self.first_entry)
                );
                // find the position of the message in the buffer
                let pos = msg_id - (self.last_sent + 1) + self.first_entry;
                debug!("try to insert message {} at pos {}", msg_id, pos);
                if self.buffer[pos].is_some() {
                    // this is a duplicate message, drop it and do nothing
                    info!("Received DUP message, drop it");
                    return Ok((vec![], vec![]));
                }
                debug!(
                    "add message {} at pos {} and try to release msgs",
                    msg_id, pos
                );
                // add the message to the buffer and check if it is possible
                // to send some message to the application
                self.buffer[pos] = Some(msg);

                // return the messages if possible
                Ok((self.release_msgs(), vec![]))
            } else {
                // the message is out of the current buffer
                // add more entries to it and return an empty vec
                // the next id to add at the end of the buffer is
                // ((self.last_sent + 1) + (self.buffer.len() - self.first_entry))
                // loop up to msg_id - 1 (the last element is not in the range)
                let mut rtx = Vec::new();
                for i in ((self.last_sent + 1) + (self.buffer.len() - self.first_entry))..msg_id {
                    self.buffer.push(None);
                    rtx.push(i as u32);
                    debug!("detect packet loss {} to add at the end of the buffer", i);
                }
                debug!("add packet {} at the end of the buffer", msg_id);
                self.buffer.push(Some(msg));
                Ok((vec![], rtx))
            }
        }
    }

    pub fn on_lost_message(
        &mut self,
        msg_id: u32,
    ) -> Result<Vec<Option<Message>>, ReceiverBufferError> {
        debug!("message {} is definitely lost", msg_id);
        self.lost_msgs.insert(msg_id as usize);
        Ok(self.release_msgs())
    }

    fn release_msgs(&mut self) -> Vec<Option<Message>> {
        let mut i = self.first_entry;
        let mut ret = vec![];
        while i < self.buffer.len() {
            if self.buffer[i].is_some() {
                // this message can be sent to the app
                ret.push(self.buffer[i].take());
                // increase last_sent on first_entry
                self.last_sent += 1;
                self.first_entry += 1;
                debug!(
                    "return message at pos {}, new buffer state: last_sent {}, first_index {}",
                    i, self.last_sent, self.first_entry
                );
            } else {
                // check is the mgs id is in the set of lost messages
                // the id of the message to look for is self.last_sent + 1
                if self.lost_msgs.contains(&(self.last_sent + 1)) {
                    // this message cannot be recovered anymore
                    // add a None in the ret vec and release it
                    ret.push(None);
                    self.lost_msgs.remove(&(self.last_sent + 1));
                    // increase all counters anyway because this
                    // position of the buffer will not be used anymore
                    self.last_sent += 1;
                    self.first_entry += 1;
                    debug!(
                        "message {} is lost, return none, new buffer state: last_sent {}, first_index {}",
                        self.last_sent, self.last_sent, self.first_entry
                    );
                } else {
                    // we need to wait a bit more
                    break;
                }
            }
            i += 1;
        }
        // check if the buffer is now empty
        if self.first_entry == self.buffer.len() {
            debug!("clean reception buffer which is empty now");
            // rest the buffer
            self.first_entry = 0;
            self.buffer = vec![];
        }
        // check if the next message in line is the lost set
        // this should never happen in reality
        let mut stop = false;
        while !stop {
            if self.lost_msgs.contains(&(self.last_sent + 1)) {
                self.last_sent += 1;
                ret.push(None);
                self.lost_msgs.remove(&(self.last_sent));
                debug!(
                    "found another lost message to release, last_sent {}",
                    self.last_sent
                );
            } else {
                stop = true;
            }
        }
        ret
    }
}

// tests
#[cfg(test)]
mod tests {
    use agp_datapath::messages::encoder::{Agent, AgentType};
    use agp_datapath::pubsub::proto::pubsub::v1::SessionHeaderType;
    use agp_datapath::pubsub::{AgpHeader, SessionHeader};
    use tracing_test::traced_test;

    use super::*;

    #[test]
    #[traced_test]
    fn test_receiver_buffer() {
        let src = Agent::from_strings("org", "ns", "type", 0);
        let name_type = AgentType::from_strings("org", "ns", "type");

        let agp_header = AgpHeader::new(&src, &name_type, Some(1), None);

        let h0 = SessionHeader::new(SessionHeaderType::Fnf.into(), 0, 0);
        let h1 = SessionHeader::new(SessionHeaderType::Fnf.into(), 0, 1);
        let h2 = SessionHeader::new(SessionHeaderType::Fnf.into(), 0, 2);
        let h3 = SessionHeader::new(SessionHeaderType::Fnf.into(), 0, 3);
        let h4 = SessionHeader::new(SessionHeaderType::Fnf.into(), 0, 4);
        let h5 = SessionHeader::new(SessionHeaderType::Fnf.into(), 0, 5);

        let p0 = Message::new_publish_with_headers(Some(agp_header), Some(h0), "", vec![]);
        let p1 = Message::new_publish_with_headers(Some(agp_header), Some(h1), "", vec![]);
        let p2 = Message::new_publish_with_headers(Some(agp_header), Some(h2), "", vec![]);
        let p3 = Message::new_publish_with_headers(Some(agp_header), Some(h3), "", vec![]);
        let p4 = Message::new_publish_with_headers(Some(agp_header), Some(h4), "", vec![]);
        let p5 = Message::new_publish_with_headers(Some(agp_header), Some(h5), "", vec![]);

        // insert in order
        let mut buffer = ReceiverBuffer::default();

        let ret = buffer.on_received_message(p0.clone());
        assert!(ret.is_ok());
        let (recv, rtx) = ret.unwrap();
        assert_eq!(recv.len(), 1);
        assert_eq!(rtx.len(), 0);
        assert_eq!(recv[0], Some(p0.clone()));

        let ret = buffer.on_received_message(p1.clone());
        assert!(ret.is_ok());
        let (recv, rtx) = ret.unwrap();
        assert_eq!(recv.len(), 1);
        assert_eq!(rtx.len(), 0);
        assert_eq!(recv[0], Some(p1.clone()));

        let ret = buffer.on_received_message(p2.clone());
        assert!(ret.is_ok());
        let (recv, rtx) = ret.unwrap();
        assert_eq!(recv.len(), 1);
        assert_eq!(rtx.len(), 0);
        assert_eq!(recv[0], Some(p2.clone()));

        let ret = buffer.on_received_message(p3.clone());
        assert!(ret.is_ok());
        let (recv, rtx) = ret.unwrap();
        assert_eq!(recv.len(), 1);
        assert_eq!(rtx.len(), 0);
        assert_eq!(recv[0], Some(p3.clone()));

        let ret = buffer.on_received_message(p4.clone());
        assert!(ret.is_ok());
        let (recv, rtx) = ret.unwrap();
        assert_eq!(recv.len(), 1);
        assert_eq!(rtx.len(), 0);
        assert_eq!(recv[0], Some(p4.clone()));

        // insert in order but skip first packets
        let mut buffer = ReceiverBuffer::default();

        let ret = buffer.on_received_message(p2.clone());
        assert!(ret.is_ok());
        let (recv, rtx) = ret.unwrap();
        assert_eq!(recv.len(), 1);
        assert_eq!(rtx.len(), 0);
        assert_eq!(recv[0], Some(p2.clone()));

        let ret = buffer.on_received_message(p3.clone());
        assert!(ret.is_ok());
        let (recv, rtx) = ret.unwrap();
        assert_eq!(recv.len(), 1);
        assert_eq!(rtx.len(), 0);
        assert_eq!(recv[0], Some(p3.clone()));

        let ret = buffer.on_received_message(p4.clone());
        assert!(ret.is_ok());
        let (recv, rtx) = ret.unwrap();
        assert_eq!(recv.len(), 1);
        assert_eq!(rtx.len(), 0);
        assert_eq!(recv[0], Some(p4.clone()));

        // receive DUP packets and old packets
        let mut buffer = ReceiverBuffer::default();

        let ret = buffer.on_received_message(p4.clone());
        assert!(ret.is_ok());
        let (recv, rtx) = ret.unwrap();
        assert_eq!(recv.len(), 1);
        assert_eq!(rtx.len(), 0);
        assert_eq!(recv[0], Some(p4.clone()));

        let ret = buffer.on_received_message(p4.clone());
        assert!(ret.is_ok());
        let (recv, rtx) = ret.unwrap();
        assert_eq!(recv.len(), 0);
        assert_eq!(rtx.len(), 0);

        let ret = buffer.on_received_message(p0.clone());
        assert!(ret.is_ok());
        let (recv, rtx) = ret.unwrap();
        assert_eq!(recv.len(), 0);
        assert_eq!(rtx.len(), 0);

        // insertion order 1, 4, 4, 2, 2, 3
        let mut buffer = ReceiverBuffer::default();

        // release 1
        let ret = buffer.on_received_message(p1.clone());
        assert!(ret.is_ok());
        let (recv, rtx) = ret.unwrap();
        assert_eq!(recv.len(), 1);
        assert_eq!(rtx.len(), 0);
        assert_eq!(recv[0], Some(p1.clone()));

        // detect loss for 2 and 3
        let ret = buffer.on_received_message(p4.clone());
        assert!(ret.is_ok());
        let (recv, rtx) = ret.unwrap();
        assert_eq!(recv.len(), 0);
        assert_eq!(rtx.len(), 2);
        assert_eq!(rtx[0], 2);
        assert_eq!(rtx[1], 3);

        // DUP packet, return nothing
        let ret = buffer.on_received_message(p4.clone());
        assert!(ret.is_ok());
        let (recv, rtx) = ret.unwrap();
        assert_eq!(recv.len(), 0);
        assert_eq!(rtx.len(), 0);

        // release packet 2
        let ret = buffer.on_received_message(p2.clone());
        assert!(ret.is_ok());
        let (recv, rtx) = ret.unwrap();
        assert_eq!(recv.len(), 1);
        assert_eq!(rtx.len(), 0);
        assert_eq!(recv[0], Some(p2.clone()));

        // Old packet, return nothing
        let ret = buffer.on_received_message(p2.clone());
        assert!(ret.is_ok());
        let (recv, rtx) = ret.unwrap();
        assert_eq!(recv.len(), 0);
        assert_eq!(rtx.len(), 0);

        // release packet 3 and 4
        let ret = buffer.on_received_message(p3.clone());
        assert!(ret.is_ok());
        let (recv, rtx) = ret.unwrap();
        assert_eq!(recv.len(), 2);
        assert_eq!(rtx.len(), 0);
        assert_eq!(recv[0], Some(p3.clone()));
        assert_eq!(recv[1], Some(p4.clone()));

        // insertion order 0, 2, 5, 2, 3, 4, 1
        let mut buffer = ReceiverBuffer::default();

        // release 0
        let ret = buffer.on_received_message(p0.clone());
        assert!(ret.is_ok());
        let (recv, rtx) = ret.unwrap();
        assert_eq!(recv.len(), 1);
        assert_eq!(rtx.len(), 0);
        assert_eq!(recv[0], Some(p0.clone()));

        // detect loss for 1
        let ret = buffer.on_received_message(p2.clone());
        assert!(ret.is_ok());
        let (recv, rtx) = ret.unwrap();
        assert_eq!(recv.len(), 0);
        assert_eq!(rtx.len(), 1);
        assert_eq!(rtx[0], 1);

        // detect loss for 3 and 4
        let ret = buffer.on_received_message(p5.clone());
        assert!(ret.is_ok());
        let (recv, rtx) = ret.unwrap();
        assert_eq!(recv.len(), 0);
        assert_eq!(rtx.len(), 2);
        assert_eq!(rtx[0], 3);
        assert_eq!(rtx[1], 4);

        // dup 2 return nothing
        let ret = buffer.on_received_message(p2.clone());
        assert!(ret.is_ok());
        let (recv, rtx) = ret.unwrap();
        assert_eq!(recv.len(), 0);
        assert_eq!(rtx.len(), 0);

        // add 3 to the buffer
        let ret = buffer.on_received_message(p3.clone());
        assert!(ret.is_ok());
        let (recv, rtx) = ret.unwrap();
        assert_eq!(recv.len(), 0);
        assert_eq!(rtx.len(), 0);

        // add 4 to the buffer
        let ret = buffer.on_received_message(p4.clone());
        assert!(ret.is_ok());
        let (recv, rtx) = ret.unwrap();
        assert_eq!(recv.len(), 0);
        assert_eq!(rtx.len(), 0);

        // release 1, 2, 3, 4, 5
        let ret = buffer.on_received_message(p1.clone());
        assert!(ret.is_ok());
        let (recv, rtx) = ret.unwrap();
        assert_eq!(recv.len(), 5);
        assert_eq!(rtx.len(), 0);
        assert_eq!(recv[0], Some(p1.clone()));
        assert_eq!(recv[1], Some(p2.clone()));
        assert_eq!(recv[2], Some(p3.clone()));
        assert_eq!(recv[3], Some(p4.clone()));
        assert_eq!(recv[4], Some(p5.clone()));

        // insertion order 0, 2, 4, loss(1), 5, loss(3)
        let mut buffer = ReceiverBuffer::default();

        // release 0
        let ret = buffer.on_received_message(p0.clone());
        assert!(ret.is_ok());
        let (recv, rtx) = ret.unwrap();
        assert_eq!(recv.len(), 1);
        assert_eq!(rtx.len(), 0);
        assert_eq!(recv[0], Some(p0.clone()));

        // detect loss for 1
        let ret = buffer.on_received_message(p2.clone());
        assert!(ret.is_ok());
        let (recv, rtx) = ret.unwrap();
        assert_eq!(recv.len(), 0);
        assert_eq!(rtx.len(), 1);
        assert_eq!(rtx[0], 1);

        // detect loss for 3
        let ret = buffer.on_received_message(p4.clone());
        assert!(ret.is_ok());
        let (recv, rtx) = ret.unwrap();
        assert_eq!(recv.len(), 0);
        assert_eq!(rtx.len(), 1);
        assert_eq!(rtx[0], 3);

        // 1 is lost, return up to 2
        let ret = buffer.on_lost_message(1);
        assert!(ret.is_ok());
        let recv = ret.unwrap();
        assert_eq!(recv.len(), 2);
        assert_eq!(recv[0], None);
        assert_eq!(recv[1], Some(p2.clone()));

        // 5 is lost
        let ret = buffer.on_lost_message(5);
        assert!(ret.is_ok());
        let recv = ret.unwrap();
        assert_eq!(recv.len(), 0);

        // add 3, return up to 5
        let ret = buffer.on_received_message(p3.clone());
        assert!(ret.is_ok());
        let (recv, rtx) = ret.unwrap();
        assert_eq!(recv.len(), 3);
        assert_eq!(rtx.len(), 0);
        assert_eq!(recv[0], Some(p3.clone()));
        assert_eq!(recv[1], Some(p4.clone()));
        assert_eq!(recv[2], None);
    }
}
