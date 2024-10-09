"""
Assignment 2 - Sample Tests

=== CSC148 Winter 2024 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2024 Bogdan Simion, David Liu, Diane Horton, Jacqueline Smith

=== Module Description ===
This module contains sample tests for Assignment 2, Tasks 1 and 2.
The tests use the provided example-directory, so make sure you have downloaded
and extracted it into the same place as this test file.
This test suite is very small. You should plan to add to it significantly to
thoroughly test your code.

IMPORTANT NOTES:
    - If using PyCharm, go into your Settings window, and go to
      Editor -> General.
      Make sure the "Ensure line feed at file end on Save" is NOT checked.
      Then, make sure none of the example files have a blank line at the end.
      (If they do, the data size will be off.)

    - os.listdir behaves differently on different
      operating systems.  These tests expect the outcomes that one gets
      when running on the *Teaching Lab machines*.
      Please run all of your tests there - otherwise,
      you might get inaccurate test failures!

    - Depending on your operating system or other system settings, you
      may end up with other files in your example-directory that will cause
      inaccurate test failures. That will not happen on the Teachin Lab
      machines.  This is a second reason why you should run this test module
      there.
"""
import os

from hypothesis import given
from hypothesis.strategies import integers

from tm_trees1 import TMTree, FileSystemTree

# This should be the path to the "workshop" folder in the sample data.
EXAMPLE_PATH = os.path.join(os.getcwd(), 'example-directory', 'workshop')


def test_data_size() -> None:
    """ Test data size initialization. """
    # Verify that data_size is used if subtrees = []
    subtree_1 = TMTree("Subtree", [], 20)
    subtree_2 = TMTree("Subtree", [], 35)
    assert subtree_1.data_size == 20
    assert subtree_2.data_size == 35

    # Verify that data_size parameter is ignored
    tree = TMTree("Tree", [subtree_1, subtree_2], 999)
    assert tree.data_size == 55


def test_parent_tree() -> None:
    """ Test parent tree is initialised correctly. """
    subtree_1 = TMTree("Subtree", [], 20)
    subtree_2 = TMTree("Subtree 2", [], 20)
    assert subtree_1._parent_tree is None
    assert subtree_2._parent_tree is None

    tree = TMTree("Tree", [subtree_1, subtree_2], 999)
    assert subtree_1._parent_tree is tree
    assert subtree_2._parent_tree is tree

    # Root node has no parent
    assert tree._parent_tree is None


def test_valid_colors() -> None:
    """ Test color initialization in correct range. """
    for _ in range(999):
        tree = TMTree("Tree", [], 1)
        assert is_valid_colour(tree._colour)


def test_name_initialisation() -> None:
    """ Test if name is correctly initialised. """
    # Test directory names
    workshop = FileSystemTree(EXAMPLE_PATH)
    assert workshop._name == 'workshop'

    activities = FileSystemTree(os.path.join(EXAMPLE_PATH, 'activities'))
    assert activities._name == 'activities'

    # Test single file names
    draft = FileSystemTree(os.path.join(EXAMPLE_PATH, 'draft.pptx'))
    assert draft._name == 'draft.pptx'

    plan = FileSystemTree(os.path.join(EXAMPLE_PATH, 'activities', 'Plan.tex'))
    assert plan._name == 'Plan.tex'


def test_data_size_init() -> None:
    """ Test data size is correctly initialised. """
    # Test directory sizes
    workshop = FileSystemTree(EXAMPLE_PATH)
    assert workshop.data_size == 151

    activities = FileSystemTree(os.path.join(EXAMPLE_PATH, 'activities'))
    assert activities.data_size == 71

    # Test single file sizes
    draft = FileSystemTree(os.path.join(EXAMPLE_PATH, 'draft.pptx'))
    assert draft.data_size == 58

    plan = FileSystemTree(os.path.join(EXAMPLE_PATH, 'activities', 'Plan.tex'))
    assert plan.data_size == 2


def test_rect_init() -> None:
    """ Test if rect is correctly initialised. """
    tree = FileSystemTree(EXAMPLE_PATH)
    assert tree.rect == (0, 0, 0, 0)

    for subtree in tree._subtrees:
        assert subtree.rect == (0, 0, 0, 0)


