'''
Descripttion: 
version: 
Author: Mengwei Li
Date: 2025-02-19 12:50:07
LastEditors: Mengwei Li
LastEditTime: 2025-03-04 14:14:33
'''

import pandas as pd
import scipy.stats as stats
import numpy as np
from statsmodels.api import OLS, add_constant
from statsmodels.stats.multitest import multipletests
import statsmodels.api as sm

def get_sample_metadata(adata, sample_col):
    """
    Extracts metadata from an AnnData object and removes duplicates by sample.

    Parameters:
    - adata: AnnData object containing single-cell data.
    - sample_col: Column name in adata.obs that represents sample identity.

    Returns:
    - DataFrame with unique metadata per sample.
    """
    metadata = adata.obs.copy()
    unique_metadata = metadata.drop_duplicates(subset=[sample_col])
    unique_metadata = unique_metadata.set_index(sample_col)
    return unique_metadata

def corr_lr_interaction(lr_scores, metadata, correlate_with):
    """
    Perform correlation analysis between ligand-receptor interaction scores and a continuous metadata field.

    Parameters:
    - lr_scores: DataFrame containing ligand-receptor interaction scores per sample.
    - metadata: DataFrame containing sample metadata.
    - correlate_with: Column name in metadata to compute correlation with.

    Returns:
    - DataFrame containing correlation results (correlation coefficient and p-values).
    """
    score_col = "score"  # Only use non-normalized score

    # Ensure metadata has the sample column
    if "sample" not in metadata.columns:
        metadata = metadata.reset_index()
    
    # Ensure sample names are strings
    metadata["sample"] = metadata["sample"].astype(str)
    lr_scores["sample"] = lr_scores["sample"].astype(str)

    # Merge metadata with LR scores
    merged_data = lr_scores.merge(metadata[["sample", correlate_with]], on="sample", how="left")

    # Create a new column for LR-Cell Type pairs
    merged_data["LRSR"] = merged_data["ligand"] + "_" + merged_data["receptor"] + "_" + merged_data["sender"] + "_" + merged_data["receiver"]

    # Pivot table to get average scores per (LR-CellType, Sample)
    heatmap_data = merged_data.groupby(["LRSR", "sample"])[score_col].mean().unstack(fill_value=0)

    # Get metadata values for correlation
    continuous_values = metadata.set_index("sample")[correlate_with].loc[heatmap_data.columns]

    # Compute Spearman correlation
    correlations = []
    p_values = []
    for lr in heatmap_data.index:
        cor, p_val = stats.spearmanr(heatmap_data.loc[lr], continuous_values)
        correlations.append(cor)
        p_values.append(p_val)
    
    # Adjust p-values using Benjamini-Hochberg correction (FDR)
    from statsmodels.stats.multitest import multipletests
    adjusted_p_values = multipletests(p_values, method="fdr_bh")[1]
    
    # Split LRSR into separate columns
    lr_split = [lr.split("_") for lr in heatmap_data.index]
    ligand, receptor, sender, receiver = zip(*lr_split)

    # Store results in a DataFrame
    result_df = pd.DataFrame({
        "ligand": ligand,
        "receptor": receptor,
        "sender": sender,
        "receiver": receiver,
        "correlation": correlations,
        "p_value": p_values,
        "adjusted_p_value": adjusted_p_values
    })

    # Sort by significance
    result_df = result_df.sort_values(by="adjusted_p_value")

    return result_df

def diff_lr_interaction(lr_scores, metadata, group_by, ident1, ident2):
    """
    Perform differential ligand-receptor interaction analysis between two sample groups.

    Parameters:
    - lr_scores: DataFrame containing ligand-receptor interaction scores per sample.
    - metadata: DataFrame containing sample metadata.
    - group_by: Metadata field to define sample groups.
    - ident1: Value in `group_by` to define the first group.
    - ident2: Value in `group_by` to define the second group.

    Returns:
    - DataFrame containing differential interaction results (mean scores, logFC, p-values).
    """
    score_col = "score"  # Only use non-normalized score

    # Ensure metadata has the sample column
    if "sample" not in metadata.columns:
        metadata = metadata.reset_index()
    
    # Ensure sample names are strings
    metadata["sample"] = metadata["sample"].astype(str)
    lr_scores["sample"] = lr_scores["sample"].astype(str)

    # Merge metadata with LR scores
    merged_data = lr_scores.merge(metadata[["sample", group_by]], on="sample", how="left")

    # Create a new column for LR-Cell Type pairs
    merged_data["LRSR"] = merged_data["ligand"] + "_" + merged_data["receptor"] + "_" + merged_data["sender"] + "_" + merged_data["receiver"]

    # Pivot table to get average scores per (LR-CellType, Sample)
    heatmap_data = merged_data.groupby(["LRSR", "sample"])[score_col].mean().unstack(fill_value=0)

    # Get sample groups
    samples_ident1 = metadata.loc[metadata[group_by] == ident1, "sample"].values
    samples_ident2 = metadata.loc[metadata[group_by] == ident2, "sample"].values

    # Subset the heatmap data based on groups
    group1_data = heatmap_data[samples_ident1].mean(axis=1)
    group2_data = heatmap_data[samples_ident2].mean(axis=1)

    # Compute log fold change
    logFC = np.log2(group1_data + 1e-6) - np.log2(group2_data + 1e-6)  # Avoid log(0) issues

    # Perform statistical testing (Mann-Whitney U test)
    p_values = [stats.mannwhitneyu(heatmap_data.loc[lr, samples_ident1], 
                                   heatmap_data.loc[lr, samples_ident2], 
                                   alternative='two-sided')[1] for lr in heatmap_data.index]

    # Adjust p-values using Benjamini-Hochberg correction (FDR)
    adjusted_p_values = multipletests(p_values, method="fdr_bh")[1]

    # Split LRSR into separate columns
    lr_split = [lr.split("_") for lr in heatmap_data.index]
    ligand, receptor, sender, receiver = zip(*lr_split)

    # Store results in a DataFrame
    result_df = pd.DataFrame({
        "ligand": ligand,
        "receptor": receptor,
        "sender": sender,
        "receiver": receiver,
        "mean_group1": group1_data.values,
        "mean_group2": group2_data.values,
        "logFC": logFC.values,
        "p_value": p_values,
        "adjusted_p_value": adjusted_p_values
    })

    # Sort by significance
    result_df = result_df.sort_values(by="adjusted_p_value")

    return result_df



