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
import tempfile
import pytest
from papers import PaperTree, _build_tree_from_dict, _load_papers_to_dict

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


def test_empty_data_size_rect() -> None:
    """ Test rectangle with empty data size. """
    tree = TMTree("Tree", [], 0)
    tree.update_rectangles((0, 0, 100, 100))
    rects = [r[0] for r in tree.get_rectangles()]
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
    tree = FileSystemTree(os.path.join(EXAMPLE_PATH, ".."))

    # Delete workshop folder
    assert tree._subtrees[0].delete_self()

    tree.update_rectangles((0, 0, 100, 100))
    rects = [r[0] for r in tree.get_rectangles()]
    assert rects == []


def test_delete_entire_tree() -> None:
    """ Test data size after deleting entire tree. """
    tree = FileSystemTree(os.path.join(EXAMPLE_PATH, ".."))
    assert tree.delete_self() is False
    assert tree.data_size != 0

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

    assert subtree._expanded is False
    tree.expand_all()
    assert subtree._expanded is False
    tree.expand()
    assert subtree._expanded is False


def test_collapse() -> None:
    """ Test collapse on tree with depth 3. """
    nested_subtree = TMTree("Nested Subtree 1", [], 100)
    subtree = TMTree("Subtree 1", [nested_subtree], 0)
    tree = TMTree("Tree", [subtree], 0)

    tree.expand_all()

    assert nested_subtree._expanded is False

    subtree.collapse()

    assert tree._expanded is False
    assert subtree._expanded is False
    assert nested_subtree._expanded is False


def test_collapse_deeper() -> None:
    """ Test collapse on tree with depth 4. """
    nested_nested_subtree = TMTree("Nested Nested Subtree 1", [], 100)
    nested_subtree = TMTree("Nested Subtree 1", [nested_nested_subtree], 0)
    subtree = TMTree("Subtree 1", [nested_subtree], 0)
    tree = TMTree("Tree", [subtree], 0)

    tree.expand_all()
    subtree.collapse()

    assert tree._expanded is False
    assert subtree._expanded is False
    assert nested_subtree._expanded is False
    assert nested_nested_subtree._expanded is False

    tree.expand_all()
    nested_subtree.collapse()

    assert tree._expanded
    assert subtree._expanded is False
    assert nested_subtree._expanded is False
    assert nested_nested_subtree._expanded is False


def test_collapse_all() -> None:
    """ Test that collapse_all correctly collapses all trees. """
    tree = FileSystemTree(EXAMPLE_PATH)
    _sort_subtrees(tree)

    assert tree._expanded is False
    tree.expand_all()
    assert tree._expanded
    tree.collapse_all()
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


def test_update_rectangle():
    test_tree = FileSystemTree(EXAMPLE_PATH)
    r = test_tree.get_rectangles()
    assert len(r) == 1
    assert test_tree.data_size > 0
    test_tree.expand()
    r = test_tree.get_rectangles()
    assert len(r) == 3

    rect = (0, 0, 200, 100)
    sub1 = TMTree("sub1", [], 10)
    sub2 = TMTree("sub2", [], 25)
    sub3 = TMTree("sub3", [], 15)
    folder = TMTree("folder", [sub1, sub2, sub3])
    _sort_subtrees(folder)
    folder.update_rectangles(rect)
    assert folder.rect == (0, 0, 200, 100)
    folder.expand_all()
    assert folder._subtrees[0].rect == (0, 0, 40, 100)
    assert folder._subtrees[1].rect == (40, 0, 100, 100)
    assert folder._subtrees[2].rect == (140, 0, 60, 100)
    s1 = TMTree("s1", [], 10)
    s2 = TMTree("s2", [], 25)
    s3 = TMTree("s3", [], 15)
    f = TMTree("f", [s1, s2, s3])
    negrect = (-10, -10, -210, -110)
    f.update_rectangles(negrect)
    assert f.rect == (-10, -10, -210, -110)
    f.expand_all()
    assert f._subtrees[0].rect == (-10, -10, -210, -22)
    assert f._subtrees[1].rect == (-10, -32, -210, -55)
    assert f._subtrees[2].rect == (-10, -87, -210, -33)


def test_empty_folder():
    tree1 = TMTree("tree1", [], 0)
    tree2 = TMTree("tree2", [tree1], 0)
    assert not tree2._expanded
    tree2.expand()
    assert tree2._expanded
    assert not tree1._expanded
    tree1.expand()
    assert not tree1._expanded
    tree1.collapse()
    assert not tree1._expanded
    tree2.collapse()


def test_empty_folder_2():
    tree1 = TMTree("tree1", [], 50)
    tree2 = TMTree("tree2", [tree1], 50)
    dest = TMTree("dest", [], 0)
    tree3 = TMTree("tree3", [tree2, dest], 50)

    assert not tree3._expanded
    tree3.expand()
    assert tree3._expanded
    assert not tree2._expanded
    assert not tree1._expanded
    tree3.expand_all()
    assert tree2._expanded
    assert tree3._expanded
    assert not tree1._expanded
    tree1.collapse_all()
    assert not tree1._expanded
    assert not tree2._expanded
    assert not tree3._expanded
    tree3.expand_all()
    tree1.move(dest)
    assert dest.data_size == 0
    assert tree2.data_size == 50
    tree1.delete_self()
    assert tree2.data_size == 0
    assert tree2._subtrees == []
    assert dest._subtrees == []
    assert dest.data_size == 0


def test_sizes():
    leaf = TMTree("leaf", [], 50)
    folder1 = TMTree("folder1", [leaf], 0)
    leaf2 = TMTree("leaf2", [], 10)
    folder2 = TMTree("folder2", [leaf2], 0)
    ultifolder = TMTree("ulti", [folder1, folder2], 0)

    assert ultifolder.data_size == 60

    folder1.update_data_sizes()
    assert folder1.data_size == 50
    leaf2.move(folder1)

    folder1.update_data_sizes()
    assert folder1.data_size == 60
    folder1.update_data_sizes()
    assert len(folder1._subtrees) == 2


def test_move_folder_to_leaf():
    leaf = TMTree("leaf", [], 50)
    folder1 = TMTree("folder1", [leaf], 50)
    leaf2 = TMTree("leaf2", [], 60)
    folder2 = TMTree("folder2", [leaf2], 60)

    folder2.move(leaf)
    assert leaf._subtrees == []
    assert folder2._parent_tree is None

    leaf.move(leaf2)
    assert leaf2._subtrees == leaf._subtrees == []
    assert leaf._parent_tree is folder1
    assert leaf2._parent_tree is folder2


def test_delete_folder():
    leaf = TMTree("leaf", [], 50)
    folder1 = TMTree("folder1", [leaf], 0)
    leaf2 = TMTree("leaf2", [], 10)
    folder2 = TMTree("folder2", [leaf2], 0)
    ultifolder = TMTree("ulti", [folder1, folder2], 0)

    folder2.delete_self()
    assert len(ultifolder._subtrees) == 1
    assert leaf2._parent_tree is folder2

    assert folder2.data_size == 0
    assert leaf2.data_size == 10
    folder2.update_data_sizes()
    assert folder2.data_size == 10
    leaf2.delete_self()
    assert folder2._subtrees == []
    assert folder2.data_size == 0


def test_delete_folder_2():
    leaf = TMTree("leaf", [], 50)
    folder1 = TMTree("folder1", [leaf], 0)
    leaf2 = TMTree("leaf2", [], 10)
    folder2 = TMTree("folder2", [leaf2], 0)
    ultifolder = TMTree("ulti", [folder1, folder2], 0)

    ultifolder.delete_self()
    assert ultifolder.data_size == 60

    folder1.delete_self()
    assert ultifolder.data_size == 10
    folder2.delete_self()
    assert folder2.data_size == 0


def test_expand_all3() -> None:
    tree1 = TMTree("tree1", [], 50)
    tree2 = TMTree("tree2", [tree1], 50)
    tree3 = TMTree("tree3", [tree2], 50)
    tree4 = TMTree("tree4", [tree3], 0)
    leaf = TMTree("leaf", [], 100)

    assert tree4.data_size == 50
    tree1.delete_self()
    assert tree4.data_size == 0
    leaf.move(tree2)
    assert leaf.data_size == 100
    assert tree4.data_size == 0
    tree4.update_data_sizes()
    assert tree4.data_size == 0

    folder = TMTree("folder", [leaf], 0)

    assert folder.data_size == 100
    leaf.move(tree2)
    assert tree4.data_size == 0
    assert leaf._parent_tree is folder

    file = TMTree("file", [], 1)
    tree2._subtrees.append(file)
    assert len(tree2._subtrees) == 1
    assert tree4.data_size == 0
    tree4.update_data_sizes()
    assert tree4.data_size == 1
    leaf.move(tree2)
    assert tree4.data_size == 101


def test_change_size():
    leaf = TMTree("leaf", [], 50)
    while not leaf.data_size == 100:
        leaf.change_size(0.01)
        leaf.update_data_sizes()
    assert leaf.data_size == 100
    leaf.change_size(0.01)
    leaf.change_size(0.01)
    assert leaf.data_size == 103
    leaf.change_size(-0.01)
    assert leaf.data_size == 101
    leaf.change_size(-0.99)
    assert leaf.data_size == 1
    leaf.change_size(-0.99)
    assert leaf.data_size == 1


def test_update_datasize():
    leaf1 = TMTree("leaf1", [], 50)
    leaf2 = TMTree("leaf2", [], 70)
    leaf3 = TMTree("leaf3", [], 100)
    folder = TMTree("folder", [leaf1, leaf2, leaf3], 0)

    assert not folder._expanded
    folder.expand_all()
    assert folder._expanded
    assert not leaf1._expanded
    r = folder.get_rectangles()
    folder.collapse_all()
    assert not folder._expanded
    assert not leaf1._expanded
    folder.expand()
    assert folder._expanded
    assert not leaf1._expanded
    leaf1.expand()
    assert not leaf1._expanded
    leaf1.expand_all()
    assert not leaf1.expand_all()
    s = folder.get_rectangles()
    assert s == r
    assert len(r) == 3

    assert folder.data_size == 220
    leaf1.delete_self()
    assert leaf1.data_size == 0
    assert folder.data_size == 170
    leaf2.delete_self()
    assert leaf2.data_size == 0
    assert folder.data_size == 100
    leaf3.delete_self()
    assert leaf3.data_size == 0
    assert folder.data_size == 0


def test_move_then_expand():
    leaf = TMTree("l", [], 55)
    folder1 = TMTree("f", [leaf], 0)
    leaf2 = TMTree("l2", [], 50)
    folder2 = TMTree("f2", [leaf2], 0)

    leaf2.move(folder1)
    folder1.expand()
    r = folder1.get_rectangles()
    assert len(r) == 2
    s = folder2.get_rectangles()
    assert len(s) == 0
    folder1.collapse()
    x = folder1.get_rectangles()
    assert len(x) == 2


def test_new_update_rects():
    rect = (0, 0, 0, 0)
    leaf = TMTree("leaf", [], 50)
    leaf2 = TMTree("leaf2", [], 1)
    leaf3 = TMTree("leaf3", [], 5)
    folder = TMTree("folder", [leaf], 56)
    folder.update_rectangles(rect)
    r = folder.get_rectangles()
    assert folder.rect == (0, 0, 0, 0)
    folder.expand_all()
    s = folder.get_rectangles()
    assert leaf.rect == (0, 0, 0, 0)


def test_rect_with_1_bound():
    leaf1 = TMTree("leaf1", [], 20)
    leaf2 = TMTree("leaf2", [], 30)
    leaf3 = TMTree("leaf1", [], 10)
    leaf4 = TMTree("leaf1", [], 40)
    folder = TMTree("folder", [leaf1, leaf2, leaf3, leaf4], 100)
    rect = (0, 0, 1, 1)
    folder.update_rectangles(rect)
    r = folder.get_rectangles()
    assert folder.rect == (0, 0, 1, 1)
    folder.expand_all()
    folder.update_rectangles(rect)
    assert folder._subtrees[0].rect == (0, 0, 1, 0)
    assert folder._subtrees[1].rect == (0, 0, 1, 0)
    assert folder._subtrees[2].rect == (0, 0, 1, 0)
    assert folder._subtrees[3].rect == (0, 0, 1, 1)


def test_empty_data_size():
    leaf = TMTree(None, [], 50)
    assert leaf.data_size == 50
    leaf.update_data_sizes()
    assert leaf.data_size == 50


def test_move_root_to_folder():
    subtree = TMTree("subtree", [], 5)
    tree = TMTree("tree", [subtree], 5)
    tree1 = TMTree("tree1", [], 7)
    tree2 = TMTree("tree2", [], 5)
    folder = TMTree("folder", [tree1, tree2])
    tree.move(folder)
    assert len(folder._subtrees) == 2
    assert tree._parent_tree is None
    subtree.move(folder)
    assert len(folder._subtrees) == 3
    assert subtree._parent_tree is folder


def test_empty_get_rect():
    tree = TMTree(None, [], 5)
    r = tree.get_rectangles()
    assert r == []


def test_empty_change_size():
    tree = TMTree(None, [], 5)
    tree.change_size(10)
    assert tree.data_size == 55


def test_empty_update_rect():
    tree = TMTree(None, [], 5)
    rect = (0, 0, 100, 100)
    tree.update_rectangles(rect)
    r = tree.get_rectangles()
    assert tree.rect == (0, 0, 100, 100)
    assert r == []


def test_empty_get_tree_at_pos():
    leaf = TMTree(None, [], 5)
    leaf.update_rectangles((0, 0, 10, 20))
    assert leaf.get_tree_at_position((0, 5)) == leaf