def test_subtree_order() -> None:
    """ Test subtrees are initialised in the correct order. """
    files_in_directory = os.listdir(EXAMPLE_PATH)
    tree = FileSystemTree(EXAMPLE_PATH)

    assert len(tree._subtrees) == len(files_in_directory)

    # Verify subtrees are in the order produced from os.listdir
    for index, path in enumerate(files_in_directory):
        # Get file/folder name without path
        base_filename = os.path.basename(path)

        # Check subtree name at current index
        assert tree._subtrees[index]._name == base_filename


@given(integers(min_value=100, max_value=1000),
       integers(min_value=100, max_value=1000),
       integers(min_value=100, max_value=1000),
       integers(min_value=100, max_value=1000))
def test_empty_rect(x, y, width, height) -> None:
    """ Test update rectangles with empty data. """
    rect = (x, y, width, height)

    empty_file = TMTree("Empty File", [], 0)
    empty_file.update_rectangles(rect)

    # Verify file takes up no space
    assert empty_file.rect == (0, 0, 0, 0)


@given(integers(min_value=100, max_value=1000),
       integers(min_value=100, max_value=1000),
       integers(min_value=100, max_value=1000),
       integers(min_value=100, max_value=1000))
def test_single_rect(x, y, width, height) -> None:
    """ Test update rectangles for collapsed file. """
    rect = (x, y, width, height)

    # Initialise TMTree with data size 1
    file = TMTree("File", [], 1)
    file.update_rectangles(rect)

    # Verify file takes up entire rect
    assert file.rect == rect


def test_basic_rect() -> None:
    """ Test update rectangles with basic data. """
    subtree_1 = TMTree("Subtree 1", [], 10)
    subtree_2 = TMTree("Subtree 2", [], 25)
    subtree_3 = TMTree("Subtree 3", [], 15)

    tree = TMTree("Tree", [subtree_1, subtree_2, subtree_3], 0)
    assert tree.data_size == 50

    tree.expand_all()
    tree.update_rectangles((0, 0, 200, 100))

    actual_rects = [r[0] for r in tree.get_rectangles()]
    expected_rects = [(0, 0, 40, 100), (40, 0, 100, 100), (140, 0, 60, 100)]

    assert len(actual_rects) == len(expected_rects)
    assert actual_rects == expected_rects


def test_example_rect() -> None:
    """ Test update rectangles for expanded folder. """
    # Initialise FileSystemTree
    tree = FileSystemTree(EXAMPLE_PATH)

    # Sort and expand all subtrees
    _sort_subtrees(tree)
    tree.expand_all()

    # Update rectangles
    tree.update_rectangles((0, 0, 100, 100))

    rects = tree.get_rectangles()
    assert len(rects) == 6

    actual_rects = [r[0] for r in rects]
    expected_rects = [(0, 0, 2, 47), (2, 0, 28, 47), (30, 0, 70, 47),
                      (0, 47, 100, 38), (0, 85, 72, 15), (72, 85, 28, 15)]

    assert len(actual_rects) == len(expected_rects)
    for i in range(len(actual_rects)):
        assert expected_rects[i] == actual_rects[i]


def test_no_data_size() -> None:
    """ Test rectangle with empty data size. """
    tree = TMTree("empty", [], 0)
    tree.update_rectangles((0, 0, 200, 100))
    rects = [t[0] for t in tree.get_rectangles()]
    assert rects == []


def test_empty_rectangle() -> None:
    """ Test rectangle with empty area. """
    tree = TMTree("Tree", [], 100)
    tree.update_rectangles((0, 0, 0, 0))
    rects = [r[0] for r in tree.get_rectangles()]
    assert rects == [(0, 0, 0, 0)]


def test_empty_area() -> None:
    """ Test empty data size and rectangle. """
    tree = TMTree("Tree", [], 0)
    tree.update_rectangles((0, 0, 0, 0))
    rects = [r[0] for r in tree.get_rectangles()]
    assert rects == []


