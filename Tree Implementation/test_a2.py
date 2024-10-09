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
import pytest
from hypothesis import given
from hypothesis.strategies import integers

from papers import PaperTree, _build_tree_from_dict, _load_papers_to_dict
from tm_trees1 import TMTree, FileSystemTree
import tempfile

# This should be the path to the "workshop" folder in the sample data.
# You may need to modify this, depending on where you downloaded and
# extracted the files.
EXAMPLE_PATH = os.path.join(os.getcwd(), 'example-directory', 'workshop')


# def test_expand_methods() -> None:
#     """Test the expand methods
#     """
#     tree = FileSystemTree(EXAMPLE_PATH)
#     tree.update_rectangles((0, 0, 200, 100))
#     tree.expand()
#     x2 = tree.get_rectangles()
#     assert len(x2) == len(tree._subtrees)
#     tree._subtrees[0].collapse()
#     tree.expand_all()
#     x = tree.get_rectangles()
#     assert len(x) == 6
#     assert not ((tree._subtrees[1].rect, tree._subtrees[1]._colour) in x)


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
def test_colour_range() -> None:
    """tests the randomized colours for TMTrees"""
    tree = TMTree('test', [])
    for colour_value in tree._colour:
        assert 0 <= colour_value <= 255


def test_data_size_with_no_subtrees() -> None:
    """Tests TMtree datasize innit with no subtrees """
    tree = TMTree('test', [], 10)
    assert tree.data_size == 10


def test_data_size_with_subtrees() -> None:
    """Tests TMtree datasize init with actual subtrees"""
    subtree1 = TMTree('subtree1', [], 5)
    subtree2 = TMTree('subtree2', [], 10)
    tree = TMTree('test', [subtree1, subtree2])
    assert tree.data_size == 15


def test_parent_set_for_subtrees() -> None:
    """Checks the parent tree initialization for the TMtree"""
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


def test_empty_directory(file_structure) -> None:
    # Test that an empty directory initializes correctly
    empty_dir_path = os.path.join(file_structure, 'subdir')
    empty_dir_tree = FileSystemTree(empty_dir_path)
    assert empty_dir_tree.data_size == 0
    assert len(empty_dir_tree._subtrees) == 0


def test_directory_with_files_and_subdirectories(file_structure) -> None:
    """Test that a directory with files and subdirectories initializes
    correctly"""
    dir_tree = FileSystemTree(file_structure)
    assert dir_tree._name == os.path.basename(file_structure)
    assert len(dir_tree._subtrees) == 2  # One for file, one for subdir
    assert sum(subtree.data_size for subtree in
               dir_tree._subtrees) == dir_tree.data_size


def test_single_file2(file_structure) -> None:
    """Test that a single file initializes correctly"""
    file_path = os.path.join(file_structure, 'file.txt')
    file_tree = FileSystemTree(file_path)
    assert file_tree.data_size == os.path.getsize(file_path)
    assert file_tree._name == 'file.txt'
    assert len(file_tree._subtrees) == 0


def test_data_size_of_directory(file_structure) -> None:
    """Test that the data size of a directory is the sum of its contents"""
    dir_tree = FileSystemTree(file_structure)
    expected_size = os.path.getsize(os.path.join(file_structure, 'file.txt'))
    assert dir_tree.data_size == expected_size


def test_data_size_of_file(file_structure) -> None:
    """Test that the data size of a file is equal to its size on disk"""
    file_path = os.path.join(file_structure, 'file.txt')
    file_tree = FileSystemTree(file_path)
    assert file_tree.data_size == os.path.getsize(file_path)


def test_name_attribute(file_structure) -> None:
    """Test that the _name attribute is set correctly for both files and
    directories"""
    dir_tree = FileSystemTree(file_structure)
    assert dir_tree._name == os.path.basename(file_structure)
    file_path = os.path.join(file_structure, 'file.txt')
    file_tree = FileSystemTree(file_path)
    assert file_tree._name == 'file.txt'


# ========================== Tests for the Task 2 =============================


def test_update_rectangles_complex_structure() -> None:
    """tests update rectangles for smth that i cannot bother to explain here"""
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


def test_single_child_occupies_all_space() -> None:
    """
    Test that a single child occupies all the available space of the parent.
    """
    root = TMTree("root", [TMTree("child", [], 100)], 100)
    root.update_rectangles((0, 0, 200, 100))
    assert root._subtrees[0].rect == (
        0, 0, 200, 100), "Single child should occupy all the available space."


def test_multiple_children_proportional_space_horizontal() -> None:
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


