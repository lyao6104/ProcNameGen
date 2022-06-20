from typing import List

import numpy.linalg as linalg
from numpy.typing import ArrayLike


def normalize_sum(xs):
    """
    Normalizes a list to sum to 1.0
    """
    s = sum(xs)
    return list(map(lambda x: x / s, xs))
