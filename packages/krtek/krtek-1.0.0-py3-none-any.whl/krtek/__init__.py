"""
**Krtek** is a package for mining association rules. It implements the **4ft-Miner** (GUHA) and **ReReMi** (Redescription mining) methods. These methods can be used to automatically generate and validate association rules.

The whole package is designed to be easily extendable with quantifiers, coefficients, or even new methods. The package is very focused on readability and [pythonic](https://peps.python.org/pep-0008/) code. If you want to find out more about some of the implemented features I strongly recommend reading the documented code.

This package is the result of the practical part of [master thesis](https://stag.upol.cz/StagPortletsJSR168/CleanUrl?urlid=prohlizeni-prace-detail&praceIdno=295310) on the [Department of Computer Science, Palacky University, Olomouc](https://www.inf.upol.cz). The aim of the paper was to compare two association rule mining approaches, namely **GUHA** (General Unary Hypotheses Automaton) and **Redescription mining**.
"""

from . import coefficients
from . import computation
from . import quantifiers
from . import utils
from . import logic
from . import guha
from . import redescription

from .logic import BoolAttribute, BoolAttributeQuery, LogicalOperator, Rule
from .guha import FourFtMiner, Literal, PartialCedent, Cedent
from .redescription import ReReMiMiner

__all__ = [
    'FourFtMiner',
    'ReReMiMiner',
    'LogicalOperator',
    'BoolAttribute',
    'BoolAttributeQuery',
    'Rule',
    'Literal',
    'PartialCedent',
    'Cedent',
    'coefficients',
    'computation',
    'guha',
    'logic',
    'quantifiers',
    'redescription',
    'utils',
]
