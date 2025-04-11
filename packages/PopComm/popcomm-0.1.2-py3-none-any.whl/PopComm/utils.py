"""
Descripttion:
version:
Author: Mengwei Li
Date: 2025-01-29 20:23:43
LastEditors: Mengwei Li
LastEditTime: 2025-02-05 09:43:51
"""

from scipy.stats import spearmanr, pearsonr
import numpy as np

def remove_outliers(data):
    """
    Remove outliers from a DataFrame based on the IQR method for columns 'x' and 'y'.

    Parameters:
    - data: Pandas DataFrame with columns 'x' and 'y'.

    Returns:
    - A DataFrame with outliers removed.
    """
    # Calculate IQR for column 'x'
    Q1_x = data["x"].quantile(0.25)
    Q3_x = data["x"].quantile(0.75)
    IQR_x = Q3_x - Q1_x

    # Calculate IQR for column 'y'
    Q1_y = data["y"].quantile(0.25)
    Q3_y = data["y"].quantile(0.75)
    IQR_y = Q3_y - Q1_y

    # Define outlier thresholds for 'x' and 'y'
    lower_bound_x = Q1_x - 1.5 * IQR_x
    upper_bound_x = Q3_x + 1.5 * IQR_x
    lower_bound_y = Q1_y - 1.5 * IQR_y
    upper_bound_y = Q3_y + 1.5 * IQR_y

    # Identify non-outliers
    non_outliers = (
        (data["x"] > lower_bound_x)
        & (data["x"] < upper_bound_x)
        & (data["y"] > lower_bound_y)
        & (data["y"] < upper_bound_y)
    )

    # Filter data to remove outliers
    data_clean = data[non_outliers]

    return data_clean


def compute_correlation(ligand_expr, receptor_expr, cor_method="spearman"):
    """Compute correlation and p-value between ligand and receptor expression."""
    if cor_method == "spearman":
        cor, p_val = spearmanr(ligand_expr, receptor_expr)
    elif cor_method == "pearson":
        cor, p_val = pearsonr(ligand_expr, receptor_expr)
    else:
        raise ValueError("Unsupported correlation method.")
    return cor, p_val


def project_to_line(x, y, slope, intercept):
    """Project a point (x, y) onto the regression line y = slope * x + intercept."""
    x_proj = (x + slope * (y - intercept)) / (1 + slope**2)
    x_proj = np.round(x_proj, 5)
    y_proj = slope * x_proj + intercept
    y_proj = np.round(y_proj, 5)
    return x_proj, y_proj