def test_multiple_children_proportional_space_vertical() -> None:
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


def test_empty_tree_has_zero_area() -> None:
    """
    Test that an empty tree is assigned a rectangle with zero area.
    """
    root = TMTree("root", [], 0)
    root.update_rectangles((0, 0, 100, 100))
    assert root.rect == (
        0, 0, 0, 0), "Empty tree should have a rectangle with zero area."


def test_last_child_compensates_for_rounding_errors() -> None:
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


def create_test_tree() -> TMTree:
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


def test_update_rectangles_basic() -> None:
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


def test_get_rectangles_with_zero_size() -> None:
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


def test_proportional_space_with_mixed_orientation() -> None:
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


def test_very_deep_tree_structure() -> None:
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


def test_zero_sized_leaf_among_non_zero_sized_leaves() -> None:
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


def test_non_uniform_child_sizes() -> None:
    """"tests trees with non-uniform child sizes."""
    leaf_small = TMTree("leafSmall", [], 1)
    leaf_large = TMTree("leafLarge", [], 99)
    root = TMTree("root", [leaf_small, leaf_large], 100)
    root.update_rectangles((0, 0, 200, 100))
    # Ensuring proportional allocation
    assert leaf_small.rect[2] > 0, "Small leaf should still occupy space."
    assert leaf_large.rect[2] > leaf_small.rect[
        2], "Large leaf should occupy significantly more space."


def test_get_rectangles_with_hidden_nodes() -> None:
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


# ========================== Tests for the Task 4 =============================

def test_single_leaf_node() -> None:
    """Test a single leaf node with no subtrees"""
    leaf = TMTree("leaf", [], 10)
    assert leaf.update_data_sizes() == 10, "Failed to handle single leaf node."


def test_tree_with_multiple_leaf_nodes() -> None:
    """Test a tree with multiple leaf nodes"""
    leaf1 = TMTree("leaf1", [], 10)
    leaf2 = TMTree("leaf2", [], 20)
    tree = TMTree("tree", [leaf1, leaf2])
    assert tree.update_data_sizes() == 30, ("Failed to update data size with "
                                            "multiple leaf nodes.")


def test_tree_with_nested_subtrees() -> None:
    """Test a tree with nested subtrees"""
    leaf1 = TMTree("leaf1", [], 10)
    leaf2 = TMTree("leaf2", [], 20)
    subtree = TMTree("subtree", [leaf1, leaf2])
    leaf3 = TMTree("leaf3", [], 5)
    tree = TMTree("tree", [subtree, leaf3])
    assert tree.update_data_sizes() == 35, ("Failed to correctly update data "
                                            "sizes with nested subtrees.")


def test_subtrees_with_data_size_zero() -> None:
    """Test a tree where some subtrees have a data_size of 0"""
    leaf1 = TMTree("leaf1", [], 0)
    leaf2 = TMTree("leaf2", [], 20)
    tree = TMTree("tree", [leaf1, leaf2])
    assert tree.update_data_sizes() == 20, ("Failed to handle subtrees with "
                                            "data_size of 0 correctly.")


def test_adding_subtree_updates_data_sizes() -> None:
    """Test that adding a subtree correctly updates the data sizes"""
    leaf1 = TMTree("leaf1", [], 10)
    tree = TMTree("tree", [leaf1])
    leaf2 = TMTree("leaf2", [], 15)
    tree._subtrees.append(leaf2)  # Simulate adding a subtree
    tree.update_data_sizes()
    assert tree.data_size == 25, ("Failed to update data sizes after adding a "
                                  "subtree.")


def test_removing_subtree_updates_data_sizes() -> None:
    """Test that removing a subtree correctly updates the data sizes"""
    leaf1 = TMTree("leaf1", [], 10)
    leaf2 = TMTree("leaf2", [], 15)
    tree = TMTree("tree", [leaf1, leaf2])
    tree._subtrees.remove(leaf1)  # Simulate removing a subtree
    tree.update_data_sizes()
    assert tree.data_size == 15, ("Failed to update data sizes after removing "
                                  "a subtree.")


def test_stress_large_number_of_subtrees() -> None:
    """Stress test with a large number of subtrees"""
    subtrees = [TMTree(f"leaf{i}", [], 1) for i in range(1000)]
    tree = TMTree("tree", subtrees)
    assert tree.update_data_sizes() == 1000, ("Failed stress test with a large "
                                              "number of subtrees.")


