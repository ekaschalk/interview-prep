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