def test_last_rect_size_0():
    leaf1 = TMTree("leaf1", [], 20)
    leaf2 = TMTree("leaf2", [], 30)
    leaf3 = TMTree("leaf3", [], 10)
    leaf4 = TMTree("leaf4", [], 40)
    leaf5 = TMTree("leaf5", [], 0)
    folder = TMTree("folder", [leaf1, leaf2, leaf3, leaf4, leaf5], 100)
    _sort_subtrees(folder)
    folder.update_rectangles((0, 0, 200, 200))
    assert folder.rect == (0, 0, 200, 200)
    folder.expand_all()
    assert folder._subtrees[0].rect == (0, 0, 200, 40)
    assert folder._subtrees[1].rect == (0, 40, 200, 60)
    assert folder._subtrees[2].rect == (0, 100, 200, 20)
    assert folder._subtrees[3].rect == (0, 120, 200, 80)
    assert folder._subtrees[4].rect == (0, 0, 0, 0)


def test_delete_folder2():
    draft = TMTree("draft.pptx", [], 58)
    reading = TMTree("reading.md", [], 6)
    Cats = TMTree("Cats.pdf", [], 16)
    Plan = TMTree("Plan.tex", [], 2)
    Q2 = TMTree("Q2.pdf", [], 20)
    Q3 = TMTree("Q3.pdf", [], 49)
    image = TMTree("images", [Cats], 16)
    images = TMTree("images", [Q2, Q3], 69)
    prep = TMTree("prep", [image, reading], 22)
    activities = TMTree("activities", [images, Plan], 71)
    workshop = TMTree("workshop", [prep, activities, draft], 151)
    exampledirectory = TMTree("example-directory", [workshop], 151)

    exampledirectory.expand()
    workshop.expand()
    draft.delete_self()
    prep.delete_self()
    activities.delete_self()
    try:
        activities.delete_self()
    except ValueError:
        assert True
    else:
        assert False
    assert workshop.data_size == 0
    assert exampledirectory.data_size == 0
    assert images._parent_tree is activities
    assert activities._parent_tree is workshop
    assert activities not in workshop._subtrees
    assert draft.data_size == 0
    assert activities.data_size == 0


def test_move_last_sub():
    draft = TMTree("draft.pptx", [], 58)
    reading = TMTree("reading.md", [], 6)
    Cats = TMTree("Cats.pdf", [], 16)
    Plan = TMTree("Plan.tex", [], 2)
    Q2 = TMTree("Q2.pdf", [], 20)
    Q3 = TMTree("Q3.pdf", [], 49)
    image = TMTree("images", [Cats], 16)
    images = TMTree("images", [Q2, Q3], 69)
    prep = TMTree("prep", [image, reading], 22)
    activities = TMTree("activities", [images, Plan], 71)
    workshop = TMTree("workshop", [prep, activities, draft], 151)
    exampledirectory = TMTree("example-directory", [workshop], 151)

    exampledirectory.expand()
    workshop.expand()
    draft.move(activities)
    assert activities._subtrees[-1] is draft
    _sort_subtrees(activities)
    assert not activities._subtrees[-1] is draft


def test_expand_and_collapse_example_dir():
    tree = FileSystemTree(EXAMPLE_PATH)
    tree.update_rectangles((0, 0, 200, 100))

    # NEED TO SORT FOR ALL TESTCASES
    _sort_subtrees(tree)

    tree.collapse_all()
    rects = tree.get_rectangles()
    assert tree.data_size > 0
    assert len(rects) == 1
    assert tree._subtrees[0].rect != (0, 0, 0, 0)
    tree.expand()
    rects = tree.get_rectangles()

    # the original rectangle should not be included anymore, only the
    # rectangles of its subtrees
    assert len(rects) == len(tree._subtrees)

    tree.collapse()
    rects = tree.get_rectangles()
    assert tree._expanded
    assert len(rects) == 3

    tree.expand_all()
    tree.collapse()
    assert tree._subtrees[0]._expanded
    assert tree._subtrees[0]._subtrees[1]._expanded

    tree.expand_all()
    tree.collapse_all()
    rects = tree.get_rectangles()
    assert not tree._expanded
    assert len(rects) == 1

    tree.expand_all()
    rects = tree.get_rectangles()
    assert len(rects) == count_leafs(tree) == 6

    tree._subtrees[0]._subtrees[0].collapse_all()
    rects = tree.get_rectangles()
    assert len(rects) == 1

    tree.expand_all()
    tree.collapse_all()
    assert not tree._expanded

    # Try collapsing draft.ppx and check if its siblings are collapsed
    tree.expand_all()
    tree._subtrees[1].collapse()
    for sub in tree._subtrees:
        assert sub._expanded is False


