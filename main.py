# -*- coding: utf-8 -*-

import networkx as nx

from lca_types import leaf, ptwo, ptwo_bin_rel
from parse_input import read_constraints_csv
from graph_drawing import draw_DAG, get_legend_text, add_legend
from helper_functions import (
    unify_representation,
    get_R_plus,
    get_Fcl_R,
    is_intersection_F_with_cl_R_empty,
    get_R_lca,
    X1,
    Y1,
    X2_resp_Y2,
    is_transitive_closure_asymmetric,
    get_equiv_cl,
    get_q_set,
    get_order_cl,
    get_canonical_dag,
    get_FR_extension,
    get_network
)

# Algorithm 1 in Ebert and Hellmuth (2026). Inferring Phylogenetic Networks from Required and Forbidden LCA-Constraints
def Algorithm_strict_RF_realizability(X: set[leaf], R: ptwo_bin_rel, F: ptwo_bin_rel, strict_realization: bool, f_nleq: bool, f_lca: bool) \
    -> tuple[bool, tuple[nx.DiGraph, nx.DiGraph, ptwo_bin_rel, set[ptwo]] | str]:
    """
    Input:
        X: Some ground set.
        R: A binary relation on 𝒫₂(X).
        F: A binary relation on 𝒫₂(X).
        strict_realization: boolean (True if we test for strictly RF-realizable).
        f_nleq: boolean (True if we test for RF-realizable with F_nleq as definition of forbidden).
        f_lca: boolean (True if we test for RF-realizable with F_lca as definition of forbidden).
    Output:
        True, (G, N, equiv_Fcl_R, Q_set) if the pair (R,F) of relations is (strictly) RF-realizable.

        False, "Yi: ab,cd" if the pair (R,F) of relations is not (strictly) RF-realizable, where Yi says
        which condition is violated and ab,cd is the constraint that violated the condition.

    This function tests whether (R,F) is (strictly) RF-realizable.
    In the case when (R,F) is (strictly) RF-realizable, equiv_Fcl_R and Q_set are returned to be used in the legend of the drawn graphs.
    """
    R = unify_representation(R)                         # Make sure the representations of elements {a,b} = {b,a} are consistent.
    F = unify_representation(F)

    # RF-realizability w.r.t. F_nleq
    if f_nleq:
        # compare Thm. 5.2: (R,F) is RF-realizable w.r.t. F_nleq iff R realizable and intersection of cl(R) and F is empty.
        Fcl_R = get_Fcl_R(R, {}, X)                  # R is realizable iff (R,{}) is RF-realizable and Fcl(R) = cl(R).
        if not is_intersection_F_with_cl_R_empty(F,Fcl_R):
            return False, f"F intersected with cl_R is non-empty."

    # RF - realizability w.r.t. F_lca
    elif f_lca:
        # compare Thm. 5.3: (R,F) is RF-realizable w.r.t. F_lca iff (R_lca,F) is RF-realizable w.r.t. F.
        R = get_R_lca(R,F)                             # replace R by R_lca
        Fcl_R = get_Fcl_R(R, F, X)                     # 1 & 2

    # RF-realizability w.r.t. F
    else:
        Fcl_R = get_Fcl_R(R, F, X)                     # 1 & 2

    if strict_realization:                             # 3
        if not is_transitive_closure_asymmetric(R):
            return False, f"tc(R) is not asymmetric."

    bool_Y1, falsifying_constraint_Y1 = Y1(Fcl_R)
    bool_Y2, falsifying_constraint_Y2 = X2_resp_Y2(R, Fcl_R)
    if bool_Y1 and bool_Y2:                             # 3
        equiv_Fcl_R = get_equiv_cl(Fcl_R)
        Q_set = get_q_set(equiv_Fcl_R)
        order_Fcl_R = get_order_cl(Fcl_R, Q_set)
        G_RF = get_canonical_dag(order_Fcl_R)           # 4
        G = get_FR_extension(R, F, X, G_RF)             # 5
        N = get_network(G)                              # 6
        return True, (G, N, equiv_Fcl_R, Q_set)         # 7
    elif not bool_Y1:
        return False, f"Y1 is violated by: {falsifying_constraint_Y1}"  # 8
    else:
        return False, f"Y2 is violated by: {falsifying_constraint_Y2}"  # 8
   
