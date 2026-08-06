from lca_types import leaf, ptwo, ptwo_bin_rel
import networkx as nx
import copy


def get_extended_support(X: set[leaf], R: ptwo_bin_rel) -> set[ptwo]:
    """
    Input: 
        X: A set of leaf nodes.
        R: A dict representing a binary relation on 𝒫₂(X).
    Output: 
        The extended support of R, i.e., supp_plus_R.

    Given a binary relation R, get the extended support supp_plus_R.

    supp_R = { p in 𝒫₂(X) | there is some q in 𝒫₂(X) with pRq or qRp }

    supp_plus_R = supp_R union {(x,x) | x in X}
    """

    out = set(R.keys())
    for qs in R.values():
        for q in qs:
            out.add(q)

    # At this point out = supp_R

    for x in X:
        out.add((x,x))

    # At this point out = supp_plus_R

    return out

# Algorithm 1 in Lindeberg et al. (2026). Inferring DAGs and phylogenetic networks from least common ancestors
def get_R_plus(R: ptwo_bin_rel, X: set[leaf]) -> ptwo_bin_rel:
    """
    Input:
        R: A binary relation on 𝒫₂(X).
        X: A set of leaf nodes.
    Output:
        The supp_plus_R-reflexive-, transitive-, cross-consistent closure of R, called R_plus.

    This is an implementation of Algorithm 1 in Lindeberg et al. (2026). Inferring DAGs and phylogenetic networks from least common ancestors.
        Let S = R
        R1: Add pSp for each p in supp_plus_R
        Repeatedly apply the following rules until they can no longer be applied:
            R2: if pSq and qSr, add pSr
            R3: if ab in supp_plus_R and acSxy and bdSxy for some c,d in X, add abSxy
    """
    supp_plus_R = get_extended_support(X, R)
    S: ptwo_bin_rel = copy.deepcopy(R)
    
    #R1
    for p in supp_plus_R:
        if not p in S:
            S[p] = {p}
        else:
            S[p].add(p)

    while True:

        # R2, applied exhaustively
        S = get_transitive_closure(S)

        # R3, applied exhaustively
        change_made = R3(S, supp_plus_R)
        
        if not change_made:
            break           

    return S

def get_Fcl_R(R: ptwo_bin_rel, F: ptwo_bin_rel, X: set[leaf]) -> ptwo_bin_rel:
    """
    Input:
        R: A binary relation on 𝒫₂(X).
        F: A binary relation on 𝒫₂(X).
        X: A set of leaf nodes.
    Output:
        The supp_plus_R-reflexive-, transitive-, cross-consistent, F-csym closure of R, called Fcl_R.

    This is an implementation of the construction in Theorem 4.7.
        Let S = R
        R1: Add pSp for each p in supp_plus_R
        Repeatedly apply the following rules until they can no longer be applied:
            R2: if pSq and qSr, add pSr
            R3: if ab in supp_plus_R and acSxy and bdSxy for some c,d in X, add abSxy
            R4: if pSq and pFq, add qSq
    """
    supp_plus_R = get_extended_support(X, R)
    S: ptwo_bin_rel = copy.deepcopy(R)

    #R1
    for p in supp_plus_R:
        if not p in S:
            S[p] = {p}
        else:
            S[p].add(p)

    while True:
        # R2, applied exhaustively
        S = get_transitive_closure(S)

        # R3, applied exhaustively
        change_made_1 = R3(S, supp_plus_R)

        # R4, applied exhaustively
        change_made_2 = R4(S, F)

        if change_made_1 is False and change_made_2 is False:
            break

    return S

def R3(S: ptwo_bin_rel, supp_plus: set[ptwo]) -> bool:
    """
        Input:
            S: A binary relation on 𝒫₂(X).
            supp_plus: The extended support of S.
        Output:
            True if one or more applications of the rule R3 was performed, False otherwise.

        Looks at all pairs of keys (a,c) and (b,d) in S.
        For each combination (m,n) among (a,b), (a,d), (c,b), (c,d) in the extended support,
        takes all (x,y)'s in the intersection of S[(a,c)] and S[(b,d)] and adds (m,n)S(x,y).

        Note that this preserves the property that any element {a,b} of 𝒫₂(X) in S has a consistent representation,
        since we only add values to keys already in the extended support, and the extended support uses consistent representation.
        """
    change_made = False
    for ac in S:
        for bd in S:
            # Supported combinations are all of (a,b), (a,d), (c,b), (c,d) that are in the extended support.
            # (b,a), (d,a), (b,c), and (d,c) are tested in a later execution of the nested for-loops.
            supported_combinations = get_supported_combinations(ac, bd, supp_plus)
            if len(supported_combinations) == 0:
                continue

            overlap = S[ac].intersection(S[bd])  # All xy such that acSxy and bdSxy
            if len(overlap) == 0:
                continue

            for p in supported_combinations:
                pre_len = len(S[p])             # Save the length before updates to see if a change was made
                S[p].update(overlap)
                if pre_len != len(S[p]):
                    change_made = True

    return change_made

