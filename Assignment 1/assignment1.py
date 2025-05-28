# Name: Richard Phan
# OSU Email: phanri@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 1
# Due Date: 04/22/24
# Description: 10 problems for Python Fundamentals review to test our familiarity with basic Python syntax constructs


import random
from static_array import *


# ------------------- PROBLEM 1 - MIN_MAX -----------------------------------

def min_max(arr: StaticArray) -> tuple[int, int]:
    """
    Write a function that receives a one-dimensional array of integers and returns a Python tuple with
    two values being the minimum and maximum values of the array
    """
    min = arr.get(0)
    max = arr.get(0)
    for i in range(arr.length()):
        if arr.get(i) < min:
            min = arr.get(i)
        elif arr.get(i) > max:
            max = arr.get(i)
    return (min, max)

# ------------------- PROBLEM 2 - FIZZ_BUZZ ---------------------------------

def fizz_buzz(arr: StaticArray) -> StaticArray:
    """
    Write a function that receives a StaticArray of integers and returns a new StaticArray object with
    the content modified as follows
    If number is divisible by 3, element in new array is fizz
    If number is divisible by 5, element in new array is buzz
    if number is multiple of 3 and 5, element in new array is fizzbuzz
    """
    new_arr = StaticArray(arr.length())
    for i in range(arr.length()):
        if arr.get(i) % 3 == 0 and arr.get(i) % 5 == 0:
            new_arr.set(i, "fizzbuzz")
        elif arr.get(i) % 3 == 0:
            new_arr.set(i, "fizz")
        elif arr.get(i) % 5 == 0:
            new_arr.set(i, "buzz")
        else:
            new_arr.set(i, arr.get(i))
    return new_arr

# ------------------- PROBLEM 3 - REVERSE -----------------------------------

