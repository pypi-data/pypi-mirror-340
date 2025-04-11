"""
    This file contains the implementation of logical formulas and literals.
"""

import pandas as pd
from .quantifiers import Quantifier
from .utils import Colors, colored, merge_intervals

from copy import deepcopy
from typing import List, Sequence, Union, Any
from enum import Enum


# This two constants are used to represent the quantifier symbol and the number of decimal places to round the accuracy of the rules in the string output.
QUANTIFIER_SYMBOL = "≈"
"Represents the quantifier symbol."
NUMBER_OF_DECIMAL_PLACES = 3
"Represents the number of decimal places to round the accuracy of the rules in the string output."


class LogicalOperator(Enum):
    "Represents the logical operators."
    CONJUNCTION = "∧"
    DISJUNCTION = "∨"
    NEGATION = "¬"


class BoolAttribute:
    """Represents a Boolean attribute (literal) with a name and a value.

    Attributes:
        attribute (str): The name of the attribute.
        value (Any): The value of the attribute.
    """

    attribute: str
    "The name of the attribute."
    value: Any
    "The value of the attribute."

    def __init__(self, att: str, val: Any):
        self.attribute = att
        self.value = val

    @property
    def dtype(self):
        "Returns the type of the value."
        if type(self.value) in [list, tuple]:
            return type(self.value[0])
        return type(self.value)

    def __str__(self):
        value = str(self.value) if type(self.value) is not list else ", ".join(map(str, self.value))

        return f"{colored(self.attribute, Colors.GREEN)}[{colored(value, Colors.YELLOW)}]"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash((self.attribute, self.value))


class BoolAttributeQuery:
    """Represents a logical formula (query) with multiple Boolean attributes and logical operators. It is recursive structure and can be nested.

    Attributes:
        expressions (List[Union[BoolAttribute, BoolAttributeQuery]]): A list of expressions in the query.
        operators (List[LogicalOperator]): A list of operators in the query.
        negation (List[bool]): Information whether the expression is negated.
    """

    expressions: List[Union[BoolAttribute, "BoolAttributeQuery"]]
    "A list of expressions in the query."
    operators: List[LogicalOperator]
    "A list of operators in the query."
    negation: List[bool]
    "Information whether the expression is negated."

    def __init__(self, initial_expression: Union[BoolAttribute, "BoolAttributeQuery"], negation: bool = False):
        self.expressions = [initial_expression]
        self.operators: List[LogicalOperator] = []
        self.negation: List[bool] = [negation]

    def add(self, expression: Union[BoolAttribute, "BoolAttributeQuery"], operator: LogicalOperator, negation: bool = False):
        """Adds a new expression to the query.

        Args:
            expression (BoolAttribute | BoolAttributeQuery): The expression to be added.
            operator (LogicalOperator): The operator to be added before the new expression.
            negation (bool): If the expression is negated.
        """
        self.expressions.append(expression)
        self.operators.append(operator)
        self.negation.append(negation)

    @property
    def attributes(self):
        "Returns a list of the attributes in the query."
        attributes = []
        for expression in self.expressions:
            if isinstance(expression, BoolAttribute):
                attributes.append(expression.attribute)
            else:
                attributes.extend(expression.attributes)
        return attributes

    def __str__(self):
        result = ""

        operators_to_str = list(map(lambda x: x.value, self.operators))
        operators_to_str.append("")
        for expression, operator, negation in zip(self.expressions, operators_to_str, self.negation):
            if isinstance(expression, BoolAttributeQuery) or negation:
                expression = f"({expression})"

            if negation:
                result += LogicalOperator.NEGATION.value
            result += f"{expression} {operator} "

        result = result[:-2]
        return result

    def __repr__(self):
        return str(self)

    def __iter__(self):
        self._idx = 0
        return self

    def __next__(self):
        if (self._idx >= len(self.expressions)):
            raise StopIteration

        self._idx += 1
        if self._idx == 1:
            return self.expressions[self._idx - 1], None, self.negation[self._idx - 1]

        return self.expressions[self._idx - 1], self.operators[self._idx - 2], self.negation[self._idx - 1]

    def __len__(self):
        "Returns number of literals in the query."
        return len(self.attributes)


