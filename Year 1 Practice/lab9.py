"""
UTM: CSC108, Fall 2023

Practical Lab 9

Instructors: Michael Liut, Marc De Benedetti, Rutwa Engineer, Akshay Arun Bapat

This code is provided solely for the personal and private use of
students taking the CSC108 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2023 Michael Liut, Haocheng Hu

LAB RESTRICTIONS, PLEASE READ:
   - Do not add any imports, the ones that you need will be given to you.
   - Do not use recursion.
   - Do not use break/continue.
   - Do not use try-except statements, you should be able to anticipate
     or prevent any errors from happening at all!
"""


def rotate_map(m: list[list[int]], direction: str) -> list[list[int]]:
    """
    Given a 2D representation of an elevation map <m>, rotate the map either
    to the right or to the left, depending on the <direction>. A rotation will
    be 90 degrees in the direction specified.

    Do not modify the original map.

    The <direction> argument will be one of two possible values, please use the
    given code template as a starting point.

    For example:
    >>> rotate_map([[1, 2], [3, 4]], 'left')
    [[2, 4], [1, 3]]
    >>> rotate_map([[1, 2], [3, 4], [5, 6]], 'left')
    [[2, 4, 6], [1, 3, 5]]
    >>> rotate_map([[1, 2], [3, 4], [5, 6]], 'right')
    [[5, 3, 1], [6, 4, 2]]
    >>> rotate_map([[1, 2], [3, 4], [5, 6]], 'nothing')
    [[1, 2], [3, 4], [5, 6]]
    """
    rows, cols = len(m), len(m[0])
    rotated = []
    if direction == 'left':
        for i in range(cols - 1, -1, -1):
            flipped_row = []
            for j in range(rows):
                flipped_row.append(m[j][i])
            rotated.append(flipped_row)
        return rotated
    elif direction == 'right':
        for i in range(cols):
            flipped_row = []
            for j in range(rows - 1, -1, -1):
                flipped_row.append(m[j][i])
            rotated.append(flipped_row)
        return rotated
    return m


def crop_map(m: list[list[int]], corner_1: tuple[int, int],
             corner_2: tuple[int, int]) -> list[list[int]]:
    """
    Given a 2D representation of an elevation map <m> and two points on the map
    <corner_1> and <corner_2>, crop the map and return the smallest map such
    that both these coordinates are now a corner on the new map.

    Note that the new cropped map could just be a row, a column, or even a
    single square like [[1]]. The new map must remain rectangular, that is,
    each of its rows must be equal in length.

    Do not modify the original map.

    >>> sample_map = [[1, 2, 3, 4],
    ...               [5, 6, 7, 8],
    ...               [9, 10, 11, 12],
    ...               [13, 14, 15, 16]]

    >>> crop_map(sample_map, (1, 1), (2, 2))
    [[6, 7], [10, 11]]
    >>> crop_map(sample_map, (0, 0), (3, 0))
    [[1], [5], [9], [13]]
    >>> crop_map(sample_map, (0, 3), (0, 0))
    [[1, 2, 3, 4]]
    >>> crop_map(sample_map, (0, 0), (0, 0))
    [[1]]
    """
    cropped = []
    min_row = min(corner_1[0], corner_2[0])
    min_column = min(corner_1[1], corner_2[1])
    max_row = max(corner_1[0], corner_2[0]) + 1
    max_column = max(corner_1[1], corner_2[1]) + 1
    for row in m[min_row:max_row]:
        cut = row[min_column:max_column]
        cropped.append(cut)
    return cropped


