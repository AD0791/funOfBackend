import selectors
import socket
from collections import deque

# A simple selector for managing I/O events
selector = selectors.DefaultSelector()

class EventLoop:
    def __init__(self):
        self.ready = deque()

    def run_until_complete(self, coro):
        task = Task(coro)
        self.ready.append(task)
        while self.ready:
            task = self.ready.popleft()
            try:
                fut = next(task.coro)
                fut.add_done_callback(self.ready.append)
            except StopIteration:
                continue

    def add_to_queue(self, task):
        self.ready.append(task)

class Task:
    def __init__(self, coro):
        self.coro = coro

    def add_done_callback(self, callback):
        callback(self)

class Future:
    def __init__(self):
        self.result = None
        self.callbacks = []

    def set_result(self, result):
        self.result = result
        for callback in self.callbacks:
            callback(self)

    def add_done_callback(self, callback):
        self.callbacks.append(callback)

# Example of a coroutine
async def example_coro():
    print("Step 1")
    await sleep(1)
    print("Step 2")

def sleep(delay):
    fut = Future()
    selector.register(0, selectors.EVENT_READ, fut.set_result)  # Mock selector registration
    return fut

# Running the event loop
event_loop = EventLoop()
event_loop.run_until_complete(example_coro())
