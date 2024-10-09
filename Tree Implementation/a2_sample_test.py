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

from tm_trees import TMTree, FileSystemTree

from papers import PaperTree, _build_tree_from_dict, _load_papers_to_dict

import tempfile
import csv

# This should be the path to the "workshop" folder in the sample data.
# You may need to modify this, depending on where you downloaded and
# extracted the files.
EXAMPLE_PATH = os.path.join(os.getcwd(), 'example-directory', 'workshop')
EXAMPLE_PATH2 = os.path.join(os.getcwd(), 'example-directory', 'Folder A')


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
    assert tree.data_size == 151
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


def test_empty_space_visualizer() -> None:
    """
    Testing that there is a blank space left if the last subtree in the parent
    tree has 0 as data size
    """
    path = os.path.join(os.getcwd(), 'example-directory', 'Folder A',
                        'Folder C', 'Folder B')
    tree = FileSystemTree(path)
    tree.expand_all()
    _sort_subtrees(tree)
    tree.update_rectangles((0, 0, 1200, 100))
    # print(tree._subtrees[0]._subtrees[0]._subtrees[-1].data_size)
    rectangles = tree.get_rectangles()
    assert len(tree._subtrees) == 3
    used_width = sum([val[0][2] for val in rectangles])
    assert (tree.rect[2] != used_width)


def test_delete_single_file() -> None:
    """
    Testing the properties of the deletion of a single file in a folder 'B' which
    is in another folder 'A'
    """
    tree = FileSystemTree(EXAMPLE_PATH2)
    _sort_subtrees(tree)
    tree.expand_all()
    tree.update_rectangles((0, 0, 200, 100))
    assert tree.data_size == tree._subtrees[0]._subtrees[0].data_size
    tree._subtrees[0]._subtrees[0].delete_self()
    new_path = os.path.join(os.getcwd(), 'example-directory', 'Folder A',
                            'Folder C')
    new2 = os.path.join(os.getcwd(), 'example-directory', 'Folder A',
                        'Folder C', 'Folder B')
    assert os.path.isfile(new_path) == False
    assert os.path.isfile(new2) == False
    assert tree.data_size == 0


# ====INITIALIZER TMTREES====

def test_tmtrees_init() -> None:
    """
    Test that the initializer assigns correct values for TMTrees
    """
    depth_4_tree = TMTree('dep4', [], 60)
    depth_4_tree2 = TMTree('dep4-2', [], 234)
    depth_3_tree = TMTree('dep3', [depth_4_tree, depth_4_tree2], 0)
    depth_3_tree2 = TMTree('dep3-2', [], 30)
    depth_2_tree = TMTree('dep2', [depth_3_tree, depth_3_tree2], 0)
    root_tree = TMTree('dep1', [depth_2_tree], 0)
    assert depth_4_tree._name == 'dep4'
    assert depth_4_tree.data_size == 60
    assert depth_4_tree._subtrees == []
    assert depth_4_tree2._name == 'dep4-2'
    assert depth_4_tree2._subtrees == []
    assert depth_4_tree2.data_size == 234
    assert depth_3_tree._name == 'dep3'
    assert len(depth_3_tree._subtrees) == 2
    assert depth_3_tree.data_size == 294
    assert depth_3_tree2._name == 'dep3-2'
    assert depth_3_tree2.data_size == 30
    assert len(depth_3_tree2._subtrees) == 0
    assert depth_2_tree._name == 'dep2'
    assert depth_2_tree.data_size == 294 + 30
    assert len(depth_2_tree._subtrees) == 2
    assert root_tree._name == 'dep1'
    assert root_tree.data_size == depth_2_tree.data_size
    assert len(root_tree._subtrees) == 1


