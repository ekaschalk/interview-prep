# https://github.com/donnemartin/interactive-coding-challenges

# Tree questions

import collections
import itertools
import functools
import toolz as tz

# * 1+2. Implement a Binary Search Tree (BFS and DFS included)
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

# ** Queue

class Queue(collections.deque):
    def enqueue(self, x):
        self.appendleft(x)

    def dequeue(self):
        return self.pop()

    def dequeue_all(self):
        while self:
            yield self.dequeue()

    def peek(self):
        return self[0]

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
            return

        return self._insert(item, node.left)

    def _insert_right(self, item, node):
        if node.right is None:
            node.right = Node(item)
            return

        return self._insert(item, node.right)

    def _insert(self, item, node):
        if item <= node:
            return self._insert_left(item, node)

        return self._insert_right(item, node)

    def insert(self, item):
        if self.head is None:
            self.head = Node(item)
            return

        return self._insert(item, self.head)

    def delete(self, item):
        pass

    # ** Traversal
    # *** DFS

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

    # *** BFS

    def _bfs(self, q):
        if not q:
            return

        node = q.dequeue()
        yield node

        if node.left:
            q.enqueue(node.left)
        if node.right:
            q.enqueue(node.right)

        yield from self._bfs(q)

    @property
    def bfs(self):
        if not self.head:
            return

        yield from self._bfs(Queue([self.head]))


x = BST(5, 2, 8, 1, 3)

# pre = [5, 2, 1, 3, 8]
# in_ = [1, 2, 3, 5, 8]
# post = [1, 3, 2, 8, 5]
# bfs = [5, 2, 8, 1, 3]

# x = BST(1, 2, 3, 4, 5)
# pre = [1, 2, 3, 4, 5]
# in_ = [1, 2, 3, 4, 5]
# post = [5, 4, 3, 2, 1]
# bfs = [1, 2, 3, 4, 5]

# * 3. Determine the height of a tree

class BST3(BST):
    def _height(self, node, i):
        yield node, i
        if node.left:
            yield from self._height(node.left, i+1)
        if node.right:
            yield from self._height(node.right, i+1)

    @property
    def height(self):
        just_height = lambda x: x[1]

        if not self.head:
            return 0

        return just_height(max(self._height(self.head, 1),
                               key=just_height))

x = BST3(5, 2, 8, 1, 3)
# x.height == 3
x = BST3(1, 2, 3, 4, 5)
# x.height == 5
