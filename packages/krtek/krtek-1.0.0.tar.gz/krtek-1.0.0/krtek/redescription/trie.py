"""
    This file contains the implementation of a bitwise trie, which is a data structure that allows for
    efficient storage and retrieval of bit strings.
"""


class TrieNode:
    def __init__(self):
        self.children = {}  # {'0': TrieNode, '1': TrieNode}
        self.is_end = False


class BitwiseTrie:
    def __init__(self, bit_length):
        self.root = TrieNode()
        self.bit_length = bit_length

    def insert(self, bit_string):
        "Inserts a bit string into the trie."

        if len(bit_string) != self.bit_length:
            raise ValueError("The bit string must have a fixed length.")

        node = self.root
        for bit in bit_string:
            if bit not in node.children:
                node.children[bit] = TrieNode()
            node = node.children[bit]
        node.is_end = True

    def search_with_mask(self, mask):
        "Finds all strings matching the mask."

        if len(mask) != self.bit_length:
            raise ValueError("The mask must be of a fixed length.")

        results = []
        self._search_recursive(self.root, mask, 0, "", results)
        return results

    def _search_recursive(self, node, mask, index, current, results):
        "Auxiliary recursive search function."
        if index == len(mask):  # End of mask
            if node.is_end:
                results.append(current)
            return

        char = mask[index]
        if char == "0" or char == "1":
            if char in node.children:
                self._search_recursive(
                    node.children[char],
                    mask,
                    index + 1,
                    current + char,
                    results
                )
        elif char == "?":
            for bit, child in node.children.items():
                self._search_recursive(child, mask, index + 1, current + bit, results)