def test_tree_from_expanded_trees() -> None:
    """
    test making a new tree from two expanded trees
    """
    leaf = TMTree('l', [], 5)
    leaf2 = TMTree('meh', [], 5)
    folder = TMTree('ooo', [leaf, leaf2])
    leaf3 = TMTree('boring', [], 6)
    leaf4 = TMTree('im hungry', [], 4)
    folder2 = TMTree('fold', [leaf3, leaf4])
    assert folder.data_size == 10
    assert folder2.data_size == 10
    folder.expand_all()
    folder2.expand_all()
    assert _verify_all_expand(folder)
    assert _verify_all_expand(folder2)
    tree = TMTree('expanded?', [folder, folder2])
    assert tree.data_size == 20
    assert tree._expanded is False
    assert folder._expanded is True
    tree.update_rectangles((0, 0, 200, 100))
    rects = [t[0] for t in tree.get_rectangles()]
    assert len(rects) == 1
    tree.expand()
    assert _verify_all_expand(tree)


def test_working_ri() -> None:
    """
    Test that the representation invariants expected by user. If they break RI,
    check that TMTrees doesn't fix it.
    """
    # If name is none, then data size is none and parent tree is none
    tree = TMTree(None, [], 10)
    assert tree._parent_tree is None
    assert tree.data_size == 10
    assert tree.is_empty()
    tree.expand_all()
    assert tree._expanded is False


# ====UPDATE RECTANGLES====
def test_large_tree() -> None:
    """
    Test update rectangles on a large sized leaf
    """
    leaf1 = TMTree('large', [], 540239)
    leaf2 = TMTree('smol', [], 35)
    folder = TMTree('big', [leaf1, leaf2])
    folder.update_rectangles((0, 0, 1200, 600))
    x = [t[0] for t in folder.get_rectangles()]
    assert len(x) == 1
    assert x[0][2] == 1200


# ====GET RECTANGLES====

def test_rects_empty() -> None:
    """
    Test the return value of the rects of an empty tree
    """
    empty = TMTree(None, [], 0)
    empty.update_rectangles((0, 0, 200, 100))
    rects = empty.get_rectangles()
    assert rects == []


def test_rects_no_size() -> None:
    """
    Test the return value of rects of a not empty tree with no size
    """
    no_size = TMTree('hi', [], 0)
    no_size.update_rectangles((0, 0, 200, 100))
    rect = no_size.get_rectangles()
    assert rect == []
    no_size.expand_all()
    new = no_size.get_rectangles()
    assert new == []


# ====GET TREE AT POSITION====
# ====UPDATE DATA SIZE====
# ====MOVE====

def test_different_tree_move() -> None:
    """
    Test that move works even when trying to
    move into a completely separate tree
    """
    diff_leaf = TMTree('leaf:)', [], 12)
    parent_other = TMTree('parent', [diff_leaf])
    parent_other.expand_all()
    file_1 = TMTree('file1', [], 2)
    file_2 = TMTree('file2', [], 1)
    root = TMTree('dad', [file_1, file_2])
    assert root.data_size == 3
    assert len(root._subtrees) == 2
    diff_leaf.move(root)
    assert parent_other.data_size == 0
    assert len(parent_other._subtrees) == 0
    assert len(root._subtrees) == 3
    assert root.data_size == 15


def test_move_only_leaf() -> None:
    """
    Test moving a leaf with no parent
    """
    my_leaf = TMTree('leaf', [], 5)
    file_1 = TMTree('file1', [], 2)
    file_2 = TMTree('file2', [], 1)
    root = TMTree('dad', [file_1, file_2])
    assert root.data_size == 3
    assert len(root._subtrees) == 2
    try:
        my_leaf.move(root)
    except AttributeError:
        assert True
    else:
        assert False
    assert len(root._subtrees) == 2
    assert my_leaf not in root._subtrees


# ====CHANGE SIZE====


def test_data_size_add() -> None:
    leaf = TMTree('myleaf', [], 5)
    leaf2 = TMTree('thatleaf', [], 3)
    folderz = TMTree('eugh brother', [leaf, leaf2], 10)
    assert folderz.data_size == 8
    leafa = TMTree('otherleaf', [], 0)
    leafb = TMTree(None, [], 5)
    assert leafb.data_size == 5
    parent = TMTree('mom', [folderz, leafa, leafb])
    assert parent.data_size == 13
    leaf.change_size(2)
    assert leaf.data_size == 15
    assert folderz.data_size == 18
    assert parent.data_size == 23


