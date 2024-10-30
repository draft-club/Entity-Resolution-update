# utils/data_utils.py

import pandas as pd

def filter_columns(df, exclude_contribuable=False):
    """
    Filter columns based on specified criteria.
    """
    columns = [
        col for col in df.columns if (
            col == 'primary_key' or ('_clean' in col and '_j_clean' not in col)
        )
    ]
    if exclude_contribuable:
        columns = [col for col in columns if 'contribuable' not in col]
    return df[columns]

def rename_columns(df, mapping):
    """
    Rename DataFrame columns based on mapping.
    """
    return df.rename(columns=mapping)
