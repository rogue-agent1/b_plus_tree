#!/usr/bin/env python3
"""B+ tree — disk-friendly balanced tree for database indexes."""
import sys

class BPlusNode:
    def __init__(self, leaf=False):
        self.keys = []; self.children = []; self.leaf = leaf; self.next = None

class BPlusTree:
    def __init__(self, order=4):
        self.order = order; self.root = BPlusNode(True)
    def search(self, key):
        node = self.root
        while not node.leaf:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]: i += 1
            node = node.children[i]
        return key in node.keys
    def range_query(self, lo, hi):
        node = self.root
        while not node.leaf:
            i = 0
            while i < len(node.keys) and lo >= node.keys[i]: i += 1
            node = node.children[i]
        result = []
        while node:
            for k in node.keys:
                if k > hi: return result
                if k >= lo: result.append(k)
            node = node.next
        return result
    def insert(self, key):
        root = self.root
        if len(root.keys) == self.order - 1:
            new_root = BPlusNode()
            new_root.children.append(self.root)
            self._split(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, key)
    def _insert_non_full(self, node, key):
        if node.leaf:
            i = 0
            while i < len(node.keys) and node.keys[i] < key: i += 1
            node.keys.insert(i, key)
        else:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]: i += 1
            child = node.children[i]
            if len(child.keys) == self.order - 1:
                self._split(node, i)
                if key >= node.keys[i]: i += 1
            self._insert_non_full(node.children[i], key)
    def _split(self, parent, idx):
        node = parent.children[idx]
        mid = len(node.keys) // 2
        right = BPlusNode(node.leaf)
        if node.leaf:
            right.keys = node.keys[mid:]
            node.keys = node.keys[:mid]
            right.next = node.next; node.next = right
            parent.keys.insert(idx, right.keys[0])
        else:
            right.keys = node.keys[mid+1:]
            up_key = node.keys[mid]
            node.keys = node.keys[:mid]
            right.children = node.children[mid+1:]
            node.children = node.children[:mid+1]
            parent.keys.insert(idx, up_key)
        parent.children.insert(idx+1, right)

if __name__ == "__main__":
    import random; random.seed(42)
    tree = BPlusTree(order=5)
    keys = random.sample(range(1000), 100)
    for k in keys: tree.insert(k)
    print(f"B+ Tree: 100 keys, order=5")
    print(f"Search 500: {tree.search(500)}")
    print(f"Search {keys[0]}: {tree.search(keys[0])}")
    rng = tree.range_query(100, 200)
    print(f"Range [100,200]: {len(rng)} keys → {rng[:10]}...")