def test_data_size_none() -> None:
    """
    Test the change of a folder with the name as None
    """
    proper = TMTree('properleaf', [], 4)
    not_proper = TMTree(None, [], 3)
    folder = TMTree(None, [proper, not_proper])
    assert folder.data_size == 7
    folder.change_size(1)
    assert folder.data_size == 7
    not_proper.change_size(1)
    assert folder.data_size == 10
    proper.change_size(-100)
    assert proper.data_size == 1
    honey_buns = TMTree('im hungry', [], 0)
    honey_buns.change_size(2)
    assert honey_buns.data_size == 0
    honey_buns.change_size(-15)
    assert honey_buns.data_size == 1
    try:
        honey_buns.delete_self()
    except AttributeError:
        assert True
    not_proper.change_size(-0.98)
    assert not_proper.data_size == 1
    not_proper.change_size(3)
    assert not_proper.data_size == 4
    assert folder.data_size == 5
    not_proper.change_size(-0.30)
    assert not_proper.data_size == 2


# ====DELETE SELF====

def test_data_size_change() -> None:
    """
    Check that the data size changes once deleting a file
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    _sort_subtrees(tree)
    tree.expand_all()
    tree.update_rectangles((0, 0, 1200, 300))
    expanded = tree.get_rectangles()
    assert len(expanded) == 6
    leaf = tree._subtrees[0]._subtrees[1]._subtrees[0]
    assert leaf._name == 'Q2.pdf'
    assert leaf.data_size == os.path.getsize(
        os.path.join(EXAMPLE_PATH, 'activities', 'images', 'Q2.pdf'))
    original_size = tree.data_size
    original_leaf_size = leaf.data_size
    original_parent_tree = leaf._parent_tree
    leaf.delete_self()
    assert tree.data_size == original_size - original_leaf_size
    assert leaf.data_size == 0
    assert leaf._name == 'Q2.pdf'
    assert leaf._parent_tree is original_parent_tree


def test_parent_of_delete() -> None:
    """
    Test the attributes of the parent when deleting self
    """
    leaf = TMTree('oh', [], 10)
    folder = TMTree('ya', [leaf], 50)
    assert folder.data_size == 10
    folder.expand()
    assert _verify_all_expand(folder)
    leaf.delete_self()
    assert folder.data_size == 0
    assert folder._expanded is False

    leaf2 = TMTree('eugh, brother', [], 15)
    leaf3 = TMTree('eugh', [], 30)
    folders = TMTree('f', [leaf2, leaf3], 2)
    assert folders.data_size == 45
    leaf2.change_size(1)
    assert folders.data_size == 60
    folders.expand_all()
    leaf2.delete_self()
    assert leaf2.data_size == 0
    assert folders.data_size == 30
    assert _verify_all_expand(folders)


# ====EXPAND====


def test_empty_folder_expand() -> None:
    """
    Test that an empty folder is not able to expand
    """
    empty = TMTree('mtee', [], 4)
    empty.expand_all()
    assert empty._expanded is False


def test_expand_methods() -> None:
    """Test that expand changes the rectangles
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
    assert tree._subtrees[1].rect in x


def test_expand_subtree() -> None:
    """
    test expanding a subtree without expanding its parent
    """
    blerp = TMTree('official-cool-name', [], 2)
    hungry = TMTree('im hungryy', [], 19)
    folder = TMTree('my folder', [blerp, hungry], 100)
    assert folder.data_size == 21
    parent_folder = TMTree('parent', [folder], 2)
    assert parent_folder.data_size == folder.data_size
    folder.expand()
    assert parent_folder._expanded is False
    assert _verify_all_expand(folder)


# ====EXPAND ALL====


