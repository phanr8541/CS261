# Name: Richard Phan
# OSU Email: phanri@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 2
# Due Date: 04/29/2024
# Description: Implementation of DynamicArray ADT


from static_array import StaticArray


class DynamicArrayException(Exception):
    """
    Custom exception class to be used by Dynamic Array
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._size = 0
        self._capacity = 4
        self._data = StaticArray(self._capacity)

        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        """
        Return content of dynamic array in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "DYN_ARR Size/Cap: "
        out += str(self._size) + "/" + str(self._capacity) + ' ['
        out += ', '.join([str(self._data[_]) for _ in range(self._size)])
        return out + ']'

    def __iter__(self):
        """
        Create iterator for loop
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        try:
            value = self[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value

    def get_at_index(self, index: int) -> object:
        """
        Return value from given index position
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        return self._data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        self._data[index] = value

    def __getitem__(self, index) -> object:
        """
        Same functionality as get_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        """
        Same functionality as set_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the capacity of the array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    def print_da_variables(self) -> None:
        """
        Print information contained in the dynamic array.
        Used for testing purposes.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        print(f"Length: {self._size}, Capacity: {self._capacity}, {self._data}")

    # -----------------------------------------------------------------------

    def resize(self, new_capacity: int) -> None:
        """
        Resize the dynamic array to the new capacity value
        """
        if new_capacity <= 0 or new_capacity < self._size:
            return

        # Create new array
        new_arr = StaticArray(new_capacity)

        # Copy the value from old array to new array
        for i in range(self._size):
            new_arr[i] = self._data[i]

        # Data is set to new array
        self._data = new_arr
        self._capacity = new_capacity

    def append(self, value: object) -> None:
        """
        Append a value at end of dynamic array
        If storage is already full, double its capacity before adding a new value
        """
        if self._size == self._capacity:
            self.resize(self._capacity * 2)
        self._data[self._size] = value
        self._size += 1

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Insert a value at given index in dynamic array
        If index is invalid, raise DynamicArrayException
        """
        # Check if index is valid
        if index < 0 or index > self._size:
            raise DynamicArrayException

        # Check if dynamic array is full capacity
        if self._size == self._capacity:
            self.resize(self._capacity * 2)

        # Shift elements for new value
        for i in range(self._size - 1, index - 1, - 1):
            self._data[i + 1] = self._data[i]

        # Insert new value at specified index
        self._data[index] = value
        self._size += 1

    def remove_at_index(self, index: int) -> None:
        """
        Removes value at given index in dynamic array
        If index is invalid, raise DynamicArrayException
        """
        # Check if index is valid
        if index < 0 or index >= self._size:
            raise DynamicArrayException

        # Resize self.capacity based on the size of array
        if self._size == 1 and self._capacity == 8:
            self.resize(8)
        elif self._size < (self._capacity / 4) and self._size * 2 >= 10:
            self.resize(self._size * 2)
        elif self._size < (self._capacity / 4) and self._size * 2 < 10:
            self.resize(10)

        # Remove element at specified index
        if index == self._size - 1:
            self._data[index] = 0
            self._size -= 1
            return
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]
        self._data[self._size - 1] = 0
        self._size -= 1

    def slice(self, start_index: int, size: int) -> "DynamicArray":
        """
        Returns new DynamicArray with values sliced from original array
        If start index is invalid or not enough elements in array, raise DynamicArrayException
        """
        # Handle invalid input of elements
        if size < 0 or size + start_index > self._size:
            raise DynamicArrayException

        if start_index < 0 or start_index > self._size - 1:
            raise DynamicArrayException

        # Return new dynamic array
        new_arr = DynamicArray()
        i = start_index
        while i <= start_index + size - 1:
            new_arr.append(self._data[i])
            i += 1
        return new_arr

    def map(self, map_func) -> "DynamicArray":
        """
        Return new dynamic array where each element has applied given map_func to values of original array
        """
        new_arr = DynamicArray()
        for i in range(self._size):
            new_arr.append(map_func(self._data[i]))
        return new_arr

    def filter(self, filter_func) -> "DynamicArray":
        """
        Return new dynamic array populated only with elements from original array for which filter_func
        returns True
        """
        new_arr = DynamicArray()
        for i in range(self._size):
            if filter_func(self._data[i]):
                new_arr.append(self._data[i])
        return new_arr


    def reduce(self, reduce_func, initializer=None) -> object:
        """
        Sequentially applies reduce_func to all elements of dynamic array
        Returns the resulting value
        If optional initializer parameter is not provided, first value in array is used as initializer
        If dynamic array is empty, returns value of initializer (or None if one was not provided)
        """
        # Check if input array is empty
        if self._size == 0:
            return initializer

        # Create new array to reduce and copy to new array
        new_arr = DynamicArray()
        for i in range(self._size):
            new_arr.append(self._data[i])

        # Handle initializer and apply reduce to first element
        if initializer is not None:
            first_val = new_arr[0]
            new_arr[0] = reduce_func(initializer, first_val)

        # Reduce function is applied to each pair of elements
        for num in range(new_arr._size - 1):
            new_arr[num + 1] = reduce_func(new_arr[num], new_arr[num + 1])
        return new_arr[self._size - 1]

