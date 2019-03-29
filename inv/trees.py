# https://github.com/donnemartin/interactive-coding-challenges

# Tree questions

import collections
import itertools
import functools
import toolz as tz

# * x. Implement a Binary Search Tree
# ** Node

@functools.total_ordering
class Node(object):
    def __init__(self, item):
        self.item = item
        self.left = None
        self.right = None

    def __repr__(self):
        return repr(self.item)

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.item == other.item
        return self.item == other

    def __lt__(self, other):
        if isinstance(other, Node):
            return self.item < other.item
        return self.item < other

    def find(self, item):
        return self.left if item < self else self.right

# ** BST

class BST(object):
    def __init__(self, *items):
        self.head = None

        for item in items:
            self.insert(item)

    def __iter__(self):
        yield from self.in_order

    def __len__(self):
        return len(list(iter(self)))

    def __repr__(self):
        return repr(list(iter(self)))

    # ** Mutations

    def _find(self, item, node):
        if node is None:
            return
        if item == node:
            return item

        return self._find(item, node.find(item))

    def find(self, item):
        return self._find(item, self.head)

    def _insert_left(self, item, node):
        if node.left is None:
            node.left = Node(item)
        else:
            self._insert(item, node.left)

    def _insert_right(self, item, node):
        if node.right is None:
            node.right = Node(item)
        else:
            self._insert(item, node.right)

    def _insert(self, item, node):
        if item <= node:
            self._insert_left(item, node)
        else:
            self._insert_right(item, node)

    def insert(self, item):
        if self.head is None:
            self.head = Node(item)
            return

        return self._insert(item, self.head)

    def delete(self, item):
        pass

    # ** Traversal

    def _in_order(self, node):
        if node.left:
            yield from self._in_order(node.left)
        yield node
        if node.right:
            yield from self._in_order(node.right)

    def _pre_order(self, node):
        yield node
        if node.left:
            yield from self._pre_order(node.left)
        if node.right:
            yield from self._pre_order(node.right)

    def _post_order(self, node):
        yield node
        if node.right:
            yield from self._post_order(node.right)
        if node.left:
            yield from self._post_order(node.left)

    @property
    def in_order(self):
        yield from self._in_order(self.head)

    @property
    def pre_order(self):
        yield from self._pre_order(self.head)

    @property
    def post_order(self):
        yield from self._post_order(self.head)

    @property
    def level_ordered(self):
        pass


x = BST(5, 2, 8, 1, 3)
pre = [5, 2, 1, 3, 8]
in_ = [1, 2, 3, 5, 8]
post = [1, 3, 2, 8, 5]
# assert(post == list(x.post_order))

# x = BST(1, 2, 3, 4, 5)
# pre = [1, 2, 3, 4, 5]
# in_ = [1, 2, 3, 4, 5]
# post = [5, 4, 3, 2, 1]