def _verify_all_expand(tree: TMTree) -> bool:
    """
    helper that verifies that all subtrees in tree are expanded
    """
    if tree._subtrees != [] and (not tree._expanded):
        return False
    elif tree._subtrees == [] and tree._expanded:
        return False
    else:
        for subtree in tree._subtrees:
            if not (_verify_all_expand(subtree)):
                return False
        return True


def test_expand_all_subtree() -> None:
    """
    test expanding a subtree on a collapsed tree
    """
    file1 = TMTree('file1', [], 200)
    file2 = TMTree('file2', [], 3)
    folder1 = TMTree('folder1', [file1, file2])
    file3 = TMTree('file3', [], 2)
    file4 = TMTree('file4', [], 0)
    file5 = TMTree(None, [], 3)
    folder2 = TMTree('folder2', [file3, file4, file5])
    root = TMTree('root', [folder1, folder2])
    assert folder1.data_size == 203
    assert folder2.data_size == 5
    assert root.data_size == 208

    # check the actual test below, root is already fully collapsed
    assert _verify_collapse_all(root)
    folder2.expand_all()
    assert _verify_all_expand(folder2)
    assert _verify_collapse_all(folder1)


# ====COLLAPSE====


def test_collapse_on_semi_expanded() -> None:
    """
    Test that all subtrees of a semi-expanded tree are collapsed
    """
    inner_folder = TMTree('inner',
                          [TMTree('h', [], 2)])
    file1 = TMTree('simplepdf', [], 10)
    file2 = TMTree('pdf2', [], 5)
    foldera = TMTree('open_folder', [file1, file2, inner_folder])

    file3 = TMTree('not_shown', [], 15)
    file4 = TMTree('also_not', [], 10)
    folderb = TMTree('closed_folder', [file3, file4])

    root = TMTree('root', [foldera, folderb])

    assert foldera.data_size == 17
    assert folderb.data_size == 25
    assert root.data_size == 42
    root.update_rectangles((0, 0, 1200, 100))
    # expand into the two folders
    root.expand()

    # expand folder a fully
    foldera.expand_all()
    assert inner_folder._expanded
    rects = [t[0] for t in root.get_rectangles()]
    assert len(rects) == 4

    folderb.collapse()

    assert folderb._expanded is False
    assert root._expanded is False
    assert foldera._expanded is False
    assert inner_folder._expanded is False
    assert _verify_collapse_all(root)


# ====COLLAPSE ALL====
def _verify_collapse_all(tree: TMTree) -> bool:
    """
    Verify that all subtrees in this root are collapsed
    """
    if tree._expanded:
        return False
    else:
        for subtree in tree._subtrees:
            if not (_verify_collapse_all(subtree)):
                return False
        return True


def test_collapse_depth() -> None:
    path = os.path.join(os.getcwd(), 'example-directory')
    tree = FileSystemTree(path)
    _sort_subtrees(tree)
    tree.expand_all()
    assert _verify_all_expand(tree)
    tree.collapse_all()
    assert _verify_collapse_all(tree)
    tree.expand_all()
    tree._subtrees[1]._subtrees[0].collapse_all()
    assert _verify_collapse_all(tree)
    tree.expand_all()
    tree.collapse()
    assert _verify_all_expand(tree)
    tree._subtrees[0].collapse()
    assert _verify_collapse_all(tree)
    tree.expand()
    assert tree._expanded
    tree.collapse()
    rects = tree.get_rectangles()
    assert tree._expanded
    assert len(rects) == 2
    tree.expand_all()
    tree.collapse_all()
    assert not tree._expanded


# =====PAPERS=====


# Making a temporary CSV file that has some of the papers.csv lines
def test_paper_subtrees() -> None:
    """
    Test the correct amount of subtrees of papers
    """
    tree = PaperTree('CS1', [], all_papers=True)
    assert len(tree._subtrees) == 45


def test_paper_size() -> None:
    """
    Test the correct size of papers
    """
    t = PaperTree('CS1', [], all_papers=True)
    assert t.data_size == 5048


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
