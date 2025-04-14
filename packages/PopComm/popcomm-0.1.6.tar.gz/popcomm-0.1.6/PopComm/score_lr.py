import numpy as np
import pandas as pd
import scanpy as sc
import multiprocessing as mp
from scipy.stats import linregress
from joblib import Parallel, delayed
from .utils import project_to_line

def score_lr_single(adata, sender, receiver, filtered_lr, 
                           sample_col, cell_type_col, 
                           num_cores=10):
    """
    Compute scores for ligand-receptor pairs between sender and receiver cell types.
    
    Parameters:
    - adata: AnnData object containing single-cell RNA expression data.
    - sender: Cell type designated as the ligand sender.
    - receiver: Cell type designated as the receptor receiver.
    - filtered_lr: DataFrame of ligand-receptor pairs from prior analysis (must contain an 'lr' column with 'Ligand_Receptor' format).
    - sample_col: Column in adata.obs indicating sample identifiers.
    - cell_type_col: Column in adata.obs indicating cell type classifications.
    - min_cells: Minimum cells per sample for both sender and receiver (default 50).
    - min_samples: Minimum valid samples required (default 10).
    - num_cores: Number of CPU cores for parallel processing (default 10).
    
    Returns:
    - DataFrame with projection scores for each sample and LR pair.
    """
    
    adata.obs[cell_type_col] = adata.obs[cell_type_col].astype(str)
    adata.obs[sample_col] = adata.obs[sample_col].astype(str)

    # Check core limits
    max_cores = mp.cpu_count() - 1
    if num_cores > max_cores:
        print(f"Warning: Using {num_cores} cores, exceeding system limit {max_cores}. Using {max_cores} instead.")
        num_cores = max_cores
    
    cell_types = adata.obs[cell_type_col].unique()
    
    if sender not in cell_types or receiver not in cell_types:
        raise ValueError(f"Missing cell types: {sender}, {receiver} not found in dataset.")
    
    lr_pairs_exist = ((filtered_lr['sender'] == sender) & (filtered_lr['receiver'] == receiver)).any()

    if not lr_pairs_exist:
        print(f"Sender: {sender} or receiver: {receiver} not in filtered_lr.")
        return None

    
    print(f"Analyzing ligand-receptor projection score: {sender} -> {receiver}")
    
    # Subset data to sender and receiver
    adata_sub = adata[adata.obs[cell_type_col].isin([sender, receiver])].copy()
    lr_genes = pd.unique(filtered_lr[['ligand', 'receptor']].values.ravel())
    adata_sub = adata_sub[:, adata_sub.var_names.isin(lr_genes)].copy()
    
    # Filter samples based on cell counts
    # sample_counts = adata_sub.obs.groupby([sample_col, cell_type_col]).size().unstack(fill_value=0)
    
    # valid_samples = sample_counts[(sample_counts[sender] > min_cells) & (sample_counts[receiver] > min_cells)].index
    # if len(valid_samples) < min_samples:
    #     print("Insufficient valid samples, analysis stopped.")
    #     return None
    
    # adata_sub = adata_sub[adata_sub.obs['sample'].isin(valid_samples)].copy()
    adata_sub.obs['group'] = adata_sub.obs[sample_col] + '-lr-' + adata_sub.obs[cell_type_col]
    avg_expr = (np.exp(adata_sub.to_df()) - 1).groupby(adata_sub.obs['group']).mean()
    avg_expr = np.round(avg_expr, decimals=5)
    
    
    # Extract sender and receiver expression matrices
    sender_expr = avg_expr[avg_expr.index.str.contains(sender, regex=True)]
    receiver_expr = avg_expr[avg_expr.index.str.contains(receiver, regex=True)]
    
    # Match sender and receiver samples
    sender_expr.index = sender_expr.index.str.split('-lr-').str[0]
    receiver_expr.index = receiver_expr.index.str.split('-lr-').str[0]
    
    sender_expr = sender_expr.loc[:, filtered_lr['ligand']]
    receiver_expr = receiver_expr.loc[:, filtered_lr['receptor']]
    
    sender_expr = sender_expr.loc[:, ~sender_expr.columns.duplicated()]
    receiver_expr = receiver_expr.loc[:, ~receiver_expr.columns.duplicated()]
    
    print("Calculating projection scores...")
    common_index = sender_expr.index.intersection(receiver_expr.index)
    common_index = common_index.sort_values()
    sender_expr = sender_expr.loc[common_index]
    receiver_expr = receiver_expr.loc[common_index]
    
    
    def compute_projection(i):
        ligand_gene = filtered_lr.iloc[i]['ligand']
        receptor_gene = filtered_lr.iloc[i]['receptor']
        slope = filtered_lr.iloc[i]['slope']
        intercept = filtered_lr.iloc[i]['intercept']
        
        x = sender_expr.loc[:, ligand_gene].values
        y = receiver_expr.loc[:, receptor_gene].values
        
        if np.std(x) == 0 or np.std(y) == 0:
            return None
        
        # slope, intercept, _, _, _ = linregress(x, y)
        # slope = np.round(slope, 5)
        # intercept = np.round(intercept, 5)
        
        projections = np.array([project_to_line(x[j], y[j], slope, intercept) for j in range(len(x))])
        
        dx = projections[:, 0] - np.min(projections[:, 0])
        dy = projections[:, 1] - np.min(projections[:, 1])
        
        scores = np.sqrt(dx ** 2 + dy ** 2)
        scores = np.round(scores, 5)
        normalized_scores = scores / np.max(scores)
        normalized_scores = np.round(normalized_scores, 5)
        
        return pd.DataFrame({
            'ligand': [filtered_lr.iloc[i]['ligand']] * len(sender_expr.index),
            'receptor': [filtered_lr.iloc[i]['receptor']] * len(sender_expr.index),
            'sample': sender_expr.index,
            'score': scores,
            'normalized_score': normalized_scores,
            'sender': [sender] * len(sender_expr.index),
            'receiver': [receiver] * len(sender_expr.index)
        })
    
    # Run in parallel
    results = Parallel(n_jobs=num_cores)(delayed(compute_projection)(i) for i in range(len(filtered_lr)))
    results = pd.concat([r for r in results if r is not None], ignore_index=True)
    
    
    
    print("Ligand-receptor projection score analysis complete.")
    print(results.head())
    
    return results


