import pandas as pd
import splink.comparison_library as cl
from splink import DuckDBAPI, Linker, SettingsCreator, block_on
import os
import constants
import kfp


@kfp.components.func_to_container_op
def splink_entity_resolution():
    """Run Splink entity resolution and save results."""
    try:
        concat_data = pd.read_csv(constants.CONCAT_OUTPUT_FILE, delimiter=";", low_memory=False)

        duckdb_api = DuckDBAPI()
        duckdb_api._con.execute("PRAGMA max_temp_directory_size='55GiB';")

        settings = SettingsCreator(
            link_type="dedupe_only",
            comparisons=[
                cl.ExactMatch("ifu"),
                cl.ExactMatch("num_ce"),
                cl.ExactMatch("num_cin"),
                cl.JaroAtThresholds("nom_prenom_rs", [0.8, 0.7]),
                cl.JaroAtThresholds("acronym_nom_prenom_rs", [0.8, 0.7]),
                cl.JaroAtThresholds("nom", [0.8, 0.7]),
                cl.JaroAtThresholds("prenoms", [0.8, 0.7]),
                cl.JaroAtThresholds("adresse", [0.8, 0.7]),
                cl.ExactMatch("ville").configure(term_frequency_adjustments=True),
                cl.ExactMatch("pays").configure(term_frequency_adjustments=True),
            ],
            blocking_rules_to_generate_predictions=[block_on("num_cin")]
        )

        linker = Linker(concat_data, settings, duckdb_api)

        linker.training.estimate_probability_two_random_records_match(
            [block_on("num_cin")], recall=0.7
        )
        linker.training.estimate_u_using_random_sampling(max_pairs=1e6)
        linker.training.estimate_parameters_using_expectation_maximisation(block_on("num_cin"))
        linker.training.estimate_parameters_using_expectation_maximisation(block_on("nom_prenom_rs"))

        pairwise_predictions = linker.inference.predict(threshold_match_weight=-10)
        clusters = linker.clustering.cluster_pairwise_predictions_at_threshold(
            pairwise_predictions, 0.7
        )

        df_clusters = clusters.as_pandas_dataframe()

        output_dir = "resolved_ER"
        os.makedirs(output_dir, exist_ok=True)
        df_clusters.to_csv(os.path.join(output_dir, 'ppa_resolved_entities_with_custom_ids.csv'), sep=";", index=False)

        print("Entity resolution complete.")
    except Exception as e:
        print(f"Error in splink_entity_resolution: {e}")
