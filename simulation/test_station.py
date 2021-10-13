"""
Process communication example

Covers:

- Resources: Store

Scenario:
  This example shows how to interconnect simulation model elements
  together using :class:`~simpy.resources.store.Store` for one-to-one,
  and many-to-one asynchronous processes. For one-to-many a simple
  BroadCastPipe class is constructed from Store.

When Useful:
  When a consumer process does not always wait on a generating process
  and these processes run asynchronously. This example shows how to
  create a buffer and also tell is the consumer process was late
  yielding to the event from a generating process.

  This is also useful when some information needs to be broadcast to
  many receiving processes

  Finally, using pipes can simplify how processes are interconnected to
  each other in a simulation model.

Example By:
  Keith Smith

"""
import pdb
import random

import simpy

from store import Store

RANDOM_SEED = 42
SIM_TIME = None


def message_generator(name, env, out_pipe):
    """A process which randomly generates messages."""
    for i in range(20):
        # wait for next transmission
        yield env.timeout(1)

        # messages are time stamped to later check if the consumer was
        # late getting them.  Note, using event.triggered to do this may
        # result in failure due to FIFO nature of simulation yields.
        # (i.e. if at the same env.now, message_generator puts a message
        # in the pipe first and then message_consumer gets from pipe,
        # the event.triggered will be True in the other order it will be
        # False
        msg = f"order: {i}"
        print(f"now: {env.now} generate: {msg}")
        if out_pipe.items:
            yield out_pipe.get_triggered()
            print(f"now: {env.now} put: {msg}")
            out_pipe.put(msg)
        else:
            print(f"now: {env.now} put: {msg}")
            out_pipe.put(msg)


def message_consumer(name, env, in_pipe):
    """A process which consumes messages."""
    while True:
        msg = yield in_pipe.peek()
        print(f"now: {env.now} cons {msg}")
        # Process does some other work, which may result in missing messages
        yield env.timeout(2)
        msg = yield in_pipe.get()
        print(f"now: {env.now} done: {msg}")

# Setup and start the simulation
print('Process communication')
random.seed(RANDOM_SEED)
env = simpy.Environment()

# For one-to-one or many-to-one type pipes, use Store
pipe = Store(env, capacity=1)
env.process(message_generator('Generator A', env, pipe))
env.process(message_consumer('Consumer A', env, pipe))

print('\nOne-to-one pipe communication\n')
env.run(until=SIM_TIME)

# # For one-to many use BroadcastPipe
# # (Note: could also be used for one-to-one,many-to-one or many-to-many)
# env = simpy.Environment()
# bc_pipe = BroadcastPipe(env)

# env.process(message_generator('Generator A', env, bc_pipe))
# env.process(message_consumer('Consumer A', env, bc_pipe.get_output_conn()))
# env.process(message_consumer('Consumer B', env, bc_pipe.get_output_conn()))

# print('\nOne-to-many pipe communication\n')
# env.run(until=SIM_TIME)