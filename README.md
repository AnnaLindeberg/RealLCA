# Realizable and RF-Realizable LCA-Constraints

A python program that 
* checks whether a given collection $R$ of LCA-constraints is (strictly) realizable, and generates the canonical DAG and canonical network for $R$ in the affirmative case. 
* checks whether a given pair $(R,F)$ of collections of required and forbidden LCA-constraints is (strictly) RF-realizable, and generates a phylogenetic DAG and network RF-realizing $(R,F)$ in the affirmative case. 

This program is an implementation of Algorithm 1 and Algorithm 2 from [this paper](https://doi.org/10.1016/j.tcs.2026.116114) and of Algorithm 1 from [this paper](https://doi.org/10.48550/arXiv.2605.03827). 

Depending on your usage, we refer to __Description and Usage for Realizable LCA-Constraints__ or __Description and Usage for RF-Realizable LCA-Constraints__. 

## Installation

The program requires Python 3.12 or higher.

#### Dependencies
* [NetworkX](https://networkx.github.io/)
* [matplotlib](https://matplotlib.org/) (For running main.py as a program. Not needed if you only want to import Algorithm_strict_realizability or Algorithm_strict_RF_realizability.)


## Description and Usage for Realizable LCA-Constraints 

The program takes a collection of LCA-constraints as input. It then tests whether the collection is (strictly) realizable. In the affirmative case, the program provides a plot of the canonical DAG and network. 

### Input File Format 

The expected input format is a csv-file with the leafset defined on the first row, followed by one LCA-constraint per row. A constraint should be given as 4 values, where the first 2 values are the left hand side and the last 2 values are the right hand side.
 
So the relation $R$ on $P_2(X)$ with $X = \{a,b,c,x,y,z\}$ and constraints $ab \ R \ xy$, $ac \ R \ xy$, and $xy \ R \ bc$ should be defined like this:

```
a,b,c,x,y,z
a,b,x,y
a,c,x,y
x,y,b,c
```

### Basic usage
The program can be run by passing the file `main.py` to your python interpreter.

> python3 main.py [input_file]

If no input file was given then the program will prompt you for it.

### Options
``` text
main.py [-h] [-e] [-s] [filename]

positional arguments:
  filename             The name of a csv-file specifying a leaf set and LCA-constraints. 
                       Note that this argument is optional.

options:
  -h, --help           		Show this help message and exit.
  -e, --equiv_classes  		Display a legend of all equivalence classes with two or 
							more members in the plot of the canonical DAG and canonical network. 
  -s, --strict_realization	Test for strict realizability. 
```

## Description and Usage for RF-Realizable LCA-Constraints 

The program takes a pair of collections of required and forbidden LCA-constraints as input. It then tests whether the pair is (strictly) RF-realizable. In the affirmative case, the program provides a plot of a phylogenetic DAG and a phylogenetic network RF-realizing the pair. Note that by choosing $F = \emptyset$, RF-realizability reduces to realizability. 

The user can choose between three definitions for forbidden LCA-constraints described in Definition 4.1 and 5.1 in Ebert and Hellmuth (2026). **F** is implemented as default, while **F$^\npreceq$** and **F$^\text{lca}$** can be set via parameters (see Options).

### Input File Format 

The expected input format is a csv-file containing three blocks separated by the dot symbol (.). The first block only consists of one line defining the leaf set. The second and third block contains the required and forbidden LCA-constraints, respectively, with one LCA-constraint per row. A constraint is given as 4 values, where the first 2 values are the left hand side and the last 2 values the right hand side.

So the pair $(R,F)$ of relations on $P_2(X)$ with $X = \{a,b,c,x,y,z\}$, required constraints $ab \ R \ xy$, $ac \ R \ xy$, and $xy \ R \ bc$ and forbidden constraints $xy \ F \ ab$ should be defined like this:
```
a,b,c,x,y,z
.
a,b,x,y
a,c,x,y
x,y,b,c
. 
x,y,a,b 
```

### Basic usage
The program can be run by passing the file `main.py` to your python interpreter.

> python3 main.py [input_file]

If no input file was given then the program will prompt you for it.


### Options
``` text
main.py [-h] [-e] [-s] [-fnleq] [-flca] [filename]

positional arguments:
  filename             The name of a csv-file specifying a leaf set and required and forbidden LCA-constraints. 
                       Note that this argument is optional.

options:
  -h, --help           		Show this help message and exit.
  -e, --equiv_classes  		Display a legend of all equivalence classes with two or 
							more members in the plot of a RF-realizing DAG and network. 
  -s, --strict_realization	Test for strict RF-realizability. 
  -fnleq, --forbidden_nleq	Test for RF-realizability with F_nleq as definition of forbidden. 
  -flca, --forbidden_lca	Test for RF-realizability with F_lca as definition of forbidden. 
```


## Citation and references

If you use this program in your project or code, please consider citing depending on your usage: 
  
* __A. Lindeberg, A. Alfonsson, V. Moulton, G. E. Scholz, M. Hellmuth (2026). Inferring DAGs and Phylogenetic Networks from Least Common Ancestors.__ [doi:10.1016/j.tcs.2026.116114](https://doi.org/10.1016/j.tcs.2026.116114)
* __P. Ebert, M. Hellmuth (2026). Inferring Phylogenetic Networks from Required and Forbidden LCA-Constraints.__ [arXiv:2605.03827](https://doi.org/10.48550/arXiv.2605.03827)


