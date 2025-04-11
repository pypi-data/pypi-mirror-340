import unittest
from fractal_forest import Node, Tree

class TestFractalForest(unittest.TestCase):
    
    def test_node_creation(self):
        """
        Test the creation of a single node.
        """
        node = Node((10, "root"))
        self.assertEqual(node.value, (10, "root"))
        self.assertEqual(len(node.children), 0)  # No children initially

    def test_add_child(self):
        """
        Test adding a child node to a parent node.
        """
        root = Node((10, "root"))
        child1 = Node((5, "child1"))
        root.add_child(child1)
        
        self.assertEqual(len(root.children), 1)
        self.assertEqual(root.children[0].value, (5, "child1"))
        self.assertEqual(root.value[0], 5)  # Root's value should be updated to the sum of its children's values

    def test_integrity_check(self):
        """
        Test the integrity check (sum of children's values).
        """
        root = Node((10, "root"))
        child1 = Node((5, "child1"))
        child2 = Node((7, "child2"))
        
        root.add_child(child1)
        root.add_child(child2)

        # After adding children, root's value should be the sum of the children's integer values
        self.assertEqual(root.value, (12, "root"))  # The root's value should be updated to (5 + 7, "root")

    def test_tree_creation(self):
        """
        Test the creation of a tree and adding nodes to it.
        """
        tree = Tree((10, "root"))
        child1 = tree.add_node(tree.root, (5, "child1"))
        child2 = tree.add_node(tree.root, (7, "child2"))

        # Test tree structure
        self.assertEqual(tree.root.value, (12, "root"))  # The root's value should be 5 + 7
        self.assertEqual(len(tree.root.children), 2)
        self.assertEqual(child1.value, (5, "child1"))
        self.assertEqual(child2.value, (7, "child2"))

    def test_multiple_children(self):
        """
        Test adding multiple children to a node.
        """
        root = Node((10, "root"))
        child1 = Node((5, "child1"))
        child2 = Node((7, "child2"))
        child3 = Node((3, "child3"))

        root.add_child(child1)
        root.add_child(child2)
        root.add_child(child3)

        # After adding three children, root's value should be the sum of all children's values
        self.assertEqual(root.value, (15, "root"))  # 5 + 7 + 3 = 15

    def test_empty_tree(self):
        """
        Test creating an empty tree (no nodes).
        """
        tree = Tree((0, "root"))
        self.assertEqual(tree.root.value, (0, "root"))
        self.assertEqual(len(tree.root.children), 0)

if __name__ == '__main__':
    unittest.main()
