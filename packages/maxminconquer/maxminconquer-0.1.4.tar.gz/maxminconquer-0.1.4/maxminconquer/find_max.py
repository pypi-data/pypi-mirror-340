# maxminconquer/find_max.py

def find_max(arr, left, right):
    """Finds the maximum value in the array using Divide and Conquer."""
    # Base case: If there is only one element
    if left == right:
        return arr[left]
    
    # Find the middle index
    mid = (left + right) // 2
    
    # Recursively find the maximum in both halves
    max_left = find_max(arr, left, mid)
    max_right = find_max(arr, mid + 1, right)
    
    # Return the maximum of the two halves
    return max(max_left, max_right)
