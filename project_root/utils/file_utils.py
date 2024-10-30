# utils/file_utils.py

import pandas as pd
import os
import json

def read_parquet(file_path):
    return pd.read_parquet(file_path)

def save_to_csv(df, path, sep=';'):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False, sep=sep)

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
