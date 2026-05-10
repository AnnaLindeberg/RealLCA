# -*- coding: utf-8 -*-

import networkx as nx

from lca_types import leaf, ptwo, ptwo_bin_rel
from parse_input import read_constraints_csv
from graph_drawing import draw_DAG, get_legend_text, add_legend
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
   

def Algorithm_2(X: set[leaf], R: ptwo_bin_rel) -> tuple[bool, tuple[nx.DiGraph, nx.DiGraph] | str]:
    """
    Input:
        X: Some ground set
        R: A binary relation on 𝒫₂(X) ⨉ 𝒫₂(X).
    Output:
        True, (G_r, N_r) if the relation R is realizable.

        False, "Xi: ab,cd" if the rellation R is not realizable, where Xi says 
        which condition was broken and ab,cd is the constraint the violated the condition.
    """
    R = unify_representation(R)                         # Make sure the representations of elements {a,b} = {b,a} are consistent.
    R_plus = get_R_plus(R, X)                           # 1 & 2
    bool_X1, falsifying_constraint_X1 = X1(R) 
    bool_X2, falsifying_constraint_X2 = X2(R, R_plus)
    if bool_X1 and bool_X2:                             # 3
        equiv_R_plus = get_equiv_r_plus(R_plus)         # 4
        Q_set = get_q_set(equiv_R_plus)                 # 5
        order_R_plus = get_order_r_plus(Q_set, R_plus)  # 6
        G_r = get_canoncial_dag(order_R_plus)           # 7
        N_r = get_canoncial_network(G_r)                # 8
        return True, (G_r, N_r)                         # 9
    elif not bool_X1:                                   # 10
        return False, f"X1: {falsifying_constraint_X1}"
    else:
        return False, f"X2: {falsifying_constraint_X2}"    


def Algorithm_2_full_output(X: set[leaf], R: ptwo_bin_rel) -> tuple[bool, list]:
    """
    Input:
        X: Some ground set
        R: A binary relation on 𝒫₂(X) ⨉ 𝒫₂(X).
    Output:
        False and a list with [R, supp_plus_R, R_plus] if the relations is not realizable.
        True and a list with [R, supp_plus_R, R_plus, equiv_R_plus, Q_set, order_R_plus, G_r, N_r] if the relation is realizable.
        
    Does the same thing as Algorithm_2 but also returns the result of each step in the final output.
    """
    R = unify_representation(R)                         # Make sure the representations of elements {a,b} = {b,a} are consistent.
    supp_plus_R = get_extended_support(X, R)            # 1
    R_plus = get_R_plus(R, X)                 # 2
    bool_X1, falsifying_constraint_X1 = X1(R_plus) 
    bool_X2, falsifying_constraint_X2 = X2(R, R_plus)
    if bool_X1 and bool_X2:                             # 3
        equiv_R_plus = get_equiv_r_plus(R_plus)         # 4
        Q_set = get_q_set(equiv_R_plus)                 # 5
        order_R_plus = get_order_r_plus(Q_set, R_plus)  # 6
        G_r = get_canoncial_dag(order_R_plus)           # 7
        N_r = get_canoncial_network(G_r)                # 8
        return True, [R, supp_plus_R, R_plus, equiv_R_plus, Q_set, order_R_plus, G_r, N_r]   
    elif not bool_X1:         
        return False, [R, supp_plus_R, R_plus, "X1", falsifying_constraint_X1]
    else: 
        return False, [R, supp_plus_R, R_plus, "X2", falsifying_constraint_X2]     

def main():
    """
    TODO: Add docstring
    """

    # Imports done here since needed to run as a program, but not for Algorithm_1 to work if imported to other project
    import matplotlib.pyplot as plt
    import argparse

    parser = argparse.ArgumentParser(

    )

    parser.add_argument("filename", 
                        nargs="?", 
                        default=None,
                        help="The name of a csv-file specifying a leafset and lca-constraints. Note that this argument is optional.")
    parser.add_argument('-e', '--equiv_classes', 
                        action='store_true',
                        help="Add this option to display the equivalence classes with two or more memembers."
                        )

    args = parser.parse_args()

    # Get csv file with constraints either as commandline argument or as user input
    if args.filename:
        constraint_file = args.filename
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
    
    with_legend = args.equiv_classes

    if with_legend:
        res = Algorithm_2_full_output(X, R)
        match res:
            case True, [_, _, _, equiv_R_plus, Q_set, _, G_r, N_r]:
                legend_text = get_legend_text(Q_set, equiv_R_plus)

                draw_DAG(G_r)
                add_legend(legend_text)
                plt.show()

                draw_DAG(N_r)
                add_legend(legend_text)
                plt.show()
            case False, [_, _, _, X1_or_X2, broken_constraint]:
                print("The relation is not realizable", f"{X1_or_X2}: {broken_constraint}")
                return
            case _:
                raise TypeError(f"Algorithm_1_full_output returned object of type: {type(res)}")

    else:
        res = Algorithm_2(X, R)
        match res:
            case True, (G_r, N_r):
                draw_DAG(G_r)
                plt.show()
                draw_DAG(N_r)
                plt.show()
            case False, broken_constraint:
                if type(broken_constraint) != str:
                    raise TypeError(f"type: str expected, but got: {type(broken_constraint)}")
                print("The relation is not realizable", broken_constraint)
                return
            case _:
                raise TypeError(f"Algorithm_1 returned object of type: {type(res)}")



if __name__ == "__main__":
    main()