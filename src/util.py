import numpy.linalg as linalg
from numpy.typing import ArrayLike


def normalize_sum(xs):
    """
    Normalizes a list to sum to 1.0
    """
    s = sum(xs)
    return list(map(lambda x: x / s, xs))

def lerp(x: float, y: float, t: float) -> float:
    """
    Performs linear interpolation between x and y, based on t.
    """

    # Hardcode y for t = 1, since the below formula is
    # apparently imprecise.
    if t == 1:
        return y
    return x + (y - x) * t
