class Queue:
    def __init__(self):
        # Initialize an empty queue
        self.items = []

    def enqueue(self, item):
        # Add an item to the back of the queue
        self.items.append(item)

    def dequeue(self):
        # Remove and return the front item from the queue
        if self.is_empty():
            return None
        return self.items.pop(0)

    def peek(self):
        # Return the front item without removing it
        if self.is_empty():
            return None
        return self.items[0]

    def is_empty(self):
        # Check if the queue is empty
        return len(self.items) == 0

    def __str__(self):
        # Return string representation of the queue
        return str(self.items)
 # type: ignore
