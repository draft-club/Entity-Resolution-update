# components/prepare_ref_component.py

from utils.data_utils import filter_columns, rename_columns
from utils.file_utils import read_parquet, save_to_csv, read_json
from utils.mapping_utils import generate_column_mapping
import os
import constants


def prepare_ref():
    df = read_parquet(constants.DATA_PATH_REF)
    df_filtered = filter_columns(df)

    try:
        mapping = read_json(constants.MAPPING_FILE)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    column_mapping = generate_column_mapping(df_filtered, mapping)
    df_renamed = rename_columns(df_filtered, column_mapping)

    save_to_csv(df_renamed, os.path.join(constants.OUTPUT_DIR, 'data_contribuable.csv'))
    print("Data saved to output_data/data_contribuable.csv")
