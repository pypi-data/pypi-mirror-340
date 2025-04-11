# Krtek

**Krtek** is a package for mining association rules. It implements the **4ft-Miner** (GUHA) and **ReReMi** (Redescription mining) methods. These methods can be used to automatically generate and validate association rules.

The whole package is designed to be easily extendable with quantifiers, coefficients, or even new methods. The package is very focused on readability and [pythonic](https://peps.python.org/pep-0008/) code. If you want to find out more about some of the implemented features I strongly recommend reading the documented code.

This package is the result of the practical part of [master thesis](https://stag.upol.cz/StagPortletsJSR168/CleanUrl?urlid=prohlizeni-prace-detail&praceIdno=295310) on the [Department of Computer Science, Palacky University, Olomouc](https://www.inf.upol.cz). The aim of the paper was to compare two association rule mining approaches, namely **GUHA** (General Unary Hypotheses Automaton) and **Redescription mining**.

## Installation

To install the library, you can use pip:

```sh
pip install krtek
```

Then you can start using it. You can import it like:

``` python
# As a whole package.
import krtek

# Import only individual parts
# For 4ft-Miner
from krtek import FourFtMiner, Literal, PartialCedent, Cedent, coefficients, quantifiers, utils
# For ReReMi
from krtek import ReReMiMiner, coefficients, quantifiers, utils
```

## Use examples

Here is a sample usage of the package. The first example focuses on mining redescriptions in the **Ecological Niche dataset**, and the second focuses on mining association rules in the **Student Performance dataset** **[7]**. More detailed examples can be found in the examples folder.

### Ecological Niche example:

```python
import pandas as pd
from krtek import ReReMiMiner, coefficients, quantifiers

# Load the data
data_RHS = pd.read_csv("mammals_small/data_RHS.csv")
data_LHS = pd.read_csv("mammals_small/data_LHS.csv")

# Preprocessing
# ...

lhs_attributes = # mammals
rhs_attributes = # temperatures of locations

# Here we can specify how the attributes should be used in the mining task
mammals_coefficients = {mammal: coefficients.OneCategory(True) for mammal in lhs_attributes}
temperature_coefficients = {temperature: coefficients.Sequence(1, 5) for temperature in rhs_attributes}
attributes_coefficients = {**mammals_coefficients, **temperature_coefficients}

# Defines the mining task
task = FourFtMiner(hotel, antecedent, succedent, task = ReReMiMiner(
    data,
    lhs_attributes,
    rhs_attributes,
    initial_pair_size = 10,
    beam_search_size = 10,
    max_side_size = 2,
    min_accuracy = 0.8,
    quantifier = quantifiers.Jaccard,
    operators = ["AND", "OR", "NOT"],
    category_coefficient = attributes_coefficients
)

# Starts the mining task
task.run()

# After the mining task is finished, we can print the statistics and access the results
task.print_run_info()
task.result
```

### Student Performance example:

```python
import pandas as pd
from krtek import FourFtMiner, Literal, PartialCedent, Cedent, coefficients, quantifiers

# Load the data
data_students = pd.read_csv('student performance/student-por.csv', sep=';')

# Preprocessing
# ...

# Here we can specify how the attributes should be used in the mining task
# Partial Cedent – Family
family = PartialCedent([
            Literal("famsize", coefficients.Subset(1, 1)),
            Literal("Pstatus", coefficients.Subset(1, 1)),
            Literal("Mjob", coefficients.Subset(1, 1)),
            Literal("Fjob", coefficients.Subset(1, 1)),
            Literal("guardian", coefficients.Subset(1, 1)),
            Literal("Medu", coefficients.Sequence(1, 2)),
            Literal("Fedu", coefficients.Sequence(1, 2)),
            Literal("famrel", coefficients.Sequence(1, 2)),
        ], 1, 2, name="Family"
    )

antecedent = Cedent([family])

# Partial Cedent – Performance
student_performance = PartialCedent([
            Literal("G3_grade", coefficients.Sequence(1, 2)),
        ],
        1, name="Performance"
    )

succedent = Cedent([student_performance])

# Quantifier specification
quantifier = [quantifiers.FoundedImplication(0.75, 100)]

# Starts the mining task
task = FourFtMiner(data_students, antecedent, succedent, quantifier)

# Starts the mining task
task.run()

# After the mining task is finished, we can print the statistics and access the results
task.print_run_info()
task.result
```

---

## References

**[1]** P. Hájek and T. Havránek, Mechanizing hypothesis formation. 1978. doi: 10.1007/978-3-642-66943-9.

**[2]** E. Galbrun and P. Miettinen, Redescription mining. 2017. doi: 10.1007/978-3-319-72889-6.

**[3]** E. Galbrun and P. Miettinen, “From black and white to full color: extending redescription mining outside the Boolean world,” Statistical Analysis and Data Mining the ASA Data Science Journal, vol. 5, no. 4, pp. 284–303, Apr. 2012, doi: 10.1002/sam.11145.

**[4]** J. Rauch and M. Simunek, “An alternative approach to mining association rules.,” Foundations of Data Mining and Knowledge Discovery, pp. 211–231, Jan. 2005, [Online]. Available: https://dblp.uni-trier.de/rec/series/sci/RauchS05.html.

**[5]** J. Rauch, “Classes of Association Rules: An Overview,” in Studies in computational intelligence, 2008, pp. 315–337. doi: 10.1007/978-3-540-78488-3_19.

**[6]** J. Rauch, M. Šimůnek, D. Chudán, and P. Máša, Mechanizing hypothesis formation: Principles and Case Studies, 1st ed. 2022. doi: 10.1201/9781003091448.

**[7]** Cortez, Paulo, "Student Performance.", UCI Machine Learning Repository, 2008, doi: https://doi.org/10.24432/C5TG7T.

---