"""
UTM: CSC108, Fall 2023

Practical Lab 5

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
You must not use any lists, list methods, or while loops.
Within your loops, you MUST NOT use any break or continue statements.
Furthermore, you must not use try-except statements, as you should be able to
anticipate or prevent any errors from ever occurring!
"""


def sum_string(string: str) -> int:
    """
    Given a string <string>, return the sum of this string, as computed by the
    formula given below:

    To compute the sum of a string as defined by this function, we add every
    odd positioned digit, and subtract every even positioned digit. For example,
    if we had an input of "54321", we would add 5, subtract 4, add 3, subtract
    2, and add 1, bringing us to a total of 3. In other words, you would add the
    first digit, subtract the second digit, and keep alternating until you reach
    the end of the string. If the string is empty, then the sum is 0.

    Note: since we give the input as a string, you will have to do some type
    conversion in order to solve this problem.

    Precondition: <string> will only contain the characters 0-9.
    >>> sum_string("75934209")
    1
    >>> sum_string("")
    0
    >>> sum_string("999999")
    0
    """
    acc = 0
    for i in range(len(string)):
        if i % 2 == 0:
            acc += int(string[i])
        else:
            acc -= int(string[i])
    return acc


def substring_with_largest_sum(string: str) -> str:
    """
    Given a string <string>, return the substring with the largest sum (as
    calculated by sum_string()) that exists within <string>. If there are
    multiple substrings with equally large sums, return the first one that
    occurs. The substring could just be the whole string itself, or it could
    be empty.

    To calculate the sum of the substring, you must use the function
    sum_string() which you have implemented above as a helper.

    For example, given the string "321", there are 7 possible substrings:
    "", "3", "2", "1", "32", "21", "321". For each one of them, their sum can
    be calculated as per the sum_string() function which you have already
    implemented. By using your understanding of loops, implement this function
    to return the substring with the largest sum by checking all of the
    substrings of the input string. So, "32" evaluates to 1, "21" also
    evaluates to 1, "321" evaluates to 2, resulting in "3" being the largest
    possible substring as it evaluates to 3.
    >>> substring_with_largest_sum("012")
    '2'
    >>> substring_with_largest_sum("321")
    '3'
    >>> substring_with_largest_sum("444")
    '4'
    >>> substring_with_largest_sum("2035")
    '203'
    >>> substring_with_largest_sum("2034")
    '203'
    >>> substring_with_largest_sum("")
    ''
    >>> substring_with_largest_sum("123")
    '3'
    """
    substring = ""
    biggest_value = 0
    for i in range(len(string)):
        for j in range(1, len(string) + 1):
            temp_string = string[i: j]
            if sum_string(temp_string) > biggest_value:
                biggest_value = sum_string(temp_string)
                substring = temp_string
    return substring


def helper_three(string1: str, string2: str) -> str:
    """returns the interwoven string given two strings <string1> and
    <string2> which are of the same lengths
    >>> helper_three("hi", "12")
    'h1i2'
    >>> helper_three("abc", "121")
    'a1b2c1'
    """
    acc = ""
    for i in range(len(string1)):
        for j in range(len(string2)):
            if i == j:
                acc += string1[i] + string2[j]
    return acc


def loopy_madness(string1: str, string2: str) -> str:
    """
    Given two strings <string1> and <string2>, return a new string that
    contains letters from these two strings "interwoven" together, starting with
    the first character of <string1>. If the two strings are not of equal
    length, then start looping "backwards-and-forwards" in the shorter string
    until you come to the end of the longer string.

    "interwoven" (or "interweaving") means constructing a new string by taking
    the first letter from the first string, adding the first letter of the
    second string, adding the second letter of the first string,
    adding the second letter of the second string, and so on.

    "backwards-and-forwards" is a custom looping term. First the loop starts
    at position 1 (index 0) and goes until position n (i.e., the end). Once the
    loop reaches position n, it goes backwards, starting at position n - 1 and
    goes to position 1 (index 0). This repeats until the two strings are
    interwoven. For example, the backwards-and-forwards operations of "abc"
    would be "abcbabcba..."

    Examples:
        If you are given "abc" and "123", then the output string is "a1b2c3".
        This is after taking "a" from the first string, adding "1" from the
        second string, adding "b" from the first string, and so on.

        Things get more interesting when you are given two strings that differ
        in length. For example, if you are given "abcde" and "12", then the
        output would be "a1b2c1d2e1". Notice how the shorter string loops
        around when it runs out of characters, and continues looping until the
        longer string is exhausted.

        Another example of the "backwards-and-forwards" implementation given
        two strings of differing length: "abcdfe" and "123", then the output
        would be "a1b2c3d2f1e2".

        Note that the first string could be shorter too, for example, given
        "ab" and "123", the output would be "a1b2a3".


    Precondition: both input strings will NOT be empty.

    Hint: a good sanity check is to ensure that your output string is exactly
    twice the length of the longer input string :)
    >>> loopy_madness("abcdefghijklmno", "123")
    'a1b2c3d2e1f2g3h2i1j2k3l2m1n2o3'
    >>> loopy_madness("123", "abcdefghijklmno")
    '1a2b3c2d1e2f3g2h1i2j3k2l1m2n3o'
    >>> loopy_madness("aa", "1")
    'a1a1'
    >>> loopy_madness("abcde", "12")
    'a1b2c1d2e1'
    >>> loopy_madness("abcdfe", "123")
    'a1b2c3d2f1e2'
    >>> loopy_madness("abc", "123")
    'a1b2c3'
    """
    if len(string1) > len(string2):
        string2 = ((string2 + string2[len(string2) - 2: 0: -1])
                   * ((len(string1) + 1) // len(string2)))
    elif len(string2) > len(string1):
        string1 = ((string1
                    + string1[len(string1) - 2: 0: -1])
                   * ((len(string2) + 1) // len(string1)))
    return helper_three(string1, string2)
