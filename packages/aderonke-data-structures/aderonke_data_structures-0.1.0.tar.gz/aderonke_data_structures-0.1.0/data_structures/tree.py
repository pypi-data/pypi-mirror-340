class Node:
    def __init__(self, item):
        self.item = item
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, item):
        if not self.root:
            self.root = Node(item)
        else:
            self._insert(self.root, item)

    def _insert(self, current, item):
        if item < current.item:
            if current.left:
                self._insert(current.left, item)
            else:
                current.left = Node(item)
        elif item > current.item:
            if current.right:
                self._insert(current.right, item)
            else:
                current.right = Node(item)

    def search(self, item):
        return self._search(self.root, item)

    def _search(self, current, item):
        if not current:
            return False
        if item == current.item:
            return True
        elif item < current.item:
            return self._search(current.left, item)
        else:
            return self._search(current.right, item)

    def inorder_traversal(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.item)
            self._inorder(node.right, result)
