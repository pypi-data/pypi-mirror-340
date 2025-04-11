# fractal_forest/tests/test_fractal.py
import unittest
from fractal_forest import Fractal

class TestFractalForest(unittest.TestCase):

    def test_node_creation(self):
        """Test the creation of a single node."""
        fractal = Fractal((10, "root"))
        self.assertEqual(fractal.value, (10, "root"))
        self.assertEqual(len(fractal.children), 0)  # No children initially

    def test_add_child(self):
        """Test adding a child node to a parent node."""
        root = Fractal((10, "root"))
        child1 = Fractal((5, "child1"))
        root.add_child(child1)

        self.assertEqual(len(root.children), 1)
        self.assertEqual(root.children[0].value, (5, "child1"))
        self.assertEqual(root.value[0], 5)  # Root's value should be updated to the sum of its children's values

    def test_integrity_check(self):
        """Test the integrity check (sum of children's values)."""
        root = Fractal((10, "root"))
        child1 = Fractal((5, "child1"))
        child2 = Fractal((7, "child2"))

        root.add_child(child1)
        root.add_child(child2)

        # After adding children, root's value should be the sum of the children's integer values
        self.assertEqual(root.value, (12, "root"))  # The root's value should be updated to (5 + 7, "root")

    def test_tree_creation(self):
        """Test the creation of a tree and adding nodes to it."""
        root = Fractal((10, "root"))
        child1 = Fractal((5, "child1"))
        child2 = Fractal((7, "child2"))

        root.add_child(child1)
        root.add_child(child2)

        # Test tree structure
        self.assertEqual(root.value, (5 + 7, "root"))  # The root's value should be (5 + 7)
        self.assertEqual(len(root.children), 2)
        self.assertEqual(child1.value, (5, "child1"))
        self.assertEqual(child2.value, (7, "child2"))

    def test_multiple_children(self):
        """Test adding multiple children to a node."""
        root = Fractal((10, "root"))
        child1 = Fractal((5, "child1"))
        child2 = Fractal((7, "child2"))
        child3 = Fractal((3, "child3"))

        root.add_child(child1)
        root.add_child(child2)
        root.add_child(child3)

        # After adding three children, root's value should be the sum of all children's values
        self.assertEqual(root.value, (15, "root"))  # 5 + 7 + 3 = 15

    def test_remove_child(self):
        """Test removing a child node from a parent node."""
        root = Fractal((10, "root"))
        child1 = Fractal((5, "child1"))
        child2 = Fractal((7, "child2"))

        root.add_child(child1)
        root.add_child(child2)
        root.remove_child(child1)

        # After removing child1, root's value should be updated
        self.assertEqual(root.value, (7, "root"))  # 7 + 5 - 5 = 7

    def test_print_tree(self):
        """Test printing the tree structure."""
        root = Fractal((10, "root"))
        child1 = Fractal((5, "child1"))
        child2 = Fractal((7, "child2"))

        root.add_child(child1)
        root.add_child(child2)

        root.print_tree()  # This should print the tree structure

    def test_update_leaf_value(self):
        """Test updating a leaf node and propagating to root."""
        root = Fractal((0, "root"))
        leaf = Fractal((5, "leaf"))
        root.add_child(leaf)

        leaf.update_value(10)

        # Leaf should be updated
        self.assertEqual(leaf.value[0], 10)
        # Root should reflect updated leaf
        self.assertEqual(root.value[0], 10)

    def test_update_nonleaf_value_no_change(self):
        """Test updating a non-leaf with the same value as sum of children."""
        root = Fractal((0, "root"))
        c1 = Fractal((5, "c1"))
        c2 = Fractal((7, "c2"))
        root.add_child(c1)
        root.add_child(c2)

        # Try updating root to 12, which is already the sum of children
        root.update_value(12)

        # Should remain unchanged (no extra children)
        self.assertEqual(root.value[0], 12)
        self.assertEqual(len(root.children), 2)

    def test_update_nonleaf_value_with_change(self):
        """Test updating a non-leaf with a different value."""
        root = Fractal((0, "root"))
        c1 = Fractal((5, "c1"))
        c2 = Fractal((7, "c2"))
        root.add_child(c1)
        root.add_child(c2)

        root.update_value(15)  # diff = 3, expect a new auto-generated child

        self.assertEqual(root.value[0], 15)
        self.assertEqual(len(root.children), 3)

        # The new child should have value 3 and label "auto-generated"
        auto_kids = [child for child in root.children if child.value[1] == "auto-generated"]
        self.assertEqual(len(auto_kids), 1)
        self.assertEqual(auto_kids[0].value[0], 3)

    def test_integrity_after_updates(self):
        """Test tree maintains integrity after updates and auto-child creation."""
        root = Fractal((0, "root"))
        a = Fractal((4, "A"))
        b = Fractal((6, "B"))
        root.add_child(a)
        root.add_child(b)

        # Force imbalance
        root.update_value(20)

        # Tree should still pass integrity check
        self.assertTrue(root.integrity_check())

if __name__ == '__main__':
    unittest.main()
