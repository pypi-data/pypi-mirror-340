# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0

import asyncio

import pytest

import agp_bindings


@pytest.mark.asyncio
@pytest.mark.parametrize("server", ["127.0.0.1:12344"], indirect=True)
async def test_end_to_end(server):
    # create 2 clients, Alice and Bob
    svc_alice = await agp_bindings.create_pyservice("cisco", "default", "alice", 1234)
    svc_alice.configure(agp_bindings.GatewayConfig(endpoint="http://127.0.0.1:12344"))

    svc_bob = await agp_bindings.create_pyservice("cisco", "default", "bob", 1234)
    svc_bob.configure(agp_bindings.GatewayConfig(endpoint="http://127.0.0.1:12344"))

    # connect to the service
    conn_id_alice = await agp_bindings.connect(svc_alice)
    conn_id_bob = await agp_bindings.connect(svc_bob)

    # subscribe alice and bob
    alice_class = agp_bindings.PyAgentType("cisco", "default", "alice")
    bob_class = agp_bindings.PyAgentType("cisco", "default", "bob")
    await agp_bindings.subscribe(svc_alice, conn_id_alice, alice_class, 1234)
    await agp_bindings.subscribe(svc_bob, conn_id_bob, bob_class, None)

    # set routes
    await agp_bindings.set_route(svc_alice, conn_id_alice, bob_class, None)

    # create fire and forget session
    session_info = await agp_bindings.create_ff_session(svc_alice, agp_bindings.PyFireAndForgetConfiguration())

    # send msg from Alice to Bob
    msg = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    await agp_bindings.publish(svc_alice, session_info, 1, msg, bob_class, None)

    # receive message from Alice
    session_info_ret, msg_rcv = await agp_bindings.receive(svc_bob)

    # make seure the session id corresponds
    assert session_info_ret.id == session_info.id

    # check if the message is correct
    assert msg_rcv == bytes(msg)

    # reply to Alice
    await agp_bindings.publish(svc_bob, session_info_ret, 1, msg_rcv)

    # wait for message
    session_info_ret, msg_rcv = await agp_bindings.receive(svc_alice)

    print(msg_rcv)

    # check if the message is correct
    assert msg_rcv == bytes(msg)

    # disconnect alice
    await agp_bindings.disconnect(svc_alice, conn_id_alice)

    # disconnect bob
    await agp_bindings.disconnect(svc_bob, conn_id_bob)


@pytest.mark.asyncio
@pytest.mark.parametrize("server", ["127.0.0.1:12345"], indirect=True)
async def test_gateway_wrapper(server):
    org = "cisco"
    ns = "default"
    agent1 = "gateway1"

    # create new gateway object
    gateway1 = await agp_bindings.Gateway.new(org, ns, agent1)
    gateway1.configure(agp_bindings.GatewayConfig(endpoint="http://127.0.0.1:12345", insecure=True))

    # Connect to the service and subscribe for the local name
    _ = await gateway1.connect()

    # # subscribe to the service
    # await gateway1.subscribe(org, ns, agent1)

    # create second local agent
    agent2 = "gateway2"
    gateway2 = await agp_bindings.Gateway.new(org, ns, agent2)
    gateway2.configure(agp_bindings.GatewayConfig(endpoint="http://127.0.0.1:12345", insecure=True))

    # Connect to gateway server
    _ = await gateway2.connect()

    # set route
    await gateway2.set_route("cisco", "default", agent1)

    # create session
    session_info = await gateway2.create_ff_session(agp_bindings.PyFireAndForgetConfiguration())

    async with gateway1, gateway2:
        # publish message
        msg = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        await gateway2.publish(session_info, msg, org, ns, agent1)

        # wait for a new session
        session_info_rec, _ = await gateway1.receive()

        # new session received! listen for the message
        session_info_rec, msg_rcv = await gateway1.receive(session=session_info_rec.id)

        # check if the message is correct
        assert msg_rcv == bytes(msg)

        # make sure the session info is correct
        assert session_info.id == session_info_rec.id

        # reply to Alice
        await gateway1.publish_to(session_info_rec, msg_rcv)

        # wait for message
        _, msg_rcv = await gateway2.receive(session=session_info.id)

        # check if the message is correct
        assert msg_rcv == bytes(msg)


