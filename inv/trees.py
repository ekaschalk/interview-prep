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
        yield from self.pre_order

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

    def _insert(self, item, node):
        if item <= node:
            if node.left is None:
                node.left = Node(item)
                return

            return self._insert(item, node.left)
        else:
            if node.right is None:
                node.right = Node(item)
                return

            return self._insert(item, node.right)
        return

    def insert(self, item):
        if self.head is None:
            self.head = Node(item)
            return

        return self._insert(item, self.head)

    def delete(self, item):
        pass

    # ** Traversal

    def _pre_order(self, node, stack):
        if node is None:
            return

        if node.left:
            stack.append(node.left)
            self._pre_order(node.left, stack)

        if node.right:
            stack.append(node.right)
            self._pre_order(node.right, stack)

    @property
    def pre_order(self):
        stack = [self.head] if self.head else []
        self._pre_order(self.head, stack)

        while stack:
            yield stack.pop()

    @property
    def in_order(self):
        pass

    @property
    def post_order(self):
        pass

    @property
    def level_ordered(self):
        pass


# x = BST(1, 2, 3, 4)
# x = BST(4, 2, 3, 1)
x = BST(1, 2, 3, 1, 2, 5, 2)
