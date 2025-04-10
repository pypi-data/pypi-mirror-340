"""
data_structures package - A collection of core data structure implementations.

This package provides implementations of:
- Arrays (based on numpy)
- Stacks
- Queues
- Linked Lists
- Binary Search Trees
- Graphs
"""

from .array import MyArray
from .stack import Stack
from .queue import Queue
from .linked_list import LinkedList
from .tree import BinarySearchTree, TreeNode
from .graph import Graph

__all__ = ['MyArray', 'Stack', 'Queue', 'LinkedList', 'BinarySearchTree', 'TreeNode', 'Graph']
__version__ = '0.1.0'