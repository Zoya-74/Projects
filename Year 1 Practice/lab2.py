"""
UTM: CSC108, Fall 2023

Practical Lab 2

Instructors: Michael Liut, Marc De Benedetti, Rutwa Engineer, Akshay Arun Bapat

This code is provided solely for the personal and private use of
students taking the CSC108 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2023 Michael Liut, Haocheng Hu

Do not add any imports, the ones that you need will be given to you.
"""


def my_and(a: bool, b: bool) -> bool:
    """
    Return True if <a> and <b> are both True, ONLY using 'not' and 'or'.
    This means you CANNOT use operators like ==, bool(), and *, +, etc.
    >>> my_and(True, False)
    False
    >>> my_and(True, True)
    True
    >>> my_and(False, True)
    False
    >>> my_and(False, False)
    False
    """
    return not (not a or not b)


def exists_triangle(x: float, y: float, z: float) -> bool:
    """
    Return True if there exists a proper triangle with sides <x>, <y>, and <z>.

    A proper triangle in this context means that given the three parameters
    that are lengths in this function, it is possible to form a triangle with
    them such that the area of the formed triangle is more than 0.

    Do not use 'if' statements.

    >>> exists_triangle(1.0, 1.0, 1.0)
    True
    >>> exists_triangle(0.0, 0.0, 0.0)
    False
    >>> exists_triangle(5.0, 5.0, 7.0)
    True
    >>> exists_triangle(0.0, 1.0, 0.0)
    False
    >>> exists_triangle(1.0, 1.0, 0.0)
    False
    """
    return x + y > z and y + z > x and z + x > y


def is_square(num: int) -> bool:
    """
    Returns True if <num> is a perfect square.

    That is, whether there exists an integer 'i' such that
    i*i is equal to <num>.

    You may only use arithmetic operations and comparison statements.
    This means you are NOT allowed to use any of [if, and, or].

    You can, however, use built-in functions like round(), etc.

    Precondition: num >= 0

    >>> is_square(5)
    False
    >>> is_square(9)
    True
    >>> is_square(36)
    True
    >>> is_square(20)
    False
    >>> is_square(0)
    True
    >>> is_square(1)
    True
    """
    return round(num ** 0.5) == num ** 0.5


if __name__ == '__main__':
    import doctest
    doctest.testmod()
