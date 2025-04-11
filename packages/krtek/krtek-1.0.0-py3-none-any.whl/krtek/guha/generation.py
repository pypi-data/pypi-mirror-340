"""
    This file contains functions for generating formulas from Cedent and SetOfRelevantCedents.
"""

# Optimization criterion:
# # Then if Count(alpha) < Base, then also Count(alpha and betha) < B,
# # where alpha and betha are Boolean attributes

import pandas as pd

from copy import deepcopy
from typing import Union, Generator

from .cedents import GaceType, PartialCedent, Cedent
from ..utils import _unpack, colored, Colors
from ..coefficients import Sequence
from ..logic import BoolAttribute, BoolAttributeQuery, LogicalOperator


class Node:
    """Node abstract object for tree structure of Partial Cedent.

    Attributes:
        value (Union[str, BoolAttribute]): The value of the node. It can be either string "root" or BoolAttribute object.
        children (list[Node]): The list of children nodes.
        owner (Union[Cedent, PartialCedent]): The Cedent object that this node belongs to. Used in generators.
    """
    def __init__(self, value: Union[str, BoolAttribute], owner: Union[Cedent, PartialCedent]):
        """Initialize the node with value and owner."""
        self.value = value
        self.children = []
        self.owner = owner

        # Generator for iterating over all subtree formulas
        self._generator = None
        # Indicates if the last returned formula fullfiled base
        self._last_fulfilled = None

    def add_child(self, node):
        self.children.append(node)

    def __repr__(self):
        return f"Node({self.value}, number of children: {len(self.children)})"

    def fullfiled(self, val: bool):
        self._last_fulfilled = val

    def __iter__(self):
        self._last_fulfilled = True
        self._generator = self._init_generator()

        return self

    def __next__(self):
        if self._generator is None:
            raise StopIteration
        return next(self._generator)

    def _init_generator(self) -> Generator:
        raise NotImplementedError


class PCNode(Node):
    """Node object for tree structure of Partial Cedent.

    Attributes:
        value (Union[str, BoolAttribute]): The value of the node. It can be either string "root" or BoolAttribute object.
        children (list[Node]): The list of children nodes.
        owner (PartialCedent): The Cedent object that this node belongs to.
    """

    owner: PartialCedent
    "The Partial Cedent object that this node belongs to."

    def __init__(self, value: Union[str, BoolAttribute], pc: PartialCedent):
        super().__init__(value, pc)

    def _init_generator(self):
        "Init generator (function that behaves like an iterator) that iterate over all formulas in this subtree."
        if self.value is None or not len(self.children):
            raise StopIteration

        def get_gace(node):
            "Get GACE of the node."
            attribute = node.value.attribute
            # Find literal in Partial Cedent
            for literal in self.owner.literals:
                if literal.attribute == attribute:
                    # Return GACE of the literal
                    return literal.gace

        def traverse_node(node, pile, negation):
            "A recursive function that traverse the tree and generate all formulas."

            # Pile contains all literals from staring node to this node
            if pile is None:
                new_pile = BoolAttributeQuery(node.value, negation)
            else:
                new_pile = deepcopy(pile)
                new_pile.add(node.value, self.owner.operator, negation)

            if self.owner.min_length <= len(new_pile):
                yield new_pile

            # Use optimization criterion to skip branches that can't fulfill base
            if self.owner.operator == LogicalOperator.CONJUNCTION and self._last_fulfilled is False:
                self._last_fulfilled = True
                return

            # Continue traversing
            for child in node.children:
                yield from traverse_tree(child, new_pile)

        def traverse_tree(node, pile=None):
            if node is None:
                # Termination condition
                yield pile
            else:
                # Get GACE of the curent Node
                gace = get_gace(node)

                if gace == GaceType.POSITIVE:
                    yield from traverse_node(node, pile, negation=False)
                elif gace == GaceType.NEGATIVE:
                    yield from traverse_node(node, pile, negation=True)
                elif gace == GaceType.BOTH:
                    yield from traverse_node(node, pile, negation=True)
                    yield from traverse_node(node, pile, negation=False)

        # Start traversing from the root
        if self.value == "root":
            for child in self.children:
                yield from traverse_tree(child)
        else:
            # If the node is not root, start traversing from this node
            yield from traverse_tree(self)


