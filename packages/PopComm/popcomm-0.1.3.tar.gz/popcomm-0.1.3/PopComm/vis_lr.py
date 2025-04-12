import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import FancyArrowPatch
from matplotlib.colors import Normalize


def circle_plot(filtered_lr, edge_width="count", node_colors=None, show_self_interactions=True, cutoff = 0):
    """
    Plot a circular cell-cell interaction network with curved directed edges.

    Parameters:
    - filtered_lr: DataFrame containing 'sender', 'receiver', 'cor', and optionally 'count'.
    - edge_width: Determines edge weights, "cor" (correlation) or "count" (interaction count).
    - node_colors: Dictionary mapping cell types to colors (default: auto-generated colors).
    - show_self_interactions: Whether to display self-interactions.
    """

    fig, ax = plt.subplots(figsize=(10, 10))

    # Create graph
    G = nx.DiGraph()

    # Add nodes
    cell_types = set(filtered_lr["sender"]).union(set(filtered_lr["receiver"]))
    for cell in cell_types:
        G.add_node(cell)

    # Assign colors to nodes
    if node_colors is None:
        unique_colors = plt.cm.get_cmap("tab10", len(cell_types)).colors
        node_colors = {cell: unique_colors[i] for i, cell in enumerate(cell_types)}

    # Add edges and compute edge weights
    edge_dict = {}
    for _, row in filtered_lr.iterrows():
        sender, receiver = row["sender"], row["receiver"]
        weight = row["cor"] if edge_width == "cor" else 1

        if (sender, receiver) in edge_dict:
            edge_dict[(sender, receiver)] += weight
        else:
            edge_dict[(sender, receiver)] = weight

    edge_dict = {k: v for k, v in edge_dict.items() if v >= cutoff}
    
    
    # Compute node sizes
    node_weights = {node: 0 for node in G.nodes()}
    for (sender, receiver), weight in edge_dict.items():
        node_weights[sender] += weight
        node_weights[receiver] += weight

    node_sizes = np.array(list(node_weights.values()))
    node_sizes = (node_sizes - node_sizes.min()) / (node_sizes.max() - node_sizes.min() + 1e-6) * 2000 + 300

    # Layout nodes in a circle
    pos = nx.circular_layout(G)

    # Edge width and color normalization adjustments
    all_edges = list(edge_dict.keys())

    # Select only non-self-loops
    non_self_edges = [(s, r) for s, r in all_edges if s != r]

    # Extract edge weights
    all_weights = np.array([edge_dict[e] for e in all_edges])
    non_self_weights = np.array([edge_dict[e] for e in non_self_edges]) if non_self_edges else np.array([1])

    # Normalize edge widths
    if show_self_interactions:
        norm_weights = (all_weights - all_weights.min()) / (all_weights.max() - all_weights.min() + 1e-6)
    else:
        norm_weights = (all_weights - non_self_weights.min()) / (non_self_weights.max() - non_self_weights.min() + 1e-6)

    # Normalize edge colors
    norm = plt.Normalize(vmin=non_self_weights.min() if not show_self_interactions else all_weights.min(),
                            vmax=non_self_weights.max() if not show_self_interactions else all_weights.max())
    
    # Draw edges first
    for i, ((sender, receiver), weight) in enumerate(edge_dict.items()):
        ax.annotate("",
                    xy=pos[receiver], xycoords='data',
                    xytext=pos[sender], textcoords='data',
                    arrowprops=dict(arrowstyle="-|>",
                                    lw=norm_weights[i] * 5 + 1,  # 这里控制箭头粗细
                                    color=plt.cm.coolwarm(norm(weight)),
                                    shrinkA=15, shrinkB=15,
                                    connectionstyle="arc3,rad=0.3"))

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color=[node_colors[n] for n in G.nodes()], 
                           node_size=node_sizes, edgecolors="black", ax=ax)

    # Draw self-loops
    if show_self_interactions:
        for node in G.nodes():
            if (node, node) in edge_dict:
                weight = edge_dict[(node, node)]
                edge_color = plt.cm.coolwarm(norm(weight))

                # Calculate self-loop position
                node_pos = pos[node]
                loop_shift = np.array([0.05, 0.05])
                loop_pos = node_pos + loop_shift

                # Draw self-loop (curved line)
                loop = plt.Circle(loop_pos, 0.07, color=edge_color, fill=False, lw=norm_weights[all_edges.index((node, node))] * 5 + 1)
                ax.add_patch(loop)

    # Add color bar
    sm = plt.cm.ScalarMappable(cmap=plt.cm.coolwarm, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, fraction=0.03, pad=0.04)
    cbar.set_label("Interaction Count" if edge_width == "count" else "Correlation")

    # Adjust text labels
    for node, (x, y) in pos.items():
        ax.text(x, y, node, fontsize=12, ha="center", va="center",
                bbox=dict(facecolor="white", edgecolor="none", alpha=0.7))  # 避免文字和节点颜色冲突

    plt.axis("off")
    plt.show()

