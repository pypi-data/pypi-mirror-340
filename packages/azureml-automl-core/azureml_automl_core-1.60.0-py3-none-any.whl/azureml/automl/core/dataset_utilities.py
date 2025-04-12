# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utility methods for interacting with azureml.core.Dataset."""
import json
import logging
from typing import Any, List, Optional, Tuple, Union, Dict, NoReturn

from azureml._common._error_definition import AzureMLError
from azureml._common.exceptions import AzureMLException
from azureml.automl.core.shared import logging_utilities
from azureml.automl.core.shared._diagnostics.automl_error_definitions import DatasetUserError
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared.constants import MLTableDataLabel, MLTableLiterals
from azureml.automl.core.shared.exceptions import DataprepException, ClientException, ConfigException
from azureml.core import Dataset, Workspace
from azureml.data import FileDataset, TabularDataset
from azureml.data._loggerfactory import _LoggerFactory, trace
from azureml.data.abstract_dataset import AbstractDataset
from azureml.data.constants import _AUTOML_SUBMIT_ACTIVITY, _AUTOML_INPUT_TYPE, _AUTOML_DATSET_ID, _AUTOML_COMPUTE, \
    _AUTOML_DATASETS, _AUTOML_SPARK, _AUTOML_DATAFLOW_COUNT, _AUTOML_DATASETS_COUNT, _AUTOML_TABULAR_DATASETS_COUNT, \
    _AUTOML_OTHER_COUNT, _AUTOML_PIPELINE_TABULAR_COUNT
from azureml.data.dataset_definition import DatasetDefinition
from azureml.dataprep import Dataflow
from azureml.exceptions import UserErrorException

_deprecated = 'deprecated'
_archived = 'archived'
_logger = _LoggerFactory.get_logger(__name__)
module_logger = logging.getLogger(__name__)


def is_dataset(dataset: Any) -> bool:
    """
    Check to see if the given object is a dataset or dataset definition.

    :param dataset: object to check
    """
    return isinstance(dataset, Dataset) or isinstance(dataset, DatasetDefinition) \
        or isinstance(dataset, TabularDataset) or isinstance(dataset, FileDataset)


def convert_inputs(X: Any, y: Any, sample_weight: Any, X_valid: Any, y_valid: Any,
                   sample_weight_valid: Any) -> Tuple[Any, Any, Any, Any, Any, Any]:
    """
    Convert the given datasets to trackable definitions.

    :param X: dataset representing X
    :param y: dataset representing y
    :param sample_weight: dataset representing the sample weight
    :param X_valid: dataset representing X_valid
    :param y_valid: dataset representing y_valid
    :param sample_weight_valid: dataset representing the validation sample weight
    """
    return (
        _convert_to_trackable_definition(X),
        _convert_to_trackable_definition(y),
        _convert_to_trackable_definition(sample_weight),
        _convert_to_trackable_definition(X_valid),
        _convert_to_trackable_definition(y_valid),
        _convert_to_trackable_definition(sample_weight_valid)
    )


def ensure_saved(workspace: Workspace, **kwargs: Any) -> None:
    for arg_name, dataset in kwargs.items():
        if isinstance(dataset, TabularDataset):
            dataset._ensure_saved(workspace)


def convert_inputs_dataset(*datasets: Any) \
        -> Tuple[Any, ...]:
    """
    Convert the given datasets to trackable definitions.

    :param datasets: datasets to convert to trackable definitions
    """
    return tuple([_convert_to_trackable_definition(dataset) for dataset in datasets])


def collect_usage_telemetry(compute: Any, spark_context: Any, **kwargs: Any) -> None:
    try:
        datasets = json.dumps({name: _get_dataset_payload(dataset) for name, dataset in
                               filter(lambda tup: tup[1], kwargs.items())})
        payload = {
            _AUTOML_COMPUTE: compute if type(compute) is str else type(compute).__name__,
            _AUTOML_SPARK: spark_context is not None,
            _AUTOML_DATASETS: datasets,
            **_get_dataset_count_by_type(filter(lambda _: _, kwargs.values()))
        }
        trace(_logger, _AUTOML_SUBMIT_ACTIVITY, custom_dimensions=payload)
    except Exception:
        module_logger.debug('Error collecting dataset usage telemetry.')


