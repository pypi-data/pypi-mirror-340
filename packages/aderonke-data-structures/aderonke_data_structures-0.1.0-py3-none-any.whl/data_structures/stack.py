class Stack:
    def __init__(self):
        # Initialize an empty stack
        self.items = []

    def push(self, item):
        # Add an item to the stack
        self.items.append(item)

    def pop(self):
        # Remove and return the top item from the stack
        if self.is_empty():
            return None
        return self.items.pop()

    def peek(self):
        # Return the top item without removing it
        if self.is_empty():
            return None
        return self.items[-1]

    def is_empty(self):
        # Check if the stack is empty
        return len(self.items) == 0

    def __str__(self):
        # Return string representation of the stack
        return str(self.items)
