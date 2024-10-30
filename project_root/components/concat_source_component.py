from utils.file_utils import read_csv, save_to_csv
import os
import constants
import pandas as pd


@kfp.components.func_to_container_op
def concat_source_ref():
    try:
        source_df = read_csv(constants.OUTPUT_FILE_SOURCE)
        ref_df = read_csv(constants.OUTPUT_FILE_REF)

        common_columns = source_df.columns.intersection(ref_df.columns)
        source_df = source_df[common_columns]
        ref_df = ref_df[common_columns]

        source_df['unique_id'] = ["S" + str(i) for i in source_df.index]
        ref_df['unique_id'] = ["R" + str(i + 10001) for i in ref_df.index]

        data_concatenated = pd.concat([source_df, ref_df], axis=0, ignore_index=True)

        save_to_csv(data_concatenated, constants.CONCAT_OUTPUT_FILE)
        print("Concatenated data saved to", constants.CONCAT_OUTPUT_FILE)
    except Exception as e:
        print("Error in concat_source_ref component:", e)
