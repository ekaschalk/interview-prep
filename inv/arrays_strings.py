# https://github.com/donnemartin/interactive-coding-challenges

# Array and Strings Questions

import collections
import functools
import toolz as tz

# * 1. Determine if a string contains only unique characters

def has_unique_chars(string):
    return all(map(functools.partial(int.__eq__, 1),
                   collections.Counter(string).values()))
    return all(count == 1 for count in collections.Counter(string).values())

assert(has_unique_chars(""))
assert(not(has_unique_chars("foo")))
assert(has_unique_chars("fo"))

# * 2. Determine if a string is a permutation of another

def is_permutation(string1, string2):
    string1_items = collections.Counter(string1).items()
    string2_items = collections.Counter(string2).items()

    return sorted(string1_items) == sorted(string2_items)

assert(not(is_permutation(None, 'foo')))
assert(not(is_permutation('', 'foo')))
assert(not(is_permutation('Nib', 'bin')))
assert(is_permutation('act', 'cat'))
assert(is_permutation('a ct', 'ca t'))

# * 3. Determine if a string is a rotation of another

# Call the first char in string1 c_0
# Iterate through string2
#  When char c_0 is found at position i:
#  zip string1[1:] and string2[i:]
#  take until equality breaks at position j
#  check if string1[j:] == string2[0:i]
#  If so, we have found a rotation
#  otherwise, continue

def idx_of_different_char(s1, s2):
    for (j, (c1, c2)) in enumerate(zip(s1, s2)):
        if c1 != c2:
            return j

    return None

def is_rotation(s1, s2):
    if s1 is None or s2 is None or len(s1) != len(s2):
        return False

    if s1 == "" and s2 == "":
        return True

    c_0 = s1[0]

    for i, c in enumerate(s2):
        if c_0 == c:
            j = idx_of_different_char(s1[1:], s2[(i+1):])

            if j is None or s1[j:] == s2[:(i+1)]:
                return True

    return False

def is_rotation_cleaner(s1, s2):
    if s1 is None or s2 is None or len(s1) != len(s2):
        return False

    if s1 == "" and s2 == "":
        return True

    return s1 in (s2 + s2)

assert(not(is_rotation('o', 'oo')))
assert(not(is_rotation(None, 'foo')))
assert(not(is_rotation('', 'foo')))
assert(is_rotation('', ''))
assert(is_rotation('foobarbaz', 'barbazfoo'))
assert(not(is_rotation('foobarbaz', 'barbazfooo')))
assert(not(is_rotation('foobarbazz', 'barbazfoo')))

# * 4. Compress a string

def format_compression(char, count):
    return "{}{}".format(char, count) if count > 1 else char

def compress(s):
    compressed, count, prev_char = "", 0, s[0]

    for c in s:
        if c != prev_char:
            compressed += format_compression(prev_char, count)
            count, prev_char = 0, c
        count += 1

    return compressed + format_compression(prev_char, count)

assert(compress('AAABCCDDDDE') == 'A3BC2D4E')
assert(compress('BAAACCDDDD') == 'BA3C2D4')
assert(compress('AAABAACCDDDD') == 'A3BA2C2D4')

# * 5. Reverse a string

def s_reverse(s):
    s = list(s)
    n = len(s)
    for i in range(n//2):
        s[i], s[n-i-1] = s[n-i-1], s[i]

    return s

assert(s_reverse("foo bar") == ['r', 'a', 'b', ' ', 'o', 'o', 'f'])

# * 6. Different char among two strings

# def find_diff_1(s_large, s_small):
#     return next(c1 for c1, c2 in zip(s_large, s_small) if c1 != c2)

# def find_diff(s1, s2):
#     return find_diff_1(s1, s2) if len(s1) >= len(s2) else find_diff(s2, s1)

# Above version works/faster if the strings were in same order

def find_diff(s1, s2):
    if len(s2) >= len(s1):
        s1, s2 = s2, s1

    s1_counter, s2_counter = collections.Counter(s1), collections.Counter(s2)

    for c, count in s1_counter.items():
        if s2_counter[c] == count:
            continue

        return c

    return False

assert(find_diff('ab', 'aab') == 'a')
assert(find_diff('aab', 'ab') == 'a')
assert(find_diff('abcd', 'abcde') == 'e')
assert(find_diff('aaabbcdd', 'abdbacade') == 'e')

# * 7. Find two indices that sum to a value

def two_sum(arr, target):
    partials = {}

    for i, n in enumerate(arr):
        if n in partials:
            return (partials[n], i)

        partials[target-n] = i

    return None

assert(two_sum([1, 3, 2, -7, 5], 7) == (2, 4))

# * 8. Implement a Hash Table

class Item(object):
    def __init__(self, key, val):
        self.key = key
        self.val = val

    def __repr__(self):
        return "<Item({}={})>".format(self.key, self.val)

class Bucket(object):
    def __init__(self):
        self._items = []

    def __repr__(self):
        return "".join(map(str, self)) if self else "-"

    def __bool__(self):
        return bool(self._items)

    def __iter__(self):
        yield from self._items

    def __getitem__(self, key):
        for item in self:
            if item.key == key:
                return item

    def __setitem__(self, key, val):
        if self[key]:
            self[key].val = val
        else:
            self._items.append(Item(key, val))

    def __delitem__(self, key):
        del self[key]

class HashTable(object):
    def __init__(self, **kwargs):
        self._size = 10
        self._buckets = [Bucket() for _ in range(self._size)]

        for key, val in kwargs.items():
            self[key] = val

    def __repr__(self):
        return repr(self._buckets)

    def _hash(self, key):
        return hash(key) % self._size

    def _get_bucket(self, key):
        return self._buckets[self._hash(key)]

    def __getitem__(self, key):
        return self._get_bucket(key)[key]

    def __setitem__(self, key, val):
        self._get_bucket(key)[key] = val

    def __delitem__(self, key):
        del self._get_bucket(key)[key]

# x = HashTable(foo=0, bar=1, bro=2)
# x[1] = 7
