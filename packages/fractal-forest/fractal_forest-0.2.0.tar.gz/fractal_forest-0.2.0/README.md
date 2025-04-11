# fractal-forest

**fractal-forest** is a Python library designed for efficient management and analysis of hierarchical numerical data structures. It supports recursive tree structures where each node contains a tuple of an integer and a generic value. The library can be optimized for real-time distributed processing and OLAP compatibility.

## Features

- Recursive tree structures with multiple children per node
- Node values as tuples: `(int, Any)` for numerical aggregation and associated data
- Automated tree creation and child addition
- Integrity checks with automatic propagation of updates to parent and child nodes
- Designed for hierarchical structured data such as:
  - Financial data (e.g., budgeting, accounting hierarchies)
  - Inventory systems (e.g., product categories, stock levels)
  - Organizational charts
  - Nested project management tasks
  - Any domain requiring structured aggregation and integrity validation

## Installation

```bash
pip install fractal-forest
```

## Usage

```python
# usage_example.py
from fractal_forest import Fractal

# Create the root fractal
root = Fractal((10, "root"))

# Create child fractals
child1 = Fractal((5, "child1"))
child2 = Fractal((7, "child2"))

# Add children to root
root.add_child(child1)
root.add_child(child2)

# Print the tree structure after initial addition
print("Initial tree structure:")
root.print_tree()

# Access the updated value at root
print("Root value after aggregation:", root.value)  # Output will be (12, 'root') after aggregation

# Now update the value of child1, which triggers an update in the parent (root)
child1.update_value(6)  # New value of child1 is now 6 instead of 5

# Print the tree structure after update
print("\nTree structure after child1 update:")
root.print_tree()

# Access the updated value at root after update
print("Root value after child1 update:", root.value)  # The root value will reflect the change

# Now, simulate updating the value of a non-leaf (root), which triggers the creation of a new child to handle the difference
root.update_value(30)  # This will change the value of the root from 12 to 30

# Print the tree structure after the new child is created
print("\nTree structure after root value update:")
root.print_tree()

# Final root value after the update
print("Root value after manual update:", root.value)
```

## License
MIT License