from collections import defaultdict

class Graph:
    """Graph implementation using adjacency list."""
    
    def __init__(self, directed=False):
        """
        Initialize the graph.
        
        Args:
            directed: If True, creates a directed graph
        """
        self.graph = defaultdict(list)
        self.directed = directed
    
    def add_edge(self, u, v):
        """
        Add an edge between vertices u and v.
        
        Args:
            u: First vertex
            v: Second vertex
        """
        self.graph[u].append(v)
        if not self.directed:
            self.graph[v].append(u)
    
    def dfs(self, start):
        """
        Depth-First Search traversal from a starting vertex.
        
        Args:
            start: Starting vertex
            
        Returns:
            List of vertices in DFS order
        """
        visited = []
        stack = [start]
        
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.append(vertex)
                # Push adjacent vertices in reverse order to visit them in order
                for neighbor in reversed(self.graph[vertex]):
                    if neighbor not in visited:
                        stack.append(neighbor)
        return visited
    
    def bfs(self, start):
        """
        Breadth-First Search traversal from a starting vertex.
        
        Args:
            start: Starting vertex
            
        Returns:
            List of vertices in BFS order
        """
        visited = []
        queue = [start]
        
        while queue:
            vertex = queue.pop(0)
            if vertex not in visited:
                visited.append(vertex)
                for neighbor in self.graph[vertex]:
                    if neighbor not in visited:
                        queue.append(neighbor)
        return visited
    
    def __str__(self):
        """Return string representation of the graph."""
        return "\n".join(
            f"{vertex}: {neighbors}"
            for vertex, neighbors in sorted(self.graph.items())
        )