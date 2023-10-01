class Linear:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __call__(self, t):
        return self.start + (self.end - self.start) * t
