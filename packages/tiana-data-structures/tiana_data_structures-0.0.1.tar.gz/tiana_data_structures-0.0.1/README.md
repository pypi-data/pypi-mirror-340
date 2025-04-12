# Data Structures Package

This package implements fundamental data structures in Python, including Array, LinkedList, Stack, Queue, Graph, and Tree.

---

## Classes Included

### 1. `Array`
A dynamic array implementation similar to Python’s built-in list.

#### Features:
- `append(value)` – Adds an element at the end.
- `insert(index, value)` – Inserts an element at a specific index.
- `delete(index)` – Removes an element at a specific index.
- `search(value)` – Returns the index of the value, or -1 if not found.
- `display()` – Displays the current elements.
- Automatically resizes when capacity is exceeded.

---

### 2. `LinkedList`
A singly linked list with support for insertions, deletions, search, and update.

#### Features:
- `add_Node(data, post=0)` – Adds a new node at the beginning or specified position.
- `delete_Node(data, post=0)` – Deletes a node at the beginning or a given position.
- `search(data)` – Searches for a node and returns its position.
- `get_node(position)` – Returns the node at a given position.
- `update(val, new_val)` – Updates a node's value.
- `display()` – Prints the entire list.

---

### 3. `Stack`
A simple stack using a Python list (LIFO).

#### Features:
- `push(data)` – Adds data to the top of the stack.
- `pop()` – Removes and returns the top item.
- `top()` – Returns the current top without removing it.
- `display()` – Prints stack content.
- `size()` – Returns the number of elements.

---

### 4. `Queue`
A FIFO queue using a Python list.

#### Features:
- `enqueue(data)` – Adds data to the end.
- `dequeue()` – Removes and returns the front item.
- `is_empty()` – Checks if the queue is empty.
- `size()` – Returns the queue length.
- `display()` – Displays the queue elements.

---

### 5. `Graph`
An undirected graph implemented using an adjacency list.

#### Features:
- `add_node(data)` – Adds a new node.
- `add_edge(data1, data2)` – Creates a two-way connection between nodes.
- `display()` – Shows all nodes and their neighbors.

---

### 6. `Tree`
A binary search tree (BST) implementation.

#### Features:
- `insert(data)` – Inserts a value into the tree.
- `search(data)` – Searches for a value.
- `in_order()` – Prints the tree in in-order traversal.

---

