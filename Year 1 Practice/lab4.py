"""
UTM: CSC108, Fall 2023

Practical Lab 4

Instructors: Michael Liut, Marc De Benedetti, Rutwa Engineer, Akshay Arun Bapat

This code is provided solely for the personal and private use of
students taking the CSC108 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2023 Michael Liut, Haocheng Hu

LAB RESTRICTIONS, PLEASE READ:
You are not allowed to use any imports, except for the ones given (if any).
You may not use any lists or list methods, for the same reasons as last week.
Please also do not use try-except statements, you should be able to anticipate
or prevent any errors from happening at all!
"""


def is_palindrome(string: str) -> bool:
    """
    Your "is_palindrome" implementation from last week (Lab 3), which you may
    use as is or with modifications if you didn't get it right last time.
    >>> is_palindrome("taco cat")
    True
    >>> is_palindrome("hello")
    False
    >>> is_palindrome("Laptop Tablet Scar")
    False
    >>> is_palindrome("TaCO cAt")
    True
    >>> is_palindrome("r a c ecar")
    True
    >>> is_palindrome("laptoptable")
    False
    """
    b = string.lower()
    b = b.replace(" ", "")
    return b[::-1] == b


def is_palindrome_string(string: str) -> bool:
    """
    Given a string <string>, return whether this string is a palindrome string.

    For the purposes of this function, a palindrome string is any string that
    forms a palindrome if you piece together the first letter of every word in
    the string. We define a word here to be ANY CONTINUOUS SEGMENT OF
    ALPHABETICAL CHARACTERS. That means that "abc;def", has two words: "abc"
    and "def". The separating character does not have to be whitespace, and
    there could be more than one separating character between two words.

    Since you will be using your is_palindrome function from last week, the
    definition of a palindrome will remain the same as the definition from
    last week (ignore capitalization and whitespace).

    A simple example: given the string "test string test", there are three
    words, "test", "string", and "test". The first letters of each word come
    together to form the string "tst". And since "tst" is a palindrome, this
    function should return True for the input "test string test".

    Precondition: <string> will contain at least one word.

    Restrictions: you must use your "is_palindrome" function from lab 3 as a
                  helper for this function, in addition to the lab restrictions
                  defined at the start of this file. You are allowed and are
                  encouraged to fix any issues with your previous submission
                  for this function.
    >>> is_palindrome_string("this:;works too")
    True
    >>> is_palindrome_string("Hello Girl Hi")
    True
    >>> is_palindrome_string("Does:this.;work")
    False
    >>> is_palindrome_string(":;This!should#@too!")
    True
    >>> is_palindrome_string(".,/l.,/;,m/.;,l./;")
    True
    >>> is_palindrome_string("7982M/,'[[].,/  O ,/.;;';;/.;m")
    True
    >>> is_palindrome_string("/;Thisisoneword.;'.soitshouldwork./;';too!!:)")
    True
    >>> is_palindrome_string("!@#@&@#&*^#76376")
    True
    """
    acc = ""
    if string[0].isalpha():
        acc += string[0]
    for c in string:
        if not c.isalpha():
            string = string.replace(c, " ")
    for j in range(len(string)):
        if j != len(string) - 1:
            if not string[j].isalpha():
                acc += string[j + 1]
    return is_palindrome(acc)


def reverse_sentence(s: str) -> str:
    """
    Given a sentence <s>, we define a word within <s> to be a continuous
    sequence of characters in <s> that starts with a capital letter and
    ends before the next capital letter in the string or at the end of
    the string, whichever comes first. A word can include a mixture of
    punctuation and spaces.

    This means that in the string 'ATest string!', there are in fact only two
    words: 'A' and 'Test string!'. Again, keep in mind that words start with a
    capital letter and continue until the next capital letter or the end of the
    string, which is why we consider 'Test string!' as one word.

    This function will reverse each word found in the string, and return a new
    string with the reversed words, as illustrated in the doctest below.

    >>> reverse_sentence('ATest string!')
    'A!gnirts tseT'
    >>> reverse_sentence("CheckThisOne")
    'kcehCsihTenO'
    >>> reverse_sentence("")
    ''
    >>> reverse_sentence("helloAbby")
    'helloybbA'
    >>> reverse_sentence("Abbyhello")
    'ollehybbA'
    >>> reverse_sentence("hello hi, #%^( world")
    'hello hi, #%^( world'
    >>> reverse_sentence("578@$%^%$&%&&^%")
    '578@$%^%$&%&&^%'
    """
    acc = ""
    have_reversed = ""
    include_cap = False
    for c in s:
        if c.isupper():
            include_cap = True
    if not include_cap:
        return s
    for char in s:
        if char.isupper():
            if acc.islower():
                have_reversed += acc
            else:
                have_reversed += acc[::-1]
            acc = char
        else:
            acc += char
    have_reversed += acc[::-1]
    return have_reversed
