class Stack:
    """A stack implementation using a list as underlying storage."""
    
    def __init__(self, initial_items=None):
        """
        Initialize the stack.
        
        Args:
            initial_items: Optional list of items to initialize the stack.
        """
        self.stack = [] if initial_items is None else list(initial_items)
    
    def push(self, item):
        """Add an item to the top of the stack."""
        self.stack.append(item)
    
    def pop(self):
        """
        Remove and return the item from the top of the stack.
        
        Raises:
            IndexError: If the stack is empty
        """
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self.stack.pop()
    
    def peek(self):
        """
        Return the item from the top of the stack without removing it.
        
        Raises:
            IndexError: If the stack is empty
        """
        if self.is_empty():
            raise IndexError("Peek from empty stack")
        return self.stack[-1]
    
    def is_empty(self):
        """Return True if the stack is empty, False otherwise."""
        return len(self.stack) == 0
    
    def size(self):
        """Return the number of items in the stack."""
        return len(self.stack)
    
    def __str__(self):
        """Return string representation of the stack."""
        return f"Stack({self.stack})"
    
    def __len__(self):
        """Return the number of items in the stack."""
        return self.size()