def chunk(arr: DynamicArray) -> "DynamicArray":
    """
    Receives values of DynamicArray and "chunks" it into an array of arrays
    Returns DynamicArray with each index of array consisting of DynamicArray containing one of subsequences
    """
    # Check if input array is empty
    if arr.is_empty():
        return DynamicArray()

    # Set up to store the value of element in the array
    result = DynamicArray()
    curr_chunk = DynamicArray()
    prev_value = arr.get_at_index(0)
    curr_chunk.append(prev_value)

    # Iterate through array and store value to current
    for i in range(1, arr.length()):
        curr_value = arr.get_at_index(i)

        # Handles how the chunk is broken up by comparing values
        if curr_value >= prev_value:
            curr_chunk.append(curr_value)
        else:
            result.append(curr_chunk)
            curr_chunk = DynamicArray()
            curr_chunk.append(curr_value)
        prev_value = curr_value

    result.append(curr_chunk)
    return result


def find_mode(arr: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Get a dynamic array with highest occurring values and frequencies populated
    """
    frequency = 0
    start_val = 0
    end_val = 0
    result_val = 0

    # Create result array
    result = DynamicArray()

    # Return value for single element in array
    if arr.length() == 1:
        return arr, arr.length()

    while end_val < arr.length():
        if result.length() >= 1:
            result_val = result[result.length() - 1]

        # Check for additional value with same mode
        if arr[start_val] == arr[end_val] and end_val - start_val + 1 == frequency:
            # Make sure to not add the same value
            if result.length() > 0 and result_val != arr[end_val]:
                result.append(arr[start_val])
        # Find a new mode
        elif arr[start_val] == arr[end_val] and end_val - start_val + 1 > frequency:
            # Make sure to not add the same value
            if result.length() == 1 and arr[end_val] == result_val:
                frequency += 1
            else:
                result = DynamicArray()
                result.append(arr[end_val])
                frequency += 1

        # Return mode and frequency if at end of array
        if end_val == arr.length() - 1:
            return result, frequency

        # Check if we are at the end of the array
        if arr[end_val + 1] != arr[start_val] and end_val + 1 <= arr.length() - 1:
            start_val = end_val + 1

        # Increase end index
        end_val += 1

    return result, frequency


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# resize - example 1")
    da = DynamicArray()

    # print dynamic array's size, capacity and the contents
    # of the underlying static array (data)
    da.print_da_variables()
    da.resize(8)
    da.print_da_variables()
    da.resize(2)
    da.print_da_variables()
    da.resize(0)
    da.print_da_variables()

    print("\n# resize - example 2")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8])
    print(da)
    da.resize(20)
    print(da)
    da.resize(4)
    print(da)

    print("\n# append - example 1")
    da = DynamicArray()
    da.print_da_variables()
    da.append(1)
    da.print_da_variables()
    print(da)

    print("\n# append - example 2")
    da = DynamicArray()
    for i in range(9):
        da.append(i + 101)
        print(da)

    print("\n# append - example 3")
    da = DynamicArray()
    for i in range(600):
        da.append(i)
    print(da.length())
    print(da.get_capacity())

    print("\n# insert_at_index - example 1")
    da = DynamicArray([100])
    print(da)
    da.insert_at_index(0, 200)
    da.insert_at_index(0, 300)
    da.insert_at_index(0, 400)
    print(da)
    da.insert_at_index(3, 500)
    print(da)
    da.insert_at_index(1, 600)
    print(da)

    print("\n# insert_at_index example 2")
    da = DynamicArray()
    try:
        da.insert_at_index(-1, 100)
    except Exception as e:
        print("Exception raised:", type(e))
    da.insert_at_index(0, 200)
    try:
        da.insert_at_index(2, 300)
    except Exception as e:
        print("Exception raised:", type(e))
    print(da)

    print("\n# insert at index example 3")
    da = DynamicArray()
    for i in range(1, 10):
        index, value = i - 4, i * 10
        try:
            da.insert_at_index(index, value)
        except Exception as e:
            print("Cannot insert value", value, "at index", index)
    print(da)

    print("\n# remove_at_index - example 1")
    da = DynamicArray([10, 20, 30, 40, 50, 60, 70, 80])
    print(da)
    da.remove_at_index(0)
    print(da)
    da.remove_at_index(6)
    print(da)
    da.remove_at_index(2)
    print(da)

    print("\n# remove_at_index - example 2")
    da = DynamicArray([1024])
    print(da)
    for i in range(17):
        da.insert_at_index(i, i)
    print(da.length(), da.get_capacity())
    for i in range(16, -1, -1):
        da.remove_at_index(0)
    print(da)

    print("\n# remove_at_index - example 3")
    da = DynamicArray()
    print(da.length(), da.get_capacity())
    [da.append(1) for i in range(100)]  # step 1 - add 100 elements
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(68)]  # step 2 - remove 68 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 3 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 4 - remove 1 element
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(14)]  # step 5 - remove 14 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 6 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 7 - remove 1 element
    print(da.length(), da.get_capacity())

    for i in range(14):
        print("Before remove_at_index(): ", da.length(), da.get_capacity(), end="")
        da.remove_at_index(0)
        print(" After remove_at_index(): ", da.length(), da.get_capacity())

    print("\n# remove at index - example 4")
    da = DynamicArray([1, 2, 3, 4, 5])
    print(da)
    for _ in range(5):
        da.remove_at_index(0)
        print(da)

    print("\n# slice example 1")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8, 9])
    da_slice = da.slice(1, 3)
    print(da, da_slice, sep="\n")
    da_slice.remove_at_index(0)
    print(da, da_slice, sep="\n")

    print("\n# slice example 2")
    da = DynamicArray([10, 11, 12, 13, 14, 15, 16])
    print("SOURCE:", da)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1), (6, -1)]
    for i, cnt in slices:
        print("Slice", i, "/", cnt, end="")
        try:
            print(" --- OK: ", da.slice(i, cnt))
        except:
            print(" --- exception occurred.")

    print("\n# map example 1")
    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    print(da.map(lambda x: x ** 2))

    print("\n# map example 2")


    def double(value):
        return value * 2


    def square(value):
        return value ** 2


    def cube(value):
        return value ** 3


    def plus_one(value):
        return value + 1


    da = DynamicArray([plus_one, double, square, cube])
    for value in [1, 10, 20]:
        print(da.map(lambda x: x(value)))

    print("\n# filter example 1")


    def filter_a(e):
        return e > 10


    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    result = da.filter(filter_a)
    print(result)
    print(da.filter(lambda x: (10 <= x <= 20)))

    print("\n# filter example 2")


    def is_long_word(word, length):
        return len(word) > length


    da = DynamicArray("This is a sentence with some long words".split())
    print(da)
    for length in [3, 4, 7]:
        print(da.filter(lambda word: is_long_word(word, length)))

    print("\n# reduce example 1")
    values = [100, 5, 10, 15, 20, 25]
    da = DynamicArray(values)
    print(da)
    print(da.reduce(lambda x, y: (x // 5 + y ** 2)))
    print(da.reduce(lambda x, y: (x + y ** 2), -1))

    print("\n# reduce example 2")
    da = DynamicArray([100])
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))
    da.remove_at_index(0)
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))

    def print_chunked_da(arr: DynamicArray):
        if len(str(arr)) <= 100:
            print(arr)
        else:
            print(f"DYN_ARR Size/Cap: {arr.length()}/{arr.get_capacity()}")
            print('[\n' + ',\n'.join(f'\t{chunk}' for chunk in arr) + '\n]')

    print("\n# chunk example 1")
    test_cases = [
        [10, 20, 30, 30, 5, 10, 1, 2, 3, 4],
        ['App', 'Async', 'Cloud', 'Data', 'Deploy',
         'C', 'Java', 'Python', 'Git', 'GitHub',
         'Class', 'Method', 'Heap']
    ]

    for case in test_cases:
        da = DynamicArray(case)
        chunked_da = chunk(da)
        print(da)
        print_chunked_da(chunked_da)

    print("\n# chunk example 2")
    test_cases = [[], [261], [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]]

    for case in test_cases:
        da = DynamicArray(case)
        chunked_da = chunk(da)
        print(da)
        print_chunked_da(chunked_da)

    print("\n# find_mode - example 1")
    test_cases = (
        [1, 1, 2, 3, 3, 4],
        [1, 2, 3, 4, 5],
        ["Apple", "Banana", "Banana", "Carrot", "Carrot",
         "Date", "Date", "Date", "Eggplant", "Eggplant", "Eggplant",
         "Fig", "Fig", "Grape"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}\n")

    case = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    da = DynamicArray()
    for x in range(len(case)):
        da.append(case[x])
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}")
