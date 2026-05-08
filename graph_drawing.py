
import networkx as nx
import matplotlib.axes
import matplotlib.pyplot as plt

from lca_types import (
    ptwo,
    ptwo_bin_rel,
)


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

