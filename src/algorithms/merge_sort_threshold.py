from .merge_sort import merge
from .cocktail_shaker_sort import cocktail_shaker_sort

def merge_sort_threshold(original: list[int], threshold: int = 18) -> list[int]:
    """
    A hybrid sorting algorithm that uses Merge Sort until a threshold size is reached,
    at which point it switches to Cocktail Shaker Sort for smaller sublists.

    Args:
    - original (list[int]): The list to be sorted.
    - threshold (int): The threshold size for switching from Merge Sort to Cocktail Shaker Sort.

    Returns:
    - list[int]: The sorted list.
    """
    n = len(original)

    if n > threshold:
        # Perform merge sort for larger sublists
        mid = n // 2
        left_sorted = merge_sort_threshold(original[:mid], threshold)
        right_sorted = merge_sort_threshold(original[mid:], threshold)
        return merge(left_sorted, right_sorted)

    else:
        # Switch to cocktail shaker sort for smaller sublists
        return cocktail_shaker_sort(original)
