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
      inaccurate test failures. That will not happen on the Teaching Lab
      machines.  This is a second reason why you should run this test module
      there.
"""
import os

from tm_trees import TMTree, FileSystemTree

# This should be the path to the "workshop" folder in the sample data.
# You may need to modify this, depending on where you downloaded and
# extracted the files.
EXAMPLE_PATH = os.path.join(os.getcwd(), 'example-directory', 'workshop')


def test_initialize_empty_tree() -> None:
    """
    initializes empty tree and see if it satisfies invariants
    (passes codetier list)
    """
    tree = TMTree(None,[])
    root_tree = TMTree(None,[tree])
    assert tree.is_empty()

    # Note: although tree is empty, it still has parent
    assert tree.get_parent() == root_tree

    # Note: although data_size is not 0 it still is considered empty?
    tree = TMTree(None,[], 10)
    assert tree.is_empty()


def test_initialize_negative_data_size() -> None:
    """
    Representation invariant, test for codetier list (still works)
    """
    tree = TMTree('negative_value', [], -9)
    assert tree.data_size == -9


def test_pos_example() -> None:
    """
    Test position of tree
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    tree.expand_all()
    _sort_subtrees(tree)

    tree.update_rectangles((0, 0, 200, 100))
    actual_tree = tree.get_tree_at_position((10, 9))
    expected_tree = tree._subtrees[0]._subtrees[1]._subtrees[0]
    assert actual_tree is expected_tree
    assert tree._subtrees[0]._subtrees[1]._subtrees[0].rect == (0, 2, 94, 28)


def test_out_of_range_pos_example() -> None:
    """
    Test when position is out of range
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    tree.expand_all()
    _sort_subtrees(tree)

    tree.update_rectangles((0, 0, 200, 100))
    assert tree.get_tree_at_position((300, 9)) is None


def test_uppermost_on_line_pos_example() -> None:
    """
    test position when it is on a line, should return uppermost
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    tree.expand_all()
    _sort_subtrees(tree)

    tree.update_rectangles((0, 0, 200, 100))
    actual_tree = tree.get_tree_at_position((94, 2))
    expected_tree = tree._subtrees[0]._subtrees[0]
    assert actual_tree is expected_tree
    assert tree._subtrees[0]._subtrees[0].rect == (0, 0, 94, 2)


def test_leftmost_on_line_pos_example() -> None:
    """
    test position when it is on a line, should return leftmost
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    tree.expand_all()
    _sort_subtrees(tree)

    tree.update_rectangles((0, 0, 200, 100))
    actual_tree = tree.get_tree_at_position((170, 0))
    expected_tree = tree._subtrees[1]
    assert actual_tree is expected_tree
    assert tree._subtrees[1].rect == (94, 0, 76, 100)


def test_delete_root() -> None:
    """
    Test delete when there is no parent, shouldn't do anything
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    assert not tree.delete_self()
    assert tree.data_size == 151


def test_delete_internal_node() -> None:
    """
    deletes internal nodes, checks if the data_sizes changes
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    _sort_subtrees(tree)

    subtree = tree._subtrees[0]
    next_subtree = subtree._subtrees[1]

    assert next_subtree.delete_self()
    assert next_subtree not in subtree._subtrees
    assert tree.data_size == 82
    assert subtree.data_size == 2
    assert next_subtree.data_size == 0
    assert next_subtree._subtrees[0].data_size == 20
    assert next_subtree._subtrees[1].data_size == 49

    assert subtree.delete_self()
    assert subtree not in tree._subtrees
    assert subtree.data_size == 0
    assert tree.data_size == 80
    assert subtree._subtrees[0].data_size == 2


def test_delete_leaf() -> None:
    """
    deletes leaf, checks if the data_sizes changes
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    _sort_subtrees(tree)
    leaf = tree._subtrees[1]
    assert len(tree._subtrees) == 3

    assert leaf.delete_self()
    assert leaf not in tree._subtrees
    assert tree.data_size == 93
    assert leaf.data_size == 0
    assert len(tree._subtrees) == 2


def test_empty_folder_delete() -> None:
    """
    checks if deletion works when folder is empty
    """
    leaf = TMTree("non-empty", [], 10)
    tree2 = TMTree('empty_folder2', [leaf], 0)
    tree = TMTree('empty_folder1', [tree2], 0)
    assert tree._subtrees[0]._subtrees[0].delete_self()
    assert len(tree._subtrees) == 1
    assert tree.data_size == 0


def test_move_root() -> None:
    """
    checks if the root does not move into any other subtrees
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    _sort_subtrees(tree)
    assert len(tree._subtrees[0]._subtrees) == 2
    tree.move(tree._subtrees[0])
    assert len(tree._subtrees[0]._subtrees) == 2
    assert tree not in tree._subtrees[0]._subtrees


def test_move_leaf() -> None:
    """
    Moves leaf, checks if data_sizes change
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    _sort_subtrees(tree)
    # before move
    leaf = tree._subtrees[0]._subtrees[1]._subtrees[0]
    new_tree = tree._subtrees[2]
    old_tree = tree._subtrees[0]._subtrees[1]
    assert len(new_tree._subtrees) == 2
    assert len(old_tree._subtrees) == 2
    assert new_tree.data_size == 22
    assert old_tree.data_size == 69

    new_lst = new_tree._subtrees.copy()
    old_lst = old_tree._subtrees.copy()
    leaf.move(new_tree)
    new_lst.append(leaf)
    old_lst.remove(leaf)
    # after move - should change length and sizes of old and new parents
    assert tree._subtrees[2]._subtrees == new_lst
    assert tree._subtrees[0]._subtrees[1]._subtrees == old_lst
    assert len(new_tree._subtrees) == 3
    assert len(old_tree._subtrees) == 1
    assert new_tree.data_size == 42
    assert old_tree.data_size == 49


