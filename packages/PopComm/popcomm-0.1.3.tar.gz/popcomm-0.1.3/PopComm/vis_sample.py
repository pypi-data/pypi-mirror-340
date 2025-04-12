'''
Descripttion: 
version: 
Author: Mengwei Li
Date: 2025-03-03 10:08:14
LastEditors: Mengwei Li
LastEditTime: 2025-03-03 15:19:41
'''
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def heatmap_sample(lr_scores, metadata, score="normalized", 
                    selected_sender=None, selected_receiver=None, 
                    selected_metadata=None, figsize=(12, 8), export_file=None, export_format="pdf"):
    """
    Generate a heatmap where:
    - Rows: Ligand-Receptor (LR) + Cell Type pairs
    - Columns: Samples
    - Values: Average score for LR-Cell Type pairs in each sample.

    Parameters:
    - lr_scores: DataFrame containing LR interaction scores per cell and sample.
    - metadata: DataFrame with sample metadata.
    - score: use raw or normalized score for plotting
    - selected_sender: Specific sender cell type to filter, default is None (use all).
    - selected_receiver: Specific receiver cell type to filter, default is None (use all).
    - selected_metadata: List of column names in metadata to annotate samples (default: None, use all).
    - figsize: Tuple indicating figure size.

    Returns:
    - Heatmap of average LR interaction scores per sample.
    """
    
    score_col = "normalized_score" if score == "normalized" else "score"

    if selected_sender:
        lr_scores = lr_scores[lr_scores["sender"] == selected_sender]
    if selected_receiver:
        lr_scores = lr_scores[lr_scores["receiver"] == selected_receiver]
        
    
    # Create a new column for LR-Cell Type pairs
    lr_scores["LRSR"] = lr_scores["ligand"] + "_" + lr_scores["receptor"] + "_" + lr_scores["sender"] + "_" + lr_scores["receiver"]

    # Pivot table to get average scores per (LR-CellType, Sample)
    # TODO: check mean
    heatmap_data = lr_scores.groupby(["LRSR", "sample"])[score_col].mean().unstack(fill_value=0)

    col_colors = None
    color_legend_patches = {}
    
    if selected_metadata:
        column_metadata = metadata[selected_metadata].loc[heatmap_data.columns]

    # Convert categorical metadata to color mappings
        col_colors = pd.DataFrame()
        for col in column_metadata.columns:
            unique_vals = column_metadata[col].unique()
            color_palette = sns.color_palette("husl", len(unique_vals))  # Generate distinct colors
            color_map = dict(zip(unique_vals, color_palette))  # Map unique values to colors
            col_colors[col] = column_metadata[col].map(color_map)  # Apply mapping to metadata column

            # Store legend information
            color_legend_patches[col] = [mpatches.Patch(color=color_map[val], label=f"{col}: {val}") for val in unique_vals]
    
    g = sns.clustermap(heatmap_data, cmap="coolwarm", linewidths=0.5, annot=False,linecolor="gray",
                       row_cluster=True, col_cluster=True, col_colors=col_colors, figsize=figsize, xticklabels=False, yticklabels=False)

    # Remove row and column labels
    g.ax_heatmap.set_xlabel("")
    g.ax_heatmap.set_ylabel("")
    
    # Add legend for column colors
    if color_legend_patches:
        legend_offset = 1.05
        for i, (col, patches) in enumerate(color_legend_patches.items()):
            plt.gcf().legend(handles=patches, bbox_to_anchor=(legend_offset, 1 - i * 0.3), 
                             loc='upper left', title=col, frameon=False)
            # legend_offset += 0.3  # Adjust for spacing between legendseft', title=col)
            
    if export_file:
        plt.savefig(f"{export_file}", format=export_format, bbox_inches="tight")
    
    plt.show()
    return g

def pca_sample(lr_scores, metadata, selected_sender=None, selected_receiver=None, 
                   color_by=None, n_components=2, figsize=(8, 6)):
    """
    Perform PCA on ligand-receptor interaction scores across samples and plot the results.
    
    Parameters:
    - lr_scores: DataFrame containing LR interaction scores per cell and sample.
    - metadata: DataFrame with sample metadata.
    - selected_sender: Specific sender cell type to filter, default is None (use all).
    - selected_receiver: Specific receiver cell type to filter, default is None (use all).
    - color_by: Metadata column name to color points in PCA plot.
    - n_components: Number of PCA components to compute (default: 2).
    - figsize: Tuple indicating figure size.
    
    Returns:
    - PCA plot of samples based on LR interaction scores.
    """
    
    score_col = "normalized"
    
    if selected_sender:
        lr_scores = lr_scores[lr_scores["sender"] == selected_sender]
    if selected_receiver:
        lr_scores = lr_scores[lr_scores["receiver"] == selected_receiver]

    # Create a new column for LR-Cell Type pairs
    lr_scores["LRSR"] = lr_scores["ligand"] + "_" + lr_scores["receptor"] + "_" + lr_scores["sender"] + "_" + lr_scores["receiver"]

    # Pivot table to get scores per (LR-CellType, Sample)
    # TODO: check mean
    pca_data = lr_scores.groupby(["LRSR", "sample"])[score_col].mean().unstack(fill_value=0)
    
    # Standardize data
    scaler = StandardScaler()
    standardized_data = scaler.fit_transform(pca_data.T)
    
    # Perform PCA
    pca = PCA(n_components=n_components)
    pca_result = pca.fit_transform(standardized_data)
    
    # Create PCA DataFrame
    pca_df = pd.DataFrame(pca_result, columns=[f"PC{i+1}" for i in range(n_components)], index=pca_data.columns, )
    
    if "sample" not in metadata.columns:
        metadata = metadata.reset_index()
        
    if color_by and color_by in metadata.columns:
        pca_df = pca_df.merge(metadata[["sample", color_by]], left_index=True, right_on="sample", how="left")
    
    # Plot PCA results
    plt.figure(figsize=figsize)
    sns.scatterplot(
        x="PC1", y="PC2", data=pca_df, hue=color_by if color_by else None,
        palette="husl" if color_by else None, edgecolor="black"
    )
    
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.title("PCA of Ligand-Receptor Interaction Scores")
    plt.legend(title=color_by if color_by else "", loc="best")
    plt.show()
    
    return pca_df


