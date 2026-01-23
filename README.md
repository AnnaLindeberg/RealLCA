# Realizable-LCA-constraints

A python program that checks wether a given collection _R_ of lca-constraints is realizable, and generating the canonical-DAG and canonical-network for _R_ when it is. 

Implementation of Algorithm 1 from [this paper](10.48550/arXiv.2511.07965).




## Installation

The program requires Python 3.12 or higher.

#### Dependencies
* [NetworkX](https://networkx.github.io/)
* [matplotlib](https://matplotlib.org/) (For running main.py as a program. Not needed if you only want to import Algorithm_1)


## Usage and description

The program takes a collection of lca-constraints as input. The expected input format is a csv-file with the leafset defined on the first row, followed by one lca constraint per row. A constraint should be given as 4 values, where the first 2 values are the left hand side and the last two values are the right hand side.

So the relation _R_ on P_2(X) with _X_ = {a,b,c,x,y,z} and constraints ab*R*xy, ac*R*xy and xy*R*bc should be defined like this:
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

The expected input format is a csv-file with the leafset defined on the first row, followed by one lca constraint per row. A constraint should be given as 4 values, where the first 2 values are the left hand side and the last two values are the right hand side.

So the relation R on P_2(X) with X = {a,b,c,x,y,z} and constraints abRxy, acRxy and xyRbc should be defined like this:

a,b,c,x,y,z  
a,b,x,y  
a,c,x,y  
x,y,b,c  

### Options
``` shell
main.py [-h] [-e] [filename]

positional arguments:
  filename             The name of a csv-file specifying a leafset and lca-constraints. 
                       Note that this argument is optional.

options:
  -h, --help           show this help message and exit
  -e, --equiv_classes  Add this option to display all equivalence classes with
                       two or more memembers.
```

### Use as library

You can also import the function Algorithm_1 and use it in your own code. This might be useful if you want to directly access the networkx graphs in the output or want to run it over multiple sets of constraints. 

TODO: Finish describing what parts might be interesting to import and in which module each can be found.


## Citation and references
#Todo: will this be a library? Figure out what to call it. Also find how to do proper citation.

If you use this library in your project or code, please consider citing:
  
  * __Inferring DAGs and Phylogenetic Networks from Least Common Ancestors, A. Lindeberg, A. Alfonsson, V. Moulton, G. E. Scholz, M. Hellmuth (2025)__
