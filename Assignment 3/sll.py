# Name: Richard Phan
# OSU Email: phanri@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 3
# Due Date: 05/06/2024
# Description: Implementation of Singly Linked List data structure


from SLNode import *


class SLLException(Exception):
    """
    Custom exception class to be used by Singly Linked List
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class LinkedList:
    def __init__(self, start_list=None) -> None:
        """
        Initialize new linked list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._head = SLNode(None)

        # populate SLL with initial values (if provided)
        # before using this feature, implement insert_back() method
        if start_list is not None:
            for value in start_list:
                self.insert_back(value)

    def __str__(self) -> str:
        """
        Return content of singly linked list in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'SLL ['
        node = self._head.next
        while node:
            out += str(node.value)
            if node.next:
                out += ' -> '
            node = node.next
        out += ']'
        return out

    def length(self) -> int:
        """
        Return the length of the linked list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        length = 0
        node = self._head.next
        while node:
            length += 1
            node = node.next
        return length

    def is_empty(self) -> bool:
        """
        Return True is list is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return not self._head.next

    # ------------------------------------------------------------------ #

    def insert_front(self, value: object) -> None:
        """
        Insert a new node at beginning of list after front sentinel
        O(1) runtime complexity
        """
        new_node = SLNode(value, self._head.next)
        self._head.next = new_node

    def insert_back(self, value: object) -> None:
        """
        Insert a new node at end of list
        O(N) runtime complexity
        """
        # Traverse list to find last node
        curr = self._head
        while curr.next:
            curr = curr.next
        curr.next = SLNode(value)

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Insert a new value at specified index
        O(N) runtime complexity
        """
        # Check for invalid inputs
        if index < 0 or index > self.length():
            raise SLLException

        # Keep track of index
        count = 0
        curr = self._head

        # Traverse list to find node at specified index
        while curr is not None:
            if count == index:
                new_node = SLNode(value, curr.next)
                curr.next = new_node
                return
            curr = curr.next
            count += 1


    def remove_at_index(self, index: int) -> None:
        """
        Removes node at specified index
        O(N) runtime complexity
        """
        # Check for invalid inputs
        if index < 0 or index >= self.length():
            raise SLLException

        # Keep track of index
        count = 0
        curr = self._head

        # Traverse list to find node before the one needs to be removed
        while curr is not None:
            if count == index:
                remove_node = curr.next
                curr.next = curr.next.next
                remove_node.next = None
                return
            curr = curr.next
            count += 1

    def remove(self, value: object) -> bool:
        """
        Remove a node that matches the provided value
        O(N) runtime complexity
        """
        curr = self._head
        while curr is not None:

            # Return if end of list
            if curr.next is None:
                return False

            # Remove if value is found
            if curr.next.value == value:
                remove_node = curr.next
                curr.next = remove_node.next
                remove_node.next = None
                return True
            curr = curr.next


    def count(self, value: object) -> int:
        """
        Return the count of elements that matches in the list
        O(N) runtime complexity
        """
        # Keep track of count
        count = 0
        curr = self._head
        while curr is not None:
            if curr.value == value:
                count += 1
            curr = curr.next
        return count

    def find(self, value: object) -> bool:
        """
        Check if a provided value appears in the list
        O(N) runtime complexity
        """
        curr = self._head
        while curr is not None:
            # Return True if value is found
            if curr.value == value:
                return True
            curr = curr.next
        return False

    def slice(self, start_index: int, size: int) -> "LinkedList":
        """
        Return Linkedlist of nodes that are sliced from list starting from start_index
        O(N) runtime complexity
        """
        # Check for invalid inputs
        if start_index < 0 or start_index >= self.length():
            raise SLLException
        if size < 0 or (size + start_index) > self.length():
            raise SLLException

        # Keep track of node
        position = 0
        curr = self._head
        new_list = LinkedList()

        while position < start_index:
            position += 1
            curr = curr.next

        position = 0
        new_curr = new_list._head

        while position < size:
            position += 1
            value = curr.next.value
            new_curr.next = SLNode(value)
            curr = curr.next
            new_curr = new_curr.next

        return new_list

if __name__ == "__main__":

    print("\n# insert_front example 1")
    test_case = ["A", "B", "C"]
    lst = LinkedList()
    for case in test_case:
        lst.insert_front(case)
        print(lst)

    print("\n# insert_back example 1")
    test_case = ["C", "B", "A"]
    lst = LinkedList()
    for case in test_case:
        lst.insert_back(case)
        print(lst)

    print("\n# insert_at_index example 1")
    lst = LinkedList()
    test_cases = [(0, "A"), (0, "B"), (1, "C"), (3, "D"), (-1, "E"), (5, "F")]
    for index, value in test_cases:
        print("Inserted", value, "at index", index, ": ", end="")
        try:
            lst.insert_at_index(index, value)
            print(lst)
        except Exception as e:
            print(type(e))

    print("\n# remove_at_index example 1")
    lst = LinkedList([1, 2, 3, 4, 5, 6])
    print(f"Initial LinkedList : {lst}")
    for index in [0, 2, 0, 2, 2, -2]:
        print("Removed at index", index, ": ", end="")
        try:
            lst.remove_at_index(index)
            print(lst)
        except Exception as e:
            print(type(e))

    print("\n# remove example 1")
    lst = LinkedList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(f"Initial LinkedList, Length: {lst.length()}\n  {lst}")
    for value in [7, 3, 3, 3, 3]:
        print(f"remove({value}): {lst.remove(value)}, Length: {lst.length()}"
              f"\n {lst}")

    print("\n# remove example 2")
    lst = LinkedList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(f"Initial LinkedList, Length: {lst.length()}\n  {lst}")
    for value in [1, 2, 3, 1, 2, 3, 3, 2, 1]:
        print(f"remove({value}): {lst.remove(value)}, Length: {lst.length()}"
              f"\n {lst}")

    print("\n# count example 1")
    lst = LinkedList([1, 2, 3, 1, 2, 2])
    print(lst, lst.count(1), lst.count(2), lst.count(3), lst.count(4))

    print("\n# find example 1")
    lst = LinkedList(["Waldo", "Clark Kent", "Homer", "Santa Claus"])
    print(lst)
    print(lst.find("Waldo"))
    print(lst.find("Superman"))
    print(lst.find("Santa Claus"))

    print("\n# slice example 1")
    lst = LinkedList([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ll_slice = lst.slice(1, 3)
    print("Source:", lst)
    print("Start: 1 Size: 3 :", ll_slice)
    ll_slice.remove_at_index(0)
    print("Removed at index 0 :", ll_slice)

    print("\n# slice example 2")
    lst = LinkedList([10, 11, 12, 13, 14, 15, 16])
    print("Source:", lst)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1)]
    for index, size in slices:
        print("Start:", index, "Size:", size, end="")
        try:
            print(" :", lst.slice(index, size))
        except:
            print(" : exception occurred.")
