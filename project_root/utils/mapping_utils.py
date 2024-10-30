# utils/mapping_utils.py

def generate_column_mapping(df, mapping_json):
    column_mapping = {}
    for column in df.columns:
        if column == "primary_key":
            column_mapping[column] = "primary_key"
        else:
            for category, attributes in mapping_json.items():
                if column in attributes['features']:
                    column_mapping[column] = category
                    break
    return column_mapping
