class Array:
    def __init__(self):
        self.items = []

    def insert(self, item):
        self.items.append(item)

    def insert_at(self, index, item):
        if index < 0 or index > len(self.items):
            raise IndexError("Index out of range")
        self.items.insert(index, item)

    def delete(self, item):
        try:
            self.items.remove(item)
        except ValueError:
            print("Item not found.")

    def delete_at(self, index):
        if index < 0 or index >= len(self.items):
            raise IndexError("Index out of range")
        self.items.pop(index)

    def update(self, index, new_item):
        if index < 0 or index >= len(self.items):
            raise IndexError("Index out of range")
        self.items[index] = new_item

    def access(self, index):
        if index < 0 or index >= len(self.items):
            raise IndexError("Index out of range")
        return self.items[index]

    def search(self, item):
        try:
            return self.items.index(item)
        except ValueError:
            return -1

    def get_length(self):
        return len(self.items)

    def clear(self):
        self.items.clear()

    def reverse(self):
        self.items.reverse()

    def sort(self, reverse=False):
        self.items.sort(reverse=reverse)

    def display(self):
        print(self.items)

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(self.items)

    def __str__(self):
        return str(self.items)
 # type: ignore
