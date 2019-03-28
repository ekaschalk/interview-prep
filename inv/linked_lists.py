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

        return item

    def push(self, val):
        item = Node(val)

        if self.head is not None:
            item._next = self.head

        self.head = item

        return item

    def append(self, val):
        item = Node(val)

        if self.head is None:
            self.head = item
            return item

        self.tail._next = item

        return item

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
    def find_loop(self):
        slow, fast = self.head, self.head

        while fast._next is not None:
            slow, fast = slow._next, fast._next._next
            if fast is None:
                return None
            if slow == fast:
                break

        slow = self.head

        while slow != fast:
            slow, fast = slow._next, fast._next
            if fast is None:
                return None

        return slow

x = LinkedList6()
node0 = x.append(0)
node1 = x.append(1)
node2 = x.append(2)
node3 = x.append(3)
node4 = x.append(4)
node5 = x.append(5)
node5._next = node2

# 5->2
# 0 1 2 3 4 5  2 3 4 5  2 3 4 5
# 0 2 4 2 4
# 0 1  2  3 4 5
# 4 5  2  3 4 5

# 5->1
# 0 1 2 3 4 5  1 2 3 4 5  1 2 3 4 5
# 0 2 4 1 3 5
# 0  1  2 3 4 5
# 5  1  2 3 4 5

# list(tz.take(24, zip(x, itertools.islice(x, 0, 1000, 2))))
# list(tz.take(12, x))
# x.find_loop()

# https://medium.com/100-days-of-algorithms/day-62-linked-list-cycle-detection-a3f2db8cfaa0
# ALG:
# N = len(unique)
# C = len(cyle)
# T = N-C len(not-in-cycle)
# k = steps in cycle (to meet up in the cycle)

# when C=N
# k == 2k (mod C)
# k == 0  (mod C)
# so k=C and C=N so k=N

# When C != N
# T+k == 2T + 2k (mod C)
# T+k == 0 (mod C)
# T+k == C (mod C)

# not_in_cycle + steps_in_cycle == 2*not_in_cycle+2*steps_in_cycle MOD len(cycle)
# not_cycle + steps_in_cycle == 0

#       ------------
# ------------------
# - T - ---- C ----
# ------ N ---------


# 2k catches each other up, once we "close" T
# how many steps does it take to close T?
# T + k == 2T + 2k follows

# AH Notice once T steps have been taken, then both pointers are in the loop

# Now the k == 2k congruence is in effect

#    from T == 2T (mod C) and k == 2k (mod C)

# Where do the pointers meet inside of C? They meet T away from the start of C.
# So if we move from start T and from where they meet, T away from C,
# then they meet at the start of C!

# Finalizing my understanding:
# 1. When we move T spaces inside, the fast pointer has a 2T-T=T head-start
# 2. When we detect a cycle, it will be T away from the finish.
#    - Details on this step:
#      if we move T spaces forward on both from where they meet
#      then slow will be at start of C and fast will be T away from C
#      ie. exactly where they began
#      so working backwards, we would end up T away from finish
#      when they both match
# 3. So if we move T forward from start and where we stopped, we found cycle start

# * 7. Determine if a linked list is a palindrome

# This solution is kind-of-cheeky

class LinkedList7(LinkedList):
    def palindrome(self):
        items = list(iter(self))

        return items == list(reversed(items))

x = LinkedList7()
x.append(1)
x.append(2)
x.append(3)
x.append(4)
x.append(3)
x.append(2)
x.append(1)

# x.palindrome()