def test_expand_methods() -> None:
    """Test the expand methods
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    _sort_subtrees(tree)
    tree.update_rectangles((0, 0, 200, 100))
    tree.expand()
    x2 = tree.get_rectangles()
    assert len(x2) == len(tree._subtrees)
    tree._subtrees[0].collapse()
    tree.expand_all()
    x = [t[0] for t in tree.get_rectangles()]
    assert len(x) == 6
    # TODO: ASK TA why the test case below should work
    assert tree._subtrees[1].rect in x
    # assert (tree._subtrees[-1]._subtrees[0]._subtrees[0].rect,
    #         tree._subtrees[-1]._subtrees[0]._subtrees[0]._colour) in x
    # tree._subtrees[0]._subtrees[0]._subtrees[0].collapse()
    # x4 = tree.get_rectangles()
    # assert (tree._subtrees[-1]._subtrees[0]._subtrees[0].rect,
    #         tree._subtrees[-1]._subtrees[0]._subtrees[0]._colour) in x4
    # assert (tree._subtrees[0]._subtrees[0].rect,
    #         tree._subtrees[0]._subtrees[0]._colour) in x4
    # assert len(x4) == 5
    # tree.collapse_all()
    # x3 = tree.get_rectangles()
    # assert len(x3) == 1
    # tree.expand_all()
    # actual = tree.get_tree_at_position((0, 2))
    # expected = tree._subtrees[0]._subtrees[0]._subtrees[0]
    # assert actual is expected
    # tree.collapse_all()
    # tree.expand_all()
    # tree._subtrees[0]._subtrees[0]._subtrees[0].collapse()
    # tree.expand_all()


EXAMPLE_PATH2 = os.path.join(os.getcwd(), 'example-directory', 'Folder A')


def test_delete_single_file() -> None:
    """
    Testing the properties of the deletion of a single file in a folder 'B' which
    is in another folder 'A'
    """
    tree = FileSystemTree(os.path.join(os.getcwd(), 'example-directory', 'Folder A'))
    tree.expand_all()
    tree.update_rectangles((0, 0, 200, 100))
    assert tree.data_size == tree._subtrees[0]._subtrees[0].data_size
    tree._subtrees[0]._subtrees[0].delete_self()
    new_path = os.path.join(os.getcwd(), 'Folder A', 'Folder B')
    new2 = os.path.join(os.getcwd(), 'Folder A', 'Folder B', 'Folder C')
    assert os.path.isfile(new_path) is False
    assert os.path.isfile(new2) is False
    assert tree.data_size == 0


def test_empty_space_visualizer() -> None:
    """
    Testing that there is a blank space left if the last subtree in the parent
    tree has 0 as data size
    """
    path = os.path.join(os.getcwd(), 'example-directory','Folder A', 'Folder C', 'Folder B')
    tree = FileSystemTree(path)
    tree.expand_all()
    _sort_subtrees(tree)
    tree.update_rectangles((0, 0, 1200, 100))
    rectangles = tree.get_rectangles()
    assert len(tree._subtrees) == 3
    used_width = sum([val[0][2] for val in rectangles])
    assert tree.rect[2] != used_width


# other test

def test_update_rectangle2():
    test_tree = FileSystemTree(EXAMPLE_PATH)
    r = test_tree.get_rectangles()
    assert len(r) == 1
    assert test_tree.data_size > 0
    test_tree.expand()
    r = test_tree.get_rectangles()
    assert len(r) == 3

    rect = (0, 0, 200, 100)
    sub1 = TMTree("sub1", [], 10)
    sub2 = TMTree("sub2", [], 25)
    sub3 = TMTree("sub3", [], 15)
    folder = TMTree("folder", [sub1, sub2, sub3])
    _sort_subtrees(folder)
    folder.update_rectangles(rect)
    assert folder.rect == (0, 0, 200, 100)
    folder.expand_all()
    assert folder._subtrees[0].rect == (0, 0, 40, 100)
    assert folder._subtrees[1].rect == (40, 0, 100, 100)
    assert folder._subtrees[2].rect == (140, 0, 60, 100)
    s1 = TMTree("s1", [], 10)
    s2 = TMTree("s2", [], 25)
    s3 = TMTree("s3", [], 15)
    f = TMTree("f", [s1, s2, s3])
    negrect = (-10, -10, -210, -110)
    f.update_rectangles(negrect)
    assert f.rect == (-10, -10, -210, -110)
    f.expand_all()
    assert f._subtrees[0].rect == (-10, -10, -210, -22)
    assert f._subtrees[1].rect == (-10, -32, -210, -55)
    assert f._subtrees[2].rect == (-10, -87, -210, -33)


def test_empty_folder2():
    tree1 = TMTree("tree1", [], 0)
    tree2 = TMTree("tree2", [tree1], 0)
    assert not tree2._expanded
    tree2.expand()
    assert tree2._expanded
    assert not tree1._expanded
    tree1.expand()
    assert not tree1._expanded
    tree1.collapse()
    assert not tree1._expanded
    tree2.collapse()


def test_empty_folder_3():
    tree1 = TMTree("tree1", [], 50)
    tree2 = TMTree("tree2", [tree1], 50)
    dest = TMTree("dest", [], 0)
    tree3 = TMTree("tree3", [tree2, dest], 50)

    assert not tree3._expanded
    tree3.expand()
    assert tree3._expanded
    assert not tree2._expanded
    assert not tree1._expanded
    tree3.expand_all()
    assert tree2._expanded
    assert tree3._expanded
    assert not tree1._expanded
    tree1.collapse_all()
    assert not tree1._expanded
    assert not tree2._expanded
    assert not tree3._expanded
    tree3.expand_all()
    tree1.move(dest)
    assert dest.data_size == 0
    assert tree2.data_size == 50
    tree1.delete_self()
    assert tree2.data_size == 0
    assert tree2._subtrees == []
    assert dest._subtrees == []
    assert dest.data_size == 0


def test_sizes2():
    leaf = TMTree("leaf", [], 50)
    folder1 = TMTree("folder1", [leaf], 0)
    leaf2 = TMTree("leaf2", [], 10)
    folder2 = TMTree("folder2", [leaf2], 0)
    ultifolder = TMTree("ulti", [folder1, folder2], 0)

    assert ultifolder.data_size == 60

    folder1.update_data_sizes()
    assert folder1.data_size == 50
    leaf2.move(folder1)

    folder1.update_data_sizes()
    assert folder1.data_size == 60
    folder1.update_data_sizes()
    assert len(folder1._subtrees) == 2


def test_move_folder_to_leaf2():
    leaf = TMTree("leaf", [], 50)
    folder1 = TMTree("folder1", [leaf], 50)
    leaf2 = TMTree("leaf2", [], 60)
    folder2 = TMTree("folder2", [leaf2], 60)

    folder2.move(leaf)
    assert leaf._subtrees == []
    assert folder2._parent_tree is None

    leaf.move(leaf2)
    assert leaf2._subtrees == leaf._subtrees == []
    assert leaf._parent_tree is folder1
    assert leaf2._parent_tree is folder2


def test_delete_folder3():
    leaf = TMTree("leaf", [], 50)
    folder1 = TMTree("folder1", [leaf], 0)
    leaf2 = TMTree("leaf2", [], 10)
    folder2 = TMTree("folder2", [leaf2], 0)
    ultifolder = TMTree("ulti", [folder1, folder2], 0)

    folder2.delete_self()
    assert len(ultifolder._subtrees) == 1
    assert leaf2._parent_tree is folder2

    assert folder2.data_size == 0
    assert leaf2.data_size == 10
    folder2.update_data_sizes()
    assert folder2.data_size == 10
    leaf2.delete_self()
    assert folder2._subtrees == []
    assert folder2.data_size == 0


def test_delete_folder_3():
    leaf = TMTree("leaf", [], 50)
    folder1 = TMTree("folder1", [leaf], 0)
    leaf2 = TMTree("leaf2", [], 10)
    folder2 = TMTree("folder2", [leaf2], 0)
    ultifolder = TMTree("ulti", [folder1, folder2], 0)

    ultifolder.delete_self()
    assert ultifolder.data_size == 60

    folder1.delete_self()
    assert ultifolder.data_size == 10
    folder2.delete_self()
    assert folder2.data_size == 0


def test_expand_all2():
    tree1 = TMTree("tree1", [], 50)
    tree2 = TMTree("tree2", [tree1], 50)
    tree3 = TMTree("tree3", [tree2], 50)
    tree4 = TMTree("tree4", [tree3], 0)
    leaf = TMTree("leaf", [], 100)
    assert tree4.data_size == 50
    tree1.delete_self()
    assert tree4.data_size == 0
    leaf.move(tree2)
    assert leaf.data_size == 100
    assert tree4.data_size == 0
    tree4.update_data_sizes()
    assert tree4.data_size == 0

    folder = TMTree("folder", [leaf], 0)

    assert folder.data_size == 100
    leaf.move(tree2)
    assert tree4.data_size == 0
    assert leaf._parent_tree is folder

    file = TMTree("file", [], 1)
    tree2._subtrees.append(file)
    assert len(tree2._subtrees) == 1
    assert tree4.data_size == 0
    tree4.update_data_sizes()
    assert tree4.data_size == 1
    leaf.move(tree2)
    assert tree4.data_size == 101


def test_change_size2():
    leaf = TMTree("leaf", [], 50)
    while not leaf.data_size == 100:
        leaf.change_size(0.01)
        leaf.update_data_sizes()
    assert leaf.data_size == 100
    leaf.change_size(0.01)
    leaf.change_size(0.01)
    assert leaf.data_size == 103
    leaf.change_size(-0.01)
    assert leaf.data_size == 101
    leaf.change_size(-0.99)
    assert leaf.data_size == 1
    leaf.change_size(-0.99)
    assert leaf.data_size == 1


def test_update_datasize2():
    leaf1 = TMTree("leaf1", [], 50)
    leaf2 = TMTree("leaf2", [], 70)
    leaf3 = TMTree("leaf3", [], 100)
    folder = TMTree("folder", [leaf1, leaf2, leaf3], 0)

    assert not folder._expanded
    folder.expand_all()
    assert folder._expanded
    assert not leaf1._expanded
    r = folder.get_rectangles()
    folder.collapse_all()
    assert not folder._expanded
    assert not leaf1._expanded
    folder.expand()
    assert folder._expanded
    assert not leaf1._expanded
    leaf1.expand()
    assert not leaf1._expanded
    leaf1.expand_all()
    assert not leaf1.expand_all()
    s = folder.get_rectangles()
    assert s == r
    assert len(r) == 3

    assert folder.data_size == 220
    leaf1.delete_self()
    assert leaf1.data_size == 0
    assert folder.data_size == 170
    leaf2.delete_self()
    assert leaf2.data_size == 0
    assert folder.data_size == 100
    leaf3.delete_self()
    assert leaf3.data_size == 0
    assert folder.data_size == 0


def test_move_then_expand2():
    leaf = TMTree("l", [], 55)
    folder1 = TMTree("f", [leaf], 0)
    leaf2 = TMTree("l2", [], 50)
    folder2 = TMTree("f2", [leaf2], 0)

    leaf2.move(folder1)
    folder1.expand()
    r = folder1.get_rectangles()
    assert len(r) == 2
    s = folder2.get_rectangles()
    assert len(s) == 0
    folder1.collapse()
    x = folder1.get_rectangles()
    assert len(x) == 2


def test_new_update_rects2():
    rect = (0, 0, 0, 0)
    leaf = TMTree("leaf", [], 50)
    leaf2 = TMTree("leaf2", [], 1)
    leaf3 = TMTree("leaf3", [], 5)
    folder = TMTree("folder", [leaf], 56)
    folder.update_rectangles(rect)
    r = folder.get_rectangles()
    assert folder.rect == (0, 0, 0, 0)
    folder.expand_all()
    s = folder.get_rectangles()
    assert leaf.rect == (0, 0, 0, 0)


def test_rect_with_1_bound2():
    leaf1 = TMTree("leaf1", [], 20)
    leaf2 = TMTree("leaf2", [], 30)
    leaf3 = TMTree("leaf1", [], 10)
    leaf4 = TMTree("leaf1", [], 40)
    folder = TMTree("folder", [leaf1, leaf2, leaf3, leaf4], 100)
    rect = (0, 0, 1, 1)
    folder.update_rectangles(rect)
    r = folder.get_rectangles()
    assert folder.rect == (0, 0, 1, 1)
    folder.expand_all()
    folder.update_rectangles(rect)
    assert folder._subtrees[0].rect == (0, 0, 1, 0)
    assert folder._subtrees[1].rect == (0, 0, 1, 0)
    assert folder._subtrees[2].rect == (0, 0, 1, 0)
    assert folder._subtrees[3].rect == (0, 0, 1, 1)


def test_empty_data_size3():
    leaf = TMTree(None, [], 50)
    assert leaf.data_size == 50
    leaf.update_data_sizes()
    assert leaf.data_size == 50


def test_move_root_to_folder3():
    subtree = TMTree("subtree", [], 5)
    tree = TMTree("tree", [subtree], 5)
    tree1 = TMTree("tree1", [], 7)
    tree2 = TMTree("tree2", [], 5)
    folder = TMTree("folder", [tree1, tree2])
    tree.move(folder)
    assert len(folder._subtrees) == 2
    assert tree._parent_tree is None
    subtree.move(folder)
    assert len(folder._subtrees) == 3
    assert subtree._parent_tree is folder


def test_empty_get_rect3():
    tree = TMTree(None, [], 5)
    r = tree.get_rectangles()
    assert r == []


def test_empty_change_size3():
    tree = TMTree(None, [], 5)
    tree.change_size(10)
    assert tree.data_size == 55


def test_empty_update_rect2():
    tree = TMTree(None, [], 5)
    rect = (0, 0, 100, 100)
    tree.update_rectangles(rect)
    r = tree.get_rectangles()
    assert tree.rect == (0, 0, 100, 100)
    assert r == []


def test_empty_get_tree_at_pos2():
    leaf = TMTree(None, [], 5)
    leaf.update_rectangles((0, 0, 10, 20))
    assert leaf.get_tree_at_position((0, 5)) == leaf


def test_last_rect_size_1():
    leaf1 = TMTree("leaf1", [], 20)
    leaf2 = TMTree("leaf2", [], 30)
    leaf3 = TMTree("leaf3", [], 10)
    leaf4 = TMTree("leaf4", [], 40)
    leaf5 = TMTree("leaf5", [], 0)
    folder = TMTree("folder", [leaf1, leaf2, leaf3, leaf4, leaf5], 100)
    _sort_subtrees(folder)
    folder.update_rectangles((0, 0, 200, 200))
    assert folder.rect == (0, 0, 200, 200)
    folder.expand_all()
    assert folder._subtrees[0].rect == (0, 0, 200, 40)
    assert folder._subtrees[1].rect == (0, 40, 200, 60)
    assert folder._subtrees[2].rect == (0, 100, 200, 20)
    assert folder._subtrees[3].rect == (0, 120, 200, 80)
    assert folder._subtrees[4].rect == (0, 0, 0, 0)


def test_delete_folder5():
    draft = TMTree("draft.pptx", [], 58)
    reading = TMTree("reading.md", [], 6)
    cats = TMTree("Cats.pdf", [], 16)
    plan = TMTree("Plan.tex", [], 2)
    q2 = TMTree("Q2.pdf", [], 20)
    q3 = TMTree("Q3.pdf", [], 49)
    image = TMTree("images", [cats], 16)
    images = TMTree("images", [q2, q3], 69)
    prep = TMTree("prep", [image, reading], 22)
    activities = TMTree("activities", [images, plan], 71)
    workshop = TMTree("workshop", [prep, activities, draft], 151)
    exampledirectory = TMTree("example-directory", [workshop], 151)

    exampledirectory.expand()
    workshop.expand()
    draft.delete_self()
    prep.delete_self()
    activities.delete_self()
    try:
        activities.delete_self()
    except ValueError:
        assert True
    else:
        assert False
    assert workshop.data_size == 0
    assert exampledirectory.data_size == 0
    assert images._parent_tree is activities
    assert activities._parent_tree is workshop
    assert activities not in workshop._subtrees
    assert draft.data_size == 0
    assert activities.data_size == 0


def test_move_last_sub2():
    draft = TMTree("draft.pptx", [], 58)
    reading = TMTree("reading.md", [], 6)
    cats = TMTree("Cats.pdf", [], 16)
    plan = TMTree("Plan.tex", [], 2)
    q2 = TMTree("Q2.pdf", [], 20)
    q3 = TMTree("Q3.pdf", [], 49)
    image = TMTree("images", [cats], 16)
    images = TMTree("images", [q2, q3], 69)
    prep = TMTree("prep", [image, reading], 22)
    activities = TMTree("activities", [images, plan], 71)
    workshop = TMTree("workshop", [prep, activities, draft], 151)
    exampledirectory = TMTree("example-directory", [workshop], 151)

    exampledirectory.expand()
    workshop.expand()
    draft.move(activities)
    assert activities._subtrees[-1] is draft
    _sort_subtrees(activities)
    assert not activities._subtrees[-1] is draft


def test_expand_and_collapse_example_dir2():
    tree = FileSystemTree(EXAMPLE_PATH)
    tree.update_rectangles((0, 0, 200, 100))

    # NEED TO SORT FOR ALL TESTCASES
    _sort_subtrees(tree)

    tree.collapse_all()
    rects = tree.get_rectangles()
    assert tree.data_size > 0
    assert len(rects) == 1
    assert tree._subtrees[0].rect != (0, 0, 0, 0)
    tree.expand()
    rects = tree.get_rectangles()

    # the original rectangle should not be included anymore, only the
    # rectangles of its subtrees
    assert len(rects) == len(tree._subtrees)
    assert tree._expanded

    tree.collapse()
    rects = tree.get_rectangles()
    assert tree._expanded
    assert len(rects) == 3

    tree.expand_all()
    tree.collapse()
    assert tree._subtrees[0]._expanded
    assert tree._subtrees[0]._subtrees[1]._expanded

    tree.expand_all()
    tree.collapse_all()
    rects = tree.get_rectangles()
    assert not tree._expanded
    assert len(rects) == 1

    tree.expand_all()
    rects = tree.get_rectangles()
    assert len(rects) == count_leafs(tree) == 6

    tree._subtrees[0]._subtrees[0].collapse_all()
    rects = tree.get_rectangles()
    assert len(rects) == 1

    tree.expand_all()
    tree.collapse_all()
    assert not tree._expanded

    # Try collapsing draft.ppx and check if its siblings are collapsed
    tree.expand_all()
    tree._subtrees[1].collapse()
    for sub in tree._subtrees:
        assert sub._expanded == False


def count_leafs(tree: TMTree):
    """Count the amount of leafs in a given tree
    """
    if tree.is_empty():
        return 0
    if not tree._subtrees:
        return 1
    return sum([count_leafs(i) for i in tree._subtrees])


def test_smallest_data_size() -> None:
    """
    Test that the data size cannot go below one
    """
    tree = TMTree("aaaa", [], 1)
    tree.change_size(-1)
    assert tree.data_size == 1


def test_collapse_indepth() -> None:
    """ Test collapse on tree with depth 4. """
    nested_nested_subtree = TMTree("sub-sub Subtree 1",
                                   [], 10)

    nested_subtree = TMTree("sub-Subtree 1",
                            [nested_nested_subtree], 0)
    subtree = TMTree("Subtree 1", [nested_subtree], 0)
    tree = TMTree("Tree", [subtree], 0)

    tree.expand_all()
    subtree.collapse()
    # should only make subtree._expanded false

    assert tree.data_size == 10
    assert tree._expanded is False
    assert subtree._expanded is False
    assert nested_subtree._expanded is False
    assert nested_nested_subtree._expanded is False


def test_single_file() -> None:
    """Test a tree with a single file.
    """
    tree = FileSystemTree(os.path.join(EXAMPLE_PATH, 'draft.pptx'))
    assert tree._name == 'draft.pptx'
    assert tree._subtrees == []
    assert tree._parent_tree is None
    assert tree.data_size == 58
    assert is_valid_colour(tree._colour)


def test_example_data() -> None:
    """Test the root of the tree at the 'workshop' folder in the example data
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    assert tree._name == 'workshop'
    assert tree._parent_tree is None
    # assert tree.data_size == 151
    assert is_valid_colour(tree._colour)

    assert len(tree._subtrees) == 3
    for subtree in tree._subtrees:
        # Note the use of is rather than ==.
        # This checks ids rather than values.
        assert subtree._parent_tree is tree


@given(integers(min_value=100, max_value=1000),
       integers(min_value=100, max_value=1000),
       integers(min_value=100, max_value=1000),
       integers(min_value=100, max_value=1000))
def test_single_file_rectangles(x, y, width, height) -> None:
    """Test that the correct rectangle is produced for a single file."""
    tree = FileSystemTree(os.path.join(EXAMPLE_PATH, 'draft.pptx'))
    tree.update_rectangles((x, y, width, height))
    rects = tree.get_rectangles()

    # This should be just a single rectangle and colour returned.
    assert len(rects) == 1
    rect, colour = rects[0]
    assert rect == (x, y, width, height)
    assert is_valid_colour(colour)


# def test_example_data_rectangles() -> None:
#     """This test sorts the subtrees, because different operating systems have
#     different behaviours with os.listdir.
#
#     You should *NOT* do any sorting in your own code
#     """
#     tree = FileSystemTree(EXAMPLE_PATH)
#     _sort_subtrees(tree)
#
#     tree.update_rectangles((0, 0, 200, 100))
#     rects = tree.get_rectangles()
#
#     # IMPORTANT: This test should pass when you have completed Task 2, but
#     # will fail once you have completed Task 5.
#     # You should edit it as you make progress through the tasks,
#     # and add further tests for the later task functionality.
#     assert len(rects) == 6
#
#     # UPDATED:
#     # Here, we illustrate the correct order of the returned rectangles.
#     # Note that this corresponds to the folder contents always being
#     # sorted in alphabetical order. This is enforced in these sample tests
#     # only so that you can run them on your own computer, rather than on
#     # the Teaching Labs.
#     actual_rects = [r[0] for r in rects]
#     expected_rects = [(0, 0, 94, 2), (0, 2, 94, 28), (0, 30, 94, 70),
#                       (94, 0, 76, 100), (170, 0, 30, 72), (170, 72, 30, 28)]
#
#     assert len(actual_rects) == len(expected_rects)
#     for i in range(len(actual_rects)):
#         assert expected_rects[i] == actual_rects[i]


# ========================== Tests for the Task 1 =============================

#
def test_colour_range():
    tree = TMTree('test', [])
    for colour_value in tree._colour:
        assert 0 <= colour_value <= 255


