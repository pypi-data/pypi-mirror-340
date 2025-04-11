"""
    This file contains the implementation of quantifiers used in the rules.
    Quantifiers are used to describe interesting relationships between antecedent (LHS) and succedent (RHS). Their accuracy are calculated based on contingency table of rule.

    For more information about quantifiers, please refer to the following paper:
    - Classes of Association Rules: An Overview [5]
"""
from typing import List


#
# Abstract classes
#
class Quantifier():
    "Abstract class for quantifiers"

    def calculate(self, quadruple: List[int]) -> float:
        "Calculate the quantifier based on contingency table."
        raise NotImplementedError

    def feasibility(self, quadruple: List[int]) -> bool:
        "Check whether the quantifier is feasible based on contingency table."
        raise NotImplementedError


class Statistical(Quantifier):
    "Abstract class for statistical quantifiers. They define complex formulas that should be fulfill by contingency table."

    def __init__(self, p: float):
        self.p = p


class Base(Quantifier):
    "Abstract class for Base quantifiers. Quantifiers has condition on the number of rows that must be fulfill by both the antecedent and the succedent."

    def __init__(self, base: int):
        self.base = base


class Founded(Statistical):
    "Abstract class for founded statistical quantifiers. In addition to the statistical quantifier formula, they contain a base condition."

    def __init__(self, p: float, base: int):
        self.p = p
        self.base = base
        self.base_quantifier = AbsoluteBase(base)


#
# Quantifiers
#
class Jaccard(Statistical):
    "Formula: a / (a + b + c)"

    def __init__(self):
        pass

    def calculate(self, quadruple: List[int]) -> float:
        a, b, c, _ = quadruple
        if a + b + c == 0:
            return 0
        return a / (a + b + c)


class Implication(Statistical):
    "Formula: a / (a+b) >= p"

    def __init__(self, p: float):
        super().__init__(p)

    def calculate(self, quadruple: List[int]) -> float:
        a, b, _, _ = quadruple
        if a + b == 0:
            return 0
        return a / (a + b)

    def feasibility(self, quadruple: List[int]):
        a, b, _, _ = quadruple
        if a + b == 0:
            return False
        return a / (a + b) >= self.p


class DoubleImplication(Statistical):
    "Formula: a / (a + b + c) >= p"

    def __init__(self, p: float):
        super().__init__(p)

    def calculate(self, quadruple: List[int]):
        a, b, c, _ = quadruple
        if a + b + c == 0:
            return 0
        return a / (a + b + c)

    def feasibility(self, quadruple: List[int]):
        a, b, c, _ = quadruple
        if a + b + c == 0:
            return False
        return a / (a + b + c) >= self.p


class Confidence(Statistical):
    "Formula: a / (a + b)"

    def __init__(self, conf: float):
        self.conf = conf

    def calculate(self, quadruple: List[int]) -> float:
        a, b, _, _ = quadruple
        if a + b == 0:
            return 0
        return a / (a + b)

    def feasibility(self, quadruple: List[int]):
        a, b, _, _ = quadruple
        if a + b == 0:
            return False
        return a / (a + b) >= self.conf


class FoundedImplication(Founded):
    "Formula: a/(a+b) >= p and a >= base"

    def __init__(self, p: float, base: int):
        super().__init__(p, base)

    def calculate(self, quadruple: List[int]) -> float:
        a, b, _, _ = quadruple
        if a < self.base:
            return 0
        if a + b == 0:
            return 0
        return a / (a + b)

    def feasibility(self, quadruple: List[int]):
        a, b, _, _ = quadruple
        if a + b == 0:
            return False
        return a >= self.base and a / (a + b) >= self.p


class FoundedDoubleImplication(Founded):
    "Formula: a / (a + b + c) >= p and a >= base"

    def __init__(self, p: float, base: int):
        super().__init__(p, base)

    def calculate(self, quadruple: List[int]) -> float:
        a, b, c, _ = quadruple
        if a < self.base:
            return 0
        if a + b + c == 0:
            return 0
        return a / (a + b + c)

    def feasibility(self, quadruple: List[int]):
        a, b, c, _ = quadruple
        if a + b + c == 0:
            return False
        return a >= self.base and a / (a + b + c) >= self.p


class AbsoluteBase(Base):
    "Formula: a >= base"

    def __init__(self, base: int):
        super().__init__(base)

    def calculate(self, quadruple: List[int]) -> float:
        a, _, _, _ = quadruple
        if a < self.base:
            return 0
        return a

    def feasibility(self, quadruple: List[int]) -> bool:
        a, _, _, _ = quadruple
        return a >= self.base


class RelativeBase(Base):
    "Formula: a / (a + b + c + d) >= base / 100"

    def __init__(self, base: int):
        super().__init__(base)

    def calculate(self, quadruple: List[int]) -> float:
        a, b, c, d = quadruple
        if a + b + c + d == 0:
            return 0
        if a / (a + b + c + d) < (self.base / 100):
            return 0
        return a

    def feasibility(self, quadruple: List[int]) -> bool:
        a, b, c, d = quadruple
        if a + b + c + d == 0:
            return False
        return a / (a + b + c + d) >= self.base / 100


Support = RelativeBase
"Support quantifier is equivalent to RelativeBase"
