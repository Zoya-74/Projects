"""
Assignment 2: Trees for Treemap

=== CSC148 Winter 2024 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2024 Bogdan Simion, David Liu, Diane Horton,
                   Haocheng Hu, Jacqueline Smith

=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""
from __future__ import annotations

import math
import os
from random import randint
from typing import List, Tuple, Optional


class TMTree:
    """A TreeMappableTree: a tree that is compatible with the treemap
    visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you implementing new public
    *methods* for this interface.
    You should not add any new public methods other than those required by
    the client code.
    You can, however, freely add private methods as needed.

    === Public Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.

    === Private Attributes ===
    _colour:
        The RGB colour value of the root of this tree.
    _name:
        The root value of this tree, or None if this tree is empty.
    _subtrees:
        The subtrees of this tree.
    _parent_tree:
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.
    _expanded:
        Whether or not this tree is considered expanded for visualization.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.

    - _colour's elements are each in the range 0-255.

    - If _name is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.

    - if _parent_tree is not None, then self is in _parent_tree._subtrees

    - if _expanded is True, then _parent_tree._expanded is True
    - if _expanded is False, then _expanded is False for every tree
      in _subtrees
    - if _subtrees is empty, then _expanded is False
    """

    rect: Tuple[int, int, int, int]
    data_size: int
    _colour: Tuple[int, int, int]
    _name: str
    _subtrees: List[TMTree]
    _parent_tree: Optional[TMTree]
    _expanded: bool

    def __init__(self, name: str, subtrees: List[TMTree],
                 data_size: int = 0) -> None:
        """Initialize a new TMTree with a random colour and the provided <name>.

        If <subtrees> is empty, use <data_size> to initialize this tree's
        data_size.

        If <subtrees> is not empty, ignore the parameter <data_size>,
        and calculate this tree's data_size instead.

        Set this tree as the parent for each of its subtrees.

        Precondition: if <name> is None, then <subtrees> is empty.
        """
        self.rect = (0, 0, 0, 0)
        self._name = name
        self._subtrees = subtrees[:]
        self._parent_tree = None

        # You will change this in Task 5
        self._expanded = False

        # 1. Initialize self._colour and self.data_size, according to the
        # docstring.
        self._colour = (randint(0, 255), randint(0, 255),
                        randint(0, 255))
        self.data_size = data_size
        if self._subtrees:
            self.data_size = 0
            for child in self._subtrees:
                self.data_size += child.data_size
                # child._expanded = False

        # 2. Set this tree as the parent for each of its subtrees.
        for tree in self._subtrees:
            tree._parent_tree = self

    def is_empty(self) -> bool:
        """Return True iff this tree is empty.
        """
        return self._name is None

    def get_parent(self) -> Optional[TMTree]:
        """Returns the parent of this tree.
        """
        return self._parent_tree

    # def update_rectangles(self, rect: Tuple[int, int, int, int]) -> None:
    #     """Update the rectangles in this tree and its descendents using the
    #     treemap algorithm to fill the area defined by pygame rectangle <rect>.
    #     """
    #     # Read the handout carefully to help get started
    #     # identifying base cases,
    #     # then write the outline of a recursive step.
    #     #
    #     # Programming tip: use "tuple unpacking assignment" to easily extract
    #     # elements of a rectangle, as follows.
    #     original = rect
    #     x, y, width, height = rect
    #     if self.data_size == 0:
    #         self.rect = (0, 0, 0, 0)
    #         for sub in self._subtrees:
    #             sub.update_rectangles(self.rect)
    #     elif not self._subtrees or (self.is_empty() and self.data_size > 0):
    #         self.rect = original
    #         return
    #
    #     else:
    #         self.rect = original
    #         total_size = self.data_size
    #         for subtree in self._subtrees:
    #             percent = subtree.data_size / total_size
    #             if width > height:
    #                 new_width = math.floor(width * percent)
    #                 if width < 0:
    #                     new_width = math.ceil(width * percent)
    #                 subtree.rect = (x, y, new_width, height)
    #                 if subtree is self._subtrees[-1]:
    #                     subtree.rect = (x, y, rect[2] - x + rect[0], height)
    #                     (subtree.update_rectangles
    #                      ((x, y, rect[2] - x + rect[0], height)))
    #
    #                 else:
    #                     subtree.update_rectangles(subtree.rect)
    #                 x += new_width
    #             else:
    #                 new_height = math.floor(height * percent)
    #                 if height < 0:
    #                     new_height = math.ceil(height * percent)
    #                 subtree.rect = (x, y, width, new_height)
    #                 if subtree is self._subtrees[-1]:
    #                     subtree.rect = (x, y, width, rect[3] - y + rect[1])
    #                     subtree.update_rectangles((x, y, width,
    #                                                rect[3] - y + rect[1]))
    #                 else:
    #                     subtree.update_rectangles(subtree.rect)
    #                 y += new_height

    def update_rectangles(self, rect: Tuple[int, int, int, int]) -> None:
        """Update the rectangles in this tree and its descendents using the
        treemap algorithm to fill the area defined by pygame
         rectangle <rect>."""
        x, y, width, height = rect
        if not self._handle_base_cases(rect):
            total_size = self.data_size
            if width > height:
                (self._update_rectangles_by_width
                 (x, y, (width, height),
                  (total_size, rect)))
            else:
                (self._update_rectangles_by_height
                 (x, y, (width, height),
                  (total_size, rect)))

    def _handle_base_cases(self, rect: Tuple[int, int, int, int]) -> bool:
        """helper for update rectangles that deals with the base cases."""
        original = rect
        if self.data_size == 0:
            self.rect = (0, 0, 0, 0)
            for sub in self._subtrees:
                sub.update_rectangles(self.rect)
            return True
        elif not self._subtrees or (self.is_empty() and self.data_size > 0):
            self.rect = original
            return True
        self.rect = original
        return False

    def _update_rectangles_by_width(self, x: int, y: int,
                                    tuple_width_height: Tuple[int, int],
                                    tuple_size_rect:
                                    Tuple[int, Tuple[
                                        int, int, int, int]]) -> None:
        """helper for the update rectangles that deals with the height."""
        width, height = tuple_width_height
        total_size, rect = tuple_size_rect
        for subtree in self._subtrees:
            percent = subtree.data_size / total_size
            new_width = math.floor(width * percent) if width >= 0 \
                else math.ceil(width * percent)
            subtree.rect = (x, y, new_width, height)
            if subtree is self._subtrees[-1]:
                subtree.rect = (x, y, rect[2] - x + rect[0], height)
            subtree.update_rectangles(subtree.rect)
            x += new_width

    def _update_rectangles_by_height(self, x: int, y: int,
                                     tuple_width_height: Tuple[int, int],
                                     tuple_size_rect:
                                     Tuple[int, Tuple[
                                         int, int, int, int]]) -> None:
        """helper for the update rectangles that deals with the height"""
        width, height = tuple_width_height
        total_size, rect = tuple_size_rect
        for subtree in self._subtrees:
            percent = subtree.data_size / total_size
            new_height = math.floor(height * percent) if height >= 0 \
                else math.ceil(height * percent)
            subtree.rect = (x, y, width, new_height)
            if subtree is self._subtrees[-1]:
                subtree.rect = (x, y, width, rect[3] - y + rect[1])
            subtree.update_rectangles(subtree.rect)
            y += new_height

    def get_rectangles(self) \
            -> List[Tuple[Tuple[int, int, int, int], Tuple[int, int, int]]]:
        """Return a list with tuples for every leaf in the displayed-tree
        rooted at this tree. Each tuple consists of a tuple that defines the
        appropriate pygame rectangle to display for a leaf, and the colour
        to fill it with.
        """
        if self._expanded:
            if self.is_empty():
                return []
            elif not self._subtrees:
                return [(self.rect, self._colour)]
            else:
                config = []
                for subtree in self._subtrees:
                    config.extend(subtree.get_rectangles())
                return config
        elif self.is_empty() or self.data_size == 0:
            return []
        else:
            return [(self.rect, self._colour)]

    def get_tree_at_position(self, pos: Tuple[int, int]) -> Optional[TMTree]:
        """Return the leaf in the displayed-tree rooted at this tree whose
        rectangle contains position <pos>, or None if <pos> is outside of this
        tree's rectangle.

        If <pos> is on the shared edge between two or more rectangles,
        always return the leftmost and topmost rectangle (wherever applicable).
        """
        if ((pos[0] > self.rect[2] + self.rect[0]
             or pos[1] > self.rect[3] + self.rect[1])
                or pos[0] < 0 or pos[1] < 0):
            return None
        elif not (self._subtrees and self._expanded):
            return self

        if self.rect[2] > self.rect[3]:

            for subtree in self._subtrees:
                size = subtree.rect
                if (size[0] <= pos[0] <= size[0] + size[2]
                        and self._expanded):
                    return subtree.get_tree_at_position(pos)
                elif size[0] <= pos[0] <= size[0] + size[2]:
                    return subtree

        else:
            for subtree in self._subtrees:
                size = subtree.rect
                if (size[1] <= pos[1] <= size[1] + size[3]
                        and self._expanded):
                    return subtree.get_tree_at_position(pos)
                elif size[1] <= pos[1] <= size[1] + size[3]:
                    return subtree
        return None

    def update_data_sizes(self) -> int:
        """Update the data_size for this tree and its subtrees, based on the
        size of their leaves, and return the new size.

        If this tree is a leaf, return its size unchanged.
        """
        if self.is_empty() and self.data_size == 0:
            return 0
        elif not self._subtrees:
            return self.data_size

        else:
            size = 0
            for subtrees in self._subtrees:
                size += subtrees.update_data_sizes()
            self.data_size = size
            return self.data_size

    def move(self, destination: TMTree) -> None:
        """If this tree is a leaf, and <destination> is not a leaf, move this
        tree to be the last subtree of <destination>. Otherwise, do nothing.
        """
        if self._subtrees == [] and destination._subtrees != []:
            self._parent_tree._subtrees.remove(self)
            if len(self._parent_tree._subtrees) == 0:
                self._parent_tree._expanded = False
            destination._subtrees.append(self)

            destination.data_size += self.data_size
            self._parent_tree.data_size -= self.data_size
            self._recalculate_data_size()

            self._parent_tree = destination
            self._recalculate_data_size()

    def change_size(self, factor: float) -> None:
        """Change the value of this tree's data_size attribute by <factor>.

        Always round up the amount to change, so that it's an int, and
        some change is made.

        Do nothing if this tree is not a leaf.
        """
        if not self._subtrees:
            if factor < 0:
                decrease = math.floor(factor * self.data_size)
                self.data_size += decrease
                if self.data_size < 1:
                    self.data_size = 1

            else:
                increase_by = math.ceil(factor * self.data_size)
                self.data_size += increase_by
            self._recalculate_data_size()

    def delete_self(self) -> bool:
        """Removes the current node from the visualization and
        returns whether the deletion was successful.

        Only do this if this node has a parent tree.

        Do not set self._parent_tree to None, because it might be used
        by the visualiser to go back to the parent folder.
        """

        if self._parent_tree is not None:

            self._parent_tree._subtrees.remove(self)

            if len(self._parent_tree._subtrees) == 0:
                self._parent_tree.data_size = 0
                self.collapse()
            self.data_size = 0
            self._parent_tree._recalculate_data_size()
            return True

        return False

    def expand(self) -> None:
        """Expands the current tree into its subtrees.
        If current folder is empty, do not do anything
        Precondition: the parent tree is Expanded
        """
        if self._subtrees:
            self._expanded = True

    def expand_all(self) -> None:
        """Expand the entire folder into its sub folders and their sub folders.
        """
        self.expand()
        for subtree in self._subtrees:
            if not subtree._subtrees:
                subtree.expand()
            else:
                subtree.expand_all()

    def collapse(self) -> None:
        """collapses the current folder into its parent folder."""

        if self._parent_tree is not None:
            self._parent_tree._expanded = False
            self._expanded = False
            for subtree in self._parent_tree._subtrees:
                subtree._helper_collapse()

    def _helper_collapse(self) -> None:
        """
        A helper that recursively collapses a tree and its descendants
        """
        self._expanded = False
        for sub in self._subtrees:
            sub._helper_collapse()

    def collapse_all(self) -> None:
        """Collapses the entire file into its original file
        """
        if self._parent_tree is None:
            self._helper_collapse()
            return
        root = self._parent_tree
        while root._parent_tree is not None:
            root = root._parent_tree
        root._helper_collapse()

    # Methods for the string representation
    def get_path_string(self) -> str:
        """
        Return a string representing the path containing this tree
        and its ancestors, using the separator for this OS between each
        tree's name.
        """
        if self._parent_tree is None:
            return self._name
        else:
            return self._parent_tree.get_path_string() + \
                self.get_separator() + self._name

    def _recalculate_data_size(self) -> None:
        """
        A helper function that finds the root and calls updata_data_sizes on the
        root
        """
        if self._parent_tree is None:
            self.update_data_sizes()
            return
        root = self._parent_tree
        root._recalculate_data_size()

    def get_separator(self) -> str:
        """Return the string used to separate names in the string
        representation of a path from the tree root to this tree.
        """
        raise NotImplementedError

    def get_suffix(self) -> str:
        """Return the string used at the end of the string representation of
        a path from the tree root to this tree.
        """
        raise NotImplementedError


