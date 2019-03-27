# https://github.com/donnemartin/interactive-coding-challenges

# Linked List Questions

import collections
import functools
import toolz as tz

# * 8. Implement a Linked List

class Node(object):
    def __init__(self, val, _next=None):
        self.val = val
        self._next = _next

    def __repr__(self):
        return repr(self.val)

    def __hash__(self):
        return hash(self.val)

    def __eq__(self, other):
        return isinstance(other, Node) and self.val == other.val

class LinkedList(object):
    def __init__(self):
        self.head = None

    def __repr__(self):
        return "[{}]".format(" ".join(map(repr, self)))

    def __bool__(self):
        return bool(self.head)

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node._next

    def __len__(self):
        return tz.count(iter(self))

    @property
    def tail(self):
        return tz.last(self)

    def nth(self, n):
        return tz.nth(n, self)

    # ** Insertion

    def insert_at(self, ix, val):
        if ix == 0:
            return self.push(val)

        node = self.nth(ix-1)

        if node._next is None:
            return self.append(val)

        item = Node(val, _next=node._next)
        node._next = item

    def push(self, val):
        item = Node(val)

        if self.head is not None:
            item._next = self.head

        self.head = item

    def append(self, val):
        item = Node(val)

        if self.head is None:
            self.head = item
            return

        self.tail._next = item

    # ** Deletion

    def remove_at(self, ix):
        if not self:
            return

        if ix == 0:
            self.head = self.head._next
            return

        node = self.nth(ix-1)

        if node._next is None:
            return

        node._next = node._next._next

    def pop(self):
        if self:
            self.remove_at(len(self)-1)

    def remove(self, val):
        ix = self.find_ix(val)

        while ix:
            self.remove_at(ix)
            ix = self.find_ix(val)

    def _remove_first(self, val):
        ix = self.find_ix(val)

        if ix:
            self.remove_at(ix)

    # ** Finding

    def find(self, val):
        try:
            return tz.first(node for node in self if node.val == val).val
        except StopIteration:
            return

    def find_ix(self, val):
        try:
            return tz.first(i for i, node in enumerate(self) if node.val == val)
        except StopIteration:
            return

x = LinkedList()

x.append(1)
x.append(2)
x.append(4)
x.append(4)
x.append(4)
x.push(0)
x.insert_at(3, 3)
x.remove_at(2)
x.pop()

# * 1. Remove duplicates from a linked list (2 versions)

class LinkedList1(LinkedList):
    def remove_dupes1(self):
        "Memory = o(n), speed = o(n)"
        visited = collections.defaultdict(int)
        node, prev_node = self.head, None

        while node:
            visited[node] += 1

            if visited[node] > 1:
                # Find next distinct node
                current_node = node
                while current_node == node:
                    node = node._next

                prev_node._next = node._next if node else None

            prev_node = node
            node = node._next if node else None

    def remove_dupes2(self):
        "Memory = o(1), speed = o(n^2)"
        fixed_node = self.head
        prev_node, node = None, None

        while fixed_node:
            node = fixed_node

            while node:
                prev_node = node
                node = node._next

                if node == fixed_node:
                    prev_node._next = node._next if node else None

            fixed_node = fixed_node._next

x = LinkedList1()
x.append(1)
x.append(2)
x.append(2)
x.append(3)
x.append(3)
x.append(3)
x.append(4)
x.append(4)
x.append(1)

# x.remove_dupes1()
# x.remove_dupes2()

# * 2. Find the kth to last element of a linked list

class LinkedList2(LinkedList):
    def kth_last(self, k):
        pass

x = LinkedList2()
x.append(0)
x.append(1)
x.append(2)
x.append(3)
x.append(4)
