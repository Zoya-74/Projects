"""
UTM: CSC108, Fall 2023

Practical Lab 8

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
Do not use recursion.
Do not use break/continue.
Do not use try-except statements, you should be able to anticipate
or prevent any errors from happening at all!
"""

from typing import TextIO


def get_elevation_maps(maps_file: TextIO) -> list[list[list[int]]]:
    """
    Given an open csv file <maps_file>, read the file according to the
    specification and return all the elevation maps stored within the file.

    IMPORTANT: the given argument to the function is an OPEN file <maps_file>,
    you will not need to open it again, and can begin performing standard file
    operations on it.

    The file will be structured as follows:
        - The first line will contain one number "n", which will denote the
          number of elevation maps stored within this file.
        - The next n lines will contain two numbers each, "r" and "c", which
          are the number of rows and columns of each elevation map.
        - The rest of the data will then be comprised of the elevation map
          data, which will follow one another in sequence, with no spaces in
          between.

    For an example, see "sample_data.csv".
    """
    num_maps = int(maps_file.readline())
    final_maps = []
    rows = []
    columns = []
    for _ in range(num_maps):
        temp = maps_file.readline().strip().split(',')
        rows.append(int(temp[0]))
        columns.append(int(temp[1]))

    for row_index in range(len(rows)):
        temp_line = []
        for _ in range(rows[row_index]):
            temp1 = (maps_file.readline().strip().split(','))
            temp2 = list(map(int, temp1))
            x = columns[row_index]
            temp_line.append(temp2[:x])
        final_maps.append(temp_line)
    return final_maps


def write_elevation_maps(maps_file: TextIO, maps_list: list[list[list[int]]]
                         ) -> None:
    """
    Given an open csv file <maps_file> and a list of maps <maps_list>, write
    the maps back into the csv file according to the format specified in
    <get_elevation_maps>. That is, if the same file was then read from again
    by the <get_elevation_maps> function, it should return a list identical
    to <maps_list>.

    IMPORTANT: <maps_file> is an already open file, you can begin writing to it
               immediately. Furthermore, DO NOT close the file <maps_file>
               after you are finished writing the data in.
    """
    maps = len(maps_list)
    maps_file.write(str(maps) + "\n")

    for each_map in maps_list:
        rows = str(len(each_map))
        column = str(len(each_map[0]))
        maps_file.write(rows + ',' + column + '\n')

    for one_map in maps_list:
        for one_row in one_map:
            temp = ','.join(map(str, one_row))
            maps_file.write(temp + '\n')


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