def test_dynamic_addition_and_removal_of_subtrees() -> None:
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
def setup_basic_tree() -> tuple:
    """helper to create a basic tree structure."""
    leaf1 = TMTree("leaf1", [], 10)
    leaf2 = TMTree("leaf2", [], 20)
    subtree = TMTree("subtree", [leaf1, leaf2], 30)
    return leaf1, leaf2, subtree


def test_self_move() -> None:
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


def test_move_to_direct_parent() -> None:
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


def test_move_to_current_ancestor() -> None:
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
def setup_complex_tree() -> tuple:
    """helper method to create a somewhat complex tree structure."""
    leaf1 = TMTree("leaf1", [], 10)
    leaf2 = TMTree("leaf2", [], 20)
    subtree1 = TMTree("subtree1", [leaf1], 10)
    subtree2 = TMTree("subtree2", [leaf2], 20)
    mid_tree = TMTree("mid_tree", [subtree1, subtree2], 30)
    root = TMTree("root", [mid_tree], 30)
    return leaf1, leaf2, subtree1, subtree2, mid_tree, root


def test_moving_root() -> None:
    """Attempting to move the root (which has no parent) should be a no-op
    or not allowed."""
    _, _, _, _, _, root = setup_complex_tree()
    new_parent = TMTree("new_parent", [], 0)
    root.move(new_parent)

    assert root._parent_tree is None, "Root's parent should remain None."
    assert new_parent._subtrees == [], ("New parent should not have any "
                                        "subtrees after attempting to move "
                                        "the root.")


def test_move_between_siblings() -> None:
    """tests Moving a node from one parent to another parent
     where both targets are siblings."""
    leaf1, leaf2, subtree1, subtree2, _, _ = setup_complex_tree()

    # Move leaf1 from subtree1 to subtree2
    leaf1.move(subtree2)

    assert leaf1 not in subtree1._subtrees, ("Leaf1 was not removed from "
                                             "subtree1.")
    assert leaf1 in subtree2._subtrees, "Leaf1 was not added to subtree2."


# ========================== Tests for the Task 5 =============================

def test_tree_already_expanded() -> None:
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


# all test up to this point pass code tier list.

def setup_tree():
    """Helper function to create a basic tree structure for testing."""
    leaf1 = TMTree("Leaf1", [], 10)
    leaf2 = TMTree("Leaf2", [], 20)
    subtree1 = TMTree("Subtree1", [leaf1, leaf2], 30)
    root = TMTree("Root", [subtree1], 30)
    return leaf1, leaf2, subtree1, root


def test_collapse_subtree():
    """Test collapsing a subtree."""
    _, _, subtree1, _ = setup_tree()
    # Initially, the subtree is expanded
    subtree1._expanded = True
    subtree1.collapse()
    assert not subtree1._parent_tree._expanded, ("Parent of the subtree should "
                                                 "be collapsed.")


def test_collapse_already_collapsed_subtree():
    """Test collapsing an already collapsed subtree."""
    _, _, subtree1, root = setup_tree()
    # Manually collapse the root, which collapses all its subtrees
    root._expanded = False
    subtree1.collapse()
    assert not root._expanded, ("Collapsing an already collapsed subtree "
                                "should leave the state unchanged.")


def test_collapse_leaf_node():
    """Test collapsing a leaf node."""
    leaf1, _, _, _ = setup_tree()
    leaf1.collapse()
    assert not leaf1._parent_tree._expanded, ("Parent of the leaf should be "
                                              "collapsed.")


def test_edge_case_with_multiple_subtrees():
    """Test collapsing one of multiple subtrees."""
    leaf1, leaf2, _, root = setup_tree()
    # Adding another leaf to root to create multiple subtrees
    leaf3 = TMTree("Leaf3", [], 30)
    root._subtrees.append(leaf3)
    leaf2.collapse()
    assert not root._expanded, ("Collapsing one subtree should collapse the "
                                "parent.")


def test_tree_with_only_one_subtree():
    """Test collapsing a tree with only one subtree."""
    _, _, subtree1, _ = setup_tree()
    subtree1.collapse()
    assert not subtree1._parent_tree._expanded, ("Parent with a single subtree "
                                                 "should be collapsed.")


# all tests till this point pass code tier list.
def setup_complex_tree2():
    """Helper function to create a complex tree structure for testing."""
    leaf1 = TMTree("Leaf1", [], 10)
    leaf2 = TMTree("Leaf2", [], 20)
    subtree1 = TMTree("Subtree1", [leaf1], 10)
    subtree2 = TMTree("Subtree2", [leaf2], 20)
    root = TMTree("Root", [subtree1, subtree2], 30)
    return leaf1, leaf2, subtree1, subtree2, root