def get_supported_combinations(ac: ptwo, bd: ptwo, supp_plus: set[ptwo]) -> set[ptwo]:
    """
    Input:
        ac: A tuple (a,c)
        bd: A tuple (b,d)
        supp_plus: The extended support for some relation
    Output:
        All combinations (g,h) where
            g in (a,c)
            and h in (b,d)
            and (g,h) in supp_plus.
    """

    a, c = ac
    b, d = bd

    supported_combinations = set()
    if (a, b) in supp_plus:
        supported_combinations.add((a, b))
    if (a, d) in supp_plus:
        supported_combinations.add((a, d))
    if (c, b) in supp_plus:
        supported_combinations.add((c, b))
    if (c, d) in supp_plus:
        supported_combinations.add((c, d))

    return supported_combinations

def R4(S: ptwo_bin_rel, F: ptwo_bin_rel) -> bool:
    """
    Input:
        S: A binary relation on 𝒫₂(X).
        F: A binary relation on 𝒫₂(X).
    Output:
        True if one or more applications of the rule R4 was performed, False otherwise.

    Look at all (p,q) in both S and F and add (q,p) to S.

    Note that this preserves the property that any element {a,b} of 𝒫₂(X) in S has a consistent representation,
    since we only add values to keys already in the extended support, and the extended support uses consistent representation.
    """
    change_made = False
    for p in S:
        if p not in F:
            continue
        for q in S[p]:
            pre_len = len(S[q])  # Save the length before updates to see if a change was made
            if q in F[p]:
                S[q].update({p})

            if pre_len != len(S[q]):
                change_made = True

    return change_made

def X1(R: ptwo_bin_rel) -> tuple[bool, tuple[ptwo, ptwo] | None]:
    """
    Input:
        R: A binary relation on 𝒫₂(X).
    Output:
        True if the relation R satisfies condition X1 given in Definition 22.

    The condition says that for all a,b,x in X: {a,b} != {x,x} implies ({a,b},{x,x}) not in R.
    Equivalently, for all a,b,x in X: if {a,b}R{x,x}, then {a,b} == {x,x}. 
    """
    for (a, b), pqs in R.items():
        for (p, q) in pqs:                      # Check for each abRpq:
            if p == q and (p != a or p != b):   # if pq = pp, and ab != pp
                return False, ((a,b), (p,q))                  # then the condition is broken
    return True, None

def Y1(Fcl_R: ptwo_bin_rel) -> tuple[bool, tuple[ptwo, ptwo] | None]:
    """
    Input:
        Fcl_R: The F-closure of a binary relation R on 𝒫₂(X).
    Output:
        True if the pair (R,F) of relations satisfies condition Y1 given in Definition 4.11.

    The condition says that for all a,b,x in X: {a,b} != {x,x} implies ({a,b},{x,x}) not in Fcl_R.
    Equivalently, for all a,b,x in X: if {a,b}Fcl_R{x,x}, then {a,b} == {x,x}.
    """
    for (a, b), pqs in Fcl_R.items():
        for (p, q) in pqs:                      # Check for each abRpq:
            if p == q and (p != a or p != b):   # if pq = pp, and ab != pp
                return False, ((a,b), (p,q))                  # then the condition is broken
    return True, None

def X2_resp_Y2(R: ptwo_bin_rel, cl: ptwo_bin_rel) -> tuple[bool, tuple[ptwo, ptwo] | None]:
    """
    Input:
        R: A binary relation on 𝒫₂(X).
        cl: The closure R_plus resp. F-closure Fcl_R of R.
    Output:
        True if the relation R satisfies condition X2 given in Definition 22.
        resp.
        True if the pair (R,F) satisfies condition Y2 given in Definition 4.11.

    The condition says that for all a,b,x,y in X: 
        if {a,b}R{x,y} but it's not the case that {x,y}tc(R){a,b}, 
        then it's not the case that {x,y}cl{a,b}.

    tc(R) is the transitive closure of R.
    """

    tc_R = get_transitive_closure(R)
    
    for ab, xys in R.items():
        for xy in xys:                                      # Check for each (ab, xy) in R.
            if (xy not in tc_R) or (ab not in tc_R[xy]):    # If (xy, ab) not in tc(R),
                if (ab in cl[xy]):                          # and (xy, ab) in cl
                    return False, (ab,xy)                   # then the condition is broken.
            
    return True, None

