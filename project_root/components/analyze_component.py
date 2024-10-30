import pandas as pd
from utils.file_utils import read_csv, save_to_csv
import os
import constants
import kfp


@kfp.components.func_to_container_op
def analyse_clusters():
    """Analyse clusters and save statistics and results."""
    try:
        df_clusters = read_csv("resolved_ER/Grossistes_resolved_entities_with_custom_ids.csv")
        grouped_clusters = df_clusters.groupby("cluster_id")

        multi_record_clusters = grouped_clusters.filter(lambda x: len(x) > 1).sort_values("cluster_id")
        multi_record_clusters.to_csv("analyze/Grossistes_clusters.csv", sep=";", index=False)

        multi_record_clusters["id_type"] = multi_record_clusters["unique_id"].apply(
            lambda x: "R" if str(x).startswith("R") else "S"
        )

        filtered_df = multi_record_clusters.groupby("cluster_id").filter(
            lambda group: not (len(group[group["id_type"] == "R"]) > 0 and len(group[group["id_type"] == "S"]) == 0)
        )

        final_filtered_df = filtered_df.groupby("cluster_id").apply(lambda group: pd.concat([
            group[group["id_type"] == "S"],
            group[group["id_type"] == "R"].head(1)
        ])).reset_index(drop=True)

        final_filtered_df["identification_status"] = final_filtered_df.apply(
            lambda row: "Reference" if row["unique_id"].startswith("R") else (
                "identified" if (row["unique_id"].startswith("S") and row["cluster_id"] in
                                 final_filtered_df[final_filtered_df["id_type"] == "R"]["cluster_id"].unique())
                else "not identified"
            ),
            axis=1
        )

        save_to_csv(final_filtered_df, "analyze/Grossistes_final_filtered_entities_with_identification_status.csv")

        summary_stats = pd.DataFrame({
            "Total R Records": [final_filtered_df[final_filtered_df['unique_id'].str.startswith('R')].shape[0]],
            "Total S Records in Final Filtered Data": [final_filtered_df[final_filtered_df['unique_id'].str.startswith('S')].shape[0]],
            "Identified S Records": [final_filtered_df[final_filtered_df['identification_status'] == 'identified'].shape[0]],
            "Non-Identified S Records": [final_filtered_df[final_filtered_df['identification_status'] == 'not identified'].shape[0]]
        })

        summary_stats.to_csv("analyze/summary_grossistes_s_record_statistics.csv", sep=";", index=False)
        print("Analysis complete.")
    except Exception as e:
        print(f"Error in analyse_clusters: {e}")
