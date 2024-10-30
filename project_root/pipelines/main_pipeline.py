import kfp
from kfp import dsl
from components.prepare_ref_component import prepare_ref
from components.prepare_source_component import prepare_source
from components.concat_component import concat_source_ref
from components.splink_component import splink_entity_resolution
from components.analyse_component import analyse_clusters


@dsl.pipeline(
    name="Entity Resolution Pipeline",
    description="Pipeline to prepare, filter, and resolve entity data"
)
def entity_resolution_pipeline():
    prepare_ref_task = prepare_ref()
    prepare_source_task = prepare_source()

    concat_task = concat_source_ref().after(prepare_ref_task, prepare_source_task)
    splink_task = splink_entity_resolution().after(concat_task)
    analyse_task = analyse_clusters().after(splink_task)


if __name__ == "__main__":
    kfp.compiler.Compiler().compile(entity_resolution_pipeline, "entity_resolution_pipeline.yaml")