def test_delete_all_subtrees() -> None:
    """ Test that deleting all subtrees makes a folder empty. """
    tree = FileSystemTree(EXAMPLE_PATH)
    _sort_subtrees(tree)

    images_folder = tree._subtrees[0]._subtrees[1]
    q2_pdf = images_folder._subtrees[0]
    q3_pdf = images_folder._subtrees[1]
    assert q2_pdf.delete_self()
    assert q3_pdf.delete_self()

    assert len(images_folder._subtrees) == 0
    assert images_folder.data_size == 0


def test_delete_workshop() -> None:
    """ Test that deleting all subtrees gives an empty rect. """
    path = os.path.join(os.getcwd(), 'example-directory')
    tree = FileSystemTree(path)

    # Delete workshop folder
    print(tree._name)
    print(tree._subtrees[0]._name)
    print(tree._subtrees[-1]._name)
    print(len(tree._subtrees))
    assert tree._subtrees[0].delete_self()
    assert tree._subtrees[-1].delete_self()
    print(len(tree._subtrees))

    tree.update_rectangles((0, 0, 100, 100))
    rects = [t[0] for t in tree.get_rectangles()]
    assert rects == []


def test_delete_entire_tree() -> None:
    """ Test data size after deleting entire tree. """
    tree = FileSystemTree(os.path.join(EXAMPLE_PATH, ".."))
    assert tree.delete_self() == False
    assert tree.data_size != 0

    assert tree._subtrees[0].delete_self()
    assert tree._subtrees[0].delete_self()
    assert tree.data_size == 0


def test_change_size_limit() -> None:
    """ Test if change size cannot go below 1. """
    tree = TMTree("Tree", [], 1)
    tree.change_size(-1)
    assert tree.data_size == 1


def test_change_size_rounding() -> None:
    """ Test if change size is rounding correctly. """
    tree = TMTree("Tree", [], 150)
    tree.change_size(0.01)

    # 1% is 1.5, rounded to 2
    assert tree.data_size == 152


def test_root_change_size() -> None:
    """ Test change size on root node. """
    subtree_1 = TMTree("Subtree 1", [], 100)
    tree = TMTree("Tree", [subtree_1], 0)

    subtree_1.change_size(0.01)
    assert subtree_1.data_size == 101
    assert tree.data_size == 101

    subtree_1.change_size(-0.01)
    assert subtree_1.data_size == 99
    assert tree.data_size == 99


def test_delete() -> None:
    """ Test data size on root after delete. """
    nested_subtree = TMTree("Nested Subtree 1", [], 100)
    subtree = TMTree("Subtree 1", [nested_subtree], 0)
    tree = TMTree("Tree", [subtree], 0)

    assert subtree.data_size == 100
    assert tree.data_size == 100

    nested_subtree.delete_self()

    assert subtree.data_size == 0
    assert tree.data_size == 0


def test_move() -> None:
    """ Test data size is updated after move. """
    subtree_1 = TMTree("Subtree 1", [], 100)
    subtree_2 = TMTree("Subtree 2", [], 0)
    tree = TMTree("Tree", [subtree_1], 0)
    tree_2 = TMTree("Tree 2", [subtree_2], 0)

    subtree_1.move(tree_2)
    _sort_subtrees(tree_2)

    assert len(tree._subtrees) == 0
    assert tree.data_size == 0
    assert tree_2._subtrees[0] == subtree_1
    assert tree_2.data_size == 100


def test_move_on_folder() -> None:
    """ Test if move does not move folders. """
    nested_subtree = TMTree("Nested Subtree", [], 100)
    subtree_1 = TMTree("Subtree 1", [nested_subtree], 0)
    subtree_2 = TMTree("Subtree 2", [], 0)
    tree = TMTree("Tree", [subtree_1], 0)
    tree_2 = TMTree("Tree 2", [subtree_2], 0)

    subtree_1.move(subtree_2)
    assert subtree_1._parent_tree == tree
    assert len(subtree_2._subtrees) == 0

    subtree_1.move(tree_2)
    assert subtree_1._parent_tree == tree
    assert len(tree_2._subtrees) == 1


def test_expand_all() -> None:
    """ Test that expand_all correctly expands all trees. """
    tree = FileSystemTree(EXAMPLE_PATH)
    assert tree._expanded is False
    tree.expand_all()
    assert tree._expanded

    assert verify_all_expanded(tree)


