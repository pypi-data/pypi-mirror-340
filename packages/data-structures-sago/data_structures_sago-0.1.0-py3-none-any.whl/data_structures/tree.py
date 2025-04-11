
# tree.py

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        """Inserts a value into the tree (unsorted, breadth)."""
        new_node = Node(value)
        if not self.root:
            self.root = new_node
            return

        queue = [self.root]
        while queue:
            current = queue.pop(0)

            if not current.left:
                current.left = new_node
                return
            else:
                queue.append(current.left)

            if not current.right:
                current.right = new_node
                return
            else:
                queue.append(current.right)

    def inorder_traversal(self, node):
        """Returns a list of values in in-order stooling."""
        if node is None:
            return []
        return (
            self.inorder_traversal(node.left) +
            [node.value] +
            self.inorder_traversal(node.right)
        )

    def display(self):
        """Displays the tree as an in-order toolpath."""
        return self.inorder_traversal(self.root)
