#!/usr/bin/env python3
"""B+ Tree — ordered key-value store with leaf-linked traversal."""

class BPlusNode:
    def __init__(self, leaf=False):
        self.keys = []; self.children = []; self.leaf = leaf
        self.next = None  # leaf chain

class BPlusTree:
    def __init__(self, order=4):
        self.order = order; self.root = BPlusNode(leaf=True)
    
    def search(self, key):
        node = self._find_leaf(key)
        for i, k in enumerate(node.keys):
            if k == key: return node.children[i]
        return None
    
    def _find_leaf(self, key):
        node = self.root
        while not node.leaf:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]: i += 1
            node = node.children[i]
        return node
    
    def insert(self, key, value):
        leaf = self._find_leaf(key)
        # Update if exists
        for i, k in enumerate(leaf.keys):
            if k == key: leaf.children[i] = value; return
        # Insert sorted
        i = 0
        while i < len(leaf.keys) and leaf.keys[i] < key: i += 1
        leaf.keys.insert(i, key); leaf.children.insert(i, value)
        if len(leaf.keys) >= self.order: self._split_leaf(leaf)
    
    def _split_leaf(self, leaf):
        mid = len(leaf.keys) // 2
        new_leaf = BPlusNode(leaf=True)
        new_leaf.keys = leaf.keys[mid:]
        new_leaf.children = leaf.children[mid:]
        new_leaf.next = leaf.next; leaf.next = new_leaf
        leaf.keys = leaf.keys[:mid]; leaf.children = leaf.children[:mid]
        self._insert_parent(leaf, new_leaf.keys[0], new_leaf)
    
    def _insert_parent(self, left, key, right):
        if left == self.root:
            new_root = BPlusNode()
            new_root.keys = [key]; new_root.children = [left, right]
            self.root = new_root; return
        parent = self._find_parent(self.root, left)
        i = parent.children.index(left) + 1
        parent.keys.insert(i - 1, key); parent.children.insert(i, right)
        if len(parent.keys) >= self.order: self._split_internal(parent)
    
    def _split_internal(self, node):
        mid = len(node.keys) // 2; up_key = node.keys[mid]
        new_node = BPlusNode()
        new_node.keys = node.keys[mid+1:]
        new_node.children = node.children[mid+1:]
        node.keys = node.keys[:mid]; node.children = node.children[:mid+1]
        self._insert_parent(node, up_key, new_node)
    
    def _find_parent(self, current, target):
        if current.leaf: return None
        for child in current.children:
            if child == target: return current
            if not child.leaf:
                result = self._find_parent(child, target)
                if result: return result
        return None
    
    def range_query(self, lo, hi):
        node = self._find_leaf(lo); results = []
        while node:
            for k, v in zip(node.keys, node.children):
                if k > hi: return results
                if k >= lo: results.append((k, v))
            node = node.next
        return results

if __name__ == "__main__":
    tree = BPlusTree(order=4)
    for k in [10, 20, 5, 6, 12, 30, 7, 17, 25, 3]:
        tree.insert(k, f"val-{k}")
    print(f"Search 12: {tree.search(12)}")
    print(f"Search 99: {tree.search(99)}")
    print(f"Range [5,20]: {tree.range_query(5, 20)}")
