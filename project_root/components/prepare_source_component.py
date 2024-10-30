from utils.data_utils import filter_columns, rename_columns
from utils.file_utils import read_csv, save_to_csv, read_json
from utils.mapping_utils import generate_column_mapping
import os
import constants


def filter_condition_source(col):
    return (col == 'primary_key' or ('_clean' in col and '_j_clean' not in col)) and 'contribuable' not in col


@kfp.components.func_to_container_op
def prepare_source():
    try:
        df = read_csv(constants.DATA_PATH_SOURCE)
        df_filtered = filter_columns(df, filter_condition_source)

        mapping = read_json(constants.MAPPING_FILE)
        column_mapping = generate_column_mapping(df_filtered, mapping)
        df_renamed = rename_columns(df_filtered, column_mapping)

        save_to_csv(df_renamed, constants.OUTPUT_FILE_SOURCE)
        print("Data saved to", constants.OUTPUT_FILE_SOURCE)
    except Exception as e:
        print("Error in prepare_source component:", e)
