import math


def project_integer(curve, duration_seconds, t_seconds):
    if t_seconds > duration_seconds:
        return None
    return math.floor(curve(t_seconds / duration_seconds))


def project(curve, duration_seconds, t_seconds):
    if t_seconds > duration_seconds:
        return None
    return curve(t_seconds / duration_seconds)
