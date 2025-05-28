# Name: Richard Phan
# OSU Email: phanri@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 06/06/2024
# Description: Implementation of chaining hash map


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        if self.table_load() >= 1.0:
            new_capacity = self._capacity * 2
            self.resize_table(new_capacity)

        # Calculate hash and index for key
        hash = self._hash_function(key)
        index = hash % self._capacity
        bucket = self._buckets[index]

        # Check if key in bucket and update value
        if bucket.contains(key):
            bucket.contains(key).value = value
        # Insert new key/value pair
        else:
            bucket.insert(key, value)
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Change capacity and rehash values on new table
        """
        # Check if new capacity is valid
        if new_capacity < 1:
            return

        # Check if new capacity is prime
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Load factor remains below 1 from resizing
        while (self._size - 1) / new_capacity >= 1:
            new_capacity *= 2
            new_capacity = self._next_prime(new_capacity)

        curr = self._buckets
        self._capacity = new_capacity
        self._buckets = DynamicArray()

        # Initialize new bucket
        for i in range(self._capacity):
            self._buckets.append(LinkedList())

        # Rehash key/value pairs to new bucket
        for i in range(curr.length()):
            if curr[i].length() > 0:
                for node in curr[i]:
                    hash = self._hash_function(node.key)
                    index = hash % self._capacity
                    self._buckets[index].insert(node.key, node.value)

    def table_load(self) -> float:
        """
        Returns current hash table load factor
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Return count of empty buckets
        """
        # Initialize count at zero
        count = 0

        # Iterate through bucket and count empty buckets
        for i in range(self._capacity):
            if self._buckets[i].length() == 0:
                count += 1

        return count

    def get(self, key: str):
        """
        Return value associated with given key
        """
        # Check if key exist and calculate hash & index for key
        if self.contains_key(key):
            hash = self._hash_function(key)
            index = hash % self._capacity
            return self._buckets[index].contains(key).value

    def contains_key(self, key: str) -> bool:
        """
        Check if given key is in hash map
        """
        # Calculate hash & index for key
        hash = self._hash_function(key)
        index = hash % self._capacity

        # Check bucket for key at calculated index
        if self._buckets[index].contains(key):
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Remove given key and value from hash map
        """
        # Check if key exist and calculate hash & index for key
        if self.contains_key(key):
            hash = self._hash_function(key)
            index = hash % self._capacity
            # Remove key at calculated index
            self._buckets[index].remove(key)
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns DynamicArray containing key/value pairs
        """
        # Create new DynamicArray for key/value pairs
        new_array = DynamicArray()

        # Iterate bucket & check for elements
        for i in range(self._capacity):
            if self._buckets[i].length() > 0:
                # Iterate in current bucket and append key/value pairs
                for node in self._buckets[i]:
                    new_array.append((node.key, node.value))
        return new_array

    def clear(self) -> None:
        """
        Clear hash map
        """
        # Initialize to DynamicArray and set hash map size to 0
        self._buckets = DynamicArray()
        self._size = 0

        # Initialize new bucket
        for i in range(self._capacity):
            self._buckets.append(LinkedList())


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Return the mode and frequency values of a given dynamic array
    O(N) runtime complexity
    """
    # Initialize to store & count frequency
    map = HashMap()
    count = 0
    curr = DynamicArray()

    # Iterate through DynamicArray & update frequency count
    for i in range(da.length()):
        if map.contains_key(da[i]):
            val = map.get(da[i])
            map.put(da[i], val + 1)
        else:
            map.put(da[i], 1)

        # Update to higher frequency count
        if map.get(da[i]) > count:
            count = map.get(da[i])

    # Get key/value pairs from hash map
    key_vals = map.get_keys_and_values()

    # Iterate pairs to find mode & append to mode array
    for i in range(key_vals.length()):
        if key_vals[i][1] == count:
            curr.append(key_vals[i][0])
    return curr, count


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
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
