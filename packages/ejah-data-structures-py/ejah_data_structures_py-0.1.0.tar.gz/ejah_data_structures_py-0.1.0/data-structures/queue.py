class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        """Add an item to the end of the queue."""
        self.items.append(item)

    def dequeue(self):
        """Remove and return the front item from the queue."""
        if not self.is_empty():
            return self.items.pop(0)
        else:
            raise IndexError("Dequeue from empty queue")

    def peek(self):
        """Return the front item without removing it."""
        if not self.is_empty():
            return self.items[0]
        else:
            raise IndexError("Peek from empty queue")

    def is_empty(self):
        """Check if the queue is empty."""
        return len(self.items) == 0

    def __str__(self):
        """String representation of the queue."""
        return f"Queue({self.items})"