def score_lr_all(adata, filtered_lr, sample_col, cell_type_col, num_cores=10):
    """
    Compute ligand-receptor interaction scores for all sender-receiver pairs.
    
    Parameters:
    - adata: AnnData object containing expression data.
    - filtered_lr: DataFrame of ligand-receptor pairs from prior analysis (must contain an 'lr' column with 'Ligand_Receptor' format).
    - sample_col: Column name in adata.obs indicating sample information.
    - cell_type_col: Column name in adata.obs indicating cell type.
    - min_cells: Minimum number of cells per sample for valid interactions.
    - min_samples: Minimum number of samples required for valid interactions.
    - num_cores: Number of CPU cores for parallel processing.

    Returns:
    - DataFrame containing scores for all sender-receiver interactions.
    """
    
    # Extract unique cell types
    cell_types = adata.obs[cell_type_col].unique()
    all_results = []

    # Iterate over all sender-receiver pairs
    for sender in cell_types:
        for receiver in cell_types:
            res = score_lr_single(
                adata=adata,
                filtered_lr=filtered_lr,
                sample_col=sample_col,
                cell_type_col=cell_type_col,
                sender=sender,
                receiver=receiver,
                num_cores=num_cores
            )
            if res is not None:
                all_results.append(res)

    # Combine results into a single DataFrame
    if not all_results:
        return None

    return pd.concat(all_results, ignore_index=True)
