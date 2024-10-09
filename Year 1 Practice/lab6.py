"""
UTM: CSC108, Fall 2023

Practical Lab 6

Instructors: Michael Liut, Marc De Benedetti, Rutwa Engineer, Akshay Arun Bapat

This code is provided solely for the personal and private use of
students taking the CSC108 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2023 Michael Liut, Haocheng Hu

LAB RESTRICTIONS, PLEASE READ:
Do not add any imports, the ones that you need will be given to you.
You may not use any dictionaries or dictionary methods.
Do not use try-except statements, you should be able to anticipate
or prevent any errors from happening at all!
"""

from typing import Any, List


def loopy_madness_with_while_loops(string1: str, string2: str) -> str:
    """
    The exact same function as loopy_madness from Lab 5, but we ask that you
    change any for loops that you used to while loops. Refer back to Lab 5 for
    the specifications of this function.

    You are NOT allowed to use any for loops for this function.
    >>> loopy_madness_with_while_loops("abcdefghijklmno", "123")
    'a1b2c3d2e1f2g3h2i1j2k3l2m1n2o3'
    >>> loopy_madness_with_while_loops("123", "abcdefghijklmno")
    '1a2b3c2d1e2f3g2h1i2j3k2l1m2n3o'
    >>> loopy_madness_with_while_loops("aa", "1")
    'a1a1'
    >>> loopy_madness_with_while_loops("abcde", "12")
    'a1b2c1d2e1'
    >>> loopy_madness_with_while_loops("abcdfe", "123")
    'a1b2c3d2f1e2'
    >>> loopy_madness_with_while_loops("abc", "123")
    'a1b2c3'
    """
    if len(string1) > len(string2):
        string2 = ((string2 + string2[len(string2) - 2: 0: -1])
                   * ((len(string1) + 1) // len(string2)))
    elif len(string2) > len(string1):
        string1 = ((string1
                    + string1[len(string1) - 2: 0: -1])
                   * ((len(string2) + 1) // len(string1)))
    acc = ""
    i = 0
    while i < min(len(string1), len(string2)):
        acc += string1[i] + string2[i]
        i += 1
    return acc


def longest_chain(lst: List[int]) -> int:
    """
    Given a list of integers, return the length of the longest chain of 1's
    that start from the beginning.

    You MUST use a while loop for this, and are not allowed to use a for loop.

    Hint: A good way to start is to define a stopping condition, and have a
    variable that keeps track of how many 1's you've seen thus far, if any.

    Precondition: <lst> will only contain the integers 1 and 0.

    >>> longest_chain([1, 1, 0])
    2
    >>> longest_chain([0, 1, 1])
    0
    >>> longest_chain([1, 0, 1, 1])
    1
    >>> longest_chain([1, 1, 1, 1, 1, 1, 1, 1, 1])
    9
    >>> longest_chain([1, 0, 0, 1, 1])
    1
    """
    length = 0
    stop = False
    i = 0
    while i < len(lst):
        if not stop:
            if lst[i] == 1:
                length += 1
            else:
                stop = True
        i += 1
    return length


def count_types(lst: List[Any]) -> List[int]:
    """
    Given a list <lst> of random types, return the number of occurrences of
    each type, in the form of a list, in the order that they were first seen.

    For example, if the input ['str1', 1, 'str2'], the output would be [2, 1],
    as a string type appears first, and occurs twice in the list. An integer
    type appears next, and only occurs once in the list.

    Another example could be [True, 'str1', 1, False, 'str2', True], where the
    output would be [3, 2, 1], as a boolean type appears first, and occurs
    three times in the list. A string appears next, and occurs twice in the
    list. Finally, an integer appears next, and occurs once in the list.

    Do not modify the input list.
    >>> count_types([True, 'str1', 1, False, 'str2', True])
    [3, 2, 1]
    >>> count_types([])
    []
    >>> count_types([42])
    [1]
    >>> count_types(['str1', 1, 'str2', 2, 'str3', 3, 'str4', 4])
    [4, 4]
    >>> count_types([1, 'str', 3.14, True, None])
    [1, 1, 1, 1, 1]
    """
    counts = []
    list_of_types = []
    for char in lst:
        if type(char) not in list_of_types:
            list_of_types.append(type(char))
            counts.append(1)
        else:
            x = list_of_types.index(type(char))
            counts[x] += 1
    return counts


def second_largest(lst: List[int]) -> int:
    """
    Given a list <lst> of integers, return the second largest item in the list
    without modifying <lst>. You cannot use any of python's builtin sorting
    functions. Do not attempt to sort the list yourself either.

    As a sanity check, you can ensure that your function returns what
    "return sorted(lst)[-2]" would. (DO NOT COPY THIS)

    For example, an input [1, 2, 3] should return an output of 2, since 2 is
    the second largest integer in the list.

    Note that when we say second largest, we do not mean second largest
    distinct element. That means that [1, 2, 4, 4] should return 4, not 2.

    Precondition: the input list has at least 2 elements.

    Something extra to think about (not graded): is it possible to write this
    function with an extra argument <n> and return the nth largest number in
    the list? Can you do this without sorting the list?
    >>> second_largest([1, 2, 3, 4, 5])
    4
    >>> second_largest([4, 4, 1, 3, 2])
    4
    >>> second_largest([1, 1, 1])
    1
    >>> second_largest([1, 2, 4, 4])
    4
    >>> second_largest([1, 3])
    1
    >>> second_largest([1, 2, 3])
    2
    >>> second_largest([-1, -2, -3, -4, 0])
    -1
    """
    new_list = lst[:]
    if len(new_list) == 2:
        return min(new_list)

    x = max(new_list)
    new_list.remove(x)
    return max(new_list)