def test_expand_all_on_leaf_node():
    """Expand all on a leaf node should not change its state."""
    leaf1, _, _, _, _ = setup_complex_tree2()
    leaf1.expand_all()
    # Since leaf1 is a leaf, it doesn't have an _expanded attribute; its
    # parent should remain unaffected.
    assert leaf1._parent_tree._expanded is False, ("Leaf node's parent should "
                                                   "not be affected by "
                                                   "expand_all on leaf.")


def test_expand_all_on_already_expanded_node():
    """Expand all on an already expanded node should keep it and all its
    subtrees expanded."""
    _, _, _, _, root = setup_complex_tree2()
    root.expand_all()
    assert root._expanded is True, "Root should remain expanded."
    for subtree in root._subtrees:
        assert subtree._expanded is True, "All subtrees should remain expanded."


def test_expand_all_on_root_node():
    """Expand all on the root node should expand the entire tree."""
    _, _, _, _, root = setup_complex_tree2()
    root.expand_all()
    assert root._expanded is True, "Root node should be expanded."
    for subtree in root._subtrees:
        assert subtree._expanded is True, ("All subtrees of the root should be "
                                           "expanded.")


def test_deeply_nested_subtrees():
    """Expand all on a tree with deeply nested subtrees should expand every
    node."""
    leaf1, leaf2, subtree1, subtree2, root = setup_complex_tree2()
    # Creating deeper nesting
    deep_subtree = TMTree("DeepSubtree", [leaf1, leaf2], 30)
    subtree1._subtrees.append(deep_subtree)
    root.expand_all()
    assert (root._expanded is True and subtree1._expanded is True and
            subtree2._expanded is True and deep_subtree._expanded is True), \
        "Every node in the tree should be expanded."


# all tests till here pass code tier list.
def setup_tree_for_collapse_all():
    """Create a complex tree with multiple levels of nesting for testing
    collapse_all."""
    leaf1 = TMTree("Leaf1", [], 10)
    leaf2 = TMTree("Leaf2", [], 20)
    subtree1 = TMTree("Subtree1", [leaf1, leaf2], 30)
    subtree2 = TMTree("Subtree2", [], 40)
    root = TMTree("Root", [subtree1, subtree2], 70)
    return root, subtree1, subtree2, leaf1, leaf2


def test_collapse_all_from_root():
    """Collapsing from root should collapse the entire tree."""
    root, subtree1, _, _, _ = setup_tree_for_collapse_all()
    root.expand_all()  # Ensure the tree is fully expanded before collapsing
    root.collapse_all()
    assert not root._expanded, "Root should be collapsed."
    assert not subtree1._expanded, "All subtrees should be collapsed."


def test_collapse_all_from_subtree():
    """Collapsing from a subtree should collapse the entire tree, not just
    the subtree."""
    root, subtree1, _, _, _ = setup_tree_for_collapse_all()
    subtree1.expand_all()
    subtree1.collapse_all()
    assert not root._expanded, ("Collapsing from subtree should collapse the "
                                "root as well.")
    assert not subtree1._expanded, ("The subtree from which collapse_all was "
                                    "called should be collapsed.")


def test_collapse_all_on_already_collapsed_tree():
    """Collapsing an already collapsed tree should leave the tree unchanged."""
    root, _, _, _, _ = setup_tree_for_collapse_all()
    # No prior expansion, tree starts collapsed
    root.collapse_all()
    assert not root._expanded, ("An already collapsed tree should remain "
                                "collapsed.")


def test_root_movement():
    root = TMTree('root', [], 5)
    subtree_a = TMTree('folder 1', [])
    subtree_b = TMTree('folder 2', [], 5)
    folder = TMTree('folder', [subtree_a, subtree_b])
    assert folder._parent_tree is None
    try:

        root.move(folder)
    except AttributeError:
        assert True
    else:
        assert False
    assert root not in folder._subtrees


def test_collapse_all_multiple_levels():
    """Collapse all should work on a tree with multiple nesting levels."""
    root, subtree1, subtree2, leaf1, leaf2 = setup_tree_for_collapse_all()
    # Create deeper nesting
    deep_subtree = TMTree("DeepSubtree", [leaf1], 10)
    subtree1._subtrees.append(deep_subtree)
    root.expand_all()  # Make sure the tree is fully expanded
    root.collapse_all()
    assert (not root._expanded and not subtree1._expanded and not
    subtree2._expanded and not deep_subtree._expanded), ("All levels of the "
                                                         "tree should be "
                                                         "collapsed.")


# all tests till here pass code tier list.

