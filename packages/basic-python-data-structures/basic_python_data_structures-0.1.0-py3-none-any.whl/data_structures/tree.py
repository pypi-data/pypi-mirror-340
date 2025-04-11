class Node:
    """
    A node in a binary tree.

    Attributes:
        value: The data stored in the node.
        left: Reference to the left child node.
        right: Reference to the right child node.
    """
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinaryTree:
    """
    A binary search tree (BST) implementation with basic operations.

    Attributes:
        root (Node): The root node of the binary tree.
    """
    def __init__(self):
        self.root = None

    def insert(self, value):
        """
        Insert a value into the binary tree.

        Args:
            value: The value to insert.
        """
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert_recursive(node.right, value)

    def search(self, value):
        """
        Search for a value in the binary tree.

        Args:
            value: The value to search for.

        Returns:
            The value if found, otherwise None.
        """
        current = self.root
        while current:
            if value == current.value:
                return value
            elif value < current.value:
                current = current.left
            else:
                current = current.right
        return None

    def delete(self, value):
        """
        Delete a node with the specified value from the tree.

        Args:
            value: The value to delete.
        """
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, node, value):
        if node is None:
            return None
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            node.value = self._min_value(node.right)
            node.right = self._delete_recursive(node.right, node.value)
        return node

    def _min_value(self, node):
        """
        Find the minimum value node in the right subtree.

        Args:
            node: The starting node.

        Returns:
            The smallest value found.
        """
        current = node
        while current.left:
            current = current.left
        return current.value

    def inorder(self):
        """
        Perform an in-order traversal (Left, Root, Right).

        Returns:
            A list of values in in-order.
        """
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)

    def preorder(self):
        """
        Perform a pre-order traversal (Root, Left, Right).

        Returns:
            A list of values in pre-order.
        """
        result = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, node, result):
        if node:
            result.append(node.value)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)

    def postorder(self):
        """
        Perform a post-order traversal (Left, Right, Root).

        Returns:
            A list of values in post-order.
        """
        result = []
        self._postorder_recursive(self.root, result)
        return result

    def _postorder_recursive(self, node, result):
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.value)
