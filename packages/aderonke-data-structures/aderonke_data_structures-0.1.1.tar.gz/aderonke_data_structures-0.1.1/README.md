# Data Structures

This documentation provides a concise overview of the custom implementations for common data structures in Python.

---

## Array

A simple dynamic array implementation using Python lists.

### Methods
- `insert(index, item)`: Insert an item at the specified index.
- `delete(index)`: Delete the item at the specified index.
- `search(item)`: Return the index of the item or -1 if not found.
- `update(index, item)`: Update the item at the specified index.
- `get(index)`: Retrieve item at a specified index.
- `display()`: Print all elements in the array.

---

## Stack

A stack (LIFO) data structure using Python list.

### Methods
- `push(item)`: Add an item to the top of the stack.
- `pop()`: Remove and return the top item.
- `peek()`: Return the top item without removing it.
- `is_empty()`: Check if the stack is empty.
- `__str__()`: Return string representation of the stack.

---

## Queue

A queue (FIFO) implementation using Python list.

### Methods
- `enqueue(item)`: Add item to the end of the queue.
- `dequeue()`: Remove and return the front item.
- `peek()`: View the front item without removing it.
- `is_empty()`: Check if the queue is empty.
- `__str__()`: String representation of the queue.

---

## LinkedList

Singly linked list implementation.

### Methods
- `insertAtBeginning(item)`: Insert at the beginning.
- `insertAfter(item, index)`: Insert after a specific index.
- `insertAtEnd(item)`: Insert at the end.
- `deleteItem(item)`: Delete the first occurrence of the item.
- `search(item)`: Search for an item.
- `get_length()`: Return length of the list.
- `access(index)`: Access item at a given index.
- `update(index, item)`: Update item at a given index.
- `display()`: Display all items.

---

## DoublyLinkedList

Doubly linked list with both forward and backward navigation.

### Methods
- `insert_at_beginning(item)`: Insert node at the start.
- `insert_at_end(item)`: Insert node at the end.
- `insert_at(index, item)`: Insert at a specific position.
- `delete_item(item)`: Delete node with matching data.
- `search(item)`: Search for item index.
- `get_length()`: Get number of nodes.
- `access(index)`: Access item by index.
- `update(index, new_data)`: Update data at index.
- `display()`: Display all nodes bidirectionally.

---

## BinarySearchTree

Binary Search Tree (BST) to maintain sorted data.

### Methods
- `insert(item)`: Insert an item into the tree.
- `search(item)`: Check if an item exists in the tree.
- `inorder_traversal()`: Return elements in sorted order.

---

## Graph

Undirected graph using an adjacency list.

### Methods
- `add_vertex(vertex)`: Add a new vertex.
- `add_edge(v1, v2)`: Create edge between vertices.
- `remove_edge(v1, v2)`: Remove edge between vertices.
- `remove_vertex(vertex)`: Remove a vertex and its edges.
- `display()`: Print the adjacency list of the graph.

