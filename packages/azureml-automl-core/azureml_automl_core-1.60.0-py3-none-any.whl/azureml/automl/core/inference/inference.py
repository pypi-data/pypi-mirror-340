# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import importlib.resources as package_resources
from packaging.requirements import Requirement
import os
import platform
from typing import Any, Dict, List, Tuple, cast, Optional
from azureml.automl.core.package_utilities import _all_dependencies, _all_dependencies_conda_list
from azureml.automl.core.shared import constants

PACKAGE_NAME = 'azureml.automl.core'
NumpyParameterType = 'NumpyParameterType'
PandasParameterType = 'PandasParameterType'
AutoMLCondaPackagesList = ['numpy==1.21.6',
                           'pandas==1.3.5',
                           'scikit-learn==1.5.1',
                           'holidays==0.29',
                           'psutil>=5.2.2,<6.0.0']
AutoMLPipPackagesList = ['azureml-train-automl-runtime', 'inference-schema',
                         'xgboost<=1.5.2',
                         'prophet==1.1.4',
                         'azureml-interpret', 'azureml-defaults']
spacy_english_tokenizer_url = "https://aka.ms/automl-resources/packages/en_core_web_sm-3.7.1.tar.gz"
AutoMLDNNPipPackagesList = ["pytorch-transformers==1.0.0", "spacy==3.7.4", spacy_english_tokenizer_url]
AutoMLDNNCondaPackagesList = ["pytorch==1.11.0", "cudatoolkit==9.0"]
AutoMLVisionCondaPackagesList = []
AutoMLNLPCondaPackagesList = ['numpy==1.21.6',
                              'pandas==1.3.5',
                              'psutil>=5.2.2,<6.0.0',
                              'pytorch==1.13.1']
# mlflow-skinny needs to be in this list, without which "mlflow" gets automatically added to the
# pip dependencies in conda yaml and that fails the deployment
AutoMLNLPPipPackagesList = ['azureml-automl-dnn-nlp',
                            'inference-schema',
                            'azureml-defaults',
                            'mlflow-skinny']
AMLArtifactIDHeader = 'aml://artifact/'
MaxLengthModelID = 29


class AutoMLInferenceArtifactIDs:
    CondaEnvDataLocation = 'conda_env_data_location'
    ScoringDataLocation = 'scoring_data_location'
    ScoringDataLocationV2 = 'scoring_data_location_v2'
    ScoringDataLocationPBI = 'scoring_data_location_pbi'
    ModelName = 'model_name'
    ModelDataLocation = 'model_data_location'
    PipelineGraphVersion = 'pipeline_graph_version'
    ModelSizeOnDisk = 'model_size_on_disk'


def _extract_parent_run_id_and_child_iter_number(run_id: str) -> Any:
    """
    Extract and return the parent run id and child iteration number.
    """
    parent_run_length = run_id.rfind('_')
    parent_run_id = run_id[0:parent_run_length]
    child_run_number_str = run_id[parent_run_length + 1: len(run_id)]
    try:
        # Attempt to convert child iteration number string to integer
        int(child_run_number_str)
        return parent_run_id, child_run_number_str
    except ValueError:
        return None, None


def _get_model_name(run_id: str) -> Any:
    """
    Return a model name from an AzureML run-id.

    Examples:- Input = AutoML_2cab0bf2-b6ae-4f57-b8fe-5feb13c60a5f_24
               Output = AutoML2cab0bf2b24
               Input = AutoML_2cab0bf2-b6ae-4f57-b8fe-5feb13c60a5f
               Output = AutoML2cab0bf2b
               Input = 2cab0bf2-b6ae-4f57-b8fe-5feb13c60a5f_24
               Output = 2cab0bf2b6ae4f524
    """
    run_guid, child_run_number = _extract_parent_run_id_and_child_iter_number(run_id)
    if run_guid is None:
        return run_id.replace('_', '').replace('-', '')[:MaxLengthModelID]
    else:
        return (run_guid.replace('_', '').replace('-', '')[:15] + child_run_number)[:MaxLengthModelID]


def _get_scoring_file(is_pandas_data_frame: bool,
                      input_sample_str: str, output_sample_str: str,
                      is_forecasting: bool = False,
                      task_type: str = constants.Tasks.CLASSIFICATION) -> Tuple[str, str]:
    """
    Return scoring file to be used at the inference time.

    If there are any changes to the scoring file, the version of the scoring file should
    be updated in the vendor.

    :param is_pandas_data_frame: Flag to indicate if the input_sample_str is of type Pandas.
    :param input_sample_str: The raw data snapshot of training data
    :param output_sample_str: The output data snapshot of training data
    :param automl_run_id: The AutoML run id
    :param is_forecasting: Flag to indicate if it is a forecasting run
    :param task_type: The task type of the AutoML run
    :return: Scoring python file as a string
    """
    inference_data_type = NumpyParameterType
    if is_pandas_data_frame:
        inference_data_type = PandasParameterType

    if is_forecasting:
        content_v1 = _format_scoring_file('score_forecasting.txt', inference_data_type,
                                          input_sample_str, output_sample_str)
        content_v2 = _format_scoring_file('score_forecasting_v2.txt', inference_data_type,
                                          input_sample_str, output_sample_str)
    elif task_type == constants.Tasks.REGRESSION:
        content_v1 = _format_scoring_file('score_regression.txt', inference_data_type,
                                          input_sample_str, output_sample_str)
        content_v2 = _format_scoring_file('score_regression_v2.txt', inference_data_type,
                                          input_sample_str, output_sample_str)
    else:
        content_v1 = _format_scoring_file('score_classification.txt', inference_data_type,
                                          input_sample_str, output_sample_str)
        content_v2 = _format_scoring_file('score_classification_v2.txt',
                                          inference_data_type, input_sample_str, output_sample_str)

    return content_v1, content_v2