def get_datasets_json(training_data: Any = None,
                      validation_data: Any = None,
                      test_data: Any = None) -> Optional[str]:
    """Get dataprep json.

    :param training_data: Training data.
    :type training_data: azureml.core.Dataset
    :param validation_data: Validation data
    :type validation_data: azureml.core.Dataset
    :param test_data: Test data
    :type test_data: azureml.core.Dataset
    :return: JSON string representation of a dict of Dataset
    """
    dataset_json = None
    df_value_list = [training_data, validation_data, test_data]
    if any(var is not None for var in df_value_list):
        dataset_dict = {
            'training_data': training_data,
            'validation_data': validation_data,
            'test_data': test_data
        }
        dataset_json = _save_datasets_to_json(dataset_dict)

        # We must always be able to JSON-ify Datasets
        Contract.assert_value(dataset_json, "dataset_json")

    return dataset_json


def get_dataset_from_mltable_data_json(
        ws: Workspace,
        mltable_data_json_obj: Dict[str, Any],
        data_label: MLTableDataLabel
) -> Optional[AbstractDataset]:
    """
    Get dataset from MLTable data json

    :param ws: workspace to get dataset from
    :param mltable_data_json_obj: mltable data json object
    :param data_label: label indicating dataset to load from mltable data json
    :return:
    """
    dataset = None
    data_dict = mltable_data_json_obj.get(data_label.value, None)
    if data_dict:
        dataset_uri = data_dict.get(MLTableLiterals.MLTABLE_RESOLVEDURI, None)
        try:
            dataset = AbstractDataset._load(dataset_uri, ws)
        except (UserErrorException, ValueError) as e:
            generic_msg = 'Error in loading the dataset from MLTable. Error: {0}'.format(str(e))
            module_logger.error(generic_msg)
            error = AzureMLError.create(DatasetUserError, dataset_error=str(e))
            raise UserErrorException(generic_msg)._with_error(azureml_error=error, inner_exception=e)
        except Exception as e:
            module_logger.error(f"Unexpected error: {str(e)} (type: {type(e)})")
            raise ClientException.from_exception(e)
    return dataset


def get_datasets_from_mltable_data_json(
        ws: Workspace,
        mltable_data_json_obj: Dict[str, Any],
        data_labels: List[MLTableDataLabel]
) -> Tuple[Optional[AbstractDataset], Optional[AbstractDataset], Optional[AbstractDataset]]:
    """
    Get datasets from MLTable data json (with uri)

    :param ws: workspace to get dataset from
    :param data_preparation_json: data json object
    :param data_labels: list of labels indicating dataset to load from data json
    :return:
    """
    train_dataset = None
    valid_dataset = None
    test_dataset = None
    if MLTableDataLabel.TrainData in data_labels:
        train_dataset = get_dataset_from_mltable_data_json(ws, mltable_data_json_obj, MLTableDataLabel.TrainData)
    if MLTableDataLabel.ValidData in data_labels:
        valid_dataset = get_dataset_from_mltable_data_json(ws, mltable_data_json_obj, MLTableDataLabel.ValidData)
    if MLTableDataLabel.TestData in data_labels:
        test_dataset = get_dataset_from_mltable_data_json(ws, mltable_data_json_obj, MLTableDataLabel.TestData)
    return train_dataset, valid_dataset, test_dataset