def lr_linear_model(
    lr_scores,
    metadata,
    group_variable,
    ident1,
    ident2=None,
    covariates=None,
    fdr_threshold=0.05
):
    """
    Compare LR interaction scores with a group variable using linear regression.
    Handles both continuous and binary group variables (ident1 vs ident2 or all others).

    Parameters:
    - lr_scores: DataFrame with LR interaction scores per sample.
    - metadata: DataFrame with sample metadata.
    - group_variable: Column name in metadata to compare groups (categorical or continuous).
    - ident1: If categorical, group to compare (coded as 1).
    - ident2: Reference group or list of groups (coded as 0). If None, uses all others.
    - covariates: Optional list of covariate column names.
    - fdr_threshold: Significance cutoff for adjusted p-values.

    Returns:
    - DataFrame with logFC (coefficient), p-value, adjusted p-value.
    """
    
    score_col = "score"

    if "sample" not in metadata.columns:
        metadata = metadata.reset_index()

    metadata["sample"] = metadata["sample"].astype(str)
    lr_scores["sample"] = lr_scores["sample"].astype(str)

    if np.issubdtype(metadata[group_variable].dtype, np.number):
        metadata["_group_dummy_"] = metadata[group_variable]
        keep_samples = metadata.copy()
    else:
        if ident1 is None:
            raise ValueError("ident1 must be specified for categorical group_variable.")

        if ident2 is None:
            ident2_list = metadata[group_variable].unique().tolist()
            ident2_list = [x for x in ident2_list if x != ident1]
        else:
            ident2_list = [ident2] if isinstance(ident2, str) else ident2

        keep_samples = metadata[metadata[group_variable].isin([ident1] + ident2_list)].copy()
        keep_samples["_group_dummy_"] = (keep_samples[group_variable] == ident1).astype(int)


    # Merge with LR scores
    merged_data = lr_scores.merge(keep_samples, on="sample", how="inner")

    # Create LR interaction ID
    merged_data["LRSR"] = (
        merged_data["ligand"] + "_" +
        merged_data["receptor"] + "_" +
        merged_data["sender"] + "_" +
        merged_data["receiver"]
    )

    # Average scores per LRSR-sample
    avg_scores = merged_data.groupby(["LRSR", "sample"])[score_col].mean().unstack(fill_value=0)

    # Filter metadata for matched samples
    keep_samples = keep_samples.set_index("sample").loc[avg_scores.columns]

    results = []

    for lrsr in avg_scores.index:
        y = avg_scores.loc[lrsr]

        # Design matrix
        X = keep_samples[["_group_dummy_"] + (covariates if covariates else [])].copy()
        X = pd.get_dummies(X, drop_first=True)
        X = sm.add_constant(X)
        
        y = y.astype(float)
        X = X.astype(float)

        try:
            model = sm.OLS(y, X).fit()
            coef = model.params["_group_dummy_"]
            pval = model.pvalues["_group_dummy_"]
            results.append({
                "LRSR": lrsr,
                "coef": coef,
                "p_value": pval
            })
        except Exception:
            continue

    # Compile results
    result_df = pd.DataFrame(results)

    # Adjust p-values
    result_df["adjusted_p_value"] = multipletests(result_df["p_value"], method="fdr_bh")[1]

    # Split LRSR
    lr_split = result_df["LRSR"].str.split("_", expand=True)
    result_df["ligand"] = lr_split[0]
    result_df["receptor"] = lr_split[1]
    result_df["sender"] = lr_split[2]
    result_df["receiver"] = lr_split[3]

    # Arrange columns
    result_df = result_df[[
        "ligand", "receptor", "sender", "receiver",
        "coef", "p_value", "adjusted_p_value"
    ]].sort_values("adjusted_p_value")

    result_df = result_df[result_df["adjusted_p_value"] < fdr_threshold]

    return result_df