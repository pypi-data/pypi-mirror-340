
---

#### `docs/queue.md`

```markdown
# Queue
```
A custom queue with a fixed maximum size.

## Features

- Enqueue
- Dequeue
- Peek (front and rear)
- Check full
- Check empty
- Display

## Class Overview

```python
class MyQueue:
    def __init__(self, size, queue=[]):
        self.queue = queue
        self.size = size
    ...
```