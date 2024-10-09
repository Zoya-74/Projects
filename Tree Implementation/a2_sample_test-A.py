import os
import tempfile
import pytest

from hypothesis import given
from hypothesis.strategies import integers
from tm_trees1 import TMTree, FileSystemTree

# This should be the path to the "workshop" folder in the sample data.
# You may need to modify this, depending on where you downloaded and
# extracted the files.
a = os.getcwd()
EXAMPLE_PATH = os.path.join(a, 'example-directory', 'workshop')


def test_update_rect():
    t = TMTree('t', [], 5)
    t2 = TMTree('t2', [], 6)
    t3 = TMTree('t3', [], 7)
    t4 = TMTree('t4', [t3])
    t5 = TMTree('t5', [t, t2])
    m = TMTree('m', [t5, t4])
    m.update_rectangles((0, 0, 100, 100))
    r1 = t3.rect
    r2 = t4.rect

    t3.change_size(10)
    assert t3.rect == r1
    assert t4.rect == r2

    m.update_rectangles((0,0,100,100))

    assert t3.rect != r1
    assert t4.rect != r2


def test_single_file() -> None:
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


def test_empty_folder(make_empty_dir) -> None:
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


def test_expand_all():
    t = TMTree('1', [], 5)
    a = TMTree('2', [], 5)
    b = TMTree('3', [a])
    c = TMTree('4', [t])
    main = TMTree('m', [b, c])
    main.update_rectangles((0, 0, 100, 100))
    main.expand()
    b.expand_all()
    assert not c._expanded


def test_get_tree_at_pos():
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


def test_change_size_0():
    t = TMTree('t', [], 10)
    t.change_size(0)
    assert t.data_size == 10


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


def test_move_root():
    root = TMTree('r', [], 5)
    sub1 = TMTree('s1', [])
    sub2 = TMTree('s2', [], 5)
    f = TMTree('f', [sub1, sub2])
    try:

        root.move(f)
    except AttributeError:
        assert True
    else:
        assert False
    assert root not in f._subtrees


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

    # the original rectangle should not be included anymore, only the rectangles of its subtrees
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
        assert sub._expanded == False


def test_delete_single_file(make_empty_dir):
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


def test_empty_space_visualizer() -> None:
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


def count_leafs(tree: TMTree):
    """Count the amount of leafs in a given tree
    """
    if tree.is_empty():
        return 0
    if not tree._subtrees:
        return 1
    return sum([count_leafs(i) for i in tree._subtrees])


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


# if __name__ == '__main__':
#     import pytest
#     pytest.main(['my_a2_tests.py'])

if __name__ == '__main__':
    import pytest

    # import coverage
    # #
    # # # This creates a Coverage() object and starts recording information
    # # # about which lines have been run in my_functions.py
    # cov = coverage.Coverage(include=['tm_trees.py'])
    # cov.start()
    #
    # # This line runs the pytest cases in test_my_functions.py
    pytest.main(['a2_sample_test.py'])
    #
    # # These lines stop recording information and saves it
    # cov.stop()
    # cov.save()
    #
    # # The line below will print the report to the Python Console.
    # cov.report()
    #
    # # The line below will generate a folder called htmlcov
    # # Open the index.html page to see the coverage report. You can
    # # click on the "my_functions.py" module there to see
    # # which lines might be missing.
    # cov.html_report()
