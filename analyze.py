import pandas as pd


def col_missing_values(df, cutoff=None):
    """Find number of missing values in each column.
    cutoff (int): dont list indices if more missing values than cutoff -> np.nan else.
    """
    missing_vals = pd.DataFrame(columns=["n_missing","indices"])
    for col_name in df.columns:
        is_missing = df[col_name].isna()
        missing_vals.loc[col_name, "n_missing"] = is_missing.sum()
        val_indices = df[is_missing].index
        if not cutoff or (cutoff and cutoff > len(val_indices)):
            missing_vals.loc[col_name, "indices"] = "; ".join(map(str, list(val_indices)))
        else:
            missing_vals.loc[col_name, "indices"] = float('NaN')
    return missing_vals


def row_missing_values(df, cols=None, detail=None):
    """Get a detailed overview of which columns are missing for which row.
    Args:
    - df
    - cols (list): column names to consider. All if None
    - detail (list): column names to also get value for each row.
    """
    missing_vals = pd.DataFrame(columns=["index", "missing_cols"])
    if not cols:
        cols = df.columns
    _df = df[cols]
    is_missing = _df.isna().any(axis="columns")
    for i, (index, row) in enumerate(_df[is_missing].iterrows()):
        missing_vals.loc[i, "index"] = str(index)
        missing_vals.loc[i, "missing_cols"] = "; ".join(list(row[row.isna()].index))
        if detail:
            missing_vals.loc[i, [detail]] = row[detail]
    return missing_vals
