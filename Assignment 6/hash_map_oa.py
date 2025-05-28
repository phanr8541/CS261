# Name: Richard Phan
# OSU Email: phanri@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 06/06/2024
# Description: Implementation of open access hash map

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates key/value pair in hash map
        """
        # Handle resize based on load factor threshold
        if self._size / self._capacity >= 0.5:
            self.resize_table(self._capacity * 2)

        # Calculate hash & index for key
        hash = self._hash_function(key)
        index = hash % self._capacity
        new_entry = HashEntry(key, value)

        # Insert new entry if bucket at index is empty
        if not self._buckets[index]:
            self._buckets[index] = new_entry
            self._size += 1
        else:
            probe_index = index
            probe_count = 0
            # Find empty slot or update existing entry
            while self._buckets[probe_index]:
                if self._buckets[probe_index].key == key and not self._buckets[probe_index].is_tombstone:
                    self._buckets[probe_index] = new_entry
                    return
                elif self._buckets[probe_index].is_tombstone:
                    self._buckets[probe_index] = new_entry
                    self._size += 1
                    return
                # Calculate next index by quadratic probing
                probe_count += 1
                probe_index = (index + (probe_count ** 2)) % self._capacity

            # Insert new entry at specific index
            self._buckets[probe_index] = new_entry
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Change capacity and rehash values on new table
        """
        # Check if new capacity is valid
        if new_capacity < self._size:
            return

        # Check if new capacity is prime
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Initialize bucket arrays & update capacity
        curr = self._buckets
        self._capacity = new_capacity
        self._buckets = DynamicArray()
        self._size = 0

        # Set new bucket to None
        for i in range(self._capacity):
            self._buckets.append(None)

        # Rehash non-tombstone to new bucket
        for i in range(curr.length()):
            if curr[i] and not curr[i].is_tombstone:
                key, value = curr[i].key, curr[i].value
                self.put(key, value)

    def table_load(self) -> float:
        """
        Returns current hash table load factor
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Return count of empty buckets
        """
        return self._capacity - self._size

    def get(self, key: str) -> object:
        """
        Return value associated with given key
        """
        # Check if key is in hash map
        if not self.contains_key(key):
            return

        # Initialize index for key & variable for quadratic probe
        hash = self._hash_function(key)
        index = hash % self._capacity
        probe_index = index
        probe_count = 0

        # Find key by checking if bucket contains
        while self._buckets[probe_index]:
            if self._buckets[probe_index].key == key and not self._buckets[probe_index].is_tombstone:
                return self._buckets[probe_index].value
            else:
                # Calculate next index by quadratic probing
                probe_count += 1
                probe_index = (index + (probe_count ** 2)) % self._capacity

    def contains_key(self, key: str) -> bool:
        """
        Check if given key is in hash map
        """
        # Initialize index for key & variable for quadratic probe
        hash = self._hash_function(key)
        index = hash % self._capacity
        probe_index = index
        probe_count = 0

        # Find key by checking if bucket contains
        while self._buckets[probe_index]:
            if self._buckets[probe_index].key == key and not self._buckets[probe_index].is_tombstone:
                return True
            else:
                # Calculate next index by quadratic probing
                probe_count += 1
                probe_index = (index + (probe_count ** 2)) % self._capacity
        return False

    def remove(self, key: str) -> None:
        """
        Remove given key and value from hash map
        """
        # Check if key is in hash map
        if not self.contains_key(key):
            return

        # Initialize index for key & variable for quadratic probe
        hash = self._hash_function(key)
        index = hash % self._capacity
        probe_index = index
        probe_count = 0

        # Find key by checking if bucket contains
        while self._buckets[probe_index]:
            if self._buckets[probe_index].key == key and not self._buckets[probe_index].is_tombstone:
                # Indicate entry as tombstone to be removed
                self._buckets[probe_index].is_tombstone = True
                self._size -= 1
                return
            else:
                # Calculate next index by quadratic probing
                probe_count += 1
                probe_index = (index + (probe_count ** 2)) % self._capacity

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns DynamicArray containing key/value pairs
        """
        # Create new DynamicArray for key/value pairs
        new_array = DynamicArray()

        # Check all buckets if not None & not tombstone
        for i in range(self._buckets.length()):
            if self._buckets[i] and not self._buckets[i].is_tombstone:
                new_array.append((self._buckets[i].key, self._buckets[i].value))
        return new_array

    def clear(self) -> None:
        """
        Clear hash map
        """
        # Initialize to DynamicArray and set hash map size to 0
        self._buckets = DynamicArray()
        self._size = 0
        # Append none to new bucket array
        for i in range(self._capacity):
            self._buckets.append(None)


    def __iter__(self):
        """
        Enables hash map to iterate
        """
        self._index = 0

        return self

    def __next__(self):
        """
        Return next element for hash map iterator
        """
        # Find valid entry by current entry at index
        while self._index < self._capacity:
            curr = self._buckets[self._index]
            self._index += 1
            # Check if entry is valid
            if curr and not curr.is_tombstone:
                return curr
        raise StopIteration


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
