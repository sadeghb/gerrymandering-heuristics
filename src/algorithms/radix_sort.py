def counting_sort_for_radix(arr: list[int], exp: int) -> list[int]:
    """
    A counting sort helper function for radix sort to sort based on the digit at a specific exponent.

    Args:
        arr (list[int]): The input list to be sorted.
        exp (int): The current digit's place value to sort by.

    Returns:
        list[int]: The sorted list based on the current digit.
    """
    n = len(arr)
    output = [0] * n  # Output array to store sorted elements
    count = [0] * 10  # Count array for digits (0-9)

    # Count occurrences of each digit at the current exponent
    for i in range(n):
        index = abs(arr[i]) // exp % 10
        count[index] += 1

    # Update count array to store the cumulative count
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Build the output array by placing elements in the correct position
    for i in range(n - 1, -1, -1):
        index = abs(arr[i]) // exp % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1

    return output


def radix_sort(original: list[int]) -> list[int]:
    """
    Implements the Radix Sort algorithm to sort a list in ascending order, supporting negative numbers.

    Args:
        original (list[int]): The input list to be sorted.

    Returns:
        list[int]: A new sorted list in ascending order.
    """
    if not original:
        return []

    # Separate positive and negative numbers
    positive = [num for num in original if num >= 0]
    negative = [-num for num in original if num < 0]

    # Sort positive and negative parts separately
    max_positive = max(positive) if positive else 0
    max_negative = max(negative) if negative else 0

    exp = 1
    while max_positive // exp > 0:
        positive = counting_sort_for_radix(positive, exp)
        exp *= 10

    exp = 1
    while max_negative // exp > 0:
        negative = counting_sort_for_radix(negative, exp)
        exp *= 10

    # Combine sorted negative and positive parts
    return [-num for num in reversed(negative)] + positive
