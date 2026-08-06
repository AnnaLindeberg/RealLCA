import csv


"""
We distinguish between two expected file formats for Realizability and RF-realizability. The program automatically 
recognizes the format.  

REALIZABILITY 
The expected format for a csv-file is that the first line lists all of the leaves, and every line after that uses 4 values to describe a constraint.

So the relation R on P_2(X) with X = {a,b,c,x,y,z} and constraints abRxy, acRxy and xyRbc would look like this:

a,b,c,x,y,z
a,b,x,y
a,c,x,y
x,y,b,c

RF-REALIZABILITY
The expected input format is a csv-file containing three blocks separated by the dot symbol (.). The first block only 
consists of one line defining the leaf set. The second and third block contains the required and forbidden LCA-constraints, 
respectively, with one LCA-constraint per row. 

So the pair (R,F) of relations on P_2(X) with X = {a,b,c,x,y,z} and 
- required constraints abRxy, acRxy, and xyRbc and
- forbidden constraints xyFab
would look like this:

a,b,c,x,y,z
.
a,b,x,y
a,c,x,y
x,y,b,c
.
x,y,a,b
"""

def get_constraint(relation: dict, leaves: set, i: int, constraint: list) -> dict:
    """
    Input:
        relation: dictionary of constraints
        leaves: set of leaves
        i: number of the constraint in input
        constraint: list with four values representing a constraint
    Output:
        relation where new constraint is added
    """

    if len(constraint) < 4:
        raise ValueError(
            f"Wrong formatting for constraint nr {i}, too few values. Constraint abScd should be written a,b,c,d")
    if len(constraint) > 4:
        raise ValueError(
            f"Wrong formatting for constraint nr {i}, too many values. Constraint abScd should be written a,b,c,d")

    a, b, c, d = constraint
    a, b, c, d = a.strip(), b.strip(), c.strip(), d.strip()

    if (a not in leaves
            or b not in leaves
            or c not in leaves
            or d not in leaves):
        raise ValueError(
            f"Constraint nr {i} mentions a leaf not in the leaf set. List all leaves on the first line. Constraint abScd should be written a,b,c,d")

    if (a, b) not in relation:
        relation[(a, b)] = set()
    relation[(a, b)].add((c, d))

    return relation


def read_constraints_csv(filename: str) -> (tuple[set, dict] | tuple[set, dict, dict]):
    """
    Input:
        filename: A string with the name of a csv-file describing a leaf set X and one or two relations on 𝒫₂(X).
    Output:
        The leaf set as a set of strings and the relations as dictionaries R and F.
        R[p] is a set such that q is in R[p] iff pRq. Similar for F.

    The program automatically recognizes whether one or two relations are given.
    """
    with open(filename) as file:

        rdr = csv.reader(file)

        # get leaves
        leaves = rdr.__next__()
        leaves = {leaf.strip() for leaf in leaves}

        # decide whether required or required & forbidden constraints given
        constraint = rdr.__next__()
        if constraint != ["."]:
            # get required constraints
            R = get_constraint({}, leaves, 0, constraint)

            for i, constraint in enumerate(rdr):
                R = get_constraint(R, leaves, i+1, constraint)

            return leaves, R

        else:
            # get required and forbidden constraints
            R = {}
            F = {}
            flag_required_forbidden = False

            for i, constraint in enumerate(rdr):
                if constraint == ["."]:
                    flag_required_forbidden = True
                elif not flag_required_forbidden:
                    R = get_constraint(R, leaves, i, constraint)
                else:
                    F = get_constraint(F, leaves, i, constraint)

            return leaves, R, F