from collections import deque

class SplayTreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class SplayTree:
    def __init__(self):
        self.root = None

    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _splay(self, root, key):
        # Base case: root is None or key is at the root
        if root is None or root.key == key:
            return root

        # Key lies in left subtree
        if key < root.key:
            # If the left child is None, return the root
            if root.left is None:
                return root
            
            # Zig (Single Right Rotation)
            if key == root.left.key:
                return self._right_rotate(root)
            
            # Zig-Zig (Left-Left) Case
            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._right_rotate(root)
            # Zig-Zag (Left-Right) Case
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right:
                    root.left = self._left_rotate(root.left)

            return self._right_rotate(root) if root.left else root

        # Key lies in right subtree
        else:
            # If the right child is None, return the root
            if root.right is None:
                return root

            # Zag (Single Left Rotation)
            if key == root.right.key:
                return self._left_rotate(root)

            # Zag-Zag (Right-Right) Case
            if key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._left_rotate(root)
            # Zag-Zig (Right-Left) Case
            elif key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left:
                    root.right = self._right_rotate(root.right)

            return self._left_rotate(root) if root.right else root


    def insert(self, key):
        if self.root is None:
            self.root = SplayTreeNode(key)
            return
        
        # Splay the tree to bring the key to the root
        self.root = self._splay(self.root, key)

        # If the root already has the key, it's already in the tree, no need to insert
        if self.root.key == key:
            return
        
        # Otherwise, insert the key as a new root
        new_node = SplayTreeNode(key)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None

        self.root = new_node

    def delete(self, key):
        if self.root is None:
            return

        # Splay the tree to bring the key to the root
        self.root = self._splay(self.root, key)

        # If the root doesn't have the key, it doesn't exist in the tree
        if self.root.key != key:
            return

        # If the root has no children, simply remove it
        if self.root.left is None:
            self.root = self.root.right
        elif self.root.right is None:
            self.root = self.root.left
        else:
            # If both children exist, splay the maximum node from the left subtree
            left_subtree = self.root.left
            self.root = self.root.right
            self.root = self._splay(self.root, key)
            self.root.left = left_subtree

    def search(self, key):
        self.root = self._splay(self.root, key)
        return self.root is not None and self.root.key == key

    def inorder(self, root):
        if root is not None:
            self.inorder(root.left)
            print(root.key, end=" ")
            self.inorder(root.right)

    def print_tree(self, node=None, depth=0):
        # Start from root if no specific node is provided
        if node is None:
            node = self.root
        # Base case: if node is None, return
        if node is None:
            return
        # Display right subtree
        if node.right:
            self.print_tree(node.right, depth + 1)
        # Print current node with indentation according to its depth
        print("    " * depth + f"-> {node.key}")
        # Display left subtree
        if node.left:
            self.print_tree(node.left, depth + 1)


tree = SplayTree()
tree.insert(5)
tree.insert(10)
tree.insert(1)
tree.insert(7)
tree.insert(3)
tree.insert(11)
print("Splay Tree after Inserting 11:")
tree.print_tree()
tree.search(3)
print("Splay Tree after Searching for 3:")
tree.print_tree()
