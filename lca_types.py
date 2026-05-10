import collections.abc # just for typechecking that we have things that can be used as nodes
from typing import Protocol


class leaf(collections.abc.Hashable, Protocol):
    """
    A leaf is an element of the ground set X. 
    It can be of any type that is both Hashable and Comparable. 
    While only Hashable is stricly necessary for the implementation, we also require 
    that they are Comparable to make it easier to unify the representation of sets of leaves.
    """
    def __lt__(self, other: "leaf") -> bool: ...


type ptwo = tuple[leaf,leaf] 
"""
The type ptwo represents elements in 𝒫₂(X), 1 and 2 element subsets of the leaf set X.  
Since sets are not ordered, {a, b} = {b, a} and {a,a} = {a}. 
They are implemented here as ordered pairs (tuples). 
For tuples (a,b) != (b,a). So we make sure that for each set {a,b}={b,a}, we consistently represent it either only as (a,b) or only as (b,a).   
Similarily since (a,a) != (a,), we always represent {a} = {a,a} as (a,a).
"""

type ptwo_bin_rel = dict[ptwo, set[ptwo]] 
"""
The type ptwo_bin_rel represent a binary relation R over 𝒫₂(X) ⨉ 𝒫₂(X).
A relation R is represented by a dictionary D such that {a,b}R{x,y} if and only if D[(a,b)] contains (x,y).  
"""