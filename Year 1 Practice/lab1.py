"""
UTM: CSC108, Fall 2023

Practical Lab 1

Instructors: Michael Liut, Marc De Benedetti, Rutwa Engineer, Akshay Arun Bapat

This code is provided solely for the personal and private use of
students taking the CSC108 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2023 Michael Liut, Haocheng Hu
"""

# complete the following exercises below

# TODO
# Q1
a = 1
b = 2
# without changing the values of a and b,
# declare a variable 'c' and make it equal to the value of a + b
c = a + b

# TODO
# Q2
# We are going to play with something called floor division
# Say you had 15 cookies to distribute to 4 children and you had to give the
# same number of cookies to each child, how many cookies could you afford
# to give each child?
num_cookies = 15
num_children = 4
# Use the floor division operator "//" to calculate this number
cookies_to_give_each_child = num_cookies // num_children

# Q3
# Go learn about a cool thing that you can do with just python and numbers
# explain it in a comment and show a demonstration below:

# TODO
# A cool thing we can do is create a function that will give us the value of the hypoteneuse
#of a right triangle from the 2 given sides
#
#
# TODO
# Give a demonstration of actual WORKING code below this line
def hypoteneuse (x:int, y:int) -> float:
    """returns the value of the hypoteneuse if given the other 2 sides of a right angle
    triangle
    eg; hypoteneuse (3,4)
    5"""
    return (x**2 + y**2) ** 0.5
print (hypoteneuse (3, 4))