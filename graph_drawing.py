
import networkx as nx
import matplotlib.axes
import matplotlib.pyplot as plt

from lca_types import (
    ptwo,
    ptwo_bin_rel,
)

# TODO: Add pydot options


def draw_DAG(G: nx.DiGraph, 
             ax: matplotlib.axes.Axes | None=None
             ) -> None:
    """
    Input:
        G: A networkx DiGraph where internal nodes are tuples of leaves.
        ax (optional): The matplotlib Axes to draw the figure in.
    Output:
        None
    
    Draws the network with layers aligned using matplotlib and networkx multipartite layout.
    """

    for layer, nodes in enumerate(nx.topological_generations(G)):
        for node in nodes:
            G.nodes[node]["layer"] = layer

    # TODO: This is bugged and sometimes draws the network completley wrong. THe idea is to put all leaves on the final layer.
    # leaf_list = []
    # for node in G.nodes:
    #     if type(node) != tuple and node != "rho":   # When constructing the canonical dag/network for R, we relabeled all leaves to not be tuples anymore.
    #         leaf_list.append(node)
    # leaf_layer = max(G.nodes[node]["layer"] for node in leaf_list)

    # for node in leaf_list:
    #     G.nodes[node]["layer"] = leaf_layer

    pos = nx.multipartite_layout(G, subset_key="layer", align="horizontal")
    # The layout puts the root at the bottom, so we flip it
    flipped_pos = {node: (x, -y) for (node, (x,y)) in pos.items()}

    nx.draw(G, pos=flipped_pos, ax=ax, with_labels=True)

def get_legend_text(Q_set: set[ptwo], equiv_R_plus: ptwo_bin_rel) -> list[str]:

    non_leaf_Qs = [ab for ab in Q_set if ab[0] != ab[1]]

    leg_list = []
    for ab in non_leaf_Qs:
        entry = ""
        equivalent_cds = equiv_R_plus[ab]
        for cd in equivalent_cds:
            entry = entry + f"{cd[0]}{cd[1]} = "
        entry = entry.strip(" = ")
        if len(entry) > 2:
            leg_list.append(entry)
            
    return leg_list

def add_legend(legend_text: list[str]) -> None:

    # TODO:
    # ChatGPT inspired solution to add a text-only legend. 
    # Suggestions for other ways of adding the equivalence class info are welcome.
    from matplotlib.lines import Line2D
    handles = [
        Line2D([], [], linestyle="none")
        for _ in legend_text
    ]
    plt.legend(handles, legend_text, title="Equivalence Classes", frameon=False)





def plot_results(realizable: bool, results_list: list) -> None:
    if realizable:
        plot_realizable_results(results_list)
    else:
        plot_non_realizable_results(results_list)


def plot_realizable_results(results_list) -> None:
    R, supp_plus_R, R_plus, equiv_R_plus, Q_set, order_R_plus, G_r, N_r = results_list
    graphs = [
        nx.DiGraph(R).reverse(),
        nx.DiGraph(supp_plus_R).reverse(),
        nx.DiGraph(R_plus).reverse(),
        nx.DiGraph(equiv_R_plus),
        nx.DiGraph(order_R_plus),
        G_r,
        N_r
    ]
    titles = [
        "R",
        "Extended support",
        "R-plus",
        "Equivalence relation",
        "Ordering",
        "Canonical DAG",
        "Canoncial Network"
    ]

    fig = plt.figure(figsize=(12, 10))

    # Row 1: 3 subplots
    axes = []
    for i in range(3):
        ax = fig.add_subplot(3, 3, i + 1)
        axes.append(ax)

    # Row 2: 2 subplots centered (positions 4 and 5 in a 3x3 grid)
    for i in range(3, 5):
        ax = fig.add_subplot(3, 3, i + 1)
        axes.append(ax)

    # Row 3: 2 subplots centered (positions 7 and 8 in a 3x3 grid)
    for i in range(6, 8):
        ax = fig.add_subplot(3, 3, i + 1)
        axes.append(ax)

    for ax, graph, title in list(zip(axes, graphs, titles)):
        if "Canonical" in title:
            draw_DAG(graph, ax=ax)
        else:
            nx.draw(graph, ax=ax, with_labels=True)
        ax.set_title(title)

    plt.tight_layout()


def plot_non_realizable_results(results_list) -> None:
    R, supp_plus_R, R_plus = results_list
    graphs = [
        nx.DiGraph(R).reverse(),
        nx.DiGraph(supp_plus_R).reverse(),
        nx.DiGraph(R_plus).reverse(),
    ]
    titles = [
        "R",
        "Extended support",
        "R-plus"
    ]
    _, axes = plt.subplots(1,3)

    for ax, graph, title in zip(axes, graphs, titles):
        nx.draw(graph, ax=ax, pos=nx.spring_layout(graph), with_labels=True)
        ax.set_title(title)
