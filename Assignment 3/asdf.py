class DLNode:
    """
    Doubly Linked List Node class
    """

    def __init__(self, value: object) -> None:
        self.next = None
        self.prev = None
        self.value = value

class DoublyList:
    def __init__(self, start_list=None):
        """
        Initializes a new linked list with two sentinels
        """
        self.frontsentinel = DLNode(None)
        self.backsentinel = DLNode(None)
        self.frontsentinel.prev = None
        self.frontsentinel.next = self.backsentinel
        self.backsentinel.prev = self.frontsentinel
        self.backsentinel.next = None
        self.size= 0

    def get_at_index(self, index: int) -> object:
        """Get object at given index"""
        if index < 0 or index >= self.size:
            raise DLLException

        curVal = self.frontsentinel.next
        indexCount = 0
        # iterate through while loop until index value is reached
        while indexCount != index:
            curVal = curVal.next
            indexCount += 1

        # return value in question
        return curVal.value