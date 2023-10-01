from sunrise.curves.linear import Linear


class Step:
    def __init__(self, start, end, step_start, step_end):
        self.start = start
        self.end = end
        self.step_start = step_start
        self.step_end = step_end
        self.step = Linear(start, end)

    def __call__(self, t):
        if t < self.step_start:
            return self.start
        elif t < self.step_end:
            return (self.start
                    + ((t - self.step_start) / (self.step_end - self.step_start)) * (self.end - self.start))
        else:
            return self.end
