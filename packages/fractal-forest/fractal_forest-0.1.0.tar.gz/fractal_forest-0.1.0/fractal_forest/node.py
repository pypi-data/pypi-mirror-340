# node.py

class Node:
    def __init__(self, value):
        """
        Initialize a node in the tree.
        Each node contains a tuple (int, Any) for value.
        
        :param value: A tuple (int, Any) where the first element is an integer and the second can be any value.
        """
        self.value = value  # A tuple (int, Any)
        self.children = []  # List to hold child nodes

    def add_child(self, child):
        """
        Adds a child node to the current node and updates the parent's value.
        
        :param child: The Node object to be added as a child
        """
        self.children.append(child)
        self.update_value()

    def update_value(self):
        """
        Recalculates the node's value by summing the children's integer values.
        This assumes the value is a tuple where the first element is an integer.
        """
        child_sum = sum(child.value[0] for child in self.children)  # Sum of all children's integer values
        self.value = (child_sum, self.value[1])  # Update the current node's value with the sum of children

    def __repr__(self):
        return f"Node(value={self.value}, children={len(self.children)})"