def boxplot_lr_group_comparison(lr_scores, metadata, 
                                ligand, receptor, 
                                sender, receiver, 
                                groupby,
                                score="normalized", 
                                figsize=(4, 6)):
    """
    Plot boxplot of a specific LR pair across different sample groups.

    Parameters:
    - lr_scores: DataFrame with LR interaction scores per cell and sample.
    - metadata: DataFrame with sample metadata.
    - ligand: The ligand gene name.
    - receptor: The receptor gene name.
    - sender: Sender cell type.
    - receiver: Receiver cell type.
    - groupby: Column name in metadata to group samples for comparison.
    - score: Use 'raw' or 'normalized' score (default: normalized).
    - figsize: Figure size.
    
    Returns:
    - Matplotlib boxplot comparing LR interaction scores across groups.
    """
    score_col = "normalized_score" if score == "normalized" else "score"

    # Filter data for specific LR pair and sender/receiver
    df = lr_scores[
        (lr_scores["ligand"] == ligand) & 
        (lr_scores["receptor"] == receptor) & 
        (lr_scores["sender"] == sender) & 
        (lr_scores["receiver"] == receiver)
    ][["sample", score_col]].copy()

    if df.empty:
        print("No data found for the specified LR pair and sender/receiver.")
        return

    # Merge with metadata
    if "sample" not in metadata.columns:
        metadata = metadata.reset_index()
    df = df.merge(metadata[["sample", groupby]], on="sample", how="left")
    
    # Plot
    plt.figure(figsize=figsize)
    sns.boxplot(data=df, x=groupby, y=score_col, palette="Set2")
    sns.stripplot(data=df, x=groupby, y=score_col, color="black", alpha=0.5, jitter=0.2)

    title = f"{ligand}-{receptor} ({sender}→{receiver})"
    plt.title(f"LR Score Comparison: {title}")
    plt.xticks(rotation=90)
    plt.ylabel("Interaction Score")
    plt.xlabel(groupby)
    plt.tight_layout()
    plt.show()

    return df


def dotplot_lr_continuous_group(lr_scores, metadata, 
                                ligand, receptor, 
                                sender, receiver, 
                                groupby, 
                                score="normalized", 
                                figsize=(8, 6), add_regression=True):
    """
    Plot dotplot of LR scores against a continuous group variable.

    Parameters:
    - lr_scores: DataFrame with LR interaction scores.
    - metadata: DataFrame with sample metadata.
    - ligand: Ligand gene name.
    - receptor: Receptor gene name.
    - sender: Sender cell type.
    - receiver: Receiver cell type.
    - groupby: Continuous variable column in metadata (e.g., age, severity score).
    - score: 'normalized' or 'raw'.
    - figsize: Size of the figure.
    - add_regression: Whether to add regression line (default True).
    
    Returns:
    - Scatter plot with optional regression line.
    """
    score_col = "normalized_score" if score == "normalized" else "score"

    # Filter for LR and SR pair
    df = lr_scores[
        (lr_scores["ligand"] == ligand) & 
        (lr_scores["receptor"] == receptor) & 
        (lr_scores["sender"] == sender) & 
        (lr_scores["receiver"] == receiver)
    ][["sample", score_col]].copy()

    if df.empty:
        print("No data found for the specified LR pair and sender/receiver.")
        return

    # Merge with metadata
    if "sample" not in metadata.columns:
        metadata = metadata.reset_index()
    df = df.merge(metadata[["sample", groupby]], on="sample", how="left")

    # Remove NA values in groupby
    df = df.dropna(subset=[groupby])

    # Plot
    plt.figure(figsize=figsize)
    sns.scatterplot(data=df, x=groupby, y=score_col, color="dodgerblue", s=80, edgecolor="black", alpha=0.7)

    if add_regression:
        sns.regplot(data=df, x=groupby, y=score_col, scatter=False, color="darkred", line_kws={"linewidth": 2, "linestyle": "--"})

    title = f"{ligand}-{receptor} ({sender}→{receiver})"
    plt.title(f"Dot Plot of LR Score vs {groupby}\n{title}")
    plt.xlabel(groupby)
    plt.ylabel("Interaction Score")
    plt.tight_layout()
    plt.show()

    return df