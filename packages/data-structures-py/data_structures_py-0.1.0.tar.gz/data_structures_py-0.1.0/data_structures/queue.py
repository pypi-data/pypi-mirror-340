class Queue:
    """A queue implementation using a list as underlying storage."""
    
    def __init__(self, initial_items=None):
        """
        Initialize the queue.
        
        Args:
            initial_items: Optional list of items to initialize the queue.
        """
        self.queue = [] if initial_items is None else list(initial_items)
    
    def enqueue(self, item):
        """Add an item to the end of the queue."""
        self.queue.append(item)
    
    def dequeue(self):
        """
        Remove and return the item from the front of the queue.
        
        Raises:
            IndexError: If the queue is empty
        """
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        return self.queue.pop(0)
    
    def peek(self):
        """
        Return the item from the front of the queue without removing it.
        
        Raises:
            IndexError: If the queue is empty
        """
        if self.is_empty():
            raise IndexError("Peek from empty queue")
        return self.queue[0]
    
    def is_empty(self):
        """Return True if the queue is empty, False otherwise."""
        return len(self.queue) == 0
    
    def size(self):
        """Return the number of items in the queue."""
        return len(self.queue)
    
    def __str__(self):
        """Return string representation of the queue."""
        return f"Queue({self.queue})"
    
    def __len__(self):
        """Return the number of items in the queue."""
        return self.size()