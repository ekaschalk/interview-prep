# https://github.com/donnemartin/interactive-coding-challenges

# Stacks and Queues questions

import collections
import itertools
import functools
import toolz as tz

# * 1. Implement N stacks using a single array

class Stacks1(object):
    __stack_size = 5

    def __init__(self, stacks):
        self._stacks = stacks
        self._size = stacks * self.__stack_size
        self._arr = [None for _ in range(self._size)]

    def __repr__(self):
        return repr(self._arr)

    def __len__(self):
        return len(self._arr)

    def __getitem__(self, ix):
        return self._arr[ix]

    def __setitem__(self, ix, val):
        self._arr[ix] = val

    def __delitem__(self, ix):
        self._arr[ix] = None

    def _stack_ix(self, stack):
        if stack > self._stacks:
            return

        return stack * self.__stack_size

    def _stack_ix_slice(self, stack):
        return self._stack_ix(stack), self._stack_ix(stack+1)

    def pop(self, stack):
        ix, ix_max = self._stack_ix_slice(stack)

        try:
            remove_at = tz.first(i-1
                                 for i, x in enumerate(self._arr[ix:ix_max], ix)
                                 if x is None)
        except StopIteration:
            remove_at = ix_max-1

        item = self[remove_at]
        del self[remove_at]
        return item

    def push(self, stack, item):
        ix, ix_max = self._stack_ix_slice(stack)

        try:
            insert_at = tz.first(i
                                 for i, x in enumerate(self._arr[ix:ix_max], ix)
                                 if x is None)
        except StopIteration:
            raise RuntimeError("Pushing to a full stack")

        self[insert_at] = item


x = Stacks1(3)
x.push(0, 0)
x.push(0, 1)
x.pop(0)
x.push(0, 1)
x.push(0, 2)
x.push(0, 3)
x.push(0, 4)
# x.push(0, 5)
x.pop(0)
x.push(1, 0)
x.push(2, 0)
x.push(1, 1)
x.push(2, 2)

# * 2. Stack that keeps track of its minimum element

# Constraints: push, pop, and min are O(1)

@functools.total_ordering
class Node(object):
    def __init__(self, item, _next=None):
        self.item = item
        self._next = _next

    def __repr__(self):
        return repr(self.item)

    def __eq__(self, other):
        return self.item == other.item

    def __lt__(self, other):
        return self.item < other.item

class Stacks2(object):
    __maxint = 100

    def __init__(self):
        self.head = None
        self.mins = []

    @property
    def minimum(self):
        return self.mins[-1]

    def push(self, item):
        if not self.mins:
            self.mins.append(item)
        else:
            self.mins.append(item if item < self.minimum else self.minimum)

        item = Node(item)

        if self.head is None:
            self.head = item
            return

        self.head._next = item

    def pop(self):
        if self.head is None:
            return

        self.mins.pop()
        self.head, prev_head = self.head._next, self.head

        return prev_head


x = Stacks2()

x.push(1)
x.push(2)
x.push(0)
x.pop()
x.push(5)
x.push(3)
x.push(0)
x.minimum

# * 3. SetOfStacks that wraps list of stacks, each stack bounded

# bounded by capacity

# Boring question skipping

# * 4. Implement a queue using two stacks

class Queue4(object):
    def __init__(self):
        self.stack1 = []
        self.stack2 = []
        self._cur_stack = self.stack1
        self._temp_stack = self.stack2

    def __repr__(self):
        return repr(self._cur_stack)

    def shift_stacks(self):
        while self._cur_stack:
            self._temp_stack.append(self._cur_stack.pop())

        self._cur_stack, self._temp_stack = self._temp_stack, self._cur_stack

    def enqueue(self, item):
        self._cur_stack.append(item)

    def dequeue(self):
        self.shift_stacks()
        item = self._cur_stack.pop()
        self.shift_stacks()

        return item



x = Queue4()
x.enqueue(1)
x.enqueue(2)
x.enqueue(3)
x.enqueue(4)
x.enqueue(5)
x.dequeue()
x.enqueue(6)

# * 5. Sort a stack with another stack as a buffer

class Stack5(object):
    def __init__(self):
        self.stack = []

    def __repr__(self):
        return repr(self.stack)

    def push(self, item):
        self.stack.append(item)

    def _shift_stacks(self, src, dest, insert=None):
        more_to_sort = False
        inserting = insert is not None

        if not src and inserting:
            return False

        while src:
            item = src.pop()

            if not more_to_sort and inserting and item > insert:
                dest.append(insert)
                more_to_sort = True

            dest.append(item)

        return more_to_sort

    def sort(self):
        if not self.stack:
            return

        buffer_ = []
        more_to_sort = True

        while more_to_sort:
            item = self.stack.pop()
            self._shift_stacks(self.stack, buffer_)
            more_to_sort = self._shift_stacks(buffer_, self.stack, insert=item)

        self.stack.append(item)

# [1 2 3 4 5 2]
# pop() = 2
# 5 4 3 2 1
# => ins
# 5 4 3 2 1 2
# => flip

# [1 2 2 3 4 5]
# pop() = 5
# 4 3 2 2 1
# => buffer_ is exhaused without a (strict) inequality found
# => done

# TEST CASE
# [0, 1, 2, 3, 2, -1, 2]
# =>
# [-1, 0, 1, 2, 2, 2, 3]

x = Stack5()
x.push(0)
x.push(0)
x.push(1)
x.push(2)
x.push(3)
x.push(2)
x.push(-1)
x.push(2)

# * 8. Implement a priority queue backed by an array

@functools.total_ordering
class Node(object):
    def __init__(self, item, priority):
        self.item = item
        self.priority = priority

    def __repr__(self):
        return repr(self.item)

    def __eq__(self, other):
        return self.priority == other.priority

    def __lt__(self, other):
        return self.priority < other.priority


class PriorityQueue(object):
    def __init__(self):
        self._arr = []

    def __repr__(self):
        return repr(self._arr)

    def __len__(self):
        return len(self._arr)

    def __getitem__(self, ix):
        return self._arr[ix]

    # * O(n)

    def enqueue_linear(self, item, priority):
        node = Node(item, priority)

        try:
            ix = next(i for i, x in enumerate(self._arr) if x > node)
            self._arr.insert(ix, node)
        except StopIteration:
            self._arr.append(node)

    # * O(log(n))

    def _search(self, node, a=0, b=None):
        b = len(self) if b is None else b
        m = (a + b) // 2

        if a >= b or self[m] == node:
            return m
        elif self[m] < node:
            return self._search(node, a=m+1, b=b)
        elif self[m] > node:
            return self._search(node, a=a, b=m)

    def enqueue(self, item, priority):
        node = Node(item, priority)

        ix = self._search(node)
        self._arr.insert(ix, node)

    def dequeue(self):
        return self._arr.pop()


# [0, 1, 2, '2-3', 3, 4]
x = PriorityQueue()
x.enqueue(1, 1)
x.enqueue(2, 10)
x.enqueue(3, 100)
x.enqueue(0, 0)
x.enqueue(4, 1000)
x.enqueue("2-3", 50)
# x.dequeue()
