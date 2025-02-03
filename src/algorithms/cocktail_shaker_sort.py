def cocktail_shaker_sort(original: list[int]) -> list[int]:
    """
    Implements the Cocktail Shaker Sort algorithm to sort a list in ascending order.

    Args:
        original (list[int]): The input list to be sorted.

    Returns:
        list[int]: A new sorted list in ascending order.
    """
    n = len(original)
    if n <= 1:
        return original.copy()

    solution = original.copy()
    swapped = True
    start = 0
    end = n - 1

    while swapped:
        swapped = False

        # Forward pass
        for i in range(start, end):
            if solution[i] > solution[i + 1]:
                solution[i], solution[i + 1] = solution[i + 1], solution[i]
                swapped = True

        if not swapped:
            break

        swapped = False
        end -= 1

        # Backward pass
        for i in range(end - 1, start - 1, -1):
            if solution[i] > solution[i + 1]:
                solution[i], solution[i + 1] = solution[i + 1], solution[i]
                swapped = True

        start += 1

    return solution
