from kfp import dsl
from kfp import compiler

import google.cloud.aiplatform as aip

from custom_kfp_components.data_ingestion.load_csv import LoadCsv
from custom_kfp_components.data_preparation.label_encoding import LabelEncoding


@dsl.pipeline
def pipeline():
    data_load = LoadCsv(
        base_image='python:3.10',
        file_path="https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv")

    label_encoding = LabelEncoding(
        label_name='species',
        input_dataset=data_load.outputs['dataset'])


if __name__ == "__main__":
    # First we define our pipeline's name and specs filename
    job_name = 'demo_pipeline'
    job_spec_file_name = f'demo/{job_name}.yaml'

    # Then we compile our pipeline
    compiler.Compiler().compile(
        pipeline_func=pipeline,
        package_path=job_spec_file_name)

    # Finally we create and submit our pipeline job
    job = aip.PipelineJob(
        display_name=job_name,
        template_path=job_spec_file_name,
        parameter_values={})

    job.submit()
