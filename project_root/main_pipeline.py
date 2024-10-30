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
