import pandas as pd
import json
import os


def read_parquet(file_path):
    """Read a Parquet file into a DataFrame."""
    return pd.read_parquet(file_path)


def read_csv(file_path, delimiter=";"):
    """Read a CSV file into a DataFrame."""
    return pd.read_csv(file_path, delimiter=delimiter)


def save_to_csv(df, output_path, delimiter=";"):
    """Save DataFrame to CSV with specified delimiter."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False, sep=delimiter)


def read_json(file_path):
    """Read JSON file into a dictionary."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
