"""
UTM: CSC108, Fall 2023

Practical Lab 10

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
Do not use try-except statements, you should be able to anticipate
or prevent any errors from happening at all!
"""

from typing import Callable


def test_template(f: Callable) -> None:
    """
    This is a template for the tests you will write for this lab.

    Implement your tests as top level functions that begin with the
    word 'test' and take in a callable function <f>.

    You are free to do some amount of work to construct your test cases
    within the function but your function must make use of assert statements
    in the form "assert f('string') == 'some string'" to check for correctness.

    An assert statement means that you expect the boolean expression following
    to evaluate to True. With regards to this lab, it means that you expect the
    function call on the left to return the string on the right. If this does
    not happen, then the assert statement will raise an AssertionError, which
    we will catch and take to mean that this particular test failed.

    IMPORTANT:
    The goal of this part of the lab is to write a set of tests such that that
    ALL of them pass for any correct implementation, but AT LEAST ONE of them
    fail for any incorrect implementation (of "find_email"). You will receive
    no marks for the testing portion of this lab if any of your tests fail on
    a correct implementation of "find_email".
    """
    assert f('test@0.com') == 'test@0.com'


def test_emptystring(f: Callable) -> None:
    """Input is an empty string so which must return
    empty string
    """
    assert f('') == ''


def test_nodomain(f: Callable) -> None:
    """The input string will contain everything required for email
    but no numerical domain
    """
    assert f('he8_nf@hfjf.ca') == ''


def test_minname_mindomain(f: Callable) -> None:
    """The input string will contain the smallest possible name
    and smallest possible domain divisible by 5
    """
    assert f('^%*&^&^&$*_z@0.cagrnj934') == 'z@0.ca'


def test_maxname(f: Callable) -> None:
    """The input string will contain the largest possible name with
    """
    assert f('$^%^%^374yhf4rynfr_hunv@45.ca.illou') == 'f4rynfr_hunv@45.ca'


def test_noatsymbol(f: Callable) -> None:
    """the input string will not contain the @ symbol, thus no valid
    email will be found
    """
    assert f('pythoniscoolscienceiscool-billnye.catrythis') == ''


def test_noending(f: Callable) -> None:
    """the string will not have an email ending in ca or com
    """
    assert f('thisisa_testemail@65.notcom') == ''


def test_specialcharacters(f: Callable) -> None:
    """the email will only contain special characters that are not
    allowed
    """
    assert f('!#*&^$%)(@690.com&^$') == ''


def test_onlyemail(f: Callable) -> None:
    """the string will only contain the email with no extra
    characters
    """
    assert f('zoya.fatima@150.ca') == 'zoya.fatima@150.ca'


def test_notdivisible(f: Callable) -> None:
    """the string will have everything valid for an email
    except the domain will not be divisible by 5
    """
    assert f('$(*^_notdivi.-sible@79.com') == ''


def test_startwithspecial(f: Callable) -> None:
    """the string will be an email where the name starts with
    special characters and no letters
    """
    assert f('_@90.comSpecialcharacter') == ''


def test_whitespaces(f: Callable) -> None:
    """tests email with whitespaces between the characters
    """
    assert f('hi this is white space@65.ca more space') == 'space@65.ca'


def test_notdot(f: Callable) -> None:
    """tests string with email but not '.' after the domain
    """
    assert f('_-.properemailwithnodot@_ca') == ''


def test_nodot(f: Callable) -> None:
    """tests string with email but no '.' after the domain
    """
    assert f('_-.properemailwithnodot@ca') == ''


def run_tests() -> tuple:
    """
    Runs all tests in this file if run as main.

    Do not modify this function. You can leave it in for the final submission.
    """
    passed, failed = [], []
    for name, func in globals().items():
        if name.startswith('test') and callable(func):
            try:
                func(find_email)
            except AssertionError:
                failed.append(func.__name__)
                continue
            passed.append(func.__name__)
    return passed, failed


if __name__ == '__main__':
    from lab10 import find_email

    # the code below runs the tests defined above against your local
    # implementation of find_email, you can leave this in your final submission
    np, nf = run_tests()
    print(f'Total {len(np) + len(nf)} tests detected. '
          f'{len(np)} passed and {len(nf)} failed.')
    print('Tests passed:')
    x = [print(p) for p in np]
    del x
    print('\nTests failed:')
    x = [print(f) for f in nf]
    del x
