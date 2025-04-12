class Node:
    def __init__(self, item):
        self.item = item
        self.next = None


class LinkedList:

    def __init__(self):
        self.head = None

    def insertAtBeginning(self, item):
        new_node = Node(item)
        new_node.next = self.head
        self.head = new_node

    def insertAfter(self, item, index):
        if index < 0 or index >= self.get_length():
            raise IndexError("Index out of bounds")

        new_node = Node(item)
        current = self.head
        count = 0

        while current:
            if count == index:
                new_node.next = current.next
                current.next = new_node
                return
            current = current.next
            count += 1

    def insertAtEnd(self, item):
        new_node = Node(item)
        if not self.head:
            self.head = new_node
            return

        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def deleteItem(self, item):
        current = self.head
        previous = None

        while current:
            if current.item == item:
                if previous:
                    previous.next = current.next
                else:
                    self.head = current.next
                return True
            previous = current
            current = current.next
        return False

    def display(self):
        node = self.head
        while node:
            print(node.item, end=" -> ")
            node = node.next
        print("None")

    def search(self, item):
        current = self.head
        while current:
            if current.item == item:
                return True
            current = current.next
        return False

    def get_length(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def access(self, index):
        if index < 0 or index >= self.get_length():
            raise IndexError("Index out of bounds")

        current = self.head
        count = 0
        while current:
            if count == index:
                return current.item
            current = current.next
            count += 1

    def update(self, index, new_item):
        if index < 0 or index >= self.get_length():
            raise IndexError("Index out of bounds")

        current = self.head
        count = 0
        while current:
            if count == index:
                current.item = new_item
                return
            current = current.next
            count += 1