def test_data_size_with_no_subtrees():
    tree = TMTree('test', [], 10)
    assert tree.data_size == 10


def test_data_size_with_subtrees():
    subtree1 = TMTree('subtree1', [], 5)
    subtree2 = TMTree('subtree2', [], 10)
    tree = TMTree('test', [subtree1, subtree2])
    assert tree.data_size == 15


def test_parent_set_for_subtrees():
    subtree = TMTree('subtree', [])
    tree = TMTree('test', [subtree])
    assert subtree._parent_tree is tree


# HELPER
@pytest.fixture
def file_structure():
    # Set up a temporary directory with a known file structure
    with tempfile.TemporaryDirectory() as tmpdirname:
        os.makedirs(os.path.join(tmpdirname, 'subdir'))
        filepath = os.path.join(tmpdirname, 'file.txt')
        with open(filepath, 'w') as f:
            f.write('Hello, world!')
        yield tmpdirname


def test_empty_directory(file_structure):
    # Test that an empty directory initializes correctly
    empty_dir_path = os.path.join(file_structure, 'subdir')
    empty_dir_tree = FileSystemTree(empty_dir_path)
    assert empty_dir_tree.data_size == 0
    assert len(empty_dir_tree._subtrees) == 0


def test_directory_with_files_and_subdirectories(file_structure):
    # Test that a directory with files and subdirectories initializes correctly
    dir_tree = FileSystemTree(file_structure)
    assert dir_tree._name == os.path.basename(file_structure)
    assert len(dir_tree._subtrees) == 2  # One for file, one for subdir
    assert sum(subtree.data_size for subtree in
               dir_tree._subtrees) == dir_tree.data_size


def test_single_file2(file_structure):
    # Test that a single file initializes correctly
    file_path = os.path.join(file_structure, 'file.txt')
    file_tree = FileSystemTree(file_path)
    assert file_tree.data_size == os.path.getsize(file_path)
    assert file_tree._name == 'file.txt'
    assert len(file_tree._subtrees) == 0


def test_data_size_of_directory(file_structure):
    # Test that the data size of a directory is the sum of its contents
    dir_tree = FileSystemTree(file_structure)
    expected_size = os.path.getsize(os.path.join(file_structure, 'file.txt'))
    assert dir_tree.data_size == expected_size


def test_data_size_of_file(file_structure):
    # Test that the data size of a file is equal to its size on disk
    file_path = os.path.join(file_structure, 'file.txt')
    file_tree = FileSystemTree(file_path)
    assert file_tree.data_size == os.path.getsize(file_path)


def test_name_attribute(file_structure):
    # Test that the _name attribute is set correctly for both files and
    # directories
    dir_tree = FileSystemTree(file_structure)
    assert dir_tree._name == os.path.basename(file_structure)
    file_path = os.path.join(file_structure, 'file.txt')
    file_tree = FileSystemTree(file_path)
    assert file_tree._name == 'file.txt'


# all the test cases up until this point passes the codetierlist solution.


# ========================== Tests for the Task 2 =============================


def test_update_rectangles_complex_structure():
    child1 = TMTree("child1", [], 25)
    child2 = TMTree("child2", [], 25)
    child3 = TMTree("child3", [], 50)
    parent = TMTree("parent", [child1, child2, child3])
    parent.update_rectangles((0, 0, 200, 100))
    assert child1.rect == (
        0, 0, 50,
        100), "Incorrect rectangle for first child in complex structure."
    assert child2.rect == (50, 0, 50,
                           100), ("Incorrect rectangle for second child in "
                                  "complex structure.")
    assert child3.rect == (100, 0, 100,
                           100), ("Incorrect rectangle for third child in "
                                  "complex structure.")


def test_single_child_occupies_all_space():
    """
    Test that a single child occupies all the available space of the parent.
    """
    root = TMTree("root", [TMTree("child", [], 100)], 100)
    root.update_rectangles((0, 0, 200, 100))
    assert root._subtrees[0].rect == (
        0, 0, 200, 100), "Single child should occupy all the available space."


def test_multiple_children_proportional_space_horizontal():
    """
    Test that multiple children occupy proportional space horizontally.
    """
    child1 = TMTree("child1", [], 50)
    child2 = TMTree("child2", [], 50)
    root = TMTree("root", [child1, child2], 100)
    root.update_rectangles((0, 0, 200, 100))
    assert child1.rect == (
        0, 0, 100,
        100), "First child should occupy half the width horizontally."
    assert child2.rect == (100, 0, 100,
                           100), ("Second child should occupy the other half "
                                  "of the width horizontally.")


def test_multiple_children_proportional_space_vertical():
    """
    Test that multiple children occupy proportional space vertically.
    """
    child1 = TMTree("child1", [], 1)
    child2 = TMTree("child2", [], 1)
    child3 = TMTree("child3", [], 1)
    root = TMTree("root", [child1, child2, child3], 3)
    root.update_rectangles((0, 0, 100, 300))
    assert child1.rect == (
        0, 0, 100, 100), "First child should occupy one-third of the height."
    assert child2.rect == (0, 100, 100,
                           100), ("Second child should occupy the second third "
                                  "of the height.")
    assert child3.rect == (
        0, 200, 100,
        100), "Third child should occupy the last third of the height."


def test_empty_tree_has_zero_area():
    """
    Test that an empty tree is assigned a rectangle with zero area.
    """
    root = TMTree("root", [], 0)
    root.update_rectangles((0, 0, 100, 100))
    assert root.rect == (
        0, 0, 0, 0), "Empty tree should have a rectangle with zero area."


def test_last_child_compensates_for_rounding_errors():
    """
    Test that the last child compensates for any rounding errors, ensuring
    full coverage of the parent area.
    """
    child1 = TMTree("child1", [], 33)
    child2 = TMTree("child2", [], 33)
    child3 = TMTree("child3", [], 34)
    root = TMTree("root", [child1, child2, child3], 100)
    root.update_rectangles((0, 0, 99, 50))
    # Expect the last child to compensate for rounding,
    # fully covering the parent width
    total_width_covered = child1.rect[2] + child2.rect[2] + child3.rect[2]
    assert total_width_covered == 99, ("The last child should compensate for "
                                       "rounding errors to ensure full "
                                       "coverage.")


# all the tests up until this point pass the codetierlist solution.

def create_test_tree():
    """
    Helper function to create a predefined test tree structure.
    This example creates a simple tree for demonstration. Adjust according
    to your TMTree implementation details.
    """
    leaf1 = TMTree("leaf1", [], 10)
    leaf2 = TMTree("leaf2", [], 20)
    leaf3 = TMTree("leaf3", [], 30)
    inner1 = TMTree("inner1", [leaf1, leaf2],
                    0)  # Size is computed from subtrees
    root = TMTree("root", [inner1, leaf3], 0)
    return root


def test_update_rectangles_basic():
    """
    Test that update_rectangles correctly updates the rectangle of a simple tree
    """
    root = create_test_tree()
    root.update_rectangles((0, 0, 600, 400))
    assert root.rect == (
        0, 0, 600, 400), "Root rectangle was not updated correctly."

    # Check if the rectangles were divided correctly, considering rounding.
    # Assuming horizontal split for simplicity. Adjust based on your logic.
    assert root._subtrees[0].rect == (
        0, 0, 300, 400), "Inner rectangle was not updated correctly."
    assert root._subtrees[1].rect == (
        300, 0, 300, 400), "Leaf rectangle was not updated correctly."


def test_get_rectangles_with_zero_size():
    """
    Test handling of nodes with zero size.
    """
    leaf1 = TMTree("leaf1", [], 0)
    leaf2 = TMTree("leaf2", [], 20)
    root = TMTree("root", [leaf1, leaf2], 0)
    root.update_rectangles((0, 0, 100, 100))

    rectangles = root.get_rectangles()

    # Only leaf2 should be returned since leaf1 has zero size.
    assert len(rectangles) == 1, "Zero-size leaf should not be included."
    assert rectangles[0][0] == (
        0, 0, 100, 100), "Incorrect rectangle for non-zero size leaf."


# all these tests up until here, pass codetierlist.

def test_proportional_space_with_mixed_orientation():
    """This tests whether the update_rectangles method correctly handles a
    mix of horizontal and vertical splits based on the ratio of width to
    height in the provided rectangle."""
    child1_1 = TMTree("child1_1", [], 20)
    child1_2 = TMTree("child1_2", [], 30)
    child1 = TMTree("child1", [child1_1, child1_2], 50)
    child2 = TMTree("child2", [], 50)
    root = TMTree("root", [child1, child2], 100)
    root.update_rectangles((0, 0, 150, 100))
    assert child1.rect == (
        0, 0, 75, 100), "Incorrect rectangle for first child."
    assert child2.rect == (
        75, 0, 75, 100), "Incorrect rectangle for second child."
    assert child1_1.rect == (
        0, 0, 75, 40), "Incorrect rectangle for child1's first subchild."
    assert child1_2.rect == (
        0, 40, 75, 60), "Incorrect rectangle for child1's second subchild."


def test_very_deep_tree_structure():
    """This tests whether the treemap can handle a very deep tree structure
    without errors and whether it assigns at least the minimum viable space to
    the deepest nodes."""
    root = TMTree("root", [], 1)
    current = root
    for i in range(10):  # Create a depth of 10
        new_child = TMTree(f"child{i}", [], 1)
        current._subtrees = [new_child]
        current = new_child
    root.update_rectangles((0, 0, 1024, 768))
    assert current.rect == (0, 0, 1024, 768), ("Deep child does not occupy all "
                                               "the space.")


def test_zero_sized_leaf_among_non_zero_sized_leaves():
    """This checks how zero-sized leaves are treated among non-zero-sized
    siblings, ensuring they don't occupy space."""
    leaf1 = TMTree("leaf1", [], 0)
    leaf2 = TMTree("leaf2", [], 50)
    leaf3 = TMTree("leaf3", [], 50)
    root = TMTree("root", [leaf1, leaf2, leaf3], 100)
    root.update_rectangles((0, 0, 200, 100))
    assert leaf1.rect == (
        0, 0, 0, 0), "Zero-sized leaf should not occupy space."
    assert leaf2.rect == (0, 0, 100, 100), "Incorrect rectangle for leaf2."
    assert leaf3.rect == (100, 0, 100, 100), "Incorrect rectangle for leaf3."


def test_non_uniform_child_sizes():
    """"tests trees with non-uniform child sizes."""
    leaf_small = TMTree("leafSmall", [], 1)
    leaf_large = TMTree("leafLarge", [], 99)
    root = TMTree("root", [leaf_small, leaf_large], 100)
    root.update_rectangles((0, 0, 200, 100))
    # Ensuring proportional allocation
    assert leaf_small.rect[2] > 0, "Small leaf should still occupy space."
    assert leaf_large.rect[2] > leaf_small.rect[
        2], "Large leaf should occupy significantly more space."


def test_get_rectangles_with_hidden_nodes():
    """checks if after deletion the node still is there.
    """
    # Assuming a method collapse exists to collapse a subtree
    child1 = TMTree("child1", [], 50)
    child2 = TMTree("child2", [], 50)
    root = TMTree("root", [child1, child2], 100)
    child1._parent_tree = root
    child2._parent_tree = root
    child1.delete_self()
    rectangles = root.get_rectangles()
    assert len(rectangles) == 1


# all tests up until this point pass code tier list.

# ========================== Tests for the Task 4 =============================

def test_single_leaf_node():
    """Test a single leaf node with no subtrees"""
    leaf = TMTree("leaf", [], 10)
    assert leaf.update_data_sizes() == 10, "Failed to handle single leaf node."


def test_tree_with_multiple_leaf_nodes():
    """Test a tree with multiple leaf nodes"""
    leaf1 = TMTree("leaf1", [], 10)
    leaf2 = TMTree("leaf2", [], 20)
    tree = TMTree("tree", [leaf1, leaf2])
    assert tree.update_data_sizes() == 30, ("Failed to update data size with "
                                            "multiple leaf nodes.")


def test_tree_with_nested_subtrees():
    """Test a tree with nested subtrees"""
    leaf1 = TMTree("leaf1", [], 10)
    leaf2 = TMTree("leaf2", [], 20)
    subtree = TMTree("subtree", [leaf1, leaf2])
    leaf3 = TMTree("leaf3", [], 5)
    tree = TMTree("tree", [subtree, leaf3])
    assert tree.update_data_sizes() == 35, ("Failed to correctly update data "
                                            "sizes with nested subtrees.")


def test_subtrees_with_data_size_zero():
    """Test a tree where some subtrees have a data_size of 0"""
    leaf1 = TMTree("leaf1", [], 0)
    leaf2 = TMTree("leaf2", [], 20)
    tree = TMTree("tree", [leaf1, leaf2])
    assert tree.update_data_sizes() == 20, ("Failed to handle subtrees with "
                                            "data_size of 0 correctly.")


def test_adding_subtree_updates_data_sizes():
    """Test that adding a subtree correctly updates the data sizes"""
    leaf1 = TMTree("leaf1", [], 10)
    tree = TMTree("tree", [leaf1])
    leaf2 = TMTree("leaf2", [], 15)
    tree._subtrees.append(leaf2)  # Simulate adding a subtree
    tree.update_data_sizes()
    assert tree.data_size == 25, ("Failed to update data sizes after adding a "
                                  "subtree.")


def test_removing_subtree_updates_data_sizes():
    """Test that removing a subtree correctly updates the data sizes"""
    leaf1 = TMTree("leaf1", [], 10)
    leaf2 = TMTree("leaf2", [], 15)
    tree = TMTree("tree", [leaf1, leaf2])
    tree._subtrees.remove(leaf1)  # Simulate removing a subtree
    tree.update_data_sizes()
    assert tree.data_size == 15, ("Failed to update data sizes after removing "
                                  "a subtree.")


