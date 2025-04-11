# tree.py

from .node import Node

class Tree:
    def __init__(self, root_value):
        """
        Initialize the tree with a root node.
        
        :param root_value: The initial value for the root node, a tuple (int, Any).
        """
        self.root = Node(root_value)

    def add_node(self, parent_node, value):
        """
        Adds a new node to the tree under a specific parent node.
        
        :param parent_node: The Node to add the new child node under
        :param value: The value for the new child node, a tuple (int, Any)
        :return: The newly created child node
        """
        new_node = Node(value)
        parent_node.add_child(new_node)
        return new_node

    def __repr__(self):
        return f"Tree(root={self.root})"
