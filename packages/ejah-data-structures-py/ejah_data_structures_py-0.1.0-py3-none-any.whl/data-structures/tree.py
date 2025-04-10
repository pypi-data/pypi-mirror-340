class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    
    def _insert_recursive(self, node, data):
        """Helper function to recursively insert a new node."""
        if data < node.data:
            if node.left is None:
                node.left = Node(data)
            else:
                self._insert_recursive(node.left, data)
        elif data > node.data:
            if node.right is None:
                node.right = Node(data)
            else:
                self._insert_recursive(node.right, data)

    def insert(self, data):
        """Insert a new node with the given data into the BST."""
        if self.root is None:
            self.root = Node(data)
        else:
            self._insert_recursive(self.root, data)

    def search(self, data):
        """Search for a node with the given data in the BST."""
        return self._search_recursive(self.root, data)

    def _search_recursive(self, node, data):
        """Helper function to recursively search for a node."""
        if node is None:
            return False
        if node.data == data:
            return True
        elif data < node.data:
            return self._search_recursive(node.left, data)
        else:
            return self._search_recursive(node.right, data)
        
    def _inorder_recursive(self, node, elements):
        """Helper function for recursive inorder traversal."""
        if node is not None:
            self._inorder_recursive(node.left, elements)
            elements.append(node.data)
            self._inorder_recursive(node.right, elements)


    def inorder_traversal(self):
        """Return a list of the elements in the BST in inorder."""
        elements = []
        self._inorder_recursive(self.root, elements)
        return elements


    def __str__(self):
        return " -> ".join(map(str, self.inorder_traversal())) if self.root else "Empty"