# Algorithm 2 in Lindeberg et al. (2026). Inferring DAGs and phylogenetic networks from least common ancestors
# extended by an optional check for strict realizability
def Algorithm_strict_realizability(X: set[leaf], R: ptwo_bin_rel, strict_realization: bool) \
    -> tuple[bool, tuple[nx.DiGraph, nx.DiGraph, ptwo_bin_rel, set[ptwo]] | str]:
    """
    Input:
        X: Some ground set.
        R: A binary relation on 𝒫₂(X).
        strict_realization: boolean (True if we test for strictly realizable).
    Output:
        True, (G_r, N_r, equiv_R_plus, Q_set) if the relation R is (strictly) realizable.

        False, "Xi: ab,cd" if the relation R is not realizable, where Xi says
        which condition is violated and ab,cd is the constraint that violated the condition.

    This function tests whether R is (strictly) realizable.
    In the case when R is realizable, equiv_R_plus and Q_set are returned to be used in the legend of the drawn graphs.
    """
    R = unify_representation(R)                         # Make sure the representations of elements {a,b} = {b,a} are consistent.
    R_plus = get_R_plus(R, X)                           # 1 & 2 - The extended support is computed inside of get_cl and stored implicitly as the keys of R_plus
    bool_X1, falsifying_constraint_X1 = X1(R) 
    bool_X2, falsifying_constraint_X2 = X2_resp_Y2(R, R_plus)
    if strict_realization:                              # 3
        if not is_transitive_closure_asymmetric(R):
            return False, f"tc(R) is not asymmetric."

    if bool_X1 and bool_X2:                             # 3
        equiv_R_plus = get_equiv_cl(R_plus)
        Q_set = get_q_set(equiv_R_plus)                 # 4
        order_R_plus = get_order_cl(R_plus, Q_set)
        G_r = get_canonical_dag(order_R_plus)           # 5
        N_r = get_network(G_r)                          # 6
        return True, (G_r, N_r, equiv_R_plus, Q_set)    # 7
    elif not bool_X1:                                   
        return False, f"X1 is violated by: {falsifying_constraint_X1}" # 8
    else:
        return False, f"X2 is violated by: {falsifying_constraint_X2}" # 8

def RF_realizability(X: set[leaf], R: ptwo_bin_rel, F: ptwo_bin_rel, with_legend: bool, strict_realization: bool, f_nleq: bool, f_lca: bool) -> None:
    """
    Input:
        X: Some ground set.
        R: A binary relation on 𝒫₂(X).
        F: A binary relation on 𝒫₂(X).
        with_legend: boolean (True if we add a legend to plots)
        strict_realization: boolean (True if we test for strictly realizable).
        f_nleq: boolean (True if we test for RF-realizable with F_nleq as definition of forbidden).
        f_lca: boolean (True if we test for RF-realizable with F_lca as definition of forbidden).
    Output:
        None

    This function tests whether (R,F) is (strictly) RF-realizable. In the affirmative case, it provides a plot of a DAG
    and a network that (strictly) RF-realize (R,F) and otherwise provides the reason for why (R,F) is not (strictly) RF-realizable.
    """

    # Imports done here since needed to run as a program, but not for get_Fcl_R to work if imported to other project
    import matplotlib.pyplot as plt

    res = Algorithm_strict_RF_realizability(X, R, F, strict_realization, f_nleq, f_lca)

    match res:
        # (R,F) RF-realizable
        case True, (G, N, equiv_Fcl_R, Q_set):
            draw_DAG(G)
            if with_legend:
                legend_text = get_legend_text(Q_set, equiv_Fcl_R)
                add_legend(legend_text)
            plt.show()

            draw_DAG(N)
            if with_legend:
                add_legend(legend_text)  # type: ignore . draw_DAG cannot change the value of with_legend or legend_text
            plt.show()

        # (R,F) not RF-realizable
        case False, broken_constraint:
            if type(broken_constraint) != str:
                raise TypeError(f"type: str expected, but got: {type(broken_constraint)}")

            strictly = "strictly" if strict_realization else ""
            if f_nleq:
                forbidden = "w.r.t. F_nleq"
            elif f_lca:
                forbidden = "w.r.t. F_lca"
            else:
                forbidden = "w.r.t. F"

            print(f"The pair of relations is not {strictly} RF-realizable {forbidden}, since", broken_constraint)

            return

        case _:
            raise TypeError(f"Algorithm 1 returned object of type: {type(res)}")

    return