def get_datasets_from_dataprep_json(
        ws: Workspace,
        dataprep_json: Dict[str, Any],
        data_labels: List[MLTableDataLabel]
) -> Tuple[Optional[AbstractDataset], Optional[AbstractDataset], Optional[AbstractDataset]]:
    """
    Get dataset from Dataprep json (with dataset id)

    :param ws: workspace to get dataset from
    :param data_preparation_json: data json object
    :param data_labels: list of labels indicating dataset to load from data json
    :return:
    """
    train_dataset = None
    valid_dataset = None
    test_dataset = None

    if MLTableDataLabel.TrainData in data_labels:
        train_data_obj = dataprep_json.get('training_data')
        if train_data_obj:
            train_dataset_id = train_data_obj['datasetId']
            train_dataset = Dataset.get_by_id(ws, train_dataset_id)

    if MLTableDataLabel.ValidData in data_labels:
        valid_data_obj = dataprep_json.get('validation_data')
        if valid_data_obj:
            valid_dataset_id = valid_data_obj['datasetId']
            valid_dataset = Dataset.get_by_id(ws, valid_dataset_id)

    if MLTableDataLabel.TestData in data_labels:
        test_data_obj = dataprep_json.get('test_data')
        if test_data_obj:
            test_dataset_id = test_data_obj['datasetId']
            test_dataset = Dataset.get_by_id(ws, test_dataset_id)

    return train_dataset, valid_dataset, test_dataset


def get_datasets_from_data_json(
        ws: Workspace,
        data_preparation_json: Dict[str, Any],
        data_labels: List[MLTableDataLabel]
) -> Tuple[Optional[AbstractDataset], Optional[AbstractDataset], Optional[AbstractDataset]]:
    """
    Get datasets from data json that can be either MLTable data json (with uri) or Dataprep json (with dataset id)

    :param ws: workspace to get dataset from
    :param data_preparation_json: data json object
    :param data_labels: list of labels indicating dataset to load from data json
    :return:
    """
    try:
        if data_preparation_json.get('Type', None) == MLTableLiterals.MLTABLE:
            return get_datasets_from_mltable_data_json(ws, data_preparation_json, data_labels)
        else:
            return get_datasets_from_dataprep_json(ws, data_preparation_json, data_labels)
    except (UserErrorException, ValueError) as e:
        generic_msg = 'Failed to get dataset. Error: {0}'.format(str(e))
        module_logger.error(generic_msg)
        error = AzureMLError.create(DatasetUserError, dataset_error=str(e))
        raise UserErrorException(generic_msg)._with_error(azureml_error=error, inner_exception=e)
    except (AzureMLException, SystemError) as e:
        raise ClientException.from_exception(e).with_generic_msg("Failed to get dataset.") from e


def _save_datasets_to_json(dataset_dict: Dict[str, Any]) -> Optional[str]:
    """Save dataflows to json.

    :param dataset_dict: the dict with key as dataflow name and value as dataset
    :type dataset_dict: dict(str, azureml.dataprep.Dataflow)
    :return: the JSON string representation of a dict of Dataset
    """
    dataset_json_dict = {}     # type: Dict[str, Any]
    for name in dataset_dict:
        dataset = dataset_dict[name]
        if not type(dataset) in [TabularDataset, FileDataset]:
            module_logger.info("JSON serialization of input of type {} is un-supported.".format(type(dataset)))
            continue
        dataset_json = {'datasetId': dataset.id}
        dataset_json_dict[name] = dataset_json

    if len(dataset_json_dict) == 0:
        return None

    # This key is added to help the validation service decide on the correct validation path
    dataset_json_dict['datasets'] = 0
    return json.dumps(dataset_json_dict)


def _convert_to_trackable_definition(dataset: Any) -> Union[Any, Dataflow]:
    definition, trackable = _reference_dataset(dataset)
    if not trackable:
        module_logger.debug('Unable to convert input to trackable definition')
    return definition


def _reference_dataset(dataset: Any) -> Tuple[Union[Any, Dataflow], bool]:
    from azureml.dataprep import Dataflow

    if not is_dataset(dataset) and not isinstance(dataset, Dataflow):
        return dataset, False

    if type(dataset) == Dataflow:
        return dataset, _contains_dataset_ref(dataset)

    if type(dataset) in [TabularDataset, FileDataset]:
        return dataset._dataflow, False

    # un-registered dataset
    if isinstance(dataset, DatasetDefinition) and not dataset._workspace:
        return dataset, _contains_dataset_ref(dataset)

    _verify_dataset(dataset)
    return Dataflow.reference(dataset), True


