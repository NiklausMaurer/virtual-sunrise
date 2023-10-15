import itertools
import math
from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


@dataclass
class Leg:
    start: Point
    end: Point

    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end


class Path:
    def __init__(self, *args: Point):
        pairs = itertools.pairwise(args)
        self.legs = [Leg(start, end) for start, end in pairs]
        self.number_of_legs = len(self.legs)
        self.leg_duration = 1.0 / self.number_of_legs

    def __call__(self, t):
        leg_index = math.ceil(t / self.leg_duration) - 1
        leg = self.legs[leg_index]
        return Point(
            leg.start.x + (leg.end.x - leg.start.x) * (t - leg_index * self.leg_duration) / self.leg_duration,
            leg.start.y + (leg.end.y - leg.start.y) * (t - leg_index * self.leg_duration) / self.leg_duration,
        )
