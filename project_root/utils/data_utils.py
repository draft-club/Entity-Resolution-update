import pandas as pd


def filter_columns(df, column_conditions):
    """Filter DataFrame columns based on conditions."""
    filtered_columns = [col for col in df.columns if column_conditions(col)]
    return df[filtered_columns]


def rename_columns(df, column_mapping):
    """Rename DataFrame columns based on a mapping dictionary."""
    return df.rename(columns=column_mapping)
