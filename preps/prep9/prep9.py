"""Prep 9 Synthesize: Binary Search Trees

=== CSC148 Winter 2024 ===
Department of Mathematical and Computational Sciences,
University of Toronto Mississauga

=== Module Description ===
Your task in this prep's synthesize is to implement each of the unimplemented
BinarySearchTree methods in this file.

Take advantage of the BinarySearchTree property to ensure that you are only
making the recursive calls that are required to implement the function---
do not make any unnecessary calls!
(The prep readings illustrate this idea in the discussion of how __contains__
is implemented.)

NOTE: the doctests access and assign to private attributes directly, which is
not good practice (although python_ta doesn't complain about it in doctests).
We'll fix this in lecture/lab this week when we implement an `insert` method.
"""
from __future__ import annotations

from typing import Any, Optional


class BinarySearchTree:
    """Binary Search Tree class.

    This class represents a binary tree satisfying the Binary Search Tree
    property: for every node, its value is >= all items stored in its left
    subtree, and <= all items stored in its right subtree.
    """
    # === Private Attributes ===
    # The item stored at the root of the tree, or None if the tree is empty.
    _root: Optional[Any]
    # The left subtree, or None if the tree is empty.
    _left: Optional[BinarySearchTree]
    # The right subtree, or None if the tree is empty.
    _right: Optional[BinarySearchTree]

    # === Representation Invariants ===
    #  - If self._root is None, then so are self._left and self._right.
    #    This represents an empty BST.
    #  - If self._root is not None, then self._left and self._right
    #    are BinarySearchTrees.
    #  - (BST Property) If self is not empty, then
    #    all items in self._left are <= self._root, and
    #    all items in self._right are >= self._root.

    def __init__(self, root: Optional[Any]) -> None:
        """Initialize a new BST containing only the given root value.

        If <root> is None, initialize an empty tree.
        """
        if root is None:
            self._root = None
            self._left = None
            self._right = None
        else:
            self._root = root
            self._left = BinarySearchTree(None)
            self._right = BinarySearchTree(None)

    def is_empty(self) -> bool:
        """Return True if this BST is empty.

        >>> bst = BinarySearchTree(None)
        >>> bst.is_empty()
        True
        >>> bst = BinarySearchTree(10)
        >>> bst.is_empty()
        False
        """
        return self._root is None

    def __contains__(self, item: Any) -> bool:
        """Return whether <item> is in this BST.

        >>> bst = BinarySearchTree(3)
        >>> bst._left = BinarySearchTree(2)
        >>> bst._right = BinarySearchTree(5)
        >>> 3 in bst
        True
        >>> 5 in bst
        True
        >>> 2 in bst
        True
        >>> 4 in bst
        False
        """
        if self.is_empty():
            return False
        elif item == self._root:
            return True
        elif item < self._root:
            return item in self._left  # or, self._left.__contains__(item)
        else:
            return item in self._right  # or, self._right.__contains__(item)

    # -------------------------------------------------------------------------
    # Additional BST methods
    # -------------------------------------------------------------------------
    def __str__(self) -> str:
        """Return a string representation of this BST.

        This string uses indentation to show depth.
        """
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this BST.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            answer = depth * '  ' + str(self._root) + '\n'
            answer += self._left._str_indented(depth + 1)
            answer += self._right._str_indented(depth + 1)
            return answer

    # -------------------------------------------------------------------------
    # Prep exercises
    # -------------------------------------------------------------------------
    def maximum(self) -> Optional[int]:
        """Return the maximum number in this BST, or None if this BST is empty.

        Hint: Review the BST property to ensure you aren't making unnecessary
        recursive calls.

        >>> BinarySearchTree(None).maximum() is None   # Empty BST
        True
        >>> BinarySearchTree(10).maximum()
        10
        >>> bst = BinarySearchTree(7)
        >>> left = BinarySearchTree(3)
        >>> left._left = BinarySearchTree(3)
        >>> left._right = BinarySearchTree(5)
        >>> right = BinarySearchTree(11)
        >>> right._left = BinarySearchTree(9)
        >>> right._right = BinarySearchTree(13)
        >>> bst._left = left
        >>> bst._right = right
        >>> bst.maximum()
        13
        >>> bst = BinarySearchTree(15)
        >>> bst._left = BinarySearchTree(10)
        >>> bst._right = BinarySearchTree(20)
        >>> bst._left._left = BinarySearchTree(5)
        >>> bst._left._right = BinarySearchTree(12)
        >>> bst._right._left = BinarySearchTree(18)
        >>> bst._right._right = BinarySearchTree(25)
        >>> bst.maximum()
        25

        >>> bst2 = BinarySearchTree(8)
        >>> bst2._left = BinarySearchTree(6)
        >>> bst2._left._left = BinarySearchTree(4)
        >>> bst2._left._left._left = BinarySearchTree(2)
        >>> bst2.maximum()
        8

        >>> bst3 = BinarySearchTree(10)
        >>> bst3._right = BinarySearchTree(20)
        >>> bst3._right._left = BinarySearchTree(15)
        >>> bst3._right._right = BinarySearchTree(25)
        >>> bst3.maximum()
        25
        """
        if self._root is None:
            return None
        elif self._right._root is None:
            return self._root
        else:
            return self._right.maximum()

    def count(self, item: Any) -> int:
        """Return the number of occurrences of <item> in this BST.

        Hint: carefully review the BST property!

        >>> BinarySearchTree(None).count(148)  # An empty BST
        0
        >>> bst = BinarySearchTree(7)
        >>> left = BinarySearchTree(3)
        >>> left._left = BinarySearchTree(3)
        >>> left._right = BinarySearchTree(5)
        >>> right = BinarySearchTree(11)
        >>> right._left = BinarySearchTree(9)
        >>> right._right = BinarySearchTree(13)
        >>> bst._left = left
        >>> bst._right = right
        >>> bst.count(7)
        1
        >>> bst.count(3)
        2
        >>> bst.count(100)
        0
        """
        if self.is_empty():
            return 0
        elif item == self._root:
            return 1 + self._left.count(item) + self._right.count(item)
        elif item < self._root:
            return self._left.count(item)
        else:
            return self._right.count(item)

    def items(self) -> list[Any]:
        """Return all of the items in the BST in sorted order.

        Do not remove duplicates.

        You should *not* need to sort the list yourself: instead, use the BST
        property and combine self._left.items() and self._right.items()
        in the right order!

        >>> BinarySearchTree(None).items()  # An empty BST
        []
        >>> bst = BinarySearchTree(7)
        >>> left = BinarySearchTree(3)
        >>> left._left = BinarySearchTree(2)
        >>> left._right = BinarySearchTree(5)
        >>> right = BinarySearchTree(11)
        >>> right._left = BinarySearchTree(9)
        >>> right._right = BinarySearchTree(13)
        >>> bst._left = left
        >>> bst._right = right
        >>> bst.items()
        [2, 3, 5, 7, 9, 11, 13]
        >>> BinarySearchTree(5).items()
        [5]

        >>> bst = BinarySearchTree(15)
        >>> bst._left = BinarySearchTree(10)
        >>> bst._right = BinarySearchTree(20)
        >>> bst._left._left = BinarySearchTree(5)
        >>> bst._left._right = BinarySearchTree(12)
        >>> bst._right._left = BinarySearchTree(18)
        >>> bst._right._right = BinarySearchTree(25)
        >>> bst.items()
        [5, 10, 12, 15, 18, 20, 25]

        >>> bst2 = BinarySearchTree(8)
        >>> bst2._left = BinarySearchTree(6)
        >>> bst2._left._left = BinarySearchTree(4)
        >>> bst2._left._left._left = BinarySearchTree(2)
        >>> bst2.items()
        [2, 4, 6, 8]

        >>> bst3 = BinarySearchTree(10)
        >>> bst3._right = BinarySearchTree(20)
        >>> bst3._right._left = BinarySearchTree(15)
        >>> bst3._right._right = BinarySearchTree(25)
        >>> bst3.items()
        [10, 15, 20, 25]
        """
        if self.is_empty():
            return []
        elif self._left.is_empty() and self._right.is_empty():
            return [self._root]
        else:
            # acc = [self._root]
            # acc.extend(self._right.items())
            # acc = self._left.items() + acc
            return self._left.items() + [self._root] + self._right.items()

    def smaller(self, item: Any) -> list[Any]:
        """Return all of the items in this BST strictly smaller than <item>.

        The items are returned in sorted order.

        Precondition: all items in this BST can be compared with <item>.

        As with BinarySearchTree.items, you should *not* need to sort the list
        yourself!

        >>> bst = BinarySearchTree(7)
        >>> left = BinarySearchTree(3)
        >>> left._left = BinarySearchTree(2)
        >>> left._right = BinarySearchTree(5)
        >>> right = BinarySearchTree(11)
        >>> right._left = BinarySearchTree(9)
        >>> right._right = BinarySearchTree(13)
        >>> bst._left = left
        >>> bst._right = right
        >>> bst.smaller(6)
        [2, 3, 5]
        >>> bst.smaller(13)
        [2, 3, 5, 7, 9, 11]
        >>> bst = BinarySearchTree(10)
        >>> bst._left = BinarySearchTree(5)
        >>> bst._right = BinarySearchTree(15)
        >>> bst._left._left = BinarySearchTree(3)
        >>> bst._left._right = BinarySearchTree(8)
        >>> bst._right._left = BinarySearchTree(12)
        >>> bst._right._right = BinarySearchTree(20)
        >>> bst.smaller(10)
        [3, 5, 8]
        >>> bst.smaller(15)
        [3, 5, 8, 10, 12]
        >>> bst.smaller(3)
        []
        >>> bst.smaller(25)
        [3, 5, 8, 10, 12, 15, 20]
        >>> bst.smaller(5)
        [3]
        >>> bst2 = BinarySearchTree(7)
        >>> bst2._left = BinarySearchTree(4)
        >>> bst2._right = BinarySearchTree(9)
        >>> bst2._left._left = BinarySearchTree(2)
        >>> bst2._left._right = BinarySearchTree(5)
        >>> bst2._right._left = BinarySearchTree(8)
        >>> bst2._right._right = BinarySearchTree(11)
        >>> bst2.smaller(6)
        [2, 4, 5]
        >>> bst2.smaller(10)
        [2, 4, 5, 7, 8, 9]
        """
        if self.is_empty():
            return []
        elif self._root < item and self._left.is_empty():
            return [self._root]
        else:
            if self._root < item:
                return (self._left.smaller(item) + [self._root]
                        + self._right.smaller(item))
            else:
                return self._left.smaller(item)


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all()
