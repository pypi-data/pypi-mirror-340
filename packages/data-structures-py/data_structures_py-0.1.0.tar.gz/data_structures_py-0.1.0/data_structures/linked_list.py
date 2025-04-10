class Node:
    """Node class for linked list."""
    
    def __init__(self, data):
        self.data = data
        self.next = None
    
    def __repr__(self):
        return f"Node({self.data})"

class LinkedList:
    """Singly linked list implementation."""
    
    def __init__(self):
        self.head = None
        self.size = 0
    
    def insert(self, data, position=0):
        """
        Insert a new node with data at the specified position.
        
        Args:
            data: Data to insert
            position: Position to insert (0-based index)
            
        Raises:
            IndexError: If position is out of range
        """
        if position < 0 or position > self.size:
            raise IndexError("Position out of range")
            
        new_node = Node(data)
        
        if position == 0:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            for _ in range(position - 1):
                current = current.next
            new_node.next = current.next
            current.next = new_node
        
        self.size += 1
    
    def delete(self, position):
        """
        Delete node at specified position.
        
        Args:
            position: Position to delete (0-based index)
            
        Raises:
            IndexError: If position is out of range or list is empty
        """
        if position < 0 or position >= self.size:
            raise IndexError("Position out of range")
            
        if position == 0:
            self.head = self.head.next
        else:
            current = self.head
            for _ in range(position - 1):
                current = current.next
            current.next = current.next.next
        
        self.size -= 1
    
    def search(self, data):
        """
        Search for data in the list.
        
        Args:
            data: Data to search for
            
        Returns:
            Position of first occurrence if found, -1 otherwise
        """
        current = self.head
        position = 0
        while current:
            if current.data == data:
                return position
            current = current.next
            position += 1
        return -1
    
    def traverse(self):
        """Return a list of all data in the linked list."""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
    
    def __len__(self):
        """Return the size of the linked list."""
        return self.size
    
    def __str__(self):
        """Return string representation of the linked list."""
        nodes = []
        current = self.head
        while current:
            nodes.append(str(current.data))
            current = current.next
        return " -> ".join(nodes) if nodes else "Empty LinkedList"