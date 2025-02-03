def merge(arr1: list[int], arr2: list[int]) -> list[int]:
    """
    Merges two sorted lists into a single sorted list.

    Args:
        arr1 (list[int]): First sorted list.
        arr2 (list[int]): Second sorted list.

    Returns:
        list[int]: A new sorted list containing all elements from arr1 and arr2.
    """
    merged_arr = []
    i, j = 0, 0

    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            merged_arr.append(arr1[i])
            i += 1
        else:
            merged_arr.append(arr2[j])
            j += 1

    # Append any remaining elements from arr1 or arr2
    merged_arr.extend(arr1[i:])
    merged_arr.extend(arr2[j:])

    return merged_arr


def merge_sort(original: list[int]) -> list[int]:
    """
    Implements the Merge Sort algorithm to sort a list in ascending order.

    Args:
        original (list[int]): The input list to be sorted.

    Returns:
        list[int]: A new sorted list in ascending order.
    """
    n = len(original)
    if n <= 1:
        return original.copy()

    mid = n // 2
    left = merge_sort(original[:mid])
    right = merge_sort(original[mid:])

    return merge(left, right)