def realizability(X: set[leaf], R: ptwo_bin_rel, with_legend: bool, strict_realization: bool) -> None:
    """
    Input:
        X: Some ground set.
        R: A binary relation on 𝒫₂(X).
        with_legend: boolean (True if we add a legend to plots)
        strict_realization: boolean (True if we test for strictly realizable).
    Output:
        None

    This function tests whether R is (strictly) realizable. In the affirmative case, it provides a plot of the canonical
    DAG and network that (strictly) realize R and otherwise provides the reason for why R is not (strictly) realizable.
    """

    # Imports done here since needed to run as a program, but not for get_R_plus (Algorithm 1) to work if imported to other project
    import matplotlib.pyplot as plt

    res = Algorithm_strict_realizability(X, R, strict_realization)

    match res:
        # R realizable
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

        # R not realizable
        case False, broken_constraint:
            if type(broken_constraint) != str:
                raise TypeError(f"type: str expected, but got: {type(broken_constraint)}")

            strictly = "strictly" if strict_realization else ""
            print(f"The relation is not {strictly} realizable, since", broken_constraint)
            return

        case _:
            raise TypeError(f"Algorithm 2 returned object of type: {type(res)}")

    return

def check_validity_of_parameters(real: bool, f_nleq: bool, f_lca: bool) -> None:
    """
    Input:
        real: boolean (True for realizable and False for RF-realizable)
        f_nleq: boolean (True if we test for RF-realizable with F_nleq as definition of forbidden).
        f_lca: boolean (True if we test for RF-realizable with F_lca as definition of forbidden).
    Output:
        None

    Checks that f_nleq and f_lca are not True if we test for realizability and that not both are True otherwise.
    """

    if real and (f_nleq or f_lca):
        raise ValueError("While testing for realizability, parameters -f_nleq and -f_lca cannot be provided.")
    if f_nleq and f_lca:
        raise ValueError(f"Parameters -fnleq and -flca cannot both be provided. ")

def get_parameters() -> tuple[str, bool, bool, bool, bool]:
    """ 
    Input:
        None
    Output:
        A tuple (constraint_file, with_legend, strict_realization, f_nleq, f_lca) where constraint_file is either None or
        a filename and with_legend, strict_realization, f_nleq, and f_lca are booleans

    Commandline interface for getting the name of the csv file with the constraints and further optional parameters
    """    
    import argparse

    parser = argparse.ArgumentParser(

    )

    parser.add_argument("filename", 
                        nargs="?", 
                        default=None,
                        help="The name of a csv-file specifying a leaf set and LCA-constraints. Note that this argument is optional.")
    parser.add_argument('-e', '--equiv_classes', 
                        action='store_true',
                        help="Display the equivalence classes with two or more members in the plot of a (RF-)realizing DAG and network."
                        )
    parser.add_argument('-s', '--strict_realization',
                        action='store_true',
                        help="Test for strict (RF-)realizability."
                        )
    parser.add_argument('-fnleq', '--forbidden_nleq',
                        action='store_true',
                        help="Verify that (R,F) is RF-realizable with F_nleq as definition of forbidden."
                        )

    parser.add_argument('-flca', '--forbidden_lca',
                        action='store_true',
                        help="Verify that (R,F) is RF-realizable with F_lca as definition of forbidden."
                        )

    args = parser.parse_args()

    # get csv file with constraints either as commandline argument or as user input
    if args.filename:
        constraint_file = args.filename
    else:
        constraint_file = input("Please write the name of a csv file defining a relation: ")

    # get optional parameters
    with_legend = args.equiv_classes
    strict_realization = args.strict_realization
    f_nleq = args.forbidden_nleq
    f_lca = args.forbidden_lca

    return constraint_file, with_legend, strict_realization, f_nleq, f_lca

def main():
    """
    Main entry point for the program. 
    Gets parameters, reads constraints from csv-file, tests for realizability or RF-realizability
    and visualizes the result if the relation is realizable resp. RF-realizable, otherwise prints
    the condition that was broken.
    """

    # get parameters
    constraint_file, with_legend, strict_realization, f_nleq, f_lca = get_parameters()

    # read leaf set and constraints
    try:
        tuple = read_constraints_csv(constraint_file)
    except ValueError as e:
        print(e)
        return
    except FileNotFoundError:
        print("The file", constraint_file, "could not be found")
        return

    # recognize whether we test for realizability or RF-realizability and check validity of parameters accordingly
    if len(tuple) == 2:
        check_validity_of_parameters(True, f_nleq, f_lca)
        X, R = tuple
        realizability(X, R, with_legend, strict_realization)
    else:
        check_validity_of_parameters(False, f_nleq, f_lca)
        X, R, F = tuple
        RF_realizability(X, R, F, with_legend, strict_realization, f_nleq, f_lca)

if __name__ == "__main__":
    main()