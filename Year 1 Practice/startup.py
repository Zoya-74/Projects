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

NOTE: you do not have to submit this file, you only need to try running it!
"""

import re
import sys

message_encoded = [10, 73, 102, 32, 121, 111, 117, 32, 99, 97, 110, 32, 114,
                   101, 97, 100, 32, 116, 104, 105, 115, 32, 109, 101, 115,
                   115, 97, 103, 101, 44, 32, 116, 104, 101, 110, 32, 121,
                   111, 117, 114, 32, 80, 121, 116, 104, 111, 110, 32, 105,
                   110, 115, 116, 97, 108, 108, 97, 116, 105, 111, 110, 32,
                   105, 115, 32, 119, 111, 114, 107, 105, 110, 103, 32, 58, 41]

# decode the "secret" message and print it
print(''.join(chr(i) for i in message_encoded))

# get the python version that is running this code, yes, there are easier ways to do this
ver = re.findall(r'\.'.join([r'\d+'] * 3), sys.version)[0]

# print out the python version that is running
print(f'The python version you are running is {ver}, is that what you installed?')