def test_move_internal_node() -> None:
    """
    Checks if the node moves, it should not
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    _sort_subtrees(tree)

    new_tree = tree._subtrees[2]
    old_tree = tree._subtrees[0]
    internal_node = tree._subtrees[0]._subtrees[1]
    # before move
    assert len(new_tree._subtrees) == 2
    assert len(old_tree._subtrees) == 2
    assert new_tree.data_size == 22
    assert old_tree.data_size == 71

    new_lst = new_tree._subtrees.copy()
    old_lst = old_tree._subtrees.copy()
    internal_node.move(new_tree)
    new_lst.append(internal_node)
    old_lst.remove(internal_node)
    # after move - should keep the same length and sizes of old and new parents
    assert tree._subtrees[2]._subtrees != new_lst
    assert tree._subtrees[0]._subtrees != old_lst
    assert len(new_tree._subtrees) == 2
    assert len(old_tree._subtrees) == 2
    assert new_tree.data_size == 22
    assert old_tree.data_size == 71


def test_last_empty_subtree1() -> None:
    """
    Testing that there is a blank space left if the last subtree in the parent
    tree has 0 as data size
    """
    leaf3 = TMTree('empty file', [], 0)
    leaf2 = TMTree('non_empty file', [], 30)
    leaf1 = TMTree('non_empty file', [], 30)
    tree_c = TMTree('Folder C', [leaf1, leaf2, leaf3], 0)
    tree_b = TMTree('Folder B', [tree_c], 0)
    tree_a = TMTree('Folder A', [tree_b], 0)
    tree_a.expand_all()
    tree_a.update_rectangles((0, 0, 200, 100))
    assert tree_a.rect[3] != leaf1.rect[3] + leaf2.rect[3]


def test_last_empty_subtree2() -> None:
    """
    Testing that there is no blank space left if the last subtree in the parent
    tree has 0 as data size
    """
    leaf2 = TMTree('empty file', [], 0)
    leaf1 = TMTree('non_empty file', [], 30)
    tree_c = TMTree('Folder C', [leaf1, leaf2], 0)
    tree_b = TMTree('Folder B', [tree_c], 0)
    tree_a = TMTree('Folder A', [tree_b], 0)
    tree_a.expand_all()
    tree_a.update_rectangles((0, 0, 200, 100))
    assert tree_a.rect[3] == leaf1.rect[3] + leaf2.rect[3]


def test_change_size_positive() -> None:
    """
    test when factor is positive, should round up
    """
    subtree = TMTree("sub", [], 50)
    tree = TMTree("root", [subtree], 0)

    subtree.change_size(0.01)
    assert subtree.data_size == 51
    assert tree.data_size == 51


def test_change_size_negative() -> None:
    """
    test when factor is positive, should round down
    """
    subtree = TMTree("sub", [], 50)
    tree = TMTree("root", [subtree], 0)
    subtree.change_size(-0.01)
    assert subtree.data_size == 49
    assert tree.data_size == 49


def test_change_size_limit() -> None:
    """
    test when data_size becomes less than 1 after factor
    """
    subtree = TMTree("sub", [], 50)
    tree = TMTree("root", [subtree], 0)
    subtree.change_size(-1)
    assert subtree.data_size == 1
    assert tree.data_size == 1


def test_expand() -> None:
    """
    expands only one node, doesn't expand leaf
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    _sort_subtrees(tree)

    assert tree._expanded is False
    tree.expand()
    assert tree._expanded is True
    actual = []
    for subtree in tree._subtrees:
        actual.append(subtree._expanded)
    expected = [False, False, False]
    assert actual == expected


def test_expand_all() -> None:
    """
    expands all nodes, doesn't expand leaves
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    _sort_subtrees(tree)
    tree.expand_all()
    assert tree._expanded is True
    actual = []
    for subtree in tree._subtrees:
        actual.append(subtree._expanded)
    expected = [True, False, True]
    assert actual == expected


def test_collapse() -> None:
    """
    collapse one node and its subtrees, doesnt collapse root
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    _sort_subtrees(tree)
    tree.expand_all()

    tree._subtrees[0]._subtrees[0].collapse()
    actual = []
    for subtree in tree._subtrees:
        actual.append(subtree._expanded)
    assert actual == [False, False, True]
    assert tree._expanded is True

    actual2 = []
    for subtree in tree._subtrees[0]._subtrees:
        actual2.append(subtree._expanded)
    assert actual2 == [False, False]


def test_collapse_all() -> None:
    """
    collapse all nodes and its subtrees
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    _sort_subtrees(tree)
    tree.expand_all()

    tree._subtrees[0]._subtrees[0].collapse_all()
    actual = []
    for subtree in tree._subtrees:
        actual.append(subtree._expanded)
    expected = [False, False, False]
    assert actual == expected
    assert tree._expanded is False


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

    pytest.main(['a2_sample_test.py'])
