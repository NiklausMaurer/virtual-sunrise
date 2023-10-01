import time


class Stopwatch:
    def __init__(self):
        self.start = time.perf_counter()

    def __call__(self):
        return time.perf_counter() - self.start
