"""
    This file contains classes for representing cedents in GUHA (LISp-Miner).
"""

from enum import Enum
from typing import Union
from ..coefficients import Coefficient
from ..logic import LogicalOperator
from ..utils import Colors, colored


class GaceType(Enum):
    "Indicates how the attribute is generated in the formula. If GACE is positive, the attribute is generated only without negation. If GACE is negative, the attribute is generated only with negation. If GACE is both, the attribute is generated with and without negation."
    POSITIVE = "positive"
    NEGATIVE = "negative"
    BOTH = "both"


class Literal:
    """Defines how an attribute is presented (generated) in the formula.

    Attributes:
        attribute (str): The name of the literal attribute.
        coefficient (Coefficient): The coefficient that will be used to generate categories of attribute. Defines how the categories (values) of attribute should be grouped.
        gace (GaceType): Indicates whether or not to use the nagation. Default is positive.
    """

    attribute: str
    "The name of the attribute."
    coefficient: Coefficient
    "The coefficient that will be used to categories of attribute. Defines how the categories (values) of attribute should be grouped."
    gace: GaceType
    "Indicates whether or not to use the nagation."

    def __init__(
            self,
            attribute: str,
            coefficient: Coefficient,
            gace: GaceType = GaceType.POSITIVE
            ):
        self.attribute = attribute
        self.coefficient = coefficient
        self.gace = gace

    def __str__(self):
        return f"{self.attribute} ({self.coefficient.__class__.__name__}, {self.coefficient.start} - {self.coefficient.end})"


class PartialCedent:
    """Act like group for Literals. It can be used to group multiple Literals based on their semantic meaning.
    For example you can use it to group mammals in one group and climate in another group.

    Attributes:
        literals (list[Literal]): The list of Literals that can be used to generate formula (or part of formula).
        min_length (int): The minimum number of Literals in generated formula. Default is 1.
        max_length (int): The maximum number of Literals in generated formula. Default value is number of literals.
        operation (LogicalOperator): The logical operator that will be used to combine Literals. Default is conjunction.
        name (str): The name of this Partial Cedent.
    """

    literals: list[Literal]
    "The list of Literals that can be used to generate formula (or part of formula)."
    min_length: int
    "The minimum number of Literals in generated formula."
    max_length: int
    "The maximum number of Literals in generated formula."
    operator: LogicalOperator
    "The logical operator that will be used to combine Literals."
    name: str
    " The name of this Partial Cedent."

    def __init__(
            self,
            literals: list[Literal],
            min_length: int = 1,
            max_length: Union[int, None] = None,
            operator: LogicalOperator = LogicalOperator.CONJUNCTION,
            name: str = ""
            ):

        if max_length is None:
            max_length = len(literals)

        if max_length < min_length:
            raise ValueError("Maximal length must be greater or equal to minimal length.")

        if not isinstance(min_length, int):
            raise ValueError("Minimal length must be instance of int. Please check order of attributes.")

        if not isinstance(max_length, int):
            raise ValueError("Maximal length must be instance of int. Please check order of attributes.")

        if not isinstance(operator, LogicalOperator):
            raise ValueError("Operator must be instance of LogicalOperator. Please check order of attributes.")

        self.literals = literals
        self.min_length = min_length
        self.max_length = max_length
        self.operator = operator
        self.name = name

    def __str__(self):
        return f"Partial Cedent – {self.name}: " + "; ".join(map(str, self.literals))


class Cedent():
    """It is used to group multiple Partial Cedents.

    Attributes:
        partial_cedents (list[Cedent]): The list of Partial Cedents that can be used to generate formula.
        min_length (int): The minimum number of Literals in generated formula. Default is 0.
        max_length (int): The maximum number of Literals in generated formula. Default is None (no upper limit).
    """

    partial_cedents: list[PartialCedent]
    "The list of Partial Cedents that can be used to generate formula."
    min_length: int
    "The minimum number of Literals in generated formula."
    max_length: int
    "The maximum number of Literals in generated formula. Default value is sum of maximal values of Partial Cedents."

    def __init__(
            self,
            partial_cedents: list[PartialCedent],
            min_length: int = 1,
            max_length: Union[int, None] = None
            ):

        if max_length is None:
            max_length = sum([pc.max_length for pc in partial_cedents])

        if max_length < min_length:
            raise ValueError("Maximal length must be greater or equal to minimal length.")

        # Warning for user
        for pc in partial_cedents:
            if pc.min_length > max_length:
                print(f"{colored('Warning:', Colors.RED)} Partial cedent {pc.name} has minimal length ({pc.min_length}) greater than maximal length of this cedent ({max_length}), therefore it can't be used in generation.")

        self.partial_cedents = partial_cedents
        self.min_length = min_length
        self.max_length = max_length

    def __str__(self):
        return f"Cedent: [{', '.join([pc.name for pc in self.partial_cedents])}], min_length: {self.min_length}, max_length: {self.max_length}"
