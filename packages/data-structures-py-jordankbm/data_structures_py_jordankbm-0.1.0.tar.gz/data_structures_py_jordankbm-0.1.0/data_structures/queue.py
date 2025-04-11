from .linked_lists import LinkedList

class Queue:
    """N is the max size of our queue"""
    N = 20

    def __init__(self, para=None):  # Initialize with an optional LinkedList
        if para is None:
            self.queue = LinkedList()  # Create an empty LinkedList if not provided
        else:
            self.queue = para  # Use the provided LinkedList
        self.size = self.queue.get_length()  # Initialize size

    def enqueue(self, new):
        if not self.isFull():
            self.queue.InsertAtEnd(new)  # Use InsertAtEnd for LinkedList
            self.size += 1  # Update size
        else:
            raise IndexError("The queue is full")

    def isNull(self):
        return self.size == 0  # Use size attribute

    def dequeue(self):
        if not self.isNull():
            removed_item = self.queue[0]  # Access the front
            self.queue.deleteItem(0)  # Remove from the front using deleteItem
            self.size -= 1  # Update size
            return removed_item
        else:
            raise IndexError("The queue is empty")

    def rear(self):
        if not self.isNull():
            return self.queue.last_node().value  # Access the last node's value
        else:
            return None

    def peek(self):
        if not self.isNull():
            return self.queue[0]  # Access the front
        else:
            return None

    def isFull(self):
        return self.size == self.__class__.N  

    def display_queue(self):
        self.queue.display()  # LinkedList's display method
