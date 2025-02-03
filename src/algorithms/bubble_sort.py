def bubble_sort(original: list[int]) -> list[int]:
    """
    Implements the Bubble Sort algorithm to sort a list in ascending order.

    Args:
        original (list[int]): The input list to be sorted.

    Returns:
        list[int]: A new sorted list in ascending order.
    """
    n = len(original)
    if n <= 1:  # Early exit for lists with 0 or 1 elements
        return original.copy()

    # Create a copy to avoid modifying the input list
    solution = original.copy()

    # Perform the bubble sort
    for i in range(n-1):
        done = True  # Assume no swaps are needed

        # Iterate through the unsorted portion of the list
        for j in range(n-i-1):
            if solution[j] > solution[j + 1]:
                # Swap adjacent elements if they are in the wrong order
                solution[j], solution[j + 1] = solution[j + 1], solution[j]
                done = False  # A swap was made, so sorting isn't finished

        if done:  # Exit early if no swaps were made
            return solution

    return solution