@pytest.fixture
def complex_tree():
    """
    Creates a more complex TMTree structure for broader test coverage.
    """
    leaf1 = TMTree("Leaf1", [], 10)
    leaf2 = TMTree("Leaf2", [], 20)
    subtree = TMTree("Subtree", [leaf1, leaf2], 30)
    root = TMTree("Root", [subtree], 30)
    return root, subtree, leaf1, leaf2


def test_empty_tree_initialization():
    """Test that an empty tree is initialized correctly."""
    empty_tree = TMTree(None, [], 0)
    assert empty_tree.is_empty() is True
    assert empty_tree.data_size == 0


def test_expand_all_leaf_does_nothing(complex_tree):
    """Test that calling expand_all on a leaf does nothing."""
    _, _, leaf1, _ = complex_tree
    leaf1.expand_all()
    assert leaf1._expanded is False


def test_collapse_all_root_collapses_everything(complex_tree):
    """Test that collapse_all on the root collapses the entire tree."""
    root, subtree, _, _ = complex_tree
    root.expand_all()  # First, ensure everything is expanded
    root.collapse_all()
    assert not root._expanded
    assert not subtree._expanded


def test_expand_on_collapsed_root_expands_it(complex_tree):
    """Test that calling expand on a collapsed root expands it."""
    root, _, _, _ = complex_tree
    root._expanded = False
    root.expand()
    assert root._expanded


def test_collapse_non_root(complex_tree):
    """Test collapsing a subtree that is not the root."""
    _, subtree, _, _ = complex_tree
    subtree.expand_all()  # Ensure it's expanded first
    subtree.collapse()
    assert not subtree._expanded


def test_update_rectangles_correctly_assigns_rectangles(complex_tree):
    """Test that update_rectangles assigns correct rectangles."""
    root, _, _, _ = complex_tree
    root.update_rectangles((0, 0, 100, 100))
    assert root.rect == (0, 0, 100, 100), "Root rectangle not updated correctly"


# all tests till here pass code tier list.


def test_empty_space_visualizer() -> None:
    """
    Testing that there is a blank space left if the last subtree in the parent
    tree has 0 as data size
    """
    path = os.path.join(os.getcwd(), 'e1', 'nested')
    tree = FileSystemTree(path)
    tree.expand_all()
    _sort_subtrees(tree)
    tree.update_rectangles((0, 0, 200, 100))
    # print(tree._subtrees[0]._subtrees[0]._subtrees[-1].data_size)
    # assert len(tree._subtrees) == 3
    assert (tree.rect[2] != tree._subtrees[0].rect[2] + tree._subtrees[1].rect[
        2])


def test_change_size_on_non_leaf() -> None:
    # Create a non-leaf node with subtrees
    subtree = TMTree(name="child", subtrees=[], data_size=5)
    non_leaf = TMTree(name="parent", subtrees=[subtree], data_size=5)

    # Store the original data_size
    original_size = non_leaf.data_size

    # Factor to change the size by
    factor = 1.2

    # Call change_size on the non-leaf node
    non_leaf.change_size(factor)

    # Check that the size has not changed
    assert non_leaf.data_size == original_size


@pytest.fixture
def large_data_tree():
    parent = TMTree("Parent", [], 2 ** 30)  # Extremely large data size
    child = TMTree(None, [], 2 ** 30)
    child._parent_tree = None
    parent._subtrees.append(child)
    return child


@pytest.fixture
def tree_with_siblings():
    parent = TMTree("Parent", [], 100)
    target = TMTree(None, [], 50)
    target._parent_tree = parent
    sibling = TMTree("Sibling", [], 50)
    sibling._parent_tree = parent
    parent._subtrees = [target, sibling]
    return target


def test_delete_tree_with_siblings(tree_with_siblings):
    assert tree_with_siblings.delete_self() is True
    assert tree_with_siblings not in tree_with_siblings._parent_tree._subtrees
    assert tree_with_siblings.data_size == 0


# Edge case: A tree with None name, non-zero data_size, attempting to delete
# itself without a parent
@pytest.fixture
def tree_without_parent():
    # No parent_tree specified
    lone_tree = TMTree(None, [], 100)
    return lone_tree


def test_delete_tree_without_parent(tree_without_parent):
    assert tree_without_parent.delete_self() is False
    # Ensure data_size remains unchanged
    assert tree_without_parent.data_size > 0


def test_rect_with_no_data_size() -> None:
    """Ensure rectangles with zero data size are handled correctly."""
    empty_tree = TMTree("EmptyNode", [], 0)
    empty_tree.update_rectangles((0, 0, 100, 100))
    assert [rectangle[0] for rectangle in empty_tree.get_rectangles()] == []