def _get_pbi_scoring_file(
        is_pandas_data_frame: bool,
        input_sample_str: str,
        output_sample_str: str,
) -> Optional[str]:
    """
    Get the scoring file for PBI. PBI scoring file for forecasting will add the quantile and
    have a different output schema with quantiles output.
    """
    inference_data_type = NumpyParameterType
    if is_pandas_data_frame:
        inference_data_type = PandasParameterType

    content_pbi_v1 = _format_scoring_file(
        'score_forecasting_pbi_v1.txt', inference_data_type,
        input_sample_str, output_sample_str)
    return content_pbi_v1


def _format_scoring_file(filename: str,
                         inference_data_type: str,
                         input_sample_str: str,
                         output_sample_str: str) -> str:
    content = None
    scoring_path = os.path.join('inference', filename)
    scoring_ref = package_resources.files(PACKAGE_NAME) / scoring_path

    with package_resources.as_file(scoring_ref) as scoring_file_path:
        with open(scoring_file_path, 'r') as scoring_file_ptr:
            content = scoring_file_ptr.read()
            content = content.replace('<<ParameterType>>', inference_data_type)
            content = content.replace('<<input_sample>>', input_sample_str)
            content = content.replace('<<output_sample>>', output_sample_str)
            content = content.replace('<<model_filename>>', constants.MODEL_FILENAME)

    return content


def _create_conda_env_file(
        include_dnn_packages: bool = False,
        pip_packages_list_override: Optional[List[str]] = None,
        conda_packages_list_override: Optional[List[str]] = None
) -> Any:
    """
    Return conda/pip dependencies for the current AutoML run.

    If there are any changes to the conda environment file, the version of the conda environment
    file should be updated in the vendor.

    :param include_dnn_packages: Flag to add dependencies for Text DNNs to inference config.
    :type include_dnn_packages: bool
    :param pip_packages_list_override: override pip packages needed for inference
    :type pip_packages_list_override: List[str]
    :param conda_packages_list_override: override conda packages needed for inference
    :type conda_packages_list_override: List[str]
    :return: Conda dependencies as string
    """
    return _get_conda_deps(
        include_dnn_packages, pip_packages_list_override, conda_packages_list_override
    ).serialize_to_string()


def get_conda_deps_as_dict(include_dnn_packages: bool = False) -> Any:
    """
    Return conda/pip dependencies as dict for the current AutoML run.

    :param include_dnn_packages: Flag to add dependencies for Text DNNs to inference config.
    :type include_dnn_packages: bool
    :return: Conda dependencies as dict
    """
    return _get_conda_deps(include_dnn_packages).as_dict()


def _get_conda_deps(
        include_dnn_packages: bool = False,
        pip_packages_list_override: Optional[List[str]] = None,
        conda_packages_list_override: Optional[List[str]] = None
) -> Any:
    """
    Return conda/pip dependencies for the current AutoML run.

    :param include_dnn_packages: Flag to add dependencies for Text DNNs to inference config.
    :type include_dnn_packages: bool
    :param pip_packages_list_override: override pip packages needed for inference
    :type pip_packages_list_override: List[str]
    :param conda_packages_list_override: override conda packages needed for inference
    :type conda_packages_list_override: List[str]
    :return: Conda dependencies as string
    """
    from azureml.core.conda_dependencies import CondaDependencies
    sdk_dependencies = _all_dependencies()
    pip_package_list_with_version = []
    if pip_packages_list_override:
        pip_packages = pip_packages_list_override
    else:
        pip_packages = AutoMLPipPackagesList
    for pip_package in pip_packages:
        if 'azureml' in pip_package and pip_package in sdk_dependencies:
            pip_package_list_with_version.append(pip_package + "==" + sdk_dependencies[pip_package])
        else:
            pip_package_list_with_version.append(pip_package)

    if conda_packages_list_override:
        conda_packages = conda_packages_list_override
    else:
        conda_packages = AutoMLCondaPackagesList

    if include_dnn_packages:
        pip_package_list_with_version.extend(AutoMLDNNPipPackagesList)
        conda_packages.extend(AutoMLDNNCondaPackagesList)

    python_version = platform.python_version()
    conda_package_list = get_local_conda_versions(conda_packages)
    myenv = CondaDependencies.create(conda_packages=conda_package_list,
                                     python_version=python_version,
                                     pip_packages=pip_package_list_with_version,
                                     pin_sdk_version=False)

    if include_dnn_packages:
        myenv.add_channel("pytorch")

    return myenv


def get_local_conda_versions(package_list: List[str]) -> List[str]:
    local_conda_package_versions = _all_dependencies_conda_list()
    conda_package_versions = []
    for pkg in package_list:
        parsed_req = Requirement(pkg).name
        if parsed_req in local_conda_package_versions:
            conda_package_versions.append(parsed_req + "==" + local_conda_package_versions[parsed_req][0])
        else:
            conda_package_versions.append(pkg)
    return conda_package_versions
