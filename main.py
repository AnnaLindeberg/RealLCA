# -*- coding: utf-8 -*-

import networkx as nx
import sys

from lca_types import leaf, ptwo, ptwo_bin_rel
from parse_input import read_constraints_csv
from graph_drawing import draw_DAG
from helper_functions import (
    unify_representation,
    get_extended_support,
    get_R_plus,
    X1,
    X2,
    get_equiv_r_plus,
    get_q_set,
    get_order_r_plus,
    get_canoncial_dag,
    get_canoncial_network
)
   

def Algorithm_1(X: set[leaf], R: ptwo_bin_rel) -> tuple[bool, tuple[nx.DiGraph, nx.DiGraph] | str]:
    """
    Input:
        X: Some ground set
        R: A binary relation on 𝒫₂(X) ⨉ 𝒫₂(X).
    Output:
        False if the relation is not realizable, otherwise returns the Canonical DAG and Canonical Network of R.
    """
    R = unify_representation(R)                         # Make sure the representations of elements {a,b} = {b,a} are consistent.
    supp_plus_R = get_extended_support(X, R)            # 1
    R_plus = get_R_plus(R, supp_plus_R)                 # 2
    bool_X1, falsifying_constraint_X1 = X1(R_plus) 
    bool_X2, falsifying_constraint_X2 = X2(R, R_plus)
    if bool_X1 and bool_X2:                             # 3
        equiv_R_plus = get_equiv_r_plus(R_plus)         # 4
        Q_set = get_q_set(equiv_R_plus)                 # 5
        order_R_plus = get_order_r_plus(Q_set, R_plus)  # 6
        G_r = get_canoncial_dag(order_R_plus)           # 7
        N_r = get_canoncial_network(G_r)                # 8
        return True, (G_r, N_r)                         # 9
    if not bool_X1:                                     # 10
        return False, f"X1: {falsifying_constraint_X1}"
    return False, f"X2: {falsifying_constraint_X2}"    


def Algorithm_1_full_output(X: set[leaf], R: ptwo_bin_rel) -> tuple[bool, list]:
    """
    Input:
        X: Some ground set
        R: A binary relation on 𝒫₂(X) ⨉ 𝒫₂(X).
    Output:
        False and a list with [R, supp_plus_R, R_plus] if the relations is not realizable.
        True and a list with [R, supp_plus_R, R_plus, equiv_R_plus, Q_set, order_R_plus, G_r, N_r] if the relation is realizable.
        
    Does the same thing as Algorithm_1 but also returns the result of each step in the final output.
    """
    R = unify_representation(R)                         # Make sure the representations of elements {a,b} = {b,a} are consistent.
    supp_plus_R = get_extended_support(X, R)            # 1
    R_plus = get_R_plus(R, supp_plus_R)                 # 2
    bool_X1, falsifying_constraint_X1 = X1(R_plus) 
    bool_X2, falsifying_constraint_X2 = X2(R, R_plus)
    if bool_X1 and bool_X2:                             # 3
        equiv_R_plus = get_equiv_r_plus(R_plus)         # 4
        Q_set = get_q_set(equiv_R_plus)                 # 5
        order_R_plus = get_order_r_plus(Q_set, R_plus)  # 6
        G_r = get_canoncial_dag(order_R_plus)           # 7
        N_r = get_canoncial_network(G_r)                # 8
        return True, [R, supp_plus_R, R_plus, equiv_R_plus, Q_set, order_R_plus, G_r, N_r]   
    if not bool_X1:         
        return False, [R, supp_plus_R, R_plus, falsifying_constraint_X1] 
    return False, [R, supp_plus_R, R_plus, falsifying_constraint_X2]     

def main():
    """
    TODO: Add docstring
    """

    # Get csv file with constraints either as commandline argument or as user input
    if len(sys.argv) == 2:
        constraint_file = sys.argv[1]
    else:
        constraint_file = input("Please write the name of a csv file defining a relation: ")

    try:
        X, R = read_constraints_csv(constraint_file)
    except ValueError as e:
        print(e)
        return
    except FileNotFoundError:
        print("The file", constraint_file, "could not be found")
        return

    res = Algorithm_1(X, R)
    match res:
        case True, graphs:
            if type(graphs) != tuple[nx.DiGraph, nx.DiGraph]:
                raise TypeError(f"type: tuple[nx.DiGraph, nx.DiGraph] expected, but got: {type(graphs)}")
            G_r, N_r = graphs
        case False, broken_constraint:
            print("The relation is not realizable", broken_constraint)
            return
        case _:
            raise TypeError(f"Algorithm_1 returned object of type: {type(res)}")


    import matplotlib.pyplot as plt
    draw_DAG(G_r)
    plt.show()
    draw_DAG(N_r)
    plt.show()


if __name__ == "__main__":
    main()