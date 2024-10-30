# compile_pipeline.py

from kfp import dsl
from kfp.compiler import Compiler
from main_pipeline import data_pipeline

if __name__ == "__main__":
    # Compile the data pipeline into a YAML file
    Compiler().compile(data_pipeline, "data_pipeline.yaml")
