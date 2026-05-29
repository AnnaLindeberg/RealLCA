# -*- coding: utf-8 -*-

import networkx as nx

from lca_types import leaf, ptwo, ptwo_bin_rel
from parse_input import read_constraints_csv
from graph_drawing import draw_DAG, get_legend_text, add_legend
from helper_functions import (
    unify_representation,
    get_R_plus,
    X1,
    X2,
    get_equiv_r_plus,
    get_q_set,
    get_order_r_plus,
    get_canoncial_dag,
    get_canoncial_network
)
   

def Algorithm_2(X: set[leaf], R: ptwo_bin_rel) \
    -> tuple[bool, tuple[nx.DiGraph, nx.DiGraph, ptwo_bin_rel, set[ptwo]] | str]:
    """
    Input:
        X: Some ground set
        R: A binary relation on 𝒫₂(X) ⨉ 𝒫₂(X).
    Output:
        True, (G_r, N_r, equiv_R_plus, Q_set) if the relation R is realizable.

        False, "Xi: ab,cd" if the rellation R is not realizable, where Xi says 
        which condition was broken and ab,cd is the constraint the violated the condition.

    In the case when R is realizable, equiv_R_plus and Q_set are returned to be used in the legend of the drawn graphs.
    """
    R = unify_representation(R)                         # Make sure the representations of elements {a,b} = {b,a} are consistent.
    R_plus = get_R_plus(R, X)                           # 1 & 2 - The extended support is computed inside of get_R_plus and stored implicitly as the keys of R_plus
    bool_X1, falsifying_constraint_X1 = X1(R) 
    bool_X2, falsifying_constraint_X2 = X2(R, R_plus)
    if bool_X1 and bool_X2:                             # 3
        equiv_R_plus = get_equiv_r_plus(R_plus)                      
        Q_set = get_q_set(equiv_R_plus)                 # 4
        order_R_plus = get_order_r_plus(Q_set, R_plus)  
        G_r = get_canoncial_dag(order_R_plus)           # 5
        N_r = get_canoncial_network(G_r)                # 6
        return True, (G_r, N_r, equiv_R_plus, Q_set)    # 7
    elif not bool_X1:                                   
        return False, f"X1: {falsifying_constraint_X1}" 
    else:
        return False, f"X2: {falsifying_constraint_X2}"    





def get_parameters() -> tuple[str, bool]:
    """ 
    Input:
        None
    Output:
        A tuple (constraint_file, with_legend) where constraint_file is either None or a filename, and with_legend is a boolean.

    Commandline interface for getting the name of the csv file with the constraints and whether to add a legend to the drawn graphs.
    """    
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

    with_legend = args.equiv_classes

    return constraint_file, with_legend


def main():
    """
    Main entry point for the program. 
    Gets paramters, reads constraints from csv-file, runs Algorihtm_2
    and visuales the result if the relation is realizable, otheriwse prints
    the condition that was broken.
    """

    # Imports done here since needed to run as a program, but not for Algorithm_1 to work if imported to other project
    import matplotlib.pyplot as plt

    constraint_file, with_legend = get_parameters()

    try:
        X, R = read_constraints_csv(constraint_file)
    except ValueError as e:
        print(e)
        return
    except FileNotFoundError:
        print("The file", constraint_file, "could not be found")
        return

    res = Algorithm_2(X, R)

    match res:
        case True, (G_r, N_r, equiv_R_plus, Q_set):
            draw_DAG(G_r)
            if with_legend:
                legend_text = get_legend_text(Q_set, equiv_R_plus)
                add_legend(legend_text)
            plt.show()

            draw_DAG(N_r)
            if with_legend:
                add_legend(legend_text) # type: ignore . draw_DAG can not change the value of with_legend or legend_text
            plt.show()

        case False, broken_constraint:
            if type(broken_constraint) != str:
                raise TypeError(f"type: str expected, but got: {type(broken_constraint)}")
            print("The relation is not realizable", broken_constraint)
            return
        
        case _:
            raise TypeError(f"Algorithm_2 returned object of type: {type(res)}")



if __name__ == "__main__":
    main()