def get_transitive_closure(R: ptwo_bin_rel) -> ptwo_bin_rel:
    """
    Input:
        R: A binary relation on 𝒫₂(X).
    Output:
        The transitive closure of R.
    
    Transforms R to a digraph and uses the transitive closure command from networkx.
    """

    R_graph = nx.DiGraph(R)
    tc_R_graph = nx.transitive_closure(R_graph)
    tc_R = nx.to_dict_of_lists(tc_R_graph)
    tc_R = {key: set(val) for key, val in tc_R.items()}
    return tc_R

def is_transitive_closure_asymmetric(R: ptwo_bin_rel) -> bool:
    """
    Input:
        R: A binary relation on 𝒫₂(X).
    Output:
        True if transitive closure of R is asymmetric otherwise false.

    Check whether for each (p,q) in tc(R), it holds that (q,p) not in tc(R).
    """

    tc_r = get_transitive_closure(R)
    for p in tc_r:
        for q in tc_r[p]:
            if q in tc_r and p in tc_r[q]:
                return False

    return True

def is_intersection_F_with_cl_R_empty(F: ptwo_bin_rel, cl_R: ptwo_bin_rel) -> bool:
    """
    Input:
        F: A binary relation on 𝒫₂(X).
        cl_R: The closure of a binary relation R on 𝒫₂(X).
    Output:
        True if intersection of F with cl_R is empty.
    """

    for p in F:
        for q in F[p]:
            if p in cl_R and q in cl_R[p]:
                    return False

    return True

def get_R_lca(R: ptwo_bin_rel, F: ptwo_bin_rel) -> ptwo_bin_rel:
    """
    Input:
        R: A binary relation on 𝒫₂(X).
        F: A binary relation on 𝒫₂(X).
    Output:
        R_lca: extended relation R

    R_lca = R union {(ab,ab) : ab in supp_F}
    """
    R_lca: ptwo_bin_rel = copy.deepcopy(R)

    # get supp_F
    supp_F = set(F.keys())
    for qs in F.values():
        for q in qs:
            supp_F.add(q)

    # extend R
    for p in supp_F:
        if p in R_lca:
            R_lca[p].add(p)
        else:
            R_lca[p] = {p}

    return R_lca

def get_equiv_cl(cl: ptwo_bin_rel) -> ptwo_bin_rel:
    """
    Input:
        cl: The closure R_plus resp. F-closure Fcl_R of a binary relation R on 𝒫₂(X).
    Output:
        An equivalence relation equiv_r_plus resp. equiv_fcl_r as described in Definition 25 resp. Definition 4.14.
        
    The relation equiv_cl is a binary relation on the extended support of R,
    and defined such that p equiv_cl q iff p cl q and q cl p.
    """

    equiv_cl: ptwo_bin_rel = {p: {p} for p in cl.keys()}   # cl is supp_plus_R-reflexive, so (p,p) is in cl for all p in the extended support.
                                                            # This is mainly for convenience to avoid key errors in the next part.

    for p, qs in cl.items():
        for q in qs:                        # For each (p,q) in cl:
            if p in cl[q]:                  # if (q,p) in cl,
                equiv_cl[p].add(q)         # then add (p,q) to equiv_cl

    return equiv_cl


def get_q_set(equiv_cl: ptwo_bin_rel) -> set[ptwo]:
    """
    Input:
        equiv_cl: An equivalence relation on the extended support of some relation R.
    Output:
        A set Q_set containing one element from each equivalence class of equiv_cl.
    """

    to_keep = set()
    to_remove = set()
    for a in equiv_cl.keys():
        if a in to_remove:
            continue
        to_keep.add(a)
        bs = equiv_cl[a]
        to_remove.update(bs)
        
    return to_keep


def get_order_cl(cl: ptwo_bin_rel, Q_set: set[ptwo]) -> ptwo_bin_rel:
    """
    Input:
        cl: The closure R_plus resp. F-closure Fcl_R of a binary relation R on 𝒫₂(X).
        Q_set: the set of equivalence classes in equiv_r_plus resp. equiv_Fcl_R.
    Output:
        An ordering of the equivalence classes in Q_set as defined in Definition 25 resp. Definition 4.14.

    For two classes [p] and [q] in Q_set, we have that [p] <= [q] iff p cl q.
    """

    order_cl = {p: {p} for p in Q_set}  # The reflexive pairs are part of the ordering,
                                        # but will not be represented in the canonical DAG
                                        # since we only add edges between distinct classes

    for p in Q_set:
        for q in Q_set:
            if q in cl[p]:
                order_cl[p].add(q)

    return order_cl