def test_no_area_rectangles() -> None:
    """Check handling of rectangles with zero area."""
    node_with_data = TMTree("NodeWithData", [], 100)
    node_with_data.update_rectangles((0, 0, 0, 0))
    assert [rectangle[0] for rectangle in node_with_data.get_rectangles()] == [
        (0, 0, 0, 0)]


def test_zero_data_and_area() -> None:
    """Test handling of nodes with no data size and rectangle area."""
    blank_node = TMTree("BlankNode", [], 0)
    blank_node.update_rectangles((0, 0, 0, 0))
    assert [rectangle[0] for rectangle in blank_node.get_rectangles()] == []


def test_removal_of_all_children() -> None:
    """Ensure nodes become empty after all children are removed."""
    file_tree = FileSystemTree(EXAMPLE_PATH)
    _sort_subtrees(file_tree)

    image_folder = file_tree._subtrees[0]._subtrees[1]
    first_pdf, second_pdf = image_folder._subtrees[:2]
    assert first_pdf.delete_self()
    assert second_pdf.delete_self()

    assert not image_folder._subtrees
    assert image_folder.data_size == 0


def test_erasing_node_results_in_empty_rectangle() -> None:
    """Verify deletion of nodes results in no rectangles."""
    file_system_tree = FileSystemTree(os.path.join(EXAMPLE_PATH, ".."))
    assert file_system_tree._subtrees[0].delete_self()

    file_system_tree.update_rectangles((0, 0, 100, 100))
    assert [rect[0] for rect in file_system_tree.get_rectangles()] == []


def test_data_size_post_full_deletion() -> None:
    """Validate that data size remains after an unsuccessful delete attempt."""
    root_tree = FileSystemTree(os.path.join(EXAMPLE_PATH, ".."))
    assert not root_tree.delete_self()
    assert root_tree.data_size > 0

    assert root_tree._subtrees[0].delete_self()
    assert root_tree.data_size == 0


def test_size_reduction_to_minimum() -> None:
    """Check that size cannot be reduced below 1."""
    singular_tree = TMTree("Single", [], 1)
    singular_tree.change_size(-1)
    assert singular_tree.data_size == 1


def test_accurate_rounding_of_size_change() -> None:
    """Ensure size changes are rounded up accurately."""
    tree_node = TMTree("Node", [], 150)
    tree_node.change_size(0.01)

    assert tree_node.data_size == 152


def test_size_change_affects_root_node() -> None:
    """Verify size changes in a subtree affect the root node's size."""
    sub_tree = TMTree("Sub1", [], 100)
    main_tree = TMTree("Main", [sub_tree], 0)

    sub_tree.change_size(0.01)
    assert sub_tree.data_size == 101
    assert main_tree.data_size == 101

    sub_tree.change_size(-0.01)
    assert sub_tree.data_size == 99
    assert main_tree.data_size == 99


def test_size_update_on_deletion() -> None:
    """Confirm that deleting a subtree updates the root's data size."""
    deep_subtree = TMTree("Deep1", [], 100)
    sub_tree = TMTree("Sub1", [deep_subtree], 0)
    main_tree = TMTree("Main", [sub_tree], 0)

    assert deep_subtree.delete_self()

    assert sub_tree.data_size == 0
    assert main_tree.data_size == 0


def test_full_expansion_of_all_nodes() -> None:
    """Confirm every node, including leaves, is correctly expanded."""
    base_tree = FileSystemTree(EXAMPLE_PATH)
    assert not base_tree._expanded
    base_tree.expand_all()
    assert base_tree._expanded


def test_leaves_remain_collapsed() -> None:
    """Validate leaves do not expand even after expand operations."""
    sub_tree = TMTree("Sub1", [], 100)
    main_tree = TMTree("Main", [sub_tree], 0)

    assert not sub_tree._expanded
    main_tree.expand_all()
    assert not sub_tree._expanded
    main_tree.expand()
    assert not sub_tree._expanded


def test_collapsing_nodes_at_various_levels() -> None:
    """Ensure nodes collapse correctly at different tree depths."""
    deepest_subtree = TMTree("Deepest", [], 100)
    deep_subtree = TMTree("Deep", [deepest_subtree], 0)
    sub_tree = TMTree("Sub", [deep_subtree], 0)
    main_tree = TMTree("Main", [sub_tree], 0)

    main_tree.expand_all()
    sub_tree.collapse()

    assert not main_tree._expanded
    assert not sub_tree._expanded
    assert not deep_subtree._expanded
    assert not deepest_subtree._expanded

    main_tree.expand_all()
    deep_subtree.collapse()

    assert main_tree._expanded
    assert not sub_tree._expanded
    assert not deep_subtree._expanded
    assert not deepest_subtree._expanded


