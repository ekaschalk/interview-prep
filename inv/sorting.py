# https://github.com/donnemartin/interactive-coding-challenges

# Sorting Questions

import collections
import itertools
import functools
import math
import toolz as tz


# * 1. Selection Sort

def selection_sort(xs):
    "n2 - find min, append it to new sorted xs, repeat."
    sorted_arr = []

    while xs:
        least, least_ix = xs[0], 0

        for ix, x in enumerate(xs):
            if least is None or x < least:
                least, least_ix = x, ix

        sorted_arr.append(least)
        xs.pop(least_ix)

    return sorted_arr


# print(selection_sort([]))
# print(selection_sort([1, 2, 5, 3, -120]))


# * 2. Insertion Sort

def insertion_sort(xs):
    "n2 - Build up sorted list by inserting each new item."
    sorted_arr = []

    for x in xs:
        for ix, y in sorted_arr:
            if x >= y:
                sorted_arr.insert(ix, x)
                break
        else:
            sorted_arr.append(x)

    return sorted_arr


# print(selection_sort([1, 2, 5, 3, -120]))


# * 3. Quick Sort
# ** Commentary

# i is the number of times we swapped plus the left index
# when we swap, the element smaller than the pivot is pushed earlier
# and the element larger later

# let left=0
# xs[0] gets first element smaller than the pivot
# xs[1] gets second element smaller than the pivot
# ...
# xs[i] gets last element smaller than the pivot
# at end, pivot is swapped into xs[i+1]
# now xs[:i+1] is < pivot, xs[i+1] is pivot, and xs[i+2:] is > pivot
# now recurse on xs[:i+1] and xs[i+2:]
# Returning i == returning the position of the pivot after mutations == i+1 above

# ** Implementation

def partition(xs, left, right):
    pivot = xs[right]
    pivot_ix = left

    for ix in range(left, right):
        if xs[ix] <= pivot:
            xs[pivot_ix], xs[ix] = xs[ix], xs[pivot_ix]
            pivot_ix += 1

    xs[pivot_ix], xs[right] = xs[right], xs[pivot_ix]

    return pivot_ix

def _quicksort(xs, left, right):
    if left >= right:
        return

    p = partition(xs, left, right)

    _quicksort(xs, left, p-1)
    _quicksort(xs, p+1, right)

def quicksort(xs):
    "n2 - Recursively: pick a pivot, reorder arround the pivot."
    _quicksort(xs, 0, len(xs)-1)
    return xs


# print(quicksort([1, 2, 5, 3, -120]))


# * 4. Merge Sort

def _mergesort(xs, left, right):
    "nlogn - Add smaller of each sorted subarrays until both exhaust."
    if left >= right-1:
        return xs[left:right]

    m = (right-left)//2 + left

    L, R = _mergesort(xs, left, m), _mergesort(xs, m, right)

    merge = []
    L_i, R_i = 0, 0
    for x in L:
        for y in R[R_i:]:
            if x <= y:
                merge.append(x)
                L_i += 1
                break

            merge.append(y)
            R_i += 1

    return merge + L[L_i:] + R[R_i:]

def mergesort(xs):
    "?? - Recursively: Merge sorted subarrays"
    return _mergesort(xs, 0, len(xs))

# print(mergesort([1, 2, 5, 3, -12, -10]))


# * 5. Radix Sort

# Most significant digit version:
# 1. Sort on most sig digit
# 2. Bucket elements with same digit
# 3. Recursively sort each bucket
# 4. Concatenate buckets

def _radixsort(xs, exp, base=10):
    if exp < 0:
        return xs

    bins = collections.defaultdict(list)
    for x in xs:
        digit = x // base**exp % base
        bins[digit].append(x)

    sorted_xs = []
    for _, group in sorted(bins.items(), key=lambda digit_group: digit_group[0]):
        sorted_xs.extend(_radixsort(group, exp-1, base=base))

    return sorted_xs

def radixsort(xs, base=10):
    max_exp = math.floor(math.log(max(xs), base))

    return _radixsort(xs, max_exp, base=base)


# print(radixsort([1, 2, 5, 3, -12, -10]))
print(radixsort([170, 45, 75, 90, 2, 802, 2, 66]))
print(radixsort([1, 2, 5, 3, 12, 10, 400, 403, 412]))


# * 6. Sort an Array of strings so anagrams are next to eachother

# An anagram is a reordering of a string
# Answer:
# 1. Sort each string
# 2. Sort the sorted strings
# 3. Transform above back to original representation

def anagramsort(xs):
    pairs = [(x, "".join(sorted(x))) for x in xs]

    return [x for x, _ in sorted(pairs, key=lambda xy: xy[1])]

# Above solves the challenge, but isn't stable (though not a requirement)
# To solve stably:
# 1. Do (original_ix, sorted_str) instead of (x, sorted_str)
# 2. Group the ixs by equal sorted_str
# 3. Concatenate the xs identifiyed by the ix_groups in order
# Note: To get their result, just do one last sort

def anagramsort_stable(xs):
    groups = collections.defaultdict(list)
    for ix, x in enumerate(xs):
        sorted_x = "".join(sorted(x))
        groups[sorted_x].append(ix)

    sorted_xs = []
    for _, ixs in groups.items():
        sorted_xs.extend(xs[ix] for ix in ixs)
        # sorted_xs.extend(sorted(xs[ix] for ix in ixs))  # for their result

    return sorted_xs


# print(anagramsort(['ram', 'act', 'arm', 'bat', 'cat', 'tab']))
# print(anagramsort_stable(['ram', 'act', 'arm', 'bat', 'cat', 'tab']))
# ['arm', 'ram', 'act', 'cat', 'bat', 'tab']

# * 7. Find an item in a sorted, rotated array

# It could be rotated multiple times
# Do it in logn
