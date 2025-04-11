class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        """Add an item to the top of the stack."""
        self.items.append(item)

    def pop(self):
        """Remove and return the top item from the stack."""
        if not self.is_empty():
            return self.items.pop()
        else:
            raise IndexError("Pop from empty stack")

    def peek(self):
        """Return the top item without removing it."""
        if not self.is_empty():
            return self.items[-1]
        else:
            raise IndexError("Peek from empty stack")

    def is_empty(self):
        """Check if the stack is empty."""
        return len(self.items) == 0

    def __str__(self):
        """String representation of the stack."""
        return f"Stack({self.items})"
