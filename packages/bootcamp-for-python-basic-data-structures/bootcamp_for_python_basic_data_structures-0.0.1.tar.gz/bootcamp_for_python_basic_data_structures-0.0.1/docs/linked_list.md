# Singly Linked List

A simple implementation of a singly linked list with common operations like insert, delete, sort, and search.

## Features

- Insertion (beginning, end, after index)
- Deletion by index
- Bubble sort
- Reversal
- Search
- Display

## Class Overview

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    ...
```
---

#### `docs/doubly_linked_list.md`

```markdown
# Doubly Linked List
```
A doubly linked list where each node points to both the next and the previous node.

## Features

- Insertion (beginning, at index, end, after a node)
- Deletion by index
- Display
- Search
- Update
- Reverse
- Sort

## Class Overview

```python
class DoublyNode:
    def __init__(self, item):
        self.data = item
        self.next = None
        self.prev = None

class DoublyLinkedList:
    ...

---
```