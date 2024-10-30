def generate_column_mapping(df, mapping, primary_key="primary_key"):
    """Generate column mapping based on JSON mapping and DataFrame columns."""
    column_mapping = {primary_key: primary_key}
    for column in df.columns:
        if column != primary_key:
            for category, attributes in mapping.items():
                if column in attributes["features"]:
                    column_mapping[column] = category
                    break
    return column_mapping
