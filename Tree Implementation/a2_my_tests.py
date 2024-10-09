import os

from hypothesis import given
from hypothesis.strategies import integers

from tm_trees1 import TMTree, FileSystemTree

EXAMPLE_PATH = os.path.join(os.getcwd(), 'example-directory', 'workshop')


#
# def test_example_data() -> None:
#     """Test the root of the tree at the 'workshop' folder in the example data
#     """
#     tree = FileSystemTree(EXAMPLE_PATH)
#     assert tree._name == 'workshop'
#     assert tree._parent_tree is None
#     assert tree.data_size == 151
#     assert is_valid_colour(tree._colour)
#
#     assert len(tree._subtrees) == 3
#     for subtree in tree._subtrees:
#         # Note the use of is rather than ==.
#         # This checks ids rather than values.
#         assert subtree._parent_tree is tree
#
#
# def test_single_file() -> None:
#     """Test a tree with a single file.
#     """
#     tree = FileSystemTree(os.path.join(EXAMPLE_PATH, 'draft.pptx'))
#     assert tree._name == 'draft.pptx'
#     assert tree._subtrees == []
#     assert tree._parent_tree is None
#     assert tree.data_size == 58
#     assert is_valid_colour(tree._colour)


def is_valid_colour(colour: tuple[int, int, int]) -> bool:
    """Return True iff <colour> is a valid colour. That is, if all of its
    values are between 0 and 255, inclusive.
    """
    for i in range(3):
        if not 0 <= colour[i] <= 255:
            return False
    return True


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
    tree = FileSystemTree(EXAMPLE_PATH2)
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


def test_expand_tree_but_not_parent():
    """
    test representation invariant if expanded is true for self, the parent
    should also be expanded, still works
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    _sort_subtrees(tree)

    tree._subtrees[0].expand()
    assert tree._subtrees[0]._expanded is True
    assert tree._expanded is False


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


# other test

def test_update_rectange():
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


# def test_expand_and_collapse_example_dir():
#     tree = FileSystemTree(EXAMPLE_PATH)
#     tree.update_rectangles((0, 0, 200, 100))
#
#
#
#     assert False
#
#
#
#     # NEED TO SORT FOR ALL TESTCASES
#     _sort_subtrees(tree)
#
#     tree.collapse_all()
#     rects = tree.get_rectangles()
#     assert tree.data_size > 0
#     assert len(rects) == 1
#     assert tree._subtrees[0].rect != (0, 0, 0, 0)
#     tree.expand()
#     rects = tree.get_rectangles()
#
#     # the original rectangle should not be included anymore, only the
#     # rectangles of its subtrees
#     assert len(rects) == len(tree._subtrees)
#
#     tree.collapse()
#     rects = tree.get_rectangles()
#     assert not tree._expanded
#     assert len(rects) == 3
#
#     tree.expand_all()
#     tree.collapse()
#     assert tree._subtrees[0]._expanded
#     assert tree._subtrees[0]._subtrees[1]._expanded
#
#     tree.expand_all()
#     tree.collapse_all()
#     rects = tree.get_rectangles()
#     assert not tree._expanded
#     assert len(rects) == 1
#
#     tree.expand_all()
#     rects = tree.get_rectangles()
#     assert len(rects) == count_leafs(tree) == 6
#
#     tree._subtrees[0]._subtrees[0].collapse_all()
#     rects = tree.get_rectangles()
#     assert len(rects) == 1
#
#     tree.expand_all()
#     tree.collapse_all()
#     assert not tree._expanded
#
#     # Try collapsing draft.ppx and check if its siblings are collapsed
#     tree.expand_all()
#     tree._subtrees[1].collapse()
#     for sub in tree._subtrees:
#         assert sub._expanded == False


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

def test_expand_all():
    tree1 = TMTree("tree1", [], 50)
    tree2 = TMTree("tree2", [tree1], 50)
    tree3 = TMTree("tree3", [tree2], 50)
    tree4 = TMTree("tree4", [tree3], 0)
    leaf = TMTree("leaf", [], 100)
    print(tree4._subtrees)
    assert tree4.data_size == 50
    tree1.delete_self()
    print(tree4._subtrees)
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
    print(tree4._subtrees)
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
    leaf.update_rectangles((0,0,10,20))
    assert leaf.get_tree_at_position((0,5)) == leaf

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


def test_delete_folder():
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


def test_move_root():
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

# ===Helpers===

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