def test_leaf_collapsed() -> None:
    """ Test if leaves are always collapsed. """
    subtree = TMTree("Subtree 1", [], 100)
    tree = TMTree("Tree", [subtree], 0)

    assert subtree._expanded == False
    tree.expand_all()
    assert subtree._expanded == False
    tree.expand()
    assert subtree._expanded == False


def test_collapse() -> None:
    """ Test collapse on tree with depth 3. """
    nested_subtree = TMTree("Nested Subtree 1", [], 100)
    subtree = TMTree("Subtree 1", [nested_subtree], 0)
    tree = TMTree("Tree", [subtree], 0)

    tree.expand_all()

    assert nested_subtree._expanded is False

    subtree.collapse()

    assert tree._expanded == False
    assert subtree._expanded == False
    assert nested_subtree._expanded == False


def test_collapse_deeper() -> None:
    """ Test collapse on tree with depth 4. """
    nested_nested_subtree = TMTree("Nested Nested Subtree 1", [], 100)
    nested_subtree = TMTree("Nested Subtree 1", [nested_nested_subtree], 0)
    subtree = TMTree("Subtree 1", [nested_subtree], 0)
    tree = TMTree("Tree", [subtree], 0)

    tree.expand_all()
    subtree.collapse()

    assert tree._expanded == False
    assert subtree._expanded == False
    assert nested_subtree._expanded == False
    assert nested_nested_subtree._expanded == False

    tree.expand_all()
    nested_subtree.collapse()

    assert tree._expanded
    assert subtree._expanded == False
    assert nested_subtree._expanded == False
    assert nested_nested_subtree._expanded == False


def test_collapse_all() -> None:
    """ Test that collapse_all correctly collapses all trees. """
    tree = FileSystemTree(EXAMPLE_PATH)
    _sort_subtrees(tree)

    assert tree._expanded == False
    tree.expand_all()
    assert tree._expanded
    print(len(tree.get_rectangles()))
    tree.collapse_all()
    print(len(tree.get_rectangles()))
    assert len(tree.get_rectangles()) == 1

    assert verify_all_collapsed(tree)


def test_get_tree_at_pos() -> None:
    """ Test get_tree_at_position """
    tree = FileSystemTree(EXAMPLE_PATH)

    _sort_subtrees(tree)
    tree.update_rectangles((0, 0, 100, 100))

    # Expand Workshop folder
    tree.expand()
    activities = tree._subtrees[0]

    assert tree.get_tree_at_position((40, 0)) is activities


##############################################################################
# Helpers
##############################################################################


def is_valid_colour(colour: tuple[int, int, int]) -> bool:
    """Return True iff <colour> is a valid colour. That is, if all of its
    values are between 0 and 255, inclusive.
    """
    for i in range(3):
        if not 0 <= colour[i] <= 255:
            return False
    return True


def verify_all_collapsed(tree) -> bool:
    """
    Verifies <tree> and all of it's subtrees are collapsed.
    """
    if len(tree._subtrees) == 0:
        return tree._expanded == False

    if tree._expanded:
        return False

    return all(verify_all_collapsed(subtree) for subtree in tree._subtrees)


def verify_all_expanded(tree) -> bool:
    """
    Verifies <tree> and all of it's subtrees are expanded.
    Verifies all leaf nodes are collapsed.
    """
    if len(tree._subtrees) == 0:
        return not tree._expanded

    if not tree._expanded:
        return False

    return all(verify_all_expanded(subtree) for subtree in tree._subtrees)


def _sort_subtrees(tree: TMTree) -> None:
    """Sort the subtrees of <tree> in alphabetical order.
    THIS IS FOR THE PURPOSES OF THE SAMPLE TEST ONLY; YOU SHOULD NOT SORT
    YOUR SUBTREES IN THIS WAY. This allows the sample test to run on different
    operating systems.

    This is recursive, and affects all levels of the tree.
    """
    if not tree.is_empty():
        for subtree in tree._subtrees:
            _sort_subtrees(subtree)

        tree._subtrees.sort(key=lambda t: t._name)


if __name__ == '__main__':
    import pytest

    pytest.main(['dont_submit_test.py'])
