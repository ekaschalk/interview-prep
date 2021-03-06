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

# * 4. Create a BST with minimal height from a sorted array

class BST4(BST3):
    def __init__(self, *sorted_items):
        self.head = None

        self.insert_sorted(sorted_items)

    def _insert_sorted(self, items, q):
        if not q:
            return

        a, b = q.pop()
        m = a + ((b - a) // 2)

        if b-a == 0:
            return

        self.insert(items[m])

        q.enqueue((a, m))
        q.enqueue((m+1, b))

        self._insert_sorted(items, q)

    def insert_sorted(self, items):
        if not items:
            return

        q = Queue()
        q.enqueue((0, len(items)))

        self._insert_sorted(items, q)

x = BST4(0, 1, 2, 3, 4, 5, 6)
# x.height == 3

x = BST4(0, 1, 2, 3, 4, 5, 6, 7)
# x.height == 4

# * 5. Create a linkedlist for each level of a binary tree

class BST5(BST):
    def _to_lists(self, q):
        if not q:
            return

        node, level = q.dequeue()
        yield node, level

        if node.left:
            q.enqueue((node.left, level+1))
        if node.right:
            q.enqueue((node.right, level+1))

        yield from self._to_lists(q)

    def to_lists(self):
        getlevel = lambda x: x[1]

        if not self.head:
            return

        pairs = self._to_lists(Queue([(self.head, 0)]))
        for _, node_level_pairs in tz.groupby(getlevel, pairs).items():
            yield [node for node, _ in node_level_pairs]

x = BST5(0, 1, 2, 3, 4, 5, 6, 7)
list(x.to_lists())
# [[0], [1], [2], [3], [4], [5], [6], [7]]

x = BST5(5, 2, 8, 1, 3)
list(x.to_lists())
# [[5], [2, 8], [1, 3]]

# * 6. Check if a binary tree is balanced

class BST6(BST5):
    @property
    def balanced(self):
        getlevel = lambda x: x[1]

        if not self.head:
            return True

        pairs = self._to_lists(Queue([(self.head, 0)]))
        pairs_by_level = list(tz.groupby(getlevel, pairs).items())

        for level, node_level_pairs in pairs_by_level[:-1]:
            if len(node_level_pairs) != 2 ** level:
                return False

        return True

x = BST6(5, 3, 8, 1, 4)
x.balanced

x = BST6(5, 3, 8, 9, 10)
x.balanced

# * 7. Check if tree is a valid binary search tree

class BST7(BST):
    def _valid(self, node):
        if node.left:
            if node.left > node:
                raise StopIteration
            return self._valid(node.left)

        if node.right:
            if node.right <= node:
                raise StopIteration
            return self._valid(node.right)
        return True

    @property
    def valid(self):
        if not self.head:
            return True

        try:
            return self._valid(self.head)
        except StopIteration:
            return False

x = BST7(5, 5, 8, 4, 6, 7)
x.valid
# True

x = BST7(5)
x.head.left = Node(8)
x.head.right = Node(5)
x.valid
# False

# * 8. Find the in-order succession of a given node in a BST

class BST8(BST):
    # In-order: left - root - right

    # Because my implementations are lazy, this is just as fast as embedding
    # the checks into the implementation. ie. this is perfect already

    # Unless the BST condition makes it possible to do it quicker...
    def successor(self, node):
        if not self.head:
            return

        ordered = self.in_order
        for item in ordered:
            if item != node:
                continue

            try:
                return next(ordered)
            except StopIteration:
                return

    def successor_smart(self, node):
        if node.left:
            pass

        if node.right:
            return left_most_node


x = BST8(5, 9, 8, 4, 6, 7)
ordered = list(x.in_order)
node = ordered[2]

x.successor(node)

# * 9. Find the 2nd-largest node in a BST