def _contains_dataset_ref(definition: DatasetDefinition) -> bool:
    for step in definition._get_steps():
        if step.step_type == 'Microsoft.DPrep.ReferenceBlock' \
                and _get_ref_container_path(step).startswith('dataset://'):
            return True
    return False


def _get_dataset_info(definition: DatasetDefinition) -> str:
    for step in definition._get_steps():
        ref_path = _get_ref_container_path(step)
        if step.step_type == 'Microsoft.DPrep.ReferenceBlock' and ref_path.startswith('dataset://'):
            return ref_path
    raise DataprepException.create_without_pii('Unexpected error, unable to retrieve dataset information.')


def _get_ref_container_path(step: Any) -> str:
    if step.step_type != 'Microsoft.DPrep.ReferenceBlock':
        return ''
    try:
        return step.arguments['reference'].reference_container_path or ''
    except AttributeError:
        # this happens when a dataflow is serialized and deserialized
        return step.arguments['reference']['referenceContainerPath'] or ''
    except KeyError:
        return ''


def _verify_dataset(dataset: Any) -> None:
    if isinstance(dataset, Dataset):
        if dataset.state == _deprecated:
            module_logger.warning('Warning: Input dataset is deprecated.')
        if dataset.state == _archived:
            message = 'Error: Input dataset is archived and cannot be used.'
            ex = DataprepException.create_without_pii(message)
            logging_utilities.log_traceback(
                ex,
                module_logger
            )
            raise ex

    if isinstance(dataset, DatasetDefinition):
        if dataset._state == _deprecated:
            message = 'Warning: this definition is deprecated.'
            dataset_and_version = ''
            if dataset._deprecated_by_dataset_id:
                dataset_and_version += 'Dataset ID: \'{}\' '.format(dataset._deprecated_by_dataset_id)
            if dataset._deprecated_by_definition_version:
                dataset_and_version += 'Definition version: \'{}\' '.format(dataset._deprecated_by_definition_version)
            if dataset_and_version:
                message += ' Please use \'{}\' instead.'.format(dataset_and_version.strip(' '))
            module_logger.warning(message)
        if dataset._state == _archived:
            message = 'Error: definition version \'{}\' is archived and cannot be used'.format(dataset._version_id)
            ex = DataprepException.create_without_pii(message)
            logging_utilities.log_traceback(
                ex,
                module_logger
            )
            raise ex


def _get_dataset_payload(dataset: Any) -> Dict[str, Optional[str]]:
    try:
        return {
            _AUTOML_INPUT_TYPE: type(dataset).__name__,
            _AUTOML_DATSET_ID: _get_dataset_id(dataset)
        }
    except Exception:
        module_logger.debug('Unable to get telemetry payload.')
        return {}


def _get_dataset_id(dataset: Any) -> Optional[str]:
    # The code below first tries the get the ID assuming the type is Dataset or _Dataset, if it fails it then assumes
    # it is of DatasetDefinition type. If that fails, it is not a known dataset type.
    id = None  # type: Optional[str]
    try:
        id = dataset.id
        return id
    except AttributeError:
        pass

    try:
        id = dataset._dataset_id
        return id
    except AttributeError:
        pass

    return None


def _get_dataset_count_by_type(datasets: Any) -> Dict[str, int]:
    def increment(dictionary, key):
        dictionary[key] = dictionary.get(key, 0) + 1

    mappings = {
        TabularDataset.__name__: _AUTOML_TABULAR_DATASETS_COUNT,
        Dataset.__name__: _AUTOML_DATASETS_COUNT,
        Dataflow.__name__: _AUTOML_DATAFLOW_COUNT,
        'PipelineOutputTabularDataset': _AUTOML_PIPELINE_TABULAR_COUNT
    }
    count = {}  # type: Dict[str, int]

    for dataset in datasets:
        increment(count, mappings.get(type(dataset).__name__, _AUTOML_OTHER_COUNT))

    return count