class FileSystemTree(TMTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _name attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/Diane/csc148/assignments'

    The data_size attribute for regular files is simply the size of the file,
    as reported by os.path.getsize.
    """

    def __init__(self, path: str) -> None:
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.
        """
        # Remember that you should recursively go through the file system
        # and create new FileSystemTree objects for each file and folder
        # encountered.
        #
        # Also remember to make good use of the superclass constructor!
        subtrees = []
        name = os.path.basename(path)

        if os.path.isfile(path):
            # if the path is a file, simply call initializer since there are no
            # other 'sub files'/subtrees
            super().__init__(name=name, subtrees=[],
                             data_size=os.path.getsize(path))

        # elif os.path.isdir(path):
        else:

            for f in os.listdir(path):
                subtrees.append(FileSystemTree(os.path.join(path, f)))

            super().__init__(name=name, subtrees=subtrees)

    def get_separator(self) -> str:
        """Return the file separator for this OS.
        """
        return os.sep

    def get_suffix(self) -> str:
        """Return the final descriptor of this tree.
        """

        def convert_size(data_size: float, suffix: str = 'B') -> str:
            suffixes = {'B': 'kB', 'kB': 'MB', 'MB': 'GB', 'GB': 'TB'}
            if data_size < 1024 or suffix == 'TB':
                return f'{data_size:.2f}{suffix}'
            return convert_size(data_size / 1024, suffixes[suffix])

        components = []
        if len(self._subtrees) == 0:
            components.append('file')
        else:
            components.append('folder')
            components.append(f'{len(self._subtrees)} items')
        components.append(convert_size(self.data_size))
        return f' ({", ".join(components)})'


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'math', 'random', 'os', '__future__'
        ]
    })