def test_stress_large_number_of_subtrees():
    """Stress test with a large number of subtrees"""
    subtrees = [TMTree(f"leaf{i}", [], 1) for i in range(1000)]
    tree = TMTree("tree", subtrees)
    assert tree.update_data_sizes() == 1000, ("Failed stress test with a large "
                                              "number of subtrees.")


def test_dynamic_addition_and_removal_of_subtrees():
    """Test dynamic addition and removal of subtrees and their
    impact on data_size"""
    leaf1 = TMTree("leaf1", [], 10)
    leaf2 = TMTree("leaf2", [], 20)
    tree = TMTree("tree", [leaf1])

    # Add leaf2 dynamically and update data sizes
    tree._subtrees.append(leaf2)
    tree.update_data_sizes()
    assert tree.data_size == 30, ("Failed to update data sizes after adding a "
                                  "subtree.")

    # Remove leaf1 dynamically and update data sizes
    tree._subtrees.remove(leaf1)
    tree.update_data_sizes()
    assert tree.data_size == 20, ("Failed to update data sizes after removing "
                                  "a subtree.")


# helper
def setup_basic_tree():
    """helper to create a basic tree structure."""
    leaf1 = TMTree("leaf1", [], 10)
    leaf2 = TMTree("leaf2", [], 20)
    subtree = TMTree("subtree", [leaf1, leaf2], 30)
    return leaf1, leaf2, subtree


def test_self_move():
    """Attempting to move a node to itself."""
    _, _, subtree = setup_basic_tree()
    initial_size = subtree.data_size

    # Attempt to move subtree to itself
    subtree.move(subtree)

    # Expectations: The move should not change the tree structure or data size
    assert subtree.data_size == initial_size, ("Self-move should not change "
                                               "data size.")
    assert subtree._parent_tree is not subtree, ("A tree should not become its "
                                                 "own parent.")


def test_move_to_direct_parent():
    """Moving a node to its direct parent (should result in no operation or
    change)."""
    leaf1, _, subtree = setup_basic_tree()
    initial_subtree_size = subtree.data_size

    # Attempt to move leaf1 to its direct parent (subtree)
    leaf1.move(subtree)

    # Expectations: The move should not affect the tree structure or sizes
    assert leaf1 in subtree._subtrees, ("Leaf1 should remain in its original "
                                        "parent.")
    assert subtree.data_size == initial_subtree_size, ("Data size should "
                                                       "remain unchanged "
                                                       "after moving to "
                                                       "direct parent.")


def test_move_to_current_ancestor():
    """Moving a node to one of its current ancestors (other than direct
    parent)."""
    leaf1, leaf2, subtree = setup_basic_tree()
    parent_tree = TMTree("parent", [subtree], 0)

    # Attempt to move leaf1 to parent_tree, which is an ancestor of leaf1
    leaf1.move(parent_tree)

    # Expectations: leaf1 should now be a direct child of parent_tree
    assert leaf1 in parent_tree._subtrees, ("Leaf1 was not moved to its "
                                            "ancestor.")
    assert leaf1._parent_tree == parent_tree, ("Leaf1's parent was not updated "
                                               "to the ancestor.")
    assert leaf1 not in subtree._subtrees, ("Leaf1 was not removed from its "
                                            "original parent.")


# helper 2
def setup_complex_tree():
    """helper method to create a somewhat complex tree structure."""
    leaf1 = TMTree("leaf1", [], 10)
    leaf2 = TMTree("leaf2", [], 20)
    subtree1 = TMTree("subtree1", [leaf1], 10)
    subtree2 = TMTree("subtree2", [leaf2], 20)
    mid_tree = TMTree("mid_tree", [subtree1, subtree2], 30)
    root = TMTree("root", [mid_tree], 30)
    return leaf1, leaf2, subtree1, subtree2, mid_tree, root


def test_moving_root():
    """Attempting to move the root (which has no parent) should be a no-op
    or not allowed."""
    _, _, _, _, _, root = setup_complex_tree()
    new_parent = TMTree("new_parent", [], 0)
    root.move(new_parent)

    assert root._parent_tree is None, "Root's parent should remain None."
    assert new_parent._subtrees == [], ("New parent should not have any "
                                        "subtrees after attempting to move "
                                        "the root.")


def test_move_between_siblings():
    """tests Moving a node from one parent to another parent
     where both targets are siblings."""
    leaf1, leaf2, subtree1, subtree2, _, _ = setup_complex_tree()

    # Move leaf1 from subtree1 to subtree2
    leaf1.move(subtree2)

    assert leaf1 not in subtree1._subtrees, ("Leaf1 was not removed from "
                                             "subtree1.")
    assert leaf1 in subtree2._subtrees, "Leaf1 was not added to subtree2."


# all tests up until this point pass code tier list.

# TODO: WRITE TESTS FOR CHANGE SIZE AND DELETE SELF.

# ========================== Tests for the Task 5 =============================

def test_tree_already_expanded():
    """Test that an already expanded tree remains unchanged."""
    subtree = TMTree("Subtree", [], 100)
    tree = TMTree("Tree", [subtree], 100)
    tree._expanded = True  # Manually set the tree as expanded

    tree.expand()
    assert tree._expanded, "Tree should remain expanded"


def test_tree_is_a_leaf():
    """Test expanding a leaf does nothing."""
    leaf = TMTree("Leaf", [], 50)

    leaf.expand()
    assert not leaf._expanded, "Leaf cannot be expanded"


def test_expanding_collapsed_tree_with_subtrees():
    """Test expanding a collapsed tree with subtrees."""
    subtree = TMTree("Subtree", [], 100)
    tree = TMTree("Tree", [subtree], 100)

    tree.expand()
    assert tree._expanded, "Tree should be expanded"
    assert not subtree._expanded, "Subtrees should remain unchanged"


def test_edge_case_with_zero_data_size():
    """Test expanding a tree with zero data size but subtrees."""
    subtree = TMTree("Subtree", [], 0)
    tree = TMTree("Tree", [subtree], 0)

    tree.expand()
    assert tree._expanded, "Tree should be expandable even with zero data size"


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


def test_size_of_tree() -> None:
    """
    Seeing the Sizes of Trees
    """
    tree1 = TMTree('hi', [], 100)
    tree2 = TMTree('heyy', [], 50)
    tree3 = TMTree('hiii', [tree1, tree2], 150)
    tree4 = TMTree('haaii', [], 40)
    tree5 = TMTree('aaa', [], 40)
    tree6 = TMTree('hh', [], 30)
    largetree = TMTree('hjeyy', [tree1, tree2, tree3, tree4, tree5, tree6], 410)

    assert tree1.data_size == 100
    assert tree2.data_size == 50
    assert tree3.data_size == 150
    assert largetree.data_size == 410


def test_change_sizes() -> None:
    """
    Changing the size of the Trees
    """
    tree1 = TMTree('hi', [], 100)
    tree1.change_size(-1000)
    assert tree1.data_size == 1
    tree1.change_size(10)
    assert tree1.data_size == 11
    tree2 = TMTree('hi', [], 100)
    not_a_leaf = TMTree('s', [tree2], 100)
    not_a_leaf.change_size(50)
    assert not_a_leaf.data_size == 100


def test_update_data_sizes() -> None:
    """
    Updating the data size of the tree
    """
    tree1 = TMTree('hi', [], 100)
    tree2 = TMTree('heyy', [], 50)
    tree3 = TMTree('hiii', [tree1, tree2], 150)
    tree4 = TMTree('hey', [], 20)
    tree5 = TMTree('hiai', [], 50)
    tree6 = TMTree('y00', [tree1, tree2, tree3, tree4, tree5], 370)
    tree3.update_data_sizes()
    assert tree3.data_size == 150
    tree6.update_data_sizes()
    assert tree6.data_size == 370
    vary_tree = TMTree('hyia', [], 50)
    root_tree = TMTree('hia', [vary_tree], 50)
    vary_tree.change_size(50)
    assert vary_tree.data_size == 2550
    root_tree.update_data_sizes()
    assert root_tree.data_size == 2550
    tree7 = TMTree('hi', [], 100)
    tree8 = TMTree('heyy', [], 50)
    tree9 = TMTree('hey', [], 20)
    tree10 = TMTree('a', [tree7, tree8, tree9], 170)
    tree7.change_size(2)
    assert tree7.data_size == 300
    tree8.change_size(3)
    assert tree8.data_size == 200
    tree10.update_data_sizes()
    assert tree10.data_size == 520


def testing_type_of_tree() -> None:
    """
    different tree types
    """
    invalid_tree = TMTree(None, [])
    assert invalid_tree.data_size == 0
    assert invalid_tree.get_parent() is None
    assert invalid_tree._subtrees == []


def test_change_size1() -> None:
    """
    Changing size
    """
    tree1 = TMTree('hii', [], 0)
    tree1.change_size(-100)
    tree1.update_data_sizes()
    assert tree1.data_size == 1
    tree2 = TMTree('heyy', [], 0)
    tree2.change_size(100)
    tree2.update_data_sizes()
    assert tree2.data_size == 0


def test_deletes() -> None:
    """
    Testing the delete size
    """
    tree1 = TMTree('hiii', [], 40)
    tree2 = TMTree('heyy', [], 40)
    tree3 = TMTree('heyy+hiii', [tree1, tree2], 80)
    tree3.update_data_sizes()
    assert tree3.data_size == 80
    tree2.delete_self()
    tree2.update_data_sizes()
    tree3.update_data_sizes()
    assert tree2.data_size == 0
    assert tree3.data_size == 40


def test_delete_larger_tree() -> None:
    tree1 = TMTree('hi', [], 50)
    tree2 = TMTree('a', [], 40)
    tree3 = TMTree('aa', [tree1, tree2], 90)
    tree35 = TMTree('aa', [], 20)
    tree4 = TMTree('hii', [tree35, tree3], 110)
    assert tree3.data_size == 90
    assert tree4.data_size == 110
    tree3.delete_self()
    tree4.update_data_sizes()
    assert tree4.data_size == 20
    assert tree3.data_size == 0
    assert tree1.data_size == 50
    assert tree2.data_size == 40


def test_moves() -> None:
    tree1 = TMTree('heyy', [], 30)
    tree2 = TMTree('hii', [], 40)
    tree3 = TMTree('heyyy', [tree1, tree2], 70)
    tree35 = TMTree('aa', [], 20)
    tree4 = TMTree('aaa', [tree35], 20)
    tree1.move(tree4)
    tree4.update_data_sizes()
    tree3.update_data_sizes()
    assert tree4.data_size == 50
    assert tree3.data_size == 40
    assert len(tree4._subtrees) == 2


def test_large_tree_moving() -> None:
    tree9 = TMTree('heyy', [], 30)
    tree10 = TMTree('heyy', [], 30)
    tree11 = TMTree('heyy', [], 30)
    tree12 = TMTree('heyy', [], 30)
    tree13 = TMTree('heyy', [], 30)
    tree14 = TMTree('heyy', [], 30)
    tree15 = TMTree('heyy', [tree9, tree10, tree11, tree12, tree14, tree13])
    tree16 = TMTree('hey', [], 20)
    tree17 = TMTree('h', [tree16], 20)
    tree16.move(tree15)
    tree15.update_data_sizes()
    tree17.update_data_sizes()
    assert tree15.data_size == 200
    assert tree17.data_size == 0


def testing_get_rectangles() -> None:
    """
    testing get rectangles
    """
    a = FileSystemTree(EXAMPLE_PATH)
    _sort_subtrees(a)
    a.update_rectangles((0, 0, 200, 100))
    rects = a.get_rectangles()
    assert len(rects) == 1
    a.expand_all()
    rects = a.get_rectangles()
    assert len(rects) == 6


def test_expands() -> None:
    """
    testing different expands
    """
    a = FileSystemTree(EXAMPLE_PATH)
    _sort_subtrees(a)
    a.update_rectangles((0, 0, 200, 100))
    rects = a.get_rectangles()
    assert len(rects) == 1
    a.expand()
    assert a._expanded is True
    rects = a.get_rectangles()
    assert len(rects) == 3
    a.expand_all()
    rects = a.get_rectangles()
    assert len(rects) == 6


def test_delete_self_leaf() -> None:
    sub = TMTree("sub", [], 10)
    tree = TMTree('tree', [sub], 20)
    tree.expand()
    tree.update_rectangles((0, 0, 100, 100))
    sub.delete_self()
    assert tree.data_size == 0
    assert tree.get_tree_at_position((4, 4)) == tree
    assert sub.rect == (0, 0, 100, 100)
    assert tree.rect == (0, 0, 100, 100)
    assert len(tree.get_rectangles()) == 0
    assert tree._expanded is False


def test_delete_self_in_node() -> None:
    hola = TMTree("hello", [], 2)
    hello = TMTree('hi', [hola], 4)
    kiddan = TMTree('kiddan', [hello], 2)
    kiddan.update_rectangles((0, 0, 100, 200))
    kiddan.expand_all()
    assert hello.delete_self()
    assert kiddan.get_tree_at_position((50, 50)) == kiddan
    assert kiddan.get_rectangles() == []
    assert kiddan.rect == (0, 0, 100, 200)
    assert hello.rect == (0, 0, 100, 200)
    assert hola.rect == (0, 0, 100, 200)
    kiddan.update_rectangles((0, 0, 300, 200))
    assert kiddan.rect == (0, 0, 0, 0)
    assert hello.rect == (0, 0, 100, 200)
    assert hola.rect == (0, 0, 100, 200)
    hello.update_rectangles((0, 0, 300, 200))
    assert hello.rect == (0, 0, 0, 0)


