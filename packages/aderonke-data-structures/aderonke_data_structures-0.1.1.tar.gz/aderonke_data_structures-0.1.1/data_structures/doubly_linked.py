class Node:
    def __init__(self, item):
        self.data = item
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_at_beginning(self, item):
        new_node = Node(item)
        if self.head:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        else:
            self.head = new_node
            self.tail = new_node

    def insert_at_end(self, item):
        new_node = Node(item)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def insert_at(self, index, item):
        if index == 0:
            self.insert_at_beginning(item)
            return

        new_node = Node(item)
        temp = self.head
        i = 0
        while temp and i < index - 1:
            temp = temp.next
            i += 1

        if temp is None:
            print("Index out of range.")
            return

        new_node.next = temp.next
        new_node.prev = temp

        if temp.next:
            temp.next.prev = new_node
        else:
            self.tail = new_node  # updating tail if inserted at the end

        temp.next = new_node

    def delete_item(self, key):
        temp = self.head

        while temp:
            if temp.data == key:
                if temp.prev:
                    temp.prev.next = temp.next
                else:
                    self.head = temp.next  # deleting head

                if temp.next:
                    temp.next.prev = temp.prev
                else:
                    self.tail = temp.prev  # deleting tail

                return  # early exit after deletion
            temp = temp.next

        print("Item not found.")

    def search(self, item):
        temp = self.head
        index = 0
        while temp:
            if temp.data == item:
                return index
            temp = temp.next
            index += 1
        return -1  # not found

    def get_length(self):
        temp = self.head
        count = 0
        while temp:
            count += 1
            temp = temp.next
        return count

    def access(self, index):
        temp = self.head
        i = 0
        while temp:
            if i == index:
                return temp.data
            temp = temp.next
            i += 1
        return None  # index out of range

    def update(self, index, new_data):
        temp = self.head
        i = 0
        while temp:
            if i == index:
                temp.data = new_data
                return True
            temp = temp.next
            i += 1
        return False  # index not found

    def display(self):
        node = self.head
        while node:
            print(node.data, end=" <--> ")
            node = node.next
        print("None")
