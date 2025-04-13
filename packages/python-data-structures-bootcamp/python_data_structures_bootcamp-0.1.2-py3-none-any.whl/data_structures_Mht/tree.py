class Node_Tree:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None

    # Add a node to the binary search tree
    def addNode(self, data):
        if self.root is None:
            self.root = Node_Tree(data)
        else:
            current = self.root
            while True:
                if data < current.data:
                    if current.left is None:
                        current.left = Node_Tree(data)
                        break
                    current = current.left
                else:
                    if current.right is None:
                        current.right = Node_Tree(data)
                        break
                    current = current.right

    # Search for a node in the binary search tree
    def searchNode(self, data):
        current = self.root
        while current:
            if current.data == data:
                return True
            elif data < current.data:
                current = current.left
            else:
                current = current.right
        return False

    # Delete a node from the binary search tree
    def deleteNode(self, data):
        self.root = self._delete(self.root, data)

    def _delete(self, node, data):
        if node is None:
            return None
        if data < node.data:
            node.left = self._delete(node.left, data)
        elif data > node.data:
            node.right = self._delete(node.right, data)
        else:
            # Node with only one child or no child
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            # Node with two children: Get the inorder successor (smallest in the right subtree)
            temp = node.right
            while temp.left:
                temp = temp.left
            node.data = temp.data
            node.right = self._delete(node.right, temp.data)
        return node

    # Inorder traversal (left, root, right)
    def displayInorder(self):
        return self._inorder(self.root)

    def _inorder(self, node):
        if node is None:
            return []
        return self._inorder(node.left) + [node.data] + self._inorder(node.right)

    # Preorder traversal (root, left, right)
    def displayPreorder(self):
        return self._preorder(self.root)

    def _preorder(self, node):
        if node is None:
            return []
        return [node.data] + self._preorder(node.left) + self._preorder(node.right)

    # Postorder traversal (left, right, root)
    def displayPostorder(self):
        return self._postorder(self.root)

    def _postorder(self, node):
        if node is None:
            return []
        return self._postorder(node.left) + self._postorder(node.right) + [node.data]