def cost_to_hike_naive(m: list[list[int]], start_point: tuple[int, int],
                       end_point: tuple[int, int]) -> int:
    """
    Given an elevation map <m> and a start and end point, calculate the cost it
    would take to hike from <start_point> to <end_point>. If the start and end
    points are the same, then return 0.

    Some definitions and rules:
        1. You can only hike to either a vertically or horizontally adjacent
           location (you cannot travel diagonally).

        2. You must only travel in the direction of the <end_point>. More
           explicitly, this means that any move you make MUST take you closer
           to the end point, so you cannot travel in the other direction.

        3. We define the cost to travel between two adjacent positions as the
           absolute difference in elevation between those positions.

        4. You will calculate the naive route here, so at every position, you
           will have two choices, to either move closer to the end point along
           a row, or along a column, and you will choose the position that
           costs the least at that point (you do not need to look ahead to see
           if the costlier route now will result in an overall cheaper route).

        5. If two choices along the route have the exact same cost, you will
           choose the direction that comes first clockwise. For example, you
           will choose to move horizontally right before vertically down,
           vertically down before horizontally left, horizontally left before
           vertically up, and vertically up before horizontally right.

    Preconditions:
        the start and end points will be a valid position on the map.

    Tips to get started:
       since there is no guarantee where the start and end points will be in
       relation to each other, it may be easier to use your rotate function
       from last week to rotate the map such that the end point is always to
       the bottom right of the start point. That is, rotate the map such that
       start_point[0] <= end_point[0] and start_point[1] <= end_point[1].
       Keep in mind that if you choose to rotate the map, the start and end
       point coordinates will change as well. If you choose to do it this way,
       then you can code your function to only consider moving horizontally
       right, or vertically down. Not rotating is fine as well, but you would
       have to consider moves in all 4 directions, depending on the start and
       end coordinates. If you choose to rotate the map, you may also find the
       crop function you implmented last week useful, as that will guarantee
       that the start and end points will be at corners of the map.

    >>> sample_map = [[1, 3],
    ...               [0, 4]]
    >>> cost_to_hike_naive(sample_map, (0, 0), (1, 1))
    5
    >>> cost_to_hike_naive(sample_map, (1, 1), (0, 0))
    3
    >>> cost_to_hike_naive([[2, 3, 1], [5, 4, -1], [10, 0, 5]], (0, 1), (2, 2))
    10
    >>> cost_to_hike_naive([[2, 3, 1], [5, 4, -1], [10, 0, 0]], (0, 1), (2, 2))
    5
    >>> cost_to_hike_naive([[2, 3, 1], [5, 4, -1], [10, 0, 0]], (2, 0), (0, 2))
    9
    >>> cost_to_hike_naive([[]], (0, 0), (0, 0))
    0
    >>> cost_to_hike_naive([[1]], (0,0), (0, 0))
    0
    """
    cost = 0
    val_1 = 0
    val_2 = 0
    start = start_point
    end = end_point
    if start == end:
        return 0
    cropped = crop_map(m, start_point, end_point)
    # rotate to have end point at the bottom right of start point
    # x and y direction compare whether start and end points are relative
    if start[0] > end[0] and start[1] > end[1]:
        new_map = rotate_map(cropped, 'left')
        new_map = rotate_map(new_map, 'left')
    elif start[0] < end[0] and start[1] > end[1]:
        new_map = rotate_map(cropped, 'left')
    elif start[0] > end[0] and start[1] < end[1]:
        new_map = rotate_map(cropped, 'right')
    else:
        new_map = cropped
    start = (0, 0)
    end = (len(new_map) - 1, len(new_map[0]) - 1)
    # compare each value by the value beside and under it, then reassign
    while start != end:
        i = start[0]
        j = start[1]
        # to avoid index error:
        if j + 1 <= end[1]:
            # check 'right' first
            val_1 = abs(new_map[i][j] - new_map[i][j + 1])
        if i + 1 <= end[0]:
            # check down after
            val_2 = abs(new_map[i][j] - new_map[i + 1][j])
        if j == end[1]:
            cost += val_2
            start = (i + 1, j)
        elif i == end[0]:
            start = (i, j + 1)
            cost += val_1
        else:
            if val_1 <= val_2:
                cost += val_1
                # here, you make your start index the one to the right
                start = (i, j + 1)
            else:
                cost += val_2
                # make start index the one to the down since down is cheaper
                start = (i + 1, j)
    return cost


def longest_unique_substring(s: str) -> str:
    """
    Given a string <s>, return the longest unique substring that occurs within
    <s>.

    A unique substring is a substring within <s> which DOES NOT have any
    repeating characters. As an example, "xd" is unique but "xxd" is not.

    If there are two equal length unique substrings within <s>, return the one
    that starts first (i.e., begins at a smaller index).

    Note on grading for this question:
      You've already implemented a function that can generate all the
      substrings of a given string in lab 5. You can use that logic to help
      here, but it will be quite slow.

    For this question, PERFORMANCE WILL MATTER, and we will run long tests with
    up to 10,000,000 characters as an input. To get full credit, an input of
    10,000,000 characters should return the correct answer within 60 seconds
    (the instructor solution takes about 2).

    Helpful tips:
      In order to get your function to run fast, consider using a dictionary to
      store the indexes of previously seen characters, from there, you can
      follow a set of rules based on each new character you see to determine
      the length of the longest unique substring seen so far.

    >>> longest_unique_substring('aab')
    'ab'
    >>> longest_unique_substring('abc123abcdefghiklmnop')
    '123abcdefghiklmnop'
    >>> longest_unique_substring('a' * 10000000)
    'a'
    """
    max_string = ''
    index_of_letters = {}
    start = 0
    # go through every letter
    for i in range(len(s)):
        # assign a letter to the current letter we are on
        letter = s[i]
    # check if the letter is already in our dict, if it is, our start would be
    # one index after the first appearance of the repeated
    # letter(removes repetition)
        if letter in index_of_letters:
            start = index_of_letters[letter] + 1
        # now, our letter is assigned its index to store in dict
        index_of_letters[letter] = i
        # current_string would be a splice of s from start(which is
        # 0 if there are no repetitions found yet) to the current
        # letter we are on!
        current_string = s[start: i + 1]
        # compare lengths and assign max_string to whichever is greater
        if len(current_string) > len(max_string):
            max_string = current_string
    return max_string