def reverse(arr: StaticArray) -> None:
    """
    Reverse the order of element in the given StaticArray in place.
    """
    for i in range(arr.length()//2):
        temp = arr.get(i)
        arr.set(i, arr.get(arr.length() - 1 - i))
        arr.set(arr.length() - 1 - i, temp)

# ------------------- PROBLEM 4 - ROTATE ------------------------------------

def rotate(arr: StaticArray, steps: int) -> StaticArray:
    """
    Write a function that receives two parameters being StaticArray and an integer value steps
    Create a new StaticArray containing original elements shifted left or right by steps
    If steps is positive rotate right, left if negative
    """
    new_arr = StaticArray(arr.length())
    for i in range(arr.length()):
        new_index = (i + steps) % arr.length()
        new_arr.set(new_index, arr.get(i))
    return new_arr

# ------------------- PROBLEM 5 - SA_RANGE ----------------------------------

def sa_range(start: int, end: int) -> StaticArray:
    """
    Write a function that receives two integers start and end and returns StaticArray that
    contains all consecutive integers between start and end (inclusive)
    """
    arr = StaticArray(abs(end - start) + 1)
    for i in range(arr.length()):
        arr[i] = start + i if start < end else start - i
    return arr

# ------------------- PROBLEM 6 - IS_SORTED ---------------------------------

def is_sorted(arr: StaticArray) -> int:
    """
    Write a function that receives StaticArray and returns an integer that describes
    if array is sorted: 1 if ascending, -1 if descending, and 0 otherwise
    """
    ascending = True
    descending = True
    for i in range(1, arr.length()):
        if arr.get(i) < arr.get(i - 1):
            ascending = False
        if arr.get(i) > arr.get(i - 1):
            descending = False
        if arr.get(i) == arr.get(i - 1):
            ascending = False
            descending = False
    if ascending:
        return 1
    elif descending:
        return -1
    else:
        return 0

# ------------------- PROBLEM 7 - FIND_MODE -----------------------------------

def find_mode(arr: StaticArray) -> tuple[object, int]:
    """
    Write a function that receives StaticArray sorted in either non-descending or non-ascending order
    Returns mode (most-occurring) of array and its frequency (times it appears)
    """
    max_count = 1
    current_count = 1
    mode = arr.get(0)
    for i in range(1, arr.length()):
        if arr.get(i) == arr.get(i - 1):
            current_count += 1
            if current_count > max_count:
                max_count = current_count
                mode = arr.get(i)
        else:
            current_count = 1
    return (mode, max_count)

# ------------------- PROBLEM 8 - REMOVE_DUPLICATES -------------------------

def remove_duplicates(arr: StaticArray) -> StaticArray:
    """
    Write a function the receives StaticArray already sorted, non-descending or non-ascending
    Returns new StaticArray with all duplicate values removed
    """
    if arr.length() <= 1:
        # If the array has only one element or is empty, duplicates are not possible
        return arr

        # Count the number of unique elements
    unique_count = 1
    for i in range(1, arr.length()):
        if arr.get(i) != arr.get(i - 1):
            unique_count += 1

    # Create a new StaticArray to store the unique elements
    unique_arr = StaticArray(unique_count)

    # Copy the unique elements to the new array
    unique_arr.set(0, arr.get(0))
    j = 1
    for i in range(1, arr.length()):
        if arr.get(i) != arr.get(i - 1):
            unique_arr.set(j, arr.get(i))
            j += 1

    return unique_arr

# ------------------- PROBLEM 9 - COUNT_SORT --------------------------------

def count_sort(arr: StaticArray) -> StaticArray:
    """
    Write a function that receives StaticArray and returns new StaticArray with same content sorted
    in non-ascending order using count sort algorithm
    """
    max = -int(10 ** 100)
    min = int(10 ** 100)
    for i in range(arr.length()):
        if max < arr.get(i):
            max = arr.get(i)
        if min > arr.get(i):
            min = arr.get(i)
    # offset the max value to accommodate for negative values
    max = max - min
    max += 1
    # Initialize count array of size (maximum of element +=1)
    count = StaticArray(max)
    # Initialize count array with zeros
    for i in range(max):
        count[i] = 0
    # Store the find the total count of each unique element and
    # store the count at corresponding index in count array
    for i in range(arr.length()):
        value = count.get(arr.get(i) - min)
        count.set(arr.get(i) - min, value + 1)
    # find the cumulative sum of count array and store it in count array itself
    for i in range(1, max):
        count.set(i, count.get(i) + count.get(i - 1))
    # Initialize the output
    output = StaticArray(arr.length())
    # Find the index of each element of the original array in count array
    # place the elements in output array
    i = arr.length() - 1
    while i >= 0:
        # If you want in ascending order use store arr[i] in index if you want in descending store it in arr.size()-index-1
        index = count.get(arr.get(i) - min) - 1
        output.set(arr.length() - index - 1, arr.get(i))
        #  decrease count of each element restored by 1
        count.set(arr.get(i) - min, count.get(arr.get(i) - min) - 1)
        i -= 1
    # return the output static  array
    return output

# ------------------- PROBLEM 10 - SORTED SQUARES ---------------------------

def sorted_squares(arr: StaticArray) -> StaticArray:
    """
    Write a function that receives StaticArray where elements are in sorted order, and returns
    a new StaticArray with squares of values from original array in non-descending order, original
    array must not be modified
    """
    squares = StaticArray(arr.length())
    l, r = 0, arr.length() - 1
    for i in range(arr.length() - 1, -1, -1):
        if abs(arr.get(l)) > abs(arr.get(r)):
            squares.set(i, arr.get(l) ** 2)
            l += 1
        else:
            squares.set(i, arr.get(r) ** 2)
            r -= 1
    return squares


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print('\n# min_max example 1')
    arr = StaticArray(5)
    for i, value in enumerate([7, 8, 6, -5, 4]):
        arr[i] = value
    print(arr)
    result = min_max(arr)
    if result:
        print(f"Min: {result[0]: 3}, Max: {result[1]}")
    else:
        print("min_max() not yet implemented")

    print('\n# min_max example 2')
    arr = StaticArray(1)
    arr[0] = 100
    print(arr)
    result = min_max(arr)
    if result:
        print(f"Min: {result[0]}, Max: {result[1]}")
    else:
        print("min_max() not yet implemented")

    print('\n# min_max example 3')
    test_cases = (
        [3, 3, 3],
        [-10, -30, -5, 0, -10],
        [25, 50, 0, 10],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print(arr)
        result = min_max(arr)
        if result:
            print(f"Min: {result[0]: 3}, Max: {result[1]}")
        else:
            print("min_max() not yet implemented")

    print('\n# fizz_buzz example 1')
    source = [_ for _ in range(-5, 20, 4)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr[i] = value
    print(fizz_buzz(arr))
    print(arr)

    print('\n# reverse example 1')
    source = [_ for _ in range(-20, 20, 7)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr.set(i, value)
    print(arr)
    reverse(arr)
    print(arr)
    reverse(arr)
    print(arr)

    print('\n# rotate example 1')
    source = [_ for _ in range(-20, 20, 7)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr.set(i, value)
    print(arr)
    for steps in [1, 2, 0, -1, -2, 28, -100, 2 ** 28, -2 ** 31]:
        space = " " if steps >= 0 else ""
        print(f"{rotate(arr, steps)} {space}{steps}")
    print(arr)

    print('\n# rotate example 2')
    array_size = 1_000_000
    source = [random.randint(-10 ** 9, 10 ** 9) for _ in range(array_size)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr[i] = value
    print(f'Started rotating large array of {array_size} elements')
    rotate(arr, 3 ** 14)
    rotate(arr, -3 ** 15)
    print(f'Finished rotating large array of {array_size} elements')

    print('\n# sa_range example 1')
    cases = [
        (1, 3), (-1, 2), (0, 0), (0, -3),
        (-95, -89), (-89, -95)]
    for start, end in cases:
        print(f"Start: {start: 4}, End: {end: 4}, {sa_range(start, end)}")

    print('\n# is_sorted example 1')
    test_cases = (
        [-100, -8, 0, 2, 3, 10, 20, 100],
        ['A', 'B', 'Z', 'a', 'z'],
        ['Z', 'T', 'K', 'A', '5'],
        [1, 3, -10, 20, -30, 0],
        [-10, 0, 0, 10, 20, 30],
        [100, 90, 0, -90, -200],
        ['apple']
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        result = is_sorted(arr)
        space = "  " if result and result >= 0 else " "
        print(f"Result:{space}{result}, {arr}")

    print('\n# find_mode example 1')
    test_cases = (
        [1, 20, 30, 40, 500, 500, 500],
        [2, 2, 2, 2, 1, 1, 1, 1],
        ["zebra", "sloth", "otter", "otter", "moose", "koala"],
        ["Albania", "Belgium", "Chile", "Denmark", "Egypt", "Fiji"]
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value

        result = find_mode(arr)
        if result:
            print(f"{arr}\nMode: {result[0]}, Frequency: {result[1]}\n")
        else:
            print("find_mode() not yet implemented\n")

    print('# remove_duplicates example 1')
    test_cases = (
        [1], [1, 2], [1, 1, 2], [1, 20, 30, 40, 500, 500, 500],
        [5, 5, 5, 4, 4, 3, 2, 1, 1], [1, 1, 1, 1, 2, 2, 2, 2]
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print(arr)
        print(remove_duplicates(arr))
    print(arr)

    print('\n# count_sort example 1')
    test_cases = (
        [1, 2, 4, 3, 5], [5, 4, 3, 2, 1], [0, -5, -3, -4, -2, -1, 0],
        [-3, -2, -1, 0, 1, 2, 3], [1, 2, 3, 4, 3, 2, 1, 5, 5, 2, 3, 1],
        [10100, 10721, 10320, 10998], [-100320, -100450, -100999, -100001],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print(f"Before: {arr}")
        result = count_sort(arr)
        print(f"After : {result}")

    print('\n# count_sort example 2')
    array_size = 5_000_000
    min_val = random.randint(-1_000_000_000, 1_000_000_000 - 998)
    max_val = min_val + 998
    case = [random.randint(min_val, max_val) for _ in range(array_size)]
    arr = StaticArray(len(case))
    for i, value in enumerate(case):
        arr[i] = value
    print(f'Started sorting large array of {array_size} elements')
    result = count_sort(arr)
    print(f'Finished sorting large array of {array_size} elements')

    print('\n# sorted_squares example 1')
    test_cases = (
        [1, 2, 3, 4, 5],
        [-5, -4, -3, -2, -1, 0],
        [-3, -2, -2, 0, 1, 2, 3],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(sorted(case)):
            arr[i] = value
        print(arr)
        result = sorted_squares(arr)
        print(result)

    print('\n# sorted_squares example 2')
    array_size = 5_000_000
    case = [random.randint(-10 ** 9, 10 ** 9) for _ in range(array_size)]
    arr = StaticArray(len(case))
    for i, value in enumerate(sorted(case)):
        arr[i] = value
    print(f'Started sorting large array of {array_size} elements')
    result = sorted_squares(arr)
    print(f'Finished sorting large array of {array_size} elements')
