from .utils import remove_outliers, compute_correlation
import pandas as pd
from statsmodels.stats.multitest import multipletests
import numpy as np
from joblib import Parallel, delayed
from scipy.stats import linregress

def filter_lr_single(
    adata,
    sender,
    receiver,
    lr_database,
    sample_col,
    cell_type_col,
    min_cells=50,
    min_samples=10,
    cor_method="spearman",
    adjust_method="fdr_bh",
    min_adjust_p=0.05,
    min_cor=0,
    min_ratio=0.1,
    min_cell_ratio=0.1,
    num_cores=10
):
    """
    Filter ligand-receptor pairs for a given sender-receiver pair.
    
    Parameters
    ----------
    show
        Boolean to turn on (True) or off (False) 'add_dendrogram'
    dendrogram_key
        Needed if `sc.tl.dendrogram` saved the dendrogram using a key different
        than the default name.
    size
        size of the dendrogram. Corresponds to width when dendrogram shown on
        the right of the plot, or height when shown on top. The unit is the same
        as in matplotlib (inches).

    Returns
    -------
    Returns `self` for method chaining.
    """

    # Get cell type annotations and sample identifiers
    cell_types = adata.obs[cell_type_col].unique()
    if sender not in cell_types or receiver not in cell_types:
        print(f"Skipping {sender} -> {receiver}, missing cell types.")
        return None

    print(f"Analyzing {sender} -> {receiver}")

    # Subset data for sender and receiver
    adata_sub = adata[adata.obs[cell_type_col].isin([sender, receiver])]
    
    # Subset data for ligand receptor gene
    lr_genes = pd.unique(lr_database[['ligand_gene_symbol', 'receptor_gene_symbol']].values.ravel())
    adata_sub = adata_sub[:, adata_sub.var_names.isin(lr_genes)].copy()

    # Filter based on minimum cell count per sample
    sample_counts = (
        adata_sub.obs.groupby([sample_col, cell_type_col], observed=True).size().unstack(fill_value=0)
    )
    valid_samples = sample_counts[
        (sample_counts[sender] > min_cells) & (sample_counts[receiver] > min_cells)
    ].index

    if len(valid_samples) < min_samples:
        print(f"Insufficient valid samples for {sender} -> {receiver}.")
        return None

    adata_sub = adata_sub[adata_sub.obs[sample_col].isin(valid_samples)]


    sender_cells = adata_sub.obs[cell_type_col] == sender
    receiver_cells = adata_sub.obs[cell_type_col] == receiver

    expr_mat = adata_sub.to_df()
    sender_pct_expr = (expr_mat[sender_cells] > 0).sum(axis=0) / sender_cells.sum()
    receiver_pct_expr = (expr_mat[receiver_cells] > 0).sum(axis=0) / receiver_cells.sum()

    
    avg_expr_sender = (np.exp(adata_sub[adata_sub.obs[cell_type_col] == sender].to_df()) - 1).groupby(adata_sub.obs[sample_col], observed=True).mean()
    avg_expr_receiver = (np.exp(adata_sub[adata_sub.obs[cell_type_col] == receiver].to_df()) - 1).groupby(adata_sub.obs[sample_col], observed=True).mean()

    lr_database = lr_database[
    (lr_database["ligand_gene_symbol"].isin(sender_pct_expr.index)) &
    (lr_database["receptor_gene_symbol"].isin(receiver_pct_expr.index))
]

    lr_database = lr_database[
        (sender_pct_expr[lr_database["ligand_gene_symbol"]].values > min_cell_ratio) &
        (receiver_pct_expr[lr_database["receptor_gene_symbol"]].values > min_cell_ratio)
    ]

    avg_expr_sender = np.round(avg_expr_sender, decimals=5)
    avg_expr_receiver = np.round(avg_expr_receiver, decimals=5)
    
    lr_database = lr_database[
        (lr_database["ligand_gene_symbol"].isin(avg_expr_sender.columns))
        & (lr_database["receptor_gene_symbol"].isin(avg_expr_receiver.columns))
    ]

    results = []

    def process_lr_pair(idx):
        ligand = lr_database.iloc[idx]["ligand_gene_symbol"]
        receptor = lr_database.iloc[idx]["receptor_gene_symbol"]

        if ligand not in avg_expr_sender.columns or receptor not in avg_expr_receiver.columns:
            return None

        ligand_expr = avg_expr_sender[ligand]
        receptor_expr = avg_expr_receiver[receptor]

        # Remove outliers
        data = pd.DataFrame({"x": ligand_expr, "y": receptor_expr})

        # Remove outliers
        data_clean = remove_outliers(data)

        if (
            len(data_clean) < min_samples
            or data_clean["x"].sum() == 0
            or data_clean["y"].sum() == 0
        ):
            return None

        ligand_expr = data_clean["x"]
        receptor_expr = data_clean["y"]

        cor, p_val = compute_correlation(ligand_expr, receptor_expr, cor_method)
        cor = np.round(cor, 5)
        p_val = np.round(p_val, 15)
        pct1 = (ligand_expr > 0).sum() / len(ligand_expr)
        pct2 = (receptor_expr > 0).sum() / len(receptor_expr)

        pct1 = np.round(pct1, 3)
        pct2 = np.round(pct2, 3)
        return [ligand, receptor, cor, p_val, pct1, pct2]
        # return [ligand, receptor, cor, p_val]
    
    for i in range(len(lr_database)):
        result = process_lr_pair(i)
        results.append(result)
    
    results = [r for r in results if r is not None]
    
    if not results:
        return None

    results_df = pd.DataFrame(
        results, columns=["ligand", "receptor", "cor", "p_val", "pct1", "pct2"]
    )

    # Adjust p-values
    results_df["adjust.p"] = multipletests(results_df["p_val"], method=adjust_method)[1]
    results_df["adjust.p"] = np.round(results_df["adjust.p"], 15)
    # Filter based on thresholds
    results_df = results_df[
        (results_df["adjust.p"] < min_adjust_p)
        & (results_df["cor"] > min_cor)
        & (results_df["pct1"] > min_ratio)
        & (results_df["pct2"] > min_ratio)
    ]

    if results_df.empty:
        return None
    
    results_df["sender"] = sender
    results_df["receiver"] = receiver

    def compute_regression(i):
        ligand = results_df.iloc[i]["ligand"]
        receptor = results_df.iloc[i]["receptor"]
        x = avg_expr_sender[ligand]
        y = avg_expr_receiver[receptor]
        
        if np.std(x) == 0 or np.std(y) == 0:
            return None
        
        slope, intercept, _, _, _ = linregress(x, y)
        slope = np.round(slope, 5)
        intercept = np.round(intercept, 5)
        return [slope, intercept]

    results = Parallel(n_jobs=num_cores)(delayed(compute_regression)(i) for i in range(results_df.shape[0]))
  
    results = pd.DataFrame(results, columns=["slope", "intercept"])

    results_df = pd.concat([results_df.reset_index(drop=True), results.reset_index(drop=True)], axis=1)
    results_df = results_df.drop(columns=['pct1', 'pct2'])
    return results_df

def filter_lr_all(
    adata,
    lr_database,
    sample_col,
    cell_type_col,
    min_cells=50,
    min_samples=10,
    cor_method="spearman",
    adjust_method="fdr_bh",
    min_adjust_p=0.05,
    min_cor=0,
    min_ratio=0.1,
    min_cell_ratio=0.1,
    num_cores=10,
):
    """Filter ligand-receptor interactions for all cell type pairs."""

    cell_types = adata.obs[cell_type_col].unique()
    all_results = []

    for sender in cell_types:
        for receiver in cell_types:
            res = filter_lr_single(
                adata,
                sender,
                receiver,
                lr_database,
                sample_col,
                cell_type_col,
                min_cells,
                min_samples,
                cor_method,
                adjust_method,
                min_adjust_p,
                min_cor,
                min_ratio,
                min_cell_ratio,
                num_cores,
            )
            if res is not None:
                all_results.append(res)

    if not all_results:
        return None

    return pd.concat(all_results)