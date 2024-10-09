"""Prep 6 Synthesize

=== CSC148 Winter 2024 ===
Department of Mathematical and Computational Sciences,
University of Toronto Mississauga

=== Module Description ===
Your task in this prep is to implement each of the following recursive functions
on nested lists, using the following steps for *Recursive Function Design*:

1.  Identify the recursive structure of the input (in this case, always a nested
    list), and write down the code template for nested lists:

    def f(obj: Union[int, list]) -> ...:
        if isinstance(obj, int):
            ...
        else:
            ...
            for sublist in obj:
                ... f(sublist) ...
            ...

2.  Implement the base case(s) directly (in this case, a single integer).
3.  Write down a concrete example with a somewhat complex argument, (in this
    case, a nested list with around 3 sub-nested-lists), and then write down
    the relevant recursive calls and what they should return.
4.  Determine how to combine the recursive calls to compute the correct output.
    Make sure you can express this in English first, and then implement your
    idea.

HINT: The implementations here should be similar to ones you've seen
before in the readings or comprehension questions.
"""
from typing import Union


def num_positives(obj: Union[int, list]) -> int:
    """Return the number of positive integers in <obj>.

    Remember, 0 is *not* positive.

    >>> num_positives(17)
    1
    >>> num_positives(-10)
    0
    >>> num_positives([1, -2, [-10, 2, [3], 4, -5], 4])
    5
    """
    if isinstance(obj, int):
        if obj > 0:
            return 1
        return 0
    else:
        x = 0
        for sub_list in obj:
            x += num_positives(sub_list)
        return x


def nested_max(obj: Union[int, list]) -> int:
    """Return the maximum integer stored in nested list <obj>.

    Return 0 if <obj> is an empty list.

    Precondition: all integers in <obj> are positive.

    >>> nested_max(17)
    17
    >>> nested_max([1, 2, [1, 2, [3], 4, 5], 4])
    5
    """
    max_ = 0
    if isinstance(obj, int):
        max_ = max(obj, max_)
        return max_
    else:
        for sub_list in obj:
            max_ = max(nested_max(sub_list), max_)
        return max_


def max_length(obj: Union[int, list]) -> int:
    """Return the maximum length of any list in nested list <obj>.

    The *maximum length* of a nested list is defined as:
    1. 0, if <obj> is a number.
    2. The maximum of len(obj) and the lengths of the nested lists contained
       in <obj>, if <obj> is a list.

    >>> max_length(17)
    0
    >>> max_length([1, 2, [1, 2], 4])
    4
    >>> max_length([1, 2, [1, 2, [3], 4, 5], 4])
    5
    >>> max_length([1, 2, [1, 2, 3, 4, 5], 6, 7, [1, 2, 3, 4, 5]])
    6
    """
    max_ = 0
    if isinstance(obj, int):
        return 0
    else:
        max_ = len(obj)
        for sub_list in obj:
            max_ = max(max_length(sub_list), max_)
        return max_


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all()