@pytest.mark.asyncio
@pytest.mark.parametrize("server", ["127.0.0.1:12346"], indirect=True)
async def test_auto_reconnect_after_server_restart(server):
    svc_alice = await agp_bindings.create_pyservice("cisco", "default", "alice", 1234)
    svc_alice.configure(agp_bindings.GatewayConfig(endpoint="http://127.0.0.1:12346"))

    svc_bob = await agp_bindings.create_pyservice("cisco", "default", "bob", 1234)
    svc_bob.configure(agp_bindings.GatewayConfig(endpoint="http://127.0.0.1:12346"))

    # connect clients and subscribe for messages
    conn_id_alice = await agp_bindings.connect(svc_alice)
    conn_id_bob = await agp_bindings.connect(svc_bob)

    alice_class = agp_bindings.PyAgentType("cisco", "default", "alice")
    bob_class = agp_bindings.PyAgentType("cisco", "default", "bob")
    await agp_bindings.subscribe(svc_alice, conn_id_alice, alice_class, 1234)
    await agp_bindings.subscribe(svc_bob, conn_id_bob, bob_class, 1234)

    # set routing from Alice to Bob
    await agp_bindings.set_route(svc_alice, conn_id_alice, bob_class, None)

    # create fire and forget session
    session_info = await agp_bindings.create_ff_session(svc_alice, agp_bindings.PyFireAndForgetConfiguration())

    # verify baseline message exchange before the simulated server restart
    baseline_msg = [1, 2, 3]
    await agp_bindings.publish(svc_alice, session_info, 1, baseline_msg, bob_class, None)

    _, received = await agp_bindings.receive(svc_bob)
    assert received == bytes(baseline_msg)

    # restart the server
    await agp_bindings.stop(server)
    await asyncio.sleep(3)  # allow time for the server to fully shut down
    await agp_bindings.serve(server)
    await asyncio.sleep(2)  # allow time for automatic reconnection

    # test that the message exchange resumes normally after the simulated restart
    test_msg = [4, 5, 6]
    await agp_bindings.publish(svc_alice, session_info, 1, test_msg, bob_class, None)
    _, received = await agp_bindings.receive(svc_bob)
    assert received == bytes(test_msg)

    # clean up
    await agp_bindings.disconnect(svc_alice, conn_id_alice)
    await agp_bindings.disconnect(svc_bob, conn_id_bob)


@pytest.mark.asyncio
@pytest.mark.parametrize("server", ["127.0.0.1:12347"], indirect=True)
async def test_error_on_nonexistent_subscription(server):
    svc_alice = await agp_bindings.create_pyservice("cisco", "default", "alice", 1234)
    svc_alice.configure(agp_bindings.GatewayConfig(endpoint="http://127.0.0.1:12347"))

    # connect client and subscribe for messages
    conn_id_alice = await agp_bindings.connect(svc_alice)
    alice_class = agp_bindings.PyAgentType("cisco", "default", "alice")
    await agp_bindings.subscribe(svc_alice, conn_id_alice, alice_class, 1234)

    # create fire and forget session
    session_info = await agp_bindings.create_ff_session(svc_alice, agp_bindings.PyFireAndForgetConfiguration())

    # create Bob's agent class, but do not instantiate or subscribe Bob
    bob_class = agp_bindings.PyAgentType("cisco", "default", "bob")

    # publish a message from Alice intended for Bob (who is not there)
    msg = [7, 8, 9]
    await agp_bindings.publish(svc_alice, session_info, 1, msg, bob_class, None)

    # an exception should be raised on receive
    try:
        _, src, received = await asyncio.wait_for(agp_bindings.receive(svc_alice), timeout=5)
    except asyncio.TimeoutError:
        pytest.fail("timed out waiting for error message on receive channel")
    except Exception as e:
        assert "no matching found" in str(e), f"Unexpected error message: {str(e)}"
    else:
        pytest.fail(f"Expected an exception, but received message: {received}")

    # clean up
    await agp_bindings.disconnect(svc_alice, conn_id_alice)
