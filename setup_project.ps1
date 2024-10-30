# Define base project directory
$ProjectDir = "project_root"
$ComponentsDir = "$ProjectDir\components"
$UtilsDir = "$ProjectDir\utils"
$AnalyzeDir = "$ProjectDir\analyze"

# Create directories
New-Item -ItemType Directory -Force -Path $ProjectDir, $ComponentsDir, $UtilsDir, $AnalyzeDir | Out-Null

# Create Python component files
Write-Output "Creating components files..."
$Components = @("prepare_ref_component", "prepare_source_component", "concat_source_component", "splink_component", "analyze_component")
ForEach ($component in $Components) {
    $Content = @"
# $component.py
from utils import data_utils, file_utils, mapping_utils

def ${component}():
    '''
    This function is part of the Kubeflow pipeline component.
    '''
    pass
"@
    $FilePath = "$ComponentsDir\$component.py"
    $Content | Out-File -Encoding UTF8 -FilePath $FilePath
}

# Create utility files
Write-Output "Creating utility files..."
$DataUtilsContent = @"
# utils/data_utils.py

def filter_columns(df, exclude_contribuable=False):
    # Filter columns based on criteria
    pass

def rename_columns(df, mapping):
    # Rename DataFrame columns based on mapping
    pass
"@
$DataUtilsContent | Out-File -Encoding UTF8 -FilePath "$UtilsDir\data_utils.py"

$FileUtilsContent = @"
# utils/file_utils.py

import pandas as pd

def read_parquet(file_path):
    # Read Parquet file and return DataFrame
    pass

def save_to_csv(df, path, sep=';'):
    # Save DataFrame to CSV
    pass

def read_json(file_path):
    # Read JSON file and return dict
    pass
"@
$FileUtilsContent | Out-File -Encoding UTF8 -FilePath "$UtilsDir\file_utils.py"

$MappingUtilsContent = @"
# utils/mapping_utils.py

def generate_column_mapping(df, mapping_json):
    # Generate column mapping based on JSON
    pass
"@
$MappingUtilsContent | Out-File -Encoding UTF8 -FilePath "$UtilsDir\mapping_utils.py"

# Create constants file
Write-Output "Creating constants file..."
$ConstantsContent = @"
# constants.py

DATA_PATH_REF = 'data_extr/contribuable_derniere_situation_cleanes_clean_all.parquet'
MAPPING_FILE = 'mapper/mapping.json'
OUTPUT_DIR = 'output_data'
"@
$ConstantsContent | Out-File -Encoding UTF8 -FilePath "$ProjectDir\constants.py"

# Create .env file
Write-Output "Creating .env file..."
$EnvContent = @"
PROJECT_ID=your_project_id
MAX_TEMP_DIR_SIZE=55GiB
"@
$EnvContent | Out-File -Encoding UTF8 -FilePath "$ProjectDir\.env"

# Create config.yaml
Write-Output "Creating config.yaml..."
$ConfigContent = @"
prepare_ref:
  input_path: 'data_extr/contribuable_derniere_situation_cleanes_clean_all.parquet'
  output_path: 'output_data/data_contribuable.csv'

prepare_source:
  input_path: 'data_input_csv/ppa.csv'
  output_path: 'output_data/source_ppa.csv'

concat_source:
  source_path: 'output_data/source_ppa.csv'
  reference_path: 'output_data/data_contribuable.csv'
  output_path: 'data_input_model/data_concatenated.csv'

splink:
  concat_data_path: 'data_input_model/data_concatenated.csv'
  output_file_path: 'resolved_ER/ppa_resolved_entities_with_custom_ids.csv'

analyze:
  input_path: 'resolved_ER/ppa_resolved_entities_with_custom_ids.csv'
  single_record_output: 'analyze/single_record_Grossistes_clusters.csv'
  final_output: 'analyze/Grossistes_final_filtered_entities_with_identification_status.csv'
  summary_stats: 'analyze/summary_grossistes_s_record_statistics.csv'
"@
$ConfigContent | Out-File -Encoding UTF8 -FilePath "$ProjectDir\config.yaml"

# Create requirements.txt
Write-Output "Creating requirements.txt..."
$RequirementsContent = @"
pandas
os
json
kubeflow
kfp
pyyaml
"@
$RequirementsContent | Out-File -Encoding UTF8 -FilePath "$ProjectDir\requirements.txt"

# Create main pipeline script
Write-Output "Creating main_pipeline.py..."
$PipelineContent = @"
# main_pipeline.py

from components.prepare_ref_component import prepare_ref_component
from components.prepare_source_component import prepare_source_component
from components.concat_source_component import concat_source_component
from components.splink_component import splink_component
from components.analyze_component import analyze_component
from kfp import dsl

@dsl.pipeline(
    name='Data Preparation and Analysis Pipeline',
    description='A pipeline to prepare and analyze data using Splink and custom filtering.'
)
def data_pipeline():
    ref_op = dsl.ContainerOp(
        name='Prepare Ref',
        image='prepare_ref_image',
        command=['python', 'prepare_ref_component.py']
    )

    source_op = dsl.ContainerOp(
        name='Prepare Source',
        image='prepare_source_image',
        command=['python', 'prepare_source_component.py']
    ).after(ref_op)

    concat_op = dsl.ContainerOp(
        name='Concatenate Sources',
        image='concat_source_image',
        command=['python', 'concat_source_component.py']
    ).after(source_op)

    splink_op = dsl.ContainerOp(
        name='Splink Processing',
        image='splink_image',
        command=['python', 'splink_component.py']
    ).after(concat_op)

    analyze_op = dsl.ContainerOp(
        name='Analyze Data',
        image='analyze_image',
        command=['python', 'analyze_component.py']
    ).after(splink_op)
"@
$PipelineContent | Out-File -Encoding UTF8 -FilePath "$ProjectDir\main_pipeline.py"

Write-Output "Project setup complete!"
