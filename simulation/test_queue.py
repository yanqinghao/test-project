import random
import simpy
from queue import Store

RANDOM_SEED = 42
SIM_TIME = None

def do_move(name, env, out_pipe, msg):
    print(f"name: {name}, time: {env.now}, start run {msg}")
    yield env.timeout(20)
    out_pipe.push(msg)


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
        if all(out_pipe.processing_queue):
            yield out_pipe.get_triggered()
            print(f"now: {env.now} put: {msg}")
            out_pipe.put(msg)
            print(f"now: {env.now} queue: {out_pipe.processing_queue}")
            env.process(do_move(f"Mover {i}", env, out_pipe, msg))
        else:
            print(f"now: {env.now} put: {msg}")
            out_pipe.put(msg)
            print(f"now: {env.now} queue: {out_pipe.processing_queue}")
            env.process(do_move(f"Mover {i}", env, out_pipe, msg))


# def message_getter(name, env, in_pipe):
#     """A process which consumes messages."""
#     while True:
#         print(f"before get: {env.now} {in_pipe.queue}")
#         msg = yield in_pipe.get()
#         print(f"after get: {env.now} get: {msg} queue: {in_pipe.queue}")


# def queue_mover(name, env, in_pipe):
#     """A process which consumes messages."""
#     while True:
#         # print(f"before shift: {env.now} {in_pipe.queue}")
#         msg = yield in_pipe.move()
#         if msg:
#           print(f"after shift: {env.now} shift: {msg} queue: {in_pipe.processing_queue}")


def queue_poper(name, env, in_pipe):
    """A process which consumes messages."""
    while True:
        # print(f"before pop: {env.now} {in_pipe.queue}")
        msg = yield in_pipe.pop()
        print(f"after pop: {env.now} pop: {msg} queue: {in_pipe.processing_queue}")


# Setup and start the simulation
print('Process communication')
random.seed(RANDOM_SEED)
env = simpy.Environment()

# For one-to-one or many-to-one type pipes, use Store
pipe = Store(env, capacity=1, length=10)
env.process(message_generator('Generator A', env, pipe))
# env.process(message_getter('Getter A', env, pipe))
env.process(queue_poper('Poper A', env, pipe))

print('\nqueue communication\n')
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