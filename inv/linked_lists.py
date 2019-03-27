# https://github.com/donnemartin/interactive-coding-challenges

# Linked List Questions

import collections
import itertools
import functools
import toolz as tz

# * 8. Implement a Linked List (base-class for rest)
# ** Node

@functools.total_ordering
class Node(object):
    def __init__(self, val, _next=None):
        self.val = val
        self._next = _next

    def __repr__(self):
        return repr(self.val)

    def __hash__(self):
        return hash(self.val)

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.val == other.val
        elif isinstance(other, int):
            return self.val == other
        return False

    def __lt__(self, other):
        if isinstance(other, Node):
            return self.val < other.val
        elif isinstance(other, int):
            return self.val < other
        return False

    def __add__(self, other):
        if isinstance(other, Node):
            return self.val + other.val
        elif isinstance(other, int):
            return self.val + other

# ** LinkedList

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

    # *** Insertion

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

    # *** Deletion

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

    # *** Finding

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
        try:
            return tz.nth(len(self) - k - 1, self)
        except (ValueError, StopIteration):
            return

x = LinkedList2()
x.append(0)
x.append(1)
x.append(2)
x.append(3)
x.append(4)

# x.kth_last(2)

# * 3. Node Deletion (already implemented)

# * 4. Partition a linked list on X

# Partition a linked list around a value x, such that all nodes less than x
# come before all nodes greater than or equal to x.

class LinkedList4(LinkedList):
    def partition(self, x):
        node = self.head

        prev_node_lt = None
        chain = LinkedList()

        while node:
            if node >= x:
                chain.append(node.val)
                prev_node_lt._next = node._next
            else:
                prev_node_lt = node

            node = node._next

        prev_node_lt._next = chain.head

x = LinkedList4()
x.append(0)
x.append(1)
x.append(2)
x.append(3)
x.append(4)
x.append(5)
x.append(0)
x.append(1)
x.append(2)
x.append(3)
x.append(4)
x.append(5)

# x.partition(2)

# * 5. Add two numbers whose digits are stored in a linked list

# Add two numbers whose digits are stored in a linked list in reverse order

# 1234 -> + 4 3 2 1
# 123 ->    3 2 1
# 1357

# 987 -> + 7 8 9
# 87 ->    7 8
# 1074


class LinkedList5(LinkedList):
    def __add__(self, other):
        partials = [x+y for x, y in
                    itertools.zip_longest(self, other, fillvalue=0)]
        digits = len(partials)-1
        potential_digit = None

        for ix, partial in enumerate(partials):
            if partial < 10:
                continue

            if ix+1 > digits:
                potential_digit = 1
            else:
                partials[ix+1] += 1
            partials[ix] -= 10

        if potential_digit:
            partials.append(potential_digit)

        return int("".join(map(str, reversed(partials))))


x = LinkedList5()
x.push(1)
x.push(2)
x.push(3)
x.push(4)
y = LinkedList5()
y.push(1)
y.push(2)
y.push(3)

# x+y

x = LinkedList5()
x.push(9)
x.push(8)
x.push(7)
y = LinkedList5()
y.push(8)
y.push(7)

# x+y

# * 6. Find the start of a linked list loop

class LinkedList6(LinkedList):
    pass