def test_empty_tree_collapse_all():
    tree = TMTree(None, [])
    tree.collapse_all()
    assert tree.is_empty() and not tree._expanded, ("Collapse all on an empty "
                                                    "tree should leave it "
                                                    "unchanged.")


def test_deeply_nested_trees_collapse():
    deep_tree = TMTree("Deep", [TMTree(f"Child {i}", []) for i in range(5)])
    for _ in range(3):  # Adding multiple levels of nesting
        deep_tree = TMTree("Parent", [deep_tree])
    deep_tree.collapse_all()
    # Verify the root is not expanded and recursively check each subtree
    assert not any_subtree_expanded(
        deep_tree), "All subtrees should be collapsed."


def test_multiple_subtrees_collapse():
    subtree1 = TMTree("Subtree 1", [TMTree(f"Leaf {i}", []) for i in range(3)])
    subtree2 = TMTree("Subtree 2", [TMTree(f"Leaf {i}", []) for i in range(3)])
    root = TMTree("Root", [subtree1, subtree2])
    root.collapse_all()
    assert not root._expanded and not (
            subtree1._expanded or subtree2._expanded), ("All subtrees "
                                                        "should be "
                                                        "collapsed.")


def test_repetitive_collapse_calls():
    tree = TMTree("Root", [TMTree(f"Child {i}", []) for i in range(5)])
    for _ in range(5):  # Repeat collapse calls
        tree.collapse_all()
    assert not tree._expanded, ("Tree should remain collapsed after repetitive "
                                "calls.")


def test_collapse_after_deletion():
    child = TMTree("Child", [])
    root = TMTree("Root", [child])
    successful_deletion = child.delete_self()
    root.collapse_all()
    assert successful_deletion and not root._expanded, ("Tree should be "
                                                        "collapsed after a "
                                                        "subtree deletion.")


def test_delete_leaf_node():
    child1 = TMTree("Child1", [], 10)
    child2 = TMTree("Child2", [], 20)
    root = TMTree("Root", [child1, child2], 30)
    assert child1.delete_self() is True, "Deletion should succeed"
    assert len(root._subtrees) == 1, "Parent should have one child left"
    assert root._subtrees[0]._name == "Child2", ("The remaining child should "
                                                 "be 'Child2'")
    assert root.data_size == 20, ("Parent's data_size should be updated "
                                  "correctly")


def test_delete_internal_node_single_child():
    child = TMTree("Child", [], 10)
    internal_node = TMTree("Internal", [child])
    root = TMTree("Root", [internal_node], 10)
    assert internal_node.delete_self() is True, "Deletion should succeed"
    assert len(root._subtrees) == 0, ("Root should have no children after "
                                      "deletion")
    assert root.data_size == 0, "Root's data_size should be updated to 0"


def test_delete_node_with_multiple_children():
    child1 = TMTree("Child1", [], 10)
    child2 = TMTree("Child2", [], 15)
    parent = TMTree("Parent", [child1, child2], 25)
    root = TMTree("Root", [parent], 25)
    assert parent.delete_self() is True, "Deletion should succeed"
    assert len(root._subtrees) == 0, "Root should have no children left"
    assert root.data_size == 0, "Root's data_size should be updated correctly"


def test_delete_root_node():
    root = TMTree("Root", [], 10)
    assert root.delete_self() is False, "Root node deletion should fail"


def test_delete_nodes_in_deeply_nested_structure():
    leaf = TMTree("Leaf", [], 5)
    level1 = TMTree("Level1", [leaf], 5)
    level2 = TMTree("Level2", [level1], 5)
    root = TMTree("Root", [level2], 5)
    assert leaf.delete_self() is True, "Leaf node deletion should succeed"
    assert level1.data_size == 0, ("Level1's data_size should be updated "
                                   "correctly")
    assert level2.data_size == 0, ("Level2's data_size should be updated "
                                   "correctly")
    assert root.data_size == 0, "Root's data_size should be updated correctly"


@pytest.fixture
def setup_tree_for_move():
    leaf = TMTree("Leaf", [], 10)
    child = TMTree("Child", [leaf], 10)
    other_child = TMTree("OtherChild", [], 20)
    root = TMTree("Root", [child, other_child], 30)
    return root, leaf, child, other_child


