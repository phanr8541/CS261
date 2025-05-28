# Name: Richard Phan
# OSU Email: phanri@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 5
# Due Date: 05/28/2024
# Description: Implementation of MinHeap


from dynamic_array import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initialize a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._heap = DynamicArray()

        # populate MinHeap with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MinHeap content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        heap_data = [self._heap[i] for i in range(self._heap.length())]
        return "HEAP " + str(heap_data)

    def add(self, node: object) -> None:
        """
        Add new node to heap while maintaining property
        Amortized O(log N) runtime complexity
        """
        # Append node to end of heap & calculation of node parent
        self._heap.append(node)
        insert_index = self._heap.length() - 1
        parent_index = (insert_index - 1) // 2

        # Percolate node up heap
        while insert_index > 0 and self._heap[insert_index] < self._heap[parent_index]:
            # Swap with parent node
            curr = self._heap[insert_index]
            self._heap[insert_index] = self._heap[parent_index]
            self._heap[parent_index] = curr
            # Update to parent index
            insert_index = parent_index
            parent_index = (insert_index - 1) // 2

    def is_empty(self) -> bool:
        """
        Check if heap is empty
        O(1) runtime complexity
        """
        if self._heap.is_empty():
            return True
        else:
            return False

    def get_min(self) -> object:
        """
        Return min value of heap
        O(1) runtime complexity
        """
        # Check for empty heap
        if self.is_empty():
            raise MinHeapException

        # Return root of heap
        min_value = self._heap.get_at_index(0)
        return min_value

    def remove_min(self) -> object:
        """
        Remove min value from heap
        Amortized O(log N) runtime complexity
        """
        # Check for empty heap
        if self.size() == 0:
            raise MinHeapException

        # Get min value to be removed and decrement size of heap
        min_value = self.get_min()
        self._heap[0] = self._heap[self.size() - 1]
        self._heap._size -= 1

        # Return removed value maintaining heap property
        _percolate_down(self._heap, 0, self._heap.length())
        return min_value

    def build_heap(self, da: DynamicArray) -> None:
        """
        Builds MinHeap from given DynamicArray in any order
        Amortized O(N) runtime complexity
        """
        # Create heap from DynamicArray
        self._heap = DynamicArray(da)
        index = (self._heap.length() // 2) - 1
        # Iterate through each node & percolate down heap property
        while index >= 0:
            _percolate_down(self._heap, index, self._heap.length())
            index -= 1

    def size(self) -> int:
        """
        Return number of items stored in heap
        O(1) runtime complexity
        """
        return self._heap.length()

    def clear(self) -> None:
        """
        Clears contents of heap
        O(1) runtime complexity
        """
        self._heap = DynamicArray()


def heapsort(da: DynamicArray) -> None:
    """
    Sort the DynamicArray using Heapsort algorithm
    O(N log N) runtime complexity
    """
    # Receive DynamicArray for heap
    index = (da.length() // 2) - 1
    while index >= 0:
        _percolate_down(da, index, da.length())
        index -= 1

    # Sort by taking max element from heap
    last_index = da.length() - 1
    while last_index >= 0:
        # Swap max element with last element
        curr = da[last_index]
        da[last_index] = da[0]
        da[0] = curr
        _percolate_down(da, 0, last_index)
        last_index -= 1


def _percolate_down(da: DynamicArray, parent: int, length: int) -> None:
    """
    Helper function to percolate down heap
    """
    while True:
        left_child = (2 * parent) + 1
        right_child = (2 * parent) + 2
        small = parent

        # Check if left child is smaller than parent
        if left_child < length and da[left_child] < da[small]:
            small = left_child

        # Check if right child is smaller than the smallest found so far
        if right_child < length and da[right_child] < da[small]:
            small = right_child

        # If the smallest element is not the parent, swap and continue percolating down
        if small != parent:
            da[small], da[parent] = da[parent], da[small]
            parent = small
        else:
            break


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - add example 1")
    print("-------------------")
    h = MinHeap()
    print(h, h.is_empty())
    for value in range(300, 200, -15):
        h.add(value)
        print(h)

    print("\nPDF - add example 2")
    print("-------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
        h.add(value)
        print(h)

    print("\nPDF - is_empty example 1")
    print("-------------------")
    h = MinHeap([2, 4, 12, 56, 8, 34, 67])
    print(h.is_empty())

    print("\nPDF - is_empty example 2")
    print("-------------------")
    h = MinHeap()
    print(h.is_empty())

    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), h.get_min())

    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    while not h.is_empty() and h.is_empty() is not None:
        print(h, end=' ')
        print(h.remove_min())

    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    h = MinHeap(['zebra', 'apple'])
    print(h)
    h.build_heap(da)
    print(h)

    print("--------------------------")
    print("Inserting 500 into input DA:")
    da[0] = 500
    print(da)

    print("Your MinHeap:")
    print(h)
    if h.get_min() == 500:
        print("Error: input array and heap's underlying DA reference same object in memory")

    print("\nPDF - size example 1")
    print("--------------------")
    h = MinHeap([100, 20, 6, 200, 90, 150, 300])
    print(h.size())

    print("\nPDF - size example 2")
    print("--------------------")
    h = MinHeap([])
    print(h.size())

    print("\nPDF - clear example 1")
    print("---------------------")
    h = MinHeap(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(h)
    print(h.clear())
    print(h)

    print("\nPDF - heapsort example 1")
    print("------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - heapsort example 2")
    print("------------------------")
    da = DynamicArray(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")