def get_canonical_dag(order_cl: ptwo_bin_rel) -> nx.DiGraph:
    """
    Input:
        order_cl: An ordering of the equivalence classes of equiv_r_plus resp. equiv_fcl_r.
    Output:
        The canonical DAG of R resp. (R,F) as a networkx DiGraph.

    See Definition 26 resp. Definition 4.15.
    The canonical DAG is the Hasse Diagram of the poset (Q_set, order_cl) with leaves (a,a) renamed to a.
    """

    G = nx.DiGraph(order_cl).reverse()            # reverse it so we get edges q -> p instead of p -> q
    G.remove_edges_from(nx.selfloop_edges(G))     # remove the self-loops
    
    # Find all classes [aa]
    leaf_list = []
    for node in G.nodes:
        if node[0] == node[1]: #type: ignore
            leaf_list.append(node)
    
    leaf_dict = {node: node[0] for node in leaf_list} # Rename each (a,a) to a
    G = nx.relabel_nodes(G, leaf_dict)
    G = nx.transitive_reduction(G)

    return G

def get_FR_extension(R: ptwo_bin_rel, F: ptwo_bin_rel, X: set[leaf], G_RF: nx.DiGraph) -> nx.DiGraph:
    """
    Input:
        R: A binary relation on 𝒫₂(X).
        F: A binary relation on 𝒫₂(X).
        X: A set of leaf nodes.
        G_RF: The canonical DAG of (R,F) as a networkx DiGraph.
    Output:
        The FR-extension of G_RF as defined before Observation 4.2.

    Computes the FR-extension of the canonical DAG of (R,F), i.e., for all xy in supp_F setminus supp_plus_R, apply a
    xy-extension to G_RF, i.e., add new vertices u,v and the arcs (u,x),(u,y),(v,x),(v,y).
    """

    G = G_RF.copy()

    supp_plus_R = get_extended_support(X, R) # compute support
    supp_plus_F = get_extended_support(X, F)

    # since R,F are both relations on P_2(X), supp_F \ supp_plus_R = supp_plus_F \ supp_plus_R

    for (x,y) in supp_plus_F:
        if (x,y) not in supp_plus_R:
            edges = [
                (f"u_{x, y}", x),
                (f"u_{x, y}", y),
                (f"v_{x, y}", x),
                (f"v_{x, y}", y),
            ]

            G.add_edges_from(edges)

    return G

def get_network(G: nx.DiGraph) -> nx.DiGraph:
    """
    Input:
        G: Some DAG as networkx DiGraph.
    Output:
        The network obtained from G by adding a unique root and connecting it to all roots of G.

    Given the canonical DAG of R, this provides the canonical network of R, see Definition 36.
    """

    N = G.copy()

    roots = find_roots(N)             # Find all roots of G

    if len(roots) != 1:
        for node in roots:
            N.add_edge("rho", node)   # If there are multiple roots, connect them all as children to a new root rho.

    return N

def find_roots(G: nx.DiGraph) -> set[ptwo]:
    """
    Input:
        G: A networkx DiGraph
    Output:
        The set of root nodes in G 
    """
    roots = set()
    for node, degree in G.in_degree:
        if degree == 0:                 # A node is a root if it has indegree 0
            roots.add(node)
    return roots



def unify_representation(S: ptwo_bin_rel) -> ptwo_bin_rel:
    """
    Input:
        S: a dictionary representing a binary relation on 𝒫₂(X), with some sets {a,b} possibly represented as both (a,b) and (b,a).
    Output:
        Modifies S and returns it as a new representation of the relation where any element {a,b} of 𝒫₂(X) now has a consistent representation (a,b) such that a <= b.
    """

    for (p, q) in S:
        if p > q:
            if (q, p) in S:
                S[(q, p)].update(S.pop((p, q)))    # adds all elements of S[(p,q)] to S[(q, p)] and removes S[(p,q)]
            else:
                S[(q, p)] = S.pop((p, q))          # moves S[(p,q)] to S[(q,p)]
    
    # Goes over all values (right-hand sides of the relation) 
    # and saves any entries (p,q)S(x,y) where (y,x) has already been decided as canonical.
    to_reverse = []
    for pq, xys in S.items():
        for (x, y) in xys:
            if x > y:
                to_reverse.append((pq, (x, y)))

    # for each saved entry (p,q)S(x,y), remove it and add the canonical representation (p,q)S(y,x)
    for (pq, (x, y)) in to_reverse:
        S[pq].remove((x, y))
        S[pq].add((y, x))

    return S