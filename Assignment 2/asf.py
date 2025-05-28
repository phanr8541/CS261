def remove_at_index(self, index: int) -> None:
    """
    Removes value at given index in dynamic array
    If index is invalid, raise DynamicArrayException
    """
    # Check if index is valid
    if index < 0 or index >= self._size:
        raise DynamicArrayException

    # Handle case where self.capacity requires resize
    if self._size == 1 and self._capacity == 8:
        self.resize(8)
    elif self._size < (self._capacity / 4) and self._size * 2 >= 10:
        self.resize(self._size * 2)
    elif self._size < (self._capacity / 4) and self._size * 2 < 10:
        self.resize(10)

    # Remove element at specified index
    for i in range(index, self._size - 1, 1):
        self._data[i] = self._data[i + 1]
    self._data[self._size - 1] = None
    self._size -= 1