"""
    This file contains the implementation of the coefficients.
    Coefficients are used to calculate all the combinations of the categories (or values) of the attribute.
"""

from enum import Enum
from collections import deque
from itertools import chain, combinations, islice


def subsets(iterable, start=0, end=None):
    """Generates all subsets of the given set. Start and end parameters can be used to specify the range of subset sizes.

    Examples:
    >>> subsets([1, 2, 3])
    [(), (1,), (2,), (3,), (1,2), (1,3), (2,3), (1,2,3)]
    >>> subsets([1, 2, 3], 2)
    [(1, 2), (1, 3), (2, 3), (1, 2, 3)]
    >>> subsets([1, 2, 3], 2, 2)
    [(1, 2), (1, 3), (2, 3)]
    """
    s = list(iterable)
    if end is None:
        end = len(s) + 1
    else:
        # Closing the length selection interval.
        end += 1
    return chain.from_iterable(combinations(s, r) for r in range(start, end))


def sequences(iterable, start=1, end=None):
    """Generates all sequences of the given set. Start and end parameters can be used to specify the range of sequences sizes.

    Examples:
    >>> sequences([1, 2, 3])
    [(1,), (2,), (3,), (1, 2), (2, 3), (1, 2, 3)]
    >>> sequences([1, 2, 3, 4], 2, 3)
    [(1, 2), (2, 3), (3, 4), (1, 2, 3), (2, 3, 4)]
    """
    s = list(iterable)
    if end is None:
        end = len(s) + 1
    else:
        # Closing the length selection interval.
        end += 1
    return chain.from_iterable(sliding_window(s, r) for r in range(start, end))


def sliding_window(iterable, n):
    """Collect data into overlapping fixed-length chunks or blocks.

    Examples:
    >>> sliding_window([1, 2, 3, 4, 5], 2)
    [(1, 2), (2, 3), (3, 4), (4, 5)]
    """
    iterator = iter(iterable)
    window = deque(islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)


# The One Category that rule them all.
def one_category(value):
    """Returns one specified attribute category.

    Examples:
    >>> one_category([1])
    [(1)]
    """
    return [(value)]


class CoefficientType(Enum):
    "Enum structure that contains all the coefficient."
    SUBSET = subsets
    SEQUENCE = sequences
    ONE_CATEGORY = one_category


class Coefficient:
    "Abstract class that represents the coefficient."
    def __init__(self, start=1, end=None):
        self.start = start
        self.end = end

    def get(self, data):
        """Returns the coefficient of the given data. The data is a list of categories (or values) of the attribute."""
        raise NotImplementedError

    def __str__(self):
        return f"Coefficient({self.__class__.__name__})"


class Subset(Coefficient):
    "Generates all subsets of the attribute's category set."
    def __init__(self, start=1, end=None):
        super().__init__(start, end)

    def get(self, data):
        return subsets(data, self.start, self.end)


class Sequence(Coefficient):
    "Generates all sequences of the attribute's category set."
    def __init__(self, start=1, end=None):
        super().__init__(start, end)

    def get(self, data):
        return sequences(data, self.start, self.end)


class OneCategory(Coefficient):
    "Returns one specified attribute category."
    def __init__(self, category):
        self.category = category
        self.start = 1
        self.end = 1

    def get(self, data):
        return one_category(self.category)