def test_attempt_to_move_root(setup_tree_for_move):
    root, _, _, _ = setup_tree_for_move
    # Assuming an imaginary tree for the destination
    imaginary_destination = TMTree("Imaginary", [], 100)
    root.move(imaginary_destination)
    assert not root._parent_tree, "Root should not have a parent"


def test_move_node_to_its_grandparent(setup_tree_for_move):
    root, leaf, child, _ = setup_tree_for_move
    child.move(root)
    assert child in root._subtrees, "Child should now be a direct child of Root"
    assert leaf not in root._subtrees, "Leaf should not be directly under Root"


def test_move_node_to_its_current_parent(setup_tree_for_move):
    _, leaf, child, _ = setup_tree_for_move
    original_subtrees = child._subtrees[:]
    leaf.move(child)
    assert child._subtrees == original_subtrees, ("Child's subtrees should be "
                                                  "unchanged")


def test_expanded_tree_but_not_parent_tree():
    """
    tests expanded tree but the parent tree is not expanded.
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    _sort_subtrees(tree)

    tree._subtrees[0].expand()
    assert tree._subtrees[0]._expanded is True
    assert tree._expanded is False


def test_empty_get_rectangle():
    # An empty tree should have an empty list of rectangles
    tree = TMTree(None, [], 0)
    return_trees = tree.get_rectangles()
    assert return_trees == [], "Expected no rectangles from an empty tree"


def test_empty_change_size_for_tree():
    # Changing the size of an empty tree should not affect its data size,
    # as empty trees should have data_size set to 0 and should not be able to
    # change.
    tree = TMTree(None, [], 0)
    tree.change_size(2000)
    assert tree.data_size == 0, ("Expected data_size to remain 0 after "
                                 "change_size on an empty tree")


def test_empty_update_rectangle():
    # Updating the rectangles of an empty tree should not change its rect
    # attribute since there's no actual rectangle to update.
    tree = TMTree(None, [], 0)
    rect = (0, 0, 100, 100)
    tree.update_rectangles(rect)
    r = tree.get_rectangles()
    assert tree.rect == (0, 0, 0, 0), ("Expected rect to remain unchanged "
                                       "after update_rectangles on an empty "
                                       "tree")
    assert r == [], ("Expected no rectangles from an empty tree after "
                     "update_rectangles")


def test_empty_get_tree_at_pos():
    # Since the tree is empty, get_tree_at_position should return None,
    # even if the position falls within the bounds of the tree's rectangle.
    tree = TMTree(None, [], 0)
    tree.update_rectangles((0, 0, 20, 40))
    assert tree.get_tree_at_position((10, 10)) is None, ("Expected None when "
                                                         "getting tree at "
                                                         "position on an "
                                                         "empty tree")


def test_tree_expanded_after_deletion():
    """tests to see if the tree get unexpanded after it becomes empty since
    leaf cannot be expanded"""
    ok5 = TMTree('ok5', [], 15)
    ok4 = TMTree('ok4', [], 40)
    ok3 = TMTree('ok3', [ok5], 0)
    ok1 = TMTree('ok1', [ok4], 5)
    ok1._expanded = True
    ok3._expanded = False
    assert ok1._expanded
    assert not ok3._expanded
    ok4.move(ok3)
    assert not ok1._expanded


# ========================== Tests for the Task 6 =============================

DATA_FILE = 'cs1_papers.csv'


def test_reading():
    """checks for validation that the subtrees being formed are in fact
    trees."""
    lst = _build_tree_from_dict(_load_papers_to_dict(False))
    assert isinstance(lst[0], PaperTree)

def _get_root(tree) -> TMTree:
    """Return the root Tree of this TMTree
    """
    if tree._parent_tree is None:
        return tree

    else:
        return tree._parent_tree._get_root()

def test_2():
    """ok"""
    p = PaperTree("ok1", [], all_papers=False)
    curr = p
    while curr._subtrees:
        curr = curr._subtrees[0]

    assert _get_root(curr) is p


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


def test_category_structure(paper_tree_no_year):
    # You will need to implement specific checks based on your tree structure
    # For example, checking that top-level categories are present
    pass


def test_year_layer(paper_tree_with_year):
    # Specific checks to ensure the year layer is correct
    pass


def test_data_integrity(paper_tree_no_year, paper_tree_with_year):
    # Count the total number of papers and compare against the expected number
    pass


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


def any_subtree_expanded(tree):
    """Helper function to recursively check if any subtree is expanded."""
    if tree._expanded:
        return True
    return any(any_subtree_expanded(subtree) for subtree in tree._subtrees)


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