def test_delete_root() -> None:
    # root delete
    hola = TMTree("hello", [], 2)
    hello = TMTree('hi', [hola], 4)
    bonjour = TMTree('bonjour', [], 8)
    kiddan = TMTree('kiddan', [hello, bonjour], 2)
    kiddan.update_rectangles((0, 0, 200, 100))
    kiddan.expand_all()
    rects = kiddan.get_rectangles()
    assert kiddan.get_tree_at_position((0, 1)) == hola
    assert not kiddan.delete_self()
    assert kiddan.get_tree_at_position((0, 1)) == hola
    assert kiddan.data_size == 10
    assert kiddan._expanded
    assert kiddan._subtrees == [hello, bonjour]
    assert kiddan.get_parent() is None
    assert kiddan.get_rectangles() == rects


def test_move_trees() -> None:
    """
    Testing the move function and if it only moves when a leaf is selected
    """
    subtree5 = TMTree('subtree5', [], 15)
    subtree4 = TMTree('subtree4', [], 40)
    subtree3 = TMTree('subtree3', [subtree5], 0)
    subtree2 = TMTree('subtree2', [], 50)
    subtree1 = TMTree('subtree1', [subtree4], 5)
    tree = TMTree('tree', [subtree3, subtree2, subtree1], 5)
    assert tree.data_size == 105
    data2 = subtree2.data_size
    data1 = subtree1.data_size
    data3 = subtree3.data_size
    tree.update_rectangles((0, 0, 300, 200))
    assert tree.get_tree_at_position((42, 0)) == tree
    tree.expand()
    subtree1.expand()
    assert not subtree3._expanded
    rects = tree.get_rectangles()

    # trying to move internal node to leaf
    subtree1.move(subtree2)
    assert subtree1.get_parent() == tree
    assert subtree4.get_parent() == subtree1
    assert len(subtree2._subtrees) == 0
    assert subtree1.data_size == data1
    assert subtree2.data_size == data2
    assert rects == tree.get_rectangles()

    # trying to move internal node to internal node
    subtree1.move(subtree3)
    assert subtree1.get_parent() == tree
    assert subtree4.get_parent() == subtree1
    assert len(subtree3._subtrees) == 1
    assert subtree1.data_size == data1
    assert subtree3.data_size == data3
    assert rects == tree.get_rectangles()

    # trying to move leaf to leaf
    subtree4.move(subtree2)
    assert subtree1.get_parent() == tree
    assert subtree4.get_parent() == subtree1
    assert len(subtree3._subtrees) == 1
    assert subtree1.data_size == data1
    assert subtree2.data_size == data2
    assert rects == tree.get_rectangles()

    # try to move it in yourself
    subtree4.move(subtree4)
    assert subtree1.get_parent() == tree
    assert subtree4.get_parent() == subtree1
    assert len(subtree3._subtrees) == 1
    assert subtree1.data_size == data1
    assert subtree2.data_size == data2
    assert rects == tree.get_rectangles()

    # trying to move leaf to internal node
    assert subtree1._expanded
    assert not subtree3._expanded
    subtree4.move(subtree3)
    assert not subtree1._expanded


def test_update_rectangles_single():
    """Test updating rectangles for a single node tree."""
    tm = TMTree('t', [], 5)
    tm.update_rectangles((0, 0, 100, 100))
    assert tm.rect == (0, 0, 100, 100)


def test_update_rectangles_subtrees():
    """Test update rectangles for a tree with two subtrees where width is
     greater than height."""
    subtree1 = TMTree('s1', [], 1)
    subtree2 = TMTree('s2', [], 1)
    tm = TMTree('t', [subtree1, subtree2], 0)
    tm.update_rectangles((0, 0, 100, 50))
    assert subtree1.rect == (0, 0, 50, 50)
    assert subtree2.rect == (50, 0, 50, 50)


def test_update_rectangles_subtrees2():
    """Test update rectangles for a tree with two subtrees where height is
     greater than width."""
    subtree1 = TMTree('s1', [], 1)
    subtree2 = TMTree('s2', [], 1)
    tm = TMTree('t', [subtree1, subtree2], 0)
    tm.update_rectangles((0, 0, 50, 100))
    assert subtree1.rect == (0, 0, 50, 50)
    assert subtree2.rect == (0, 50, 50, 50)


def test_update_rectangles_leaf():
    """Test update rectangles for a leaf"""
    leaf = TMTree('l', [], 1)
    leaf.update_rectangles((0, 0, 200, 50))
    assert leaf.rect == (0, 0, 200, 50)


# Test Cases for get_rectangles


def test_get_rectangles_empty_tree():
    """Test getting rectangles from an empty tree."""
    t = TMTree('t', [], 0)
    assert t.get_rectangles() == []


def test_get_rectangles_single_leaf():
    """Test getting rectangles from a tree with a single leaf and ensure the
    correct things are being returned."""
    t = TMTree('t', [], 5)
    t.update_rectangles((0, 0, 100, 100))
    assert t.get_rectangles() == [((0, 0, 100, 100), t._colour)]


def test_get_rectangles_unexpanded_tree():
    """Test getting rectangles from an unexpanded tree with subtrees."""
    sub = TMTree('s', [], 5)
    t = TMTree('t', [sub], 5)
    t.update_rectangles((0, 0, 100, 100))
    assert t.get_rectangles() == [((0, 0, 100, 100), t._colour)]


def test_get_rectangles_after_move():
    """Test get rectangles after moving to another tree"""
    l1 = TMTree("l1", [], 100)
    l2 = TMTree("l2", [], 100)
    l3 = TMTree("l3", [], 100)
    t1 = TMTree("t1", [l1, l2, l3], 300)
    s1 = TMTree("s1", [], 50)
    s2 = TMTree("s2", [], 50)
    dest = TMTree("dest", [s1, s2], 100)
    assert t1._subtrees == [l1, l2, l3]
    assert l3 not in dest._subtrees
    l3.move(dest)
    assert l3 == dest._subtrees[-1]
    l2.move(dest)
    assert l2 == dest._subtrees[-1]
    l1.move(dest)
    assert l1 == dest._subtrees[-1]
    assert dest.data_size == 400


# Test Cases for get_tree_at_position


def test_get_tree_at_position_outside():
    """Test that no tree is returned when position is outside the rectangle."""
    tm = TMTree('t', [], 5)
    tm.update_rectangles((0, 0, 100, 100))
    assert tm.get_tree_at_position((150, 150)) is None


def test_get_tree_at_position_inside_leaf():
    """Test that the tree is returned when position is inside the rectangle."""
    tm = TMTree('t', [], 5)
    tm.update_rectangles((0, 0, 100, 100))
    assert tm.get_tree_at_position((50, 50)) is tm

# Test Cases for update_data_sizes


def test_update_data_sizes_leaf():
    """ Test updating data sizes for a leaf node."""
    tm = TMTree('t', [], 5)
    assert tm.update_data_sizes() == 5


def test_update_data_sizes_after_move():
    """Test updating data sizes for a tree with a single subtree."""
    subtree = TMTree('s', [], 3)
    tm = TMTree('t', [subtree], 0)
    subtree.delete_self()
    assert tm.update_data_sizes() == 0
    tm.update_rectangles((0,0,100,100))
    assert tm.rect == (0,0,0,0)


def test_update_data_sizes_multiple_subtrees():
    # Test updating data sizes for a tree with multiple subtrees.
    subtree1 = TMTree('s1', [], 3)
    subtree2 = TMTree('s2', [], 2)
    tm = TMTree('t', [subtree1, subtree2], 0)
    assert tm.update_data_sizes() == 5
    tm.change_size(2)
    assert tm.data_size == 5
    subtree1.change_size(-1)
    subtree2.change_size(-1)
    assert tm.data_size == 2


# Test Cases for move


def test_move_leaf_to_empty_subtree():
    """Test moving to a leaf"""
    tm_leaf = TMTree('leaf', [], 5)
    tm_dest = TMTree('dest', [], 0)
    tm_leaf.move(tm_dest)
    assert tm_leaf._parent_tree is None


def test_move_leaf_to_subtree():
    """Test moving a leaf to a tree with subtrees."""
    tm_leaf = TMTree('leaf', [], 5)
    tm_sub = TMTree('sub', [], 10)
    tm_dest = TMTree('dest', [tm_sub], 0)
    try:
        tm_leaf.move(tm_dest)
    except AttributeError:
        assert True
    else:
        assert False


def test_move_root():
    root = TMTree('root', [], 5)
    sub1 = TMTree('folder 1', [])
    sub2 = TMTree('folder 2', [], 5)
    f = TMTree('folder', [sub1, sub2])
    assert f._parent_tree is None
    try:

        root.move(f)
    except AttributeError:
        assert True
    else:
        assert False
    assert root not in f._subtrees


def test_move_non_leaf():
    """Test moving a non-leaf tree."""
    tm_leaf = TMTree('leaf', [], 5)
    tm_sub = TMTree('sub', [tm_leaf], 0)
    tm_dest = TMTree('dest', [], 10)
    tm_sub.move(tm_dest)
    assert tm_sub not in tm_dest._subtrees
    assert tm_leaf._parent_tree is tm_sub


# Test Cases for change_size


def test_change_size_leaf_increase():
    """Test increasing the size of a leaf."""
    tm = TMTree('t', [], 5)
    tm.change_size(0.2)
    assert tm.data_size == 6


def test_change_size_leaf_decrease():
    """Test decreasing the size of a leaf."""
    tm = TMTree('t', [], 5)
    tm.change_size(-0.2)
    assert tm.data_size == 4


def test_change_size_non_leaf_does_nothing():
    """Test changing size does nothing for non-leaf nodes."""
    subtree = TMTree('s', [], 3)
    tm = TMTree('t', [subtree], 0)
    original_data_size = tm.data_size
    tm.change_size(0.2)
    assert tm.data_size == original_data_size


def test_delete_self_leaf2():
    """Test deleting a leaf from its parent."""
    tm_leaf = TMTree('leaf', [], 5)
    tm_parent = TMTree('parent', [tm_leaf], 0)
    assert tm_leaf.delete_self()
    assert tm_leaf not in tm_parent._subtrees
    assert tm_parent.data_size == 0


def test_delete_self_root_does_nothing():
    """Test deleting root."""
    tm_root = TMTree('root', [], 5)
    assert not tm_root.delete_self()


def test_delete_self_internal_node():
    """Test deleting an internal node updates parent size correctly."""
    tm_child = TMTree('child', [], 5)
    tm_internal = TMTree('internal', [tm_child], 0)
    tm_root = TMTree('root', [tm_internal], 0)
    assert tm_internal.delete_self()
    assert tm_internal not in tm_root._subtrees
    assert tm_root.data_size == 0


def test_collapse_all_leaf():
    """Collapsing all on a leaf node should do nothing."""
    leaf = TMTree('leaf', [], 5)
    leaf.collapse_all()
    assert not leaf._expanded


def test_collapse_all_leaf2():
    """Collapsing all on a leaf node should do nothing."""
    leaf = TMTree('leaf', [], 5)
    t = TMTree('t', [leaf], 5)
    t.collapse()
    assert not leaf._expanded
    t.expand_all()
    assert t._expanded
    assert not leaf._expanded
    t.collapse_all()
    assert not t._expanded
    assert not leaf._expanded


def test_collapse_all2():
    """Collapsing all on an internal node should collapse the entire tree."""
    child = TMTree('child', [], 5)
    child3 = TMTree('child3', [], 10)
    child2 = TMTree('child2', [child3], 10)
    parent = TMTree('parent', [child, child2], 15)
    parent.expand_all()
    child.collapse_all()
    assert not parent._expanded and not child._expanded
    assert not child2._expanded and not child3._expanded


DATA_FILE = 'cs1_papers.csv'


@pytest.fixture
def paper_tree_no_year():
    return PaperTree('CS1', [], all_papers=True, by_year=False)


@pytest.fixture
def paper_tree_with_year():
    return PaperTree('CS1', [], all_papers=True, by_year=True)


def test_initialization_no_year(paper_tree_no_year):
    assert paper_tree_no_year is not None


def test_initialization_with_year(paper_tree_with_year):
    assert paper_tree_with_year is not None


def test_reading():
    """checks for validation that the subtrees being formed are in fact
    trees."""
    lst = _build_tree_from_dict(_load_papers_to_dict(False))
    assert isinstance(lst[0], PaperTree)


def test_2():
    """ok"""
    p = PaperTree("ok1", [], all_papers=False)
    curr = p
    while curr._subtrees:
        curr = curr._subtrees[0]
    assert curr._find_tree_root() is p


def _get_root(self) -> TMTree:
    """Return the root Tree of this TMTree
    """
    if self._parent_tree is None:
        return self

    else:
        return self._parent_tree._get_root()

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


def test_single_file3() -> None:
    """Test a tree with a single file.
    """
    a = os.path.join(EXAMPLE_PATH, 'activities', 'Plan.tex')
    tree = FileSystemTree(a)
    assert tree._name == 'Plan.tex'
    assert tree._subtrees == []
    assert tree._parent_tree is None
    assert tree.data_size == 2
    assert is_valid_colour(tree._colour)


def test_single_file1() -> None:
    """Test a tree with a single file.
    """
    a = os.path.join(EXAMPLE_PATH, 'draft.pptx')
    tree = FileSystemTree(a)
    assert tree._name == 'draft.pptx'
    assert tree._subtrees == []
    assert tree._parent_tree is None
    assert tree.data_size == 58
    assert is_valid_colour(tree._colour)


