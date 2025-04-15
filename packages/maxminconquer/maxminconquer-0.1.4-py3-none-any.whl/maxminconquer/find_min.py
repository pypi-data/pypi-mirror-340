# maxminconquer/find_min.py

def find_min(arr, left, right):
    """Finds the minimum value in the array using Divide and Conquer."""
    # Base case: If there is only one element
    if left == right:
        return arr[left]
    
    # Find the middle index
    mid = (left + right) // 2
    
    # Recursively find the minimum in both halves
    min_left = find_min(arr, left, mid)
    min_right = find_min(arr, mid + 1, right)
    
    # Return the minimum of the two halves
    return min(min_left, min_right)
