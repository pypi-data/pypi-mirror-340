# MaxMinConquer

`maxminconquer` is a Python package that implements divide and conquer algorithms for finding the maximum and minimum values in a list.

## Functions

- `find_max(arr, left, right)` - Finds the maximum value using divide and conquer.
- `find_min(arr, left, right)` - Finds the minimum value using divide and conquer.

## Time Complexity

- Both `find_max` and `find_min` functions have a time complexity of **O(n)** where **n** is the number of elements in the array. This is because in each step, the array is split into two halves, and the maximum or minimum value is recursively calculated on each half.

## Usage

```python
from maxminconquer import find_max, find_min

arr = [1, 2, 3, 4, 10, 90, -4, 5, 65, 87, 78, 98, 41]

max_value = find_max(arr, 0, len(arr) - 1)
print("Maximum value:", max_value)

min_value = find_min(arr, 0, len(arr) - 1)
print("Minimum value:", min_value)