#
#
def test_example_data3() -> None:
    """Test the root of the tree at the 'workshop' folder in the example data
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    assert tree._name == 'workshop'
    assert tree._parent_tree is None
    assert tree.data_size == 151
    assert is_valid_colour(tree._colour)

    assert len(tree._subtrees) == 3
    for subtree in tree._subtrees:
        # Note the use of is rather than ==.
        # This checks ids rather than values.
        assert subtree._parent_tree is tree


#
#
def test_example_data_size() -> None:
    """Test the data_size of the tree is indeed the sum of the data_size of its
     subtrees
    """
    tree = FileSystemTree(EXAMPLE_PATH)

    assert len(tree._subtrees) == 3
    data_size_counter = 0
    for subtree in tree._subtrees:
        # Note the use of is rather than ==.
        # This checks ids rather than values.
        data_size_counter += subtree.data_size
    assert data_size_counter == tree.data_size


# TODO not sure when a tree will ever be empty
def test_name_is_none() -> None:
    """Test that the representation invariants are met when self._name is None
    """
    tree = TMTree(None, [])
    assert not tree._name
    assert not tree._subtrees
    assert tree.is_empty()
    assert not tree.get_parent()
    assert tree.data_size == 0
    assert is_valid_colour(tree._colour)

    tree = TMTree(None, [TMTree(None, [])])
    assert not tree._name
    # TODO: ????? FAILS REPRESENTATION INVARIANT
    assert len(tree._subtrees) == 1
    assert tree.is_empty()
    assert not tree.get_parent()
    assert tree.data_size == 0
    assert is_valid_colour(tree._colour)

    tree = TMTree(None, [], 10)
    assert tree.is_empty()
    assert tree.data_size > 0


def test_empty_folder3(make_empty_dir) -> None:
    """Test a tree with a single empty directory.
    """
    a = os.path.join(make_empty_dir, 'sub')
    tree = FileSystemTree(a)
    assert tree._name == 'sub'
    assert tree._subtrees == []
    assert tree._parent_tree is None
    assert tree.data_size == 0
    assert is_valid_colour(tree._colour)
    tree.update_rectangles((55, 55, 0, 0))
    assert tree.rect == (0, 0, 0, 0)


def test_invalid_path() -> None:
    """Test creating a tree with a path that does not exist
    """
    # This will look join empty after workshop, however, empty is not in the
    # workshop directory
    try:
        FileSystemTree(os.path.join(EXAMPLE_PATH, 'empty'))
    except FileNotFoundError:
        assert True
    else:
        assert False


def test_update_rect_sub_bigger_rect_than_parent():
    t1 = TMTree('t1', [], 10)
    t2 = TMTree('t2', [], 10)
    t3 = TMTree('t3', [], 20)
    sub1 = TMTree('s1', [t1, t2])
    sub2 = TMTree('s2', [t3])
    main = TMTree('m', [sub1, sub2])
    main.update_rectangles((0, 0, 100, 100))
    sub1.update_rectangles((0, 0, 200, 200))
    assert main.rect == (0, 0, 100, 100)
    assert sub1.rect == (0, 0, 200, 200)
    main.expand_all()
    # EDGE CASE
    assert main.get_tree_at_position((101, 100)) is None
    assert main.get_tree_at_position((101, 101)) is None

    sub1.update_rectangles((-50, -50, 40, 40))
    assert main.get_tree_at_position((-10, -30)) is None
    assert main.get_tree_at_position((-10, -29)) is None

    sub1.update_rectangles((70, 70, 40, 40))

    assert main.get_tree_at_position((110, 90)) is None
    assert main.get_tree_at_position((110, 91)) is None


def test_only_directories_rectangles(make_empty_dir) -> None:
    """This test sorts the subtrees, because different operating systems have
    different behaviours with os.listdir.

    You should *NOT* do any sorting in your own code
    """
    os.makedirs(os.path.join(make_empty_dir, 'sub', 'sub2'))

    os.makedirs(os.path.join(make_empty_dir, 'sub1a'))
    os.makedirs(os.path.join(make_empty_dir, 'sub1b'))
    tree = FileSystemTree(make_empty_dir)
    _sort_subtrees(tree)

    tree.update_rectangles((0, 0, 200, 100))
    tree.expand_all()
    rects = tree.get_rectangles()

    assert tree.data_size == 0
    assert len(rects) == 0

    actual_rects = [r[0] for r in rects]
    # TODO not sure if the last empty folder will take up all the space
    expected_rects = [(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)]

    for i in range(len(actual_rects)):
        assert expected_rects[i] == actual_rects[i]


# TODO: Test negative rectangle

def test_edge_rectangles():
    tree = FileSystemTree(EXAMPLE_PATH)
    _sort_subtrees(tree)
    tree.update_rectangles((0, 0, 0, 100))
    tree.expand_all()

    assert tree.rect == (0, 0, 0, 100)
    assert tree._subtrees[0].rect == (0, 0, 0, 47)

    tree.update_rectangles((0, 0, 100, 100))
    assert tree._subtrees[0].rect == (0, 0, 100, 47)

    tree.update_rectangles((0, 0, 1, 1))
    assert tree._subtrees[0].rect == (0, 0, 1, 0)
    assert tree._subtrees[0]._subtrees[0].rect == (0, 0, 0, 0)
    assert tree._subtrees[0]._subtrees[1].rect == (0, 0, 1, 0)
    assert tree._subtrees[1].rect == (0, 0, 1, 0)
    assert tree._subtrees[2].rect == (0, 0, 1, 1)
    assert tree._subtrees[2]._subtrees[0].rect == (0, 0, 1, 0)
    assert tree._subtrees[2]._subtrees[1].rect == (0, 0, 1, 1)
    rects = tree.get_rectangles()
    expected = [(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 1, 0), (0, 0, 1, 0),
                (0, 0, 1, 0), (0, 0, 1, 1)]
    for i in range(len(rects)):
        assert rects[i][0] == expected[i]

    tree.update_rectangles((0, 0, -200, -100))
    tree.expand_all()
    assert tree.rect == (0, 0, -200, -100)

    rects = tree.get_rectangles()
    expected = [(0, 0, -200, -1), (0, -1, -200, -13), (0, -14, -200, -33),
                (0, -47, -200, -38),
                (0, -85, -200, -10), (0, -95, -200, -5)]
    for i in range(len(rects)):
        assert rects[i][0] == expected[i]

    tree.update_rectangles((0, 0, -10, 10))
    tree._subtrees[0]._subtrees[0].collapse()
    rects = tree.get_rectangles()

    expected = [(0, 0, -10, 4), (0, 4, -10, 3), (0, 7, -10, 2), (0, 9, -10, 1)]
    for i in range(len(rects)):
        assert rects[i][0] == expected[i]

    # Test a tree two parents up with data size 0 has a child with data size 1 (impossibe ik just tryna see how they code work)
    os.mkdir('parent')
    os.mkdir('parent/sub')
    os.mkdir('parent/sub/leaf')
    # os.rmdir('parent/sub/leaf')
    # os.rmdir('parent/sub')
    # os.rmdir('parent')
    t = FileSystemTree(os.path.join(os.getcwd(), 'parent'))
    t.update_rectangles((0, 0, 200, 100))
    b = t._subtrees[0]._subtrees[0]
    b.datasize = 1
    t.update_rectangles((0, 0, 200, 100))
    assert b.rect == (0, 0, 0, 0)

    t.expand_all()
    assert [] == t.get_rectangles()
    os.rmdir('parent/sub/leaf')
    os.rmdir('parent/sub')
    os.rmdir('parent')


def test_get_tree_at_pos3():
    tree = FileSystemTree(EXAMPLE_PATH)
    _sort_subtrees(tree)
    tree.update_rectangles((0, 0, 200, 100))

    assert tree.get_tree_at_position((0, 0)) == tree

    tree.expand_all()
    assert tree.get_tree_at_position((0, 0)) == tree._subtrees[0]._subtrees[0]
    assert tree.get_tree_at_position((0, 1)) == tree._subtrees[0]._subtrees[0]
    assert tree.get_tree_at_position((1, 0)) == tree._subtrees[0]._subtrees[0]

    assert tree.get_tree_at_position((200, 100)) == tree._subtrees[2]._subtrees[
        1]
    assert tree.get_tree_at_position((201, 100)) is None

    tree._subtrees[0]._subtrees[0].collapse()
    assert tree.get_tree_at_position((0, 0)) == tree._subtrees[0]
    tree._subtrees[0].collapse()
    assert tree.get_tree_at_position((0, 0)) == tree
    assert tree.get_tree_at_position((-10, 10)) is None
    assert tree.get_tree_at_position((-10, -10)) is None

    tree.update_rectangles((0, 0, 0, 0))
    assert tree.get_tree_at_position((0, 0)) == tree
    assert tree.get_tree_at_position((0, 1)) is None

    tree.expand_all()
    tree.update_rectangles((0, 0, -10, 10))
    assert tree.get_tree_at_position((0, 0)) is None
    assert tree.get_tree_at_position((0, 1)) is None

    # negative starting position
    tree.update_rectangles((-10, -10, 10, 10))
    assert tree.get_tree_at_position((0, 0))._name == 'reading.md'

    # CAN NOT BE NEGATIVE WIDTH
    tree.update_rectangles((10, 10, -20, -20))
    assert tree.get_tree_at_position((0, 0)) is None


def test_example_data_not_displayed_rectangles() -> None:
    """This test sorts the subtrees, because different operating systems have
    different behaviours with os.listdir.

    You should *NOT* do any sorting in your own code
    """
    EXAMPLE_PATH = os.path.join(os.getcwd(),
                                'example-directory', 'workshop')

    tree = FileSystemTree(EXAMPLE_PATH)
    _sort_subtrees(tree)

    tree.update_rectangles((0, 0, 200, 100))
    assert tree.rect == (0, 0, 200, 100)
    assert tree._subtrees[0].rect == (
        0, 0, int(200 * tree._subtrees[0].data_size / tree.data_size), 100)

    start = int(200 * tree._subtrees[0].data_size / tree.data_size)
    assert tree._subtrees[1].rect == (
        start, 0, int(200 * tree._subtrees[1].data_size / tree.data_size), 100)

    # since this is the last subtree it should go to the end
    start = int(200 * tree._subtrees[0].data_size / tree.data_size) + int(
        200 * tree._subtrees[1].data_size / tree.data_size)
    assert tree._subtrees[2].rect == (start, 0, 200 - start, 100)


def test_single_directory_rectangle(make_empty_dir) -> None:
    """This test sorts the subtrees, because different operating systems have
    different behaviours with os.listdir.

    You should *NOT* do any sorting in your own code
    """
    path = os.path.join(make_empty_dir, 'sub')

    tree = FileSystemTree(path)
    _sort_subtrees(tree)

    tree.update_rectangles((0, 0, 200, 100))
    rects = tree.get_rectangles()

    assert len(rects) == 0
    assert isinstance(rects, list)
    # assert isinstance(rects[0], tuple)
    assert tree.data_size == 0
    assert tree._subtrees == []
    assert tree._name == 'sub'
    assert not tree.get_parent()


def bunch_of_subtrees_with_one_file_rectangles() -> None:
    """This test sorts the subtrees, because different operating systems have
    different behaviours with os.listdir.

    You should *NOT* do any sorting in your own code
    """
    path = os.path.join(os.getcwd(), 'bunch-of-subtrees-with-one-file')

    tree = FileSystemTree(path)
    _sort_subtrees(tree)

    tree.update_rectangles((0, 0, 200, 100))
    rects = tree.get_rectangles()

    # IMPORTANT: This test should pass when you have completed Task 2, but
    # will fail once you have completed Task 5.
    # You should edit it as you make progress through the tasks,
    # and add further tests for the later task functionality.
    assert len(rects) == 1

    # UPDATED:
    # Here, we illustrate the correct order of the returned rectangles.
    # Note that this corresponds to the folder contents always being
    # sorted in alphabetical order. This is enforced in these sample tests
    # only so that you can run them on your own computer, rather than on
    # # the Teaching Labs.
    actual_rects = [(r[0], r[1]) for r in rects]
    expected_rects = [(0, 0, 0, 0)]

    assert len(actual_rects) == len(expected_rects)
    for i in range(len(actual_rects)):
        assert expected_rects[i] == actual_rects[i][0]
        assert is_valid_colour(actual_rects[i][1])


def test_change_size_data_size_0():
    t = TMTree('t', [], 0)
    t.change_size(-1)
    assert t.data_size == 1


def test_change_size_example_directory():
    tree = FileSystemTree(EXAMPLE_PATH)
    tree.update_rectangles((0, 0, 200, 100))

    # NEED TO SORT FOR ALL TESTCASES
    _sort_subtrees(tree)

    # Attempt to change non leaf node
    d_t = tree.data_size
    tree.change_size(0.01)
    assert tree.data_size == d_t

    # Attempt to change leaf node by making it one unit bigger
    # (round up) factor
    d = tree._subtrees[1].data_size
    r = tree._subtrees[1].rect
    tree._subtrees[1].change_size(0.01)
    assert tree._subtrees[1].data_size - d == 1
    assert isinstance(tree._subtrees[1].data_size, int)
    assert tree.data_size == d_t + 1
    assert tree._subtrees[1].rect == r

    # Attempt to change leaf node by making it one unit smaller
    # (round -0.58) to -1
    d = tree._subtrees[1].data_size
    tree._subtrees[1].change_size(-0.01)
    assert tree._subtrees[1].data_size - d == -1
    assert isinstance(tree._subtrees[1].data_size, int)

    # Attempt to make a nodes data size 0 (it can not go down to 0)
    tree._subtrees[1].change_size(-1)
    assert tree._subtrees[1].data_size == 1


def test_delete_self_example_directory():
    tree = FileSystemTree(EXAMPLE_PATH)
    tree.update_rectangles((0, 0, 200, 100))

    _sort_subtrees(tree)

    # try to delete root
    assert not tree.delete_self()

    # Delete draft.pptx
    data = tree.data_size
    rect = tree._subtrees[0].rect
    lower_rect = tree._subtrees[2]._subtrees[0].rect
    subtrees = tree._subtrees.copy()

    node = tree._subtrees[1]
    node_rect = node.rect
    data_n = node.data_size

    assert node in subtrees
    assert node.delete_self()
    assert node.data_size == 0
    assert node_rect != (0, 0, 0, 0)
    assert node.rect == node_rect
    assert tree.data_size == data - data_n
    assert is_valid_colour(node._colour)
    assert len(subtrees) == len(tree._subtrees) + 1
    assert node.get_parent() is not None
    assert node not in tree._subtrees
    assert node._name is not None

    tree.update_data_sizes()
    tree.update_rectangles(tree.rect)
    assert is_valid_colour(node._colour)

    # Maybe node once it is deleted you are supposed to set its data to 0
    assert tree.data_size + data_n == data
    assert node.data_size == 0
    assert rect != tree._subtrees[0].rect
    assert lower_rect != tree._subtrees[1]._subtrees[0].rect

    # Ensure expanding does not change the actual rects
    new_rect = tree._subtrees[1]._subtrees[0].rect
    tree.expand_all()
    tree.update_rectangles(tree.rect)
    assert new_rect == tree._subtrees[1]._subtrees[0].rect

    # Delete reading.md
    read = tree._subtrees[1]._subtrees[1]
    data_read = read.data_size
    data_tree = tree.data_size
    data_sub = tree._subtrees[1].data_size
    tree.update_data_sizes()
    tree.update_rectangles(tree.rect)
    assert read in tree._subtrees[1]._subtrees
    assert read.delete_self()
    assert tree.data_size == data_tree - data_read
    assert tree._subtrees[1].data_size == data_sub - data_read


def test_move_example_directory():
    tree = FileSystemTree(EXAMPLE_PATH)
    tree.update_rectangles((0, 0, 200, 100))

    # NEED TO SORT FOR ALL TESTCASES
    _sort_subtrees(tree)
    dest_tree = tree._subtrees[0]._subtrees[1]
    move_leaf = tree._subtrees[2]._subtrees[0]._subtrees[0]

    tree.update_data_sizes()
    tree.update_rectangles(tree.rect)

    assert move_leaf._name == 'Cats.pdf'
    assert dest_tree._name == 'images'
    data1 = move_leaf.get_parent().data_size
    data2 = dest_tree.data_size
    move_leaf_rect = move_leaf.rect
    prep_rect = tree._subtrees[2].rect
    prep_data = tree._subtrees[2].data_size
    activites_data = dest_tree.get_parent().data_size

    move_leaf.move(dest_tree)

    # test that if you move something to a subtree of a bigger tree,
    # the whole trees data gets updated and rects
    assert move_leaf not in tree._subtrees[0]._subtrees[0]._subtrees
    assert move_leaf in dest_tree._subtrees
    assert tree._subtrees[0]._subtrees[0].data_size < data1
    assert data2 + move_leaf.data_size == dest_tree.data_size
    assert activites_data + move_leaf.data_size == dest_tree.get_parent().data_size
    assert prep_data - move_leaf.data_size == tree._subtrees[2].data_size
    assert move_leaf.rect == move_leaf_rect
    assert tree._subtrees[2].rect == prep_rect


# TODO: make a case where you try to move a folder to a leaf and nothing happens
# TODO: make a case where you move a leaf to a leaf and nothing happens
# TODO: make a case where you move a folder to a folder and nothing happens


# TODO: TEST EXAMPLE EXPAND ONCE THEN EXPAND ALL ON ONE OF THE SUBTREE FOLDERS,
# TODO: WONDER IF THE WHOLE TREE SHOULD EXPAND INCLUDING PREP OR JUST ACTIVITIES????????


# def test_expand_all():
#     pass


def test_move_folder():
    folder1 = FileSystemTree(os.path.join(EXAMPLE_PATH, 'activities'))
    folder2 = FileSystemTree(os.path.join(EXAMPLE_PATH, 'prep'))

    _sort_subtrees(folder1)
    _sort_subtrees(folder2)

    folder1.update_data_sizes()
    folder1.update_rectangles((0, 0, 100, 200))
    folder2.update_data_sizes()
    folder2.update_rectangles((0, 0, 100, 200))

    folder1.move(folder2)
    assert folder1 not in folder2._subtrees
    assert folder1.get_parent() is not folder2

    file = folder2._subtrees[1]
    parent = file.get_parent()
    data1 = folder1.data_size
    data2 = folder2.data_size
    subs = folder2._subtrees
    file_rect = file.rect

    file.move(folder1)

    folder2.update_data_sizes()

    assert folder2.data_size == data2 - file.data_size
    assert folder1.data_size == data1 + file.data_size
    assert file not in subs
    assert file in folder1._subtrees
    assert file.get_parent() is not parent
    assert parent is folder2
    assert file.get_parent() is folder1

    folder1.update_rectangles((0, 0, 100, 200))
    folder2.update_rectangles((0, 0, 100, 200))

    x, y, w, h = file_rect
    old_area = w * h

    x, y, w, h = file.rect
    new_area = w * h
    assert new_area < old_area


def test_move_empty():
    t1 = TMTree('1', [])
    t2 = TMTree('2', [])
    t3 = TMTree('3', [t2])
    main = TMTree('3', [t1, t3])
    t1.move(t3)
    assert t1.data_size == 0
    assert t1 in t3._subtrees


def test_expand_collapse_move_delete_one_file(make_empty_dir):
    """Test all task 5 operations on single file, one with a data size and
    a tree with data size 0
    """
    # file with a size
    a = os.path.join(EXAMPLE_PATH, 'activities', 'Plan.tex')
    tree1 = FileSystemTree(a)

    # empty dir
    b = os.path.join(make_empty_dir, 'sub')
    tree2 = FileSystemTree(b)

    tree3 = FileSystemTree(os.path.join(make_empty_dir))

    tree1.update_data_sizes()
    tree1.update_rectangles((0, 0, 200, 100))
    tree2.update_data_sizes()
    tree2.update_rectangles((0, 0, 200, 100))
    tree3.update_data_sizes()
    tree3.update_rectangles((0, 0, 200, 100))

    rect1 = tree1.get_rectangles()
    rect2 = tree2.get_rectangles()

    assert len(rect1) == 1
    assert len(rect2) == 0
    sub1 = tree1._subtrees
    parent1 = tree1._parent_tree
    tree1.move(tree1)
    assert tree1._subtrees == sub1
    assert tree1.get_parent() == parent1 is None

    sub2 = tree2._subtrees
    parent2 = tree2._parent_tree
    tree2.move(tree2)
    assert tree2._subtrees == sub2
    assert tree2.get_parent() == parent2 is None

    sub2 = tree2._subtrees
    parent1 = tree1._parent_tree

    assert tree2.data_size == 0

    # MOVE A LEAF INTO A LEAF
    # Nothing should happen because tree2 is a leaf
    tree1.move(tree2)
    assert tree1.get_parent() is parent1 is None
    assert len(tree2._subtrees) == 0
    assert tree1 not in tree2._subtrees
    assert tree2.data_size == 0

    try:
        # This is impossible because you can not move a root with no subtrees
        # into another file
        tree1.move(tree3)
    except AttributeError:
        assert True

    empty = TMTree(None, [])
    tree1._subtrees.append(empty)

    try:
        # This is impossible because you can not move a root with no subtrees
        # into another file
        empty.move(tree3)
    except AttributeError:
        assert True
        assert empty not in tree3._subtrees

    assert not empty.delete_self()

    tree1._subtrees = []
    tree2._subtrees.append(tree1)
    tree1._parent_tree = tree2
    assert tree2.data_size == 0

    tree2.update_data_sizes()
    assert tree2.data_size == tree1.data_size

    assert tree3.data_size == 0
    tree1.move(tree3)
    assert tree1.get_parent() is tree3
    assert len(tree3._subtrees) == 2
    assert tree1 in tree3._subtrees
    assert tree3.data_size == tree1.data_size
    assert tree2.data_size == 0


def test_move_root3():
    root = TMTree('r', [], 5)
    sub1 = TMTree('s1', [])
    sub2 = TMTree('s2', [], 5)
    f = TMTree('f', [sub1, sub2])
    assert f._parent_tree is None
    try:

        root.move(f)
    except AttributeError:
        assert True
    else:
        assert False
    assert root not in f._subtrees


def test_expand_and_collapse_example_dir3():
    tree = FileSystemTree(EXAMPLE_PATH)
    tree.update_rectangles((0, 0, 200, 100))

    # NEED TO SORT FOR ALL TESTCASES
    _sort_subtrees(tree)

    tree.collapse_all()
    rects = tree.get_rectangles()
    assert tree.data_size > 0
    assert len(rects) == 1
    assert tree._subtrees[0].rect != (0, 0, 0, 0)
    tree.expand()
    rects = tree.get_rectangles()

    # the original rectangle should not be included anymore, only the
    # rectangles of its subtrees
    assert len(rects) == len(tree._subtrees)

    tree.collapse()
    rects = tree.get_rectangles()
    assert tree._expanded
    assert len(rects) == 3

    tree.expand_all()
    tree.collapse()
    assert tree._subtrees[0]._expanded
    assert tree._subtrees[0]._subtrees[1]._expanded

    tree.expand_all()
    tree.collapse_all()
    rects = tree.get_rectangles()
    assert not tree._expanded
    assert len(rects) == 1

    tree.expand_all()
    rects = tree.get_rectangles()
    assert len(rects) == count_leafs(tree) == 6

    tree._subtrees[0]._subtrees[0].collapse_all()
    rects = tree.get_rectangles()
    assert len(rects) == 1

    tree.expand_all()
    tree.collapse_all()
    assert not tree._expanded

    # Try collapsing draft.ppx and check if its siblings are collapsed
    tree.expand_all()
    tree._subtrees[1].collapse()
    for sub in tree._subtrees:
        assert sub._expanded is False


def test_delete_single_file3(make_empty_dir):
    a = os.path.join(EXAMPLE_PATH, 'activities', 'Plan.tex')
    tree1 = FileSystemTree(a)
    b = os.path.join(make_empty_dir, 'sub')
    tree2 = FileSystemTree(b)
    tree1.update_rectangles((0, 0, 200, 100))
    tree3 = TMTree('3', [], 5)

    # Should not be deleted
    assert not tree1.delete_self()
    assert not tree2.delete_self()
    assert not tree3.delete_self()


def test_nested_file(make_empty_dir):
    tm1 = TMTree('t', [], 5)
    tm2 = TMTree('t2', [tm1])
    main = TMTree('m', [tm2])
    main.update_rectangles((0, 0, 100, 100))
    # Check that the main tree rect goes to (0,0,0,0)
    assert main.update_data_sizes() == 5
    assert tm1.delete_self()
    assert main.rect != (0, 0, 0, 0)
    assert main.update_data_sizes() == 0

    main.update_rectangles((0, 0, 100, 100))

    assert main.rect == (0, 0, 0, 0)
    assert tm2.rect == (0, 0, 0, 0)
    assert tm1.rect != (0, 0, 0, 0)
    assert main.update_data_sizes() == 0


def test_empty_space_visualizer3() -> None:
    """
    Testing that there is a blank space left if the last subtree in the parent
    tree has 0 as data size
    """
    a = TMTree('a', [], 5)
    b = TMTree('b', [], 6)
    c = TMTree('c', [], 0)
    tree = TMTree('t', [a, b, c])

    _sort_subtrees(tree)
    tree.expand_all()
    tree.update_rectangles((0, 0, 201, 100))
    assert len(tree._subtrees) == 3
    assert tree._subtrees[0].rect[2] + tree._subtrees[1].rect[2] != tree.rect[2]


# DIRECTORY: Folder A -> Folder B -> Folder C -> 'non-empty file', 'Z empty file'
#
# Make sure to use Z when naming the empty file so that it is the last subtree.
# Assign EXAMPLE_PATH2 to that directory

# if failing remove the mkdir start 4 lines thing and the put it back
def test_edge_update_rect():
    os.mkdir('main')
    os.mkdir('main/a')
    os.mkdir('main/b')
    os.mkdir('main/c')
    root = FileSystemTree(os.path.join(os.getcwd(), 'main'))
    a = root._subtrees[0]
    b = root._subtrees[1]
    c = root._subtrees[2]

    _sort_subtrees(root)

    a.data_size = 10
    c.data_size = 10
    root.update_data_sizes()
    root.update_rectangles((0, 0, 100, 200))
    assert b.rect == (0, 0, 0, 0)

    os.rmdir('main/a')
    os.rmdir('main/b')
    os.rmdir('main/c')
    os.rmdir('main')





# ========================================================================
#                               HELPERS
# ========================================================================

@pytest.fixture()
def make_empty_dir():
    with tempfile.TemporaryDirectory() as temp:
        os.makedirs(os.path.join(temp, 'sub'))
        yield temp


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


def test_pos_corner():
    t1 = TMTree('t1', [], 10)
    t2 = TMTree('t2', [], 10)
    t3 = TMTree('t3', [], 20)
    sub1 = TMTree('s1', [t1, t2])
    sub2 = TMTree('s2', [t3])
    main = TMTree('m', [sub1, sub2])
    main.update_rectangles((0, 0, 100, 100))
    main.expand_all()
    assert t1 is main.get_tree_at_position((25, 25))



if __name__ == '__main__':
    import pytest

    pytest.main(['dont_submit_test.py'])