def dot_plot(filtered_lr, top_n=5, axis="LR-SR", size_scale=1500, min_size=5, selected_LR=None, figsize=(12, 8)):
    """
    Create a dot plot where:
    - Rows and columns can be switched based on `axis`.
    - Dot size is scaled based on correlation (`cor`).
    - Dot color represents -log10(p_val).
    - Users can select specific LR pairs to plot.
    - Users can adjust figure size.
    - A size legend is placed far right to prevent overlap with the color legend.

    Parameters:
    - filtered_lr: DataFrame containing 'ligand', 'receptor', 'sender', 'receiver', 'cor', 'p_val'.
    - top_n: Number of top interactions to select per sender-receiver pair (default=5).
    - axis: Determines row/column configuration:
        - "LR-SR" (default): Rows = Ligand-Receptor pairs, Columns = Sender-Receiver pairs.
        - "SR-LR": Rows = Sender-Receiver pairs, Columns = Ligand-Receptor pairs.
    - size_scale: Scaling factor for dot sizes (default=1500).
    - min_size: Minimum dot size to ensure visibility (default=5).
    - selected_LR: List of ligand-receptor pairs to plot (e.g., ["EGF_EGFR", "TGFB1_TGFBR1"]). Default None (plot top_n per sender-receiver).
    - figsize: Tuple (width, height) to control figure size (default=(12, 8)).
    """
    # Create ligand-receptor (LR) pair and sender-receiver (SR) pair identifiers
    filtered_lr["LR_pair"] = filtered_lr["ligand"] + "_" + filtered_lr["receptor"]
    filtered_lr["SR_pair"] = filtered_lr["sender"] + "_" + filtered_lr["receiver"]

    # Convert -log10(p_val) for color mapping
    # TODO: set p val mininal
    filtered_lr["log_pval"] = -np.log10(filtered_lr["p_val"])
    
    # Scale dot size with more variation
    min_cor, max_cor = filtered_lr["cor"].min(), filtered_lr["cor"].max()
    filtered_lr["cor_size"] = ((filtered_lr["cor"] - min_cor) / (max_cor - min_cor + 1e-6)) ** 2 * size_scale + min_size  # Squared for better contrast

    # Filter data based on user selection or top_n
    if selected_LR:
        filtered_lr = filtered_lr[filtered_lr["LR_pair"].isin(selected_LR)]
    else:
        filtered_lr = (
            filtered_lr.sort_values(by=["SR_pair", "cor"], ascending=[True, False])
            .groupby("SR_pair")
            .head(top_n)
        )

    # Determine row & column assignments
    if axis == "LR-SR":
        row_label, col_label = "LR_pair", "SR_pair"
    elif axis == "SR-LR":
        row_label, col_label = "SR_pair", "LR_pair"
    else:
        raise ValueError("Invalid axis value. Choose 'LR-SR' or 'SR-LR'.")

    # Pivot data for plotting
    row_values = filtered_lr[row_label].unique()
    col_values = filtered_lr[col_label].unique()

    # Create mapping of row/col values to numeric indices
    row_mapping = {r: i for i, r in enumerate(row_values)}
    col_mapping = {c: i for i, c in enumerate(col_values)}

    # Prepare data for scatter plot
    x_vals = [col_mapping[c] for c in filtered_lr[col_label]]
    y_vals = [row_mapping[r] for r in filtered_lr[row_label]]
    sizes = filtered_lr["cor_size"]
    colors = filtered_lr["log_pval"]

    # Create the figure with user-defined figsize
    fig, ax = plt.subplots(figsize=figsize)
    
    # Scatter plot with color and size mapping
    scatter = ax.scatter(x_vals, y_vals, s=sizes, c=colors, cmap="coolwarm", edgecolors="black", alpha=0.8)

    # Formatting
    ax.set_xticks(range(len(col_values)))
    ax.set_xticklabels(col_values, rotation=90, fontsize=10)
    ax.set_yticks(range(len(row_values)))
    ax.set_yticklabels(row_values, fontsize=10)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title(
        f"Ligand-Receptor Interaction Dot Plot\n({'Selected LR' if selected_LR else f'Top {top_n} per Sender-Receiver'})", 
        fontsize=14
    )

    # Add color bar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label(r"$-\log_{10}(p)$", fontsize=12)

    # Add size legend further right
    legend_sizes = np.linspace(min_cor, max_cor, num=4)  # Choose 4 different size levels
    legend_scales = ((legend_sizes - min_cor) / (max_cor - min_cor + 1e-6)) ** 2 * size_scale + min_size  # Match scaling
    legend_labels = [f"{s:.2f}" for s in legend_sizes]

    legend_handles = [
        plt.scatter([], [], s=size, color="gray", edgecolors="black", alpha=0.8, label=f"cor={label}")
        for size, label in zip(legend_scales, legend_labels)
    ]

    # Move legend further right to avoid overlap
    ax.legend(handles=legend_handles, scatterpoints=1, frameon=True, labelspacing=1, title="Correlation (cor)", fontsize=10, loc="upper left", bbox_to_anchor=(1.15, 1))

    plt.show()
 