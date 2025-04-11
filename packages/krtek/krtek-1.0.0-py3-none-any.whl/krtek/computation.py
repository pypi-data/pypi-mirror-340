"""
    Functions for computing the accuracy of a Boolean Attribute and Boolean Attribute Query. All the functions are based on the bit-string representation of the data. In short, bit-string representation uses binary matrix of the data where each row represents an instance and each column represents an attribute and its category (value). The value of the cell is 1 if the instance fulfills the category and 0 otherwise. This approach is used to efficiently evaluate values of formulas.

    For more information about bit-string representation, please refer to the following paper:
    - An alternative approach to mining association rules [4]
"""

import pandas as pd
import numpy as np

from typing import List
from .logic import BoolAttribute, BoolAttributeQuery, Rule, LogicalOperator
from .utils import _unpack


def get_query_card(cards_of_attributes: pd.DataFrame, query: BoolAttributeQuery, types_of_attributes: pd.Series) -> np.ndarray:
    """Evaluates a BoolAttributeQuery with respect of the data and returns a boolean array (card) indicating which rows match the query.

    Args:
        cards_of_attributes (pd.DataFrame): DataFrame where each column represents an attribute and its category (value) and each row contains a boolean value indicating whether the instance fulfills the category.
        query (BoolAttributeQuery): List of BoolAttribute objects and logical operators (as strings) representing the query.
        types_of_attributes (pd.Series): Series containing the types of the attributes.

    Returns:
        np.ndarray: Boolean array where True indicates that the row matches the query and False otherwise.
    """
    # Start with disjunction, because it will reduce the first expression to its true value
    card = np.zeros(cards_of_attributes.shape[0], dtype=bool)  # Initialize card as a NumPy array
    for expression, operator, negation in query:
        if isinstance(expression, BoolAttributeQuery):
            # Recursively evaluate the subquery
            expression_card = get_query_card(cards_of_attributes, expression, types_of_attributes)
        else:
            expression_card = get_literal_card(cards_of_attributes, expression, types_of_attributes)

        if negation:
            expression_card = np.logical_not(expression_card)

        # We don't need to reduce it with any operator if it is first expression
        if operator is None:
            card = expression_card
            continue

        # Decide if to use logical and or logical or based on the operator
        operator_function = np.logical_or if operator is LogicalOperator.DISJUNCTION else np.logical_and

        # Reduce the card with the operator and expression card
        card = operator_function(card, expression_card)
    return card


def get_literal_card(cards_of_attributes: pd.DataFrame, literal: BoolAttribute, types_of_attributes: pd.Series) -> np.ndarray:
    """Computes a boolean array (card) indicating which rows in the DataFrame satisfy the given literal (Boolean attribute). Computation takes in the account the type of the attribute.

    Args:
        cards_of_attributes (pd.DataFrame): DataFrame where each column represents an attribute and its category (value) and each row contains a boolean value indicating whether the instance fulfills the category.
        literal (BoolAttribute): A BoolAttribute object representing the logical literal to be evaluated.
        types_of_attributes (pd.Series): Series containing the types of the attributes.

    Returns:
        np.ndarray: A boolean array where each element indicates whether the corresponding row in
        the DataFrame satisfies the given literal (Boolean attribute).

    Raises:
        ValueError: If an attribute in the formula is not categorical, boolean or object.
    """
    # If literal value is a list with a single element, unpack it
    value = _unpack(literal.value)

    if types_of_attributes[literal.attribute] in ["category", "object"]:
        if isinstance(value, list):
            # Get the card for each category in the value list
            categories_cards = cards_of_attributes[[f"{literal.attribute}_{value}" for value in literal.value]]
            categories_cards = categories_cards.to_numpy(dtype=bool)

            # Reduce all categories of the attribute to one value
            return np.logical_or.reduce(categories_cards, 1)
        else:
            # Get the card of the category (ie. single value of attribute)
            category_card = cards_of_attributes[f"{literal.attribute}_{value}"]

            return category_card.to_numpy(dtype=bool)
    elif types_of_attributes[literal.attribute] in [bool, np.bool]:
        if isinstance(value, list):
            # In this case, the list contains [True, False], so we can return all True
            return np.ones(cards_of_attributes.shape[0], dtype=bool)

        boolean_card = (cards_of_attributes[literal.attribute] == value)
        return boolean_card.to_numpy()
    else:
        raise ValueError(f"Attribute {literal.attribute} is not categorical, boolean or object.")


def calculate_rule_table(data: pd.DataFrame, antecedent: BoolAttributeQuery, succedent: BoolAttributeQuery) -> List[int]:
    """Calculates the contigency table of a rule on the given data.

    Args:
        data (pd.DataFrame): The data to calculate the contingency table on.
        antecedent (BoolAttributeQuery): The antecedent of the rule.
        succedent (BoolAttributeQuery): The succedent of the rule.

    Returns:
        List[int]: A list of integers representing the contingency table of the rule.
    """
    # Get the cards (bit strings) of the attributes
    cards_of_attributes = pd.get_dummies(data)
    types_of_attributes = data.dtypes

    # Get the binary string representation of the formula applied to the data
    antecedent_card = get_query_card(cards_of_attributes, antecedent, types_of_attributes)
    succedent_card = get_query_card(cards_of_attributes, succedent, types_of_attributes)

    # Calculate quadruple (contingency table)
    # a (E_1,1) - number of rows that satisfy both sides
    a = np.sum(np.logical_and(antecedent_card, succedent_card))
    # b (E_1,0) - number of rows that satisfy left side but not right side
    b = np.sum(antecedent_card) - a
    # c (E_0,1) - number of rows that satisfy right side but not left side
    c = np.sum(succedent_card) - a
    # d (E_0,0) - number of rows that satisfy neither side
    d = data.shape[0] - a - b - c

    return [a, b, c, d]