def generate_partial_cedent(data: pd.DataFrame, pc: PartialCedent) -> PCNode:
    """Generate all posible formulas based on specified Partial Cedent.

    Args:
        data (pd.DataFrame): Data to generate formulas on.
        pc (PartialCedent): Partial Cedent object that specifies the structure of formulas.

    Returns:
        Node: Tree structure of formulas.
    """
    if len(pc.literals) == 0:
        raise ValueError("Partial cedent must contain at least one literal.")

    def create_tree(parent: Node, ith: int = 0, depth: int = 1):
        # Parent is the node where the children will be added
        # Ith corespons starting index of literals
        # Depth corespons to the current depth of tree (number of literals in formula)

        # First condition: There is none literal to change
        # Second condition: The formula has reached its maximum length
        if len(pc.literals) == ith or depth == pc.max_length + 1:
            return []

        # Select ith literal
        literal = pc.literals[ith]
        attribute = literal.attribute
        column = data[attribute]

        # Select all values based on attribute's data type
        if type(column.dtype) is pd.CategoricalDtype:
            unique = column.cat.categories
            if type(literal.coefficient) is Sequence and column.cat.ordered is False:
                print(f"{colored('Warning:', Colors.RED)} Attribute {attribute} has the Sequence coefficient set, but does not have the specified ordering. Please check Pandas Categorical data Documentation.")
        else:
            unique = column.unique()

        # Get all values according to coefficient
        values = literal.coefficient.get(unique)

        # Create new node for each value of the attribute
        for val in values:
            node = PCNode(BoolAttribute(attribute, _unpack(val)), pc)
            parent.add_child(node)

            # Add new children (with different attribute) to new node
            create_tree(node, ith + 1, depth + 1)

        # Add new children (with different attribute) to parent node
        create_tree(parent, ith + 1, depth)

    # Create root node
    root = PCNode("root", pc)
    create_tree(root)

    return root


class CNode(Node):
    """Node object for tree structure of Partial Cedent.

    Attributes:
        value (Union[str, BoolAttribute]): The value of the node. It can be either string "root" or BoolAttribute object.
        children (list[Node]): The list of children nodes.
        owner (Cedent): The Cedent object that this node belongs to.
    """

    owner: Cedent
    "The Cedent object that this node belongs to."

    def __init__(self, value: Union[str, BoolAttribute], owner: Cedent):
        super().__init__(value, owner)

    def _init_generator(self):
        # Function for combinig all partial cedents trees
        def combine(ith: int = 0, depth: int = 0, pile=None):
            if (len(self.owner.partial_cedents) == ith or depth == self.owner.max_length + 1):
                return None

            root = self.children[ith]
            for node in root:
                if pile is None:
                    new_pile = BoolAttributeQuery(node)
                else:
                    new_pile = deepcopy(pile)
                    # Always add conjunction because of definition of Cedent
                    new_pile.add(node, LogicalOperator.CONJUNCTION)

                depth = len(new_pile)
                if self.owner.max_length < depth:
                    continue

                if self.owner.min_length <= len(new_pile):
                    yield new_pile

                # Use optimization criterion to skip branches that can't fulfill base
                if self._last_fulfilled is False:
                    root.fullfiled(False)
                    self._last_fulfilled = True
                    continue

                # Try extending new pile by changing Partial Cedent root
                yield from combine(ith + 1, depth, new_pile)

            # Change root node
            yield from combine(ith + 1, depth, pile)

        # Start traversing from the first root
        yield from combine(0)


def generate_cedent(data: pd.DataFrame, cedent: Cedent):
    """Generate all posible formulas based on specified Cedent.

    Args:
        data (pd.DataFrame): Data to generate formulas on.
        cedent (Cedent): Cedent object that specifies the structure of formulas.

    Returns:
        Union[CNode, PCNode]: Tree structure of formulas.
    """
    roots = []
    for pc in cedent.partial_cedents:
        # Generate partial cedent tree
        root = generate_partial_cedent(data, pc)
        roots.append(root)

    # Create root node
    node = CNode("root", cedent)
    node.children = roots
    return node