class Rule:
    """Represents a rule with an antecedent (LHS), a succedent (RHS), a quantifier and a contingency table of rule.
    - The quantifiers are used to evaluate the accuracy of the rule based on the contingency table.
    - The contingency table is a list with four elements: a, b, c, d. Where a is the number of true positives, b is the number of false positives, c is the number of false negatives and d is the number of true negatives.

    Attributes:
        antecedent (BoolAttributeQuery): The antecedent (LHS) of the rule.
        succedent (BoolAttributeQuery): The succedent (RHS) of the rule.
        quantifier (Sequence[Quantifier]): The quantifiers of the rule. Used to evaluate the accuracy of the rule. Can be changed.
        contingency_table (List[int]): The contingency table of the rule. Defined as a list with four elements: a, b, c, d.
        condition (Any): **Not yet implemented.** The condition of the rule.
        accuracy (float): The accuracy of the rule calculated with respect to contingency table and quantifier.
    """

    antecedent: BoolAttributeQuery
    "The antecedent (LHS) of the rule."
    succedent: BoolAttributeQuery
    "The succedent (RHS) of the rule."
    quantifiers: Sequence[Quantifier]
    "The quantifiers of the rule. Used to evaluate the accuracy of the rule. Can be changed."
    contingency_table: List[int]
    "The contingency table of the rule. Defined as a list with four elements: a, b, c, d."
    condition: Any
    "**Not yet implemented.** The condition of the rule."

    def __init__(self, antecedent: BoolAttributeQuery, succedent: BoolAttributeQuery, quantifiers: Sequence[Quantifier], contingency_table: List[int], condition=None):
        self.antecedent = deepcopy(antecedent)
        self.succedent = deepcopy(succedent)
        # TODO: Add condition typing
        self.condition = condition
        self.quantifiers = quantifiers
        self.contingency_table = contingency_table

    # LHS and RHS are aliases for antecedent and succedent.
    # DO NOT CHANGE! It breaks the the functionality in the ReReMi method.
    @property
    def lhs(self):
        "Alias for the antecedent of the rule."
        return self.antecedent

    @property
    def rhs(self):
        "Alias for the succedent of the rule."
        return self.succedent

    def posprocessing(self):
        "Posprocessing is done for interval integer values. It merges all interval Boolean attributes with `merge_intervals` function."
        def process(query):
            for expression, _, _ in query:
                if isinstance(expression, BoolAttributeQuery):
                    process(expression)
                elif expression.dtype == pd.Interval:
                    expression.value = merge_intervals(expression.value)

        for query in [self.antecedent, self.succedent]:
            process(query)

    @property
    def accuracy(self):
        "Returns the accuracy of the rule based on the contingency table and the quantifier."
        a, b, c, d = self.contingency_table
        accuracy = dict()
        for quantifier in self.quantifiers:
            accuracy[quantifier] = quantifier.calculate([a, b, c, d])
        return accuracy

    def __str__(self):
        def quantifier_accuracy_str(quantifier, acc):
            quantifier_name = quantifier.__class__.__name__
            acc = round(acc, NUMBER_OF_DECIMAL_PLACES)
            return f"{colored(quantifier_name, Colors.CYAN)}: {acc}"

        accuracy = [
            f"{quantifier_accuracy_str(quantifier, acc)}" for quantifier, acc in self.accuracy.items()]

        result = f"{'; '.join(accuracy)}"
        result += f" | {self.antecedent} {QUANTIFIER_SYMBOL} {self.succedent}"
        return result

    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        if self.quantifiers != other.quantifiers:
            raise ValueError("Quantifiers of the rules must be the same to compare them.")

        accuracy_self = self.accuracy
        accuracy_other = other.accuracy
        for key in accuracy_self.keys():
            if accuracy_self[key] >= accuracy_other[key]:
                return False
        return True
