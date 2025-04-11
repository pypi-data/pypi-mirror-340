class Fractal:
    def __init__(self, value):
        """Initializes a Fractal with a value (a tuple: (int, label))."""
        self.value = value
        self.children = []
        self.parent = None

    def is_root(self):
        return self.parent is None

    def is_leaf(self):
        return len(self.children) == 0

    def add_child(self, child):
        """Adds a child Fractal to the current Fractal."""
        if child not in self.children:
            self.children.append(child)
            child.parent = self

            child_value = child.value[0]
            if len(self.children) == 1:
                # First child: set parent value to child value, discard initial
                self.value = (child_value, self.value[1])
            else:
                self.value = (self.value[0] + child_value, self.value[1])

            if self.parent:
                self.parent._update_aggregate_value()

    def remove_child(self, child):
        """Removes a child from the current Fractal."""
        if child in self.children:
            self.children.remove(child)
            child.parent = None
            self.value = (self.value[0] - child.value[0], self.value[1])
            if self.parent:
                self.parent._update_aggregate_value()

    def _update_aggregate_value(self):
        """Recalculates this node's value based on its children."""
        total = sum(child.value[0] for child in self.children)
        self.value = (total, self.value[1])
        if self.parent:
            self.parent._update_aggregate_value()
        return total

    def update_value(self, new_value: int):
        """Attempts to update the value of the Fractal node to new_value."""
        current = self.value[0]
        if new_value == current:
            return  # No change needed

        if self.is_leaf():
            self.value = (new_value, self.value[1])
            if self.parent:
                self.parent._update_aggregate_value()
        else:
            sum_children = sum(child.value[0] for child in self.children)
            if new_value == sum_children:
                return  # Still consistent
            else:
                # Create a new child to balance the difference
                diff = new_value - sum_children
                auto_child = Fractal((diff, "auto-generated"))
                self.add_child(auto_child)

    def find_root(self):
        node = self
        while node.parent is not None:
            node = node.parent
        return node

    def integrity_check(self):
        """Checks if the fractal tree is consistent."""
        def check_node(node):
            if not node.children:
                return node.value[0]
            child_sum = sum(check_node(child) for child in node.children)
            return child_sum

        root = self.find_root()
        expected = check_node(root)
        return expected == root.value[0]

    def print_tree(self, level=0):
        print("  " * level + f"{self.value}")
        for child in self.children:
            child.print_tree(level + 1)

    def __repr__(self):
        return f"Fractal(value={self.value}, children_count={len(self.children)})"
