# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Module for starting forecast DNN run with passed in model."""
import argparse
import os
import math
import json
import logging
import numpy as np
import pandas as pd
from typing import Any, cast, Dict, Optional, Tuple

from ....constants import ForecastConstant
from ....wrapper.forecast_wrapper import DNNForecastWrapper, DNNParams
from ....wrapper.deep4cast_wrapper import Deep4CastWrapper
from ....wrapper.forecast_tcn_wrapper import ForecastTCNWrapper

import azureml.automl.core  # noqa: F401
from azureml.automl.core._run import run_lifecycle_utilities
from azureml.automl.core.systemusage_telemetry import SystemResourceUsageTelemetryFactory
from azureml.automl.core.shared import constants, logging_utilities
from azureml.automl.runtime import _time_series_training_utilities
from azureml.automl.runtime.experiment_store import ExperimentStore
from azureml.automl.runtime.featurizer.transformer.timeseries.timeseries_transformer import TimeSeriesTransformer
from azureml.automl.runtime.shared.lazy_azure_blob_cache_store import LazyAzureBlobCacheStore
from azureml.contrib.automl.dnn.forecasting.wrapper import _wrapper_util
from azureml.contrib.automl.dnn.forecasting.wrapper._distributed_helper import DistributedHelper
from azureml.core.run import Run
from azureml.data import TabularDataset
from azureml.train.automl._azureautomlsettings import AzureAutoMLSettings
from azureml.train.automl.runtime._data_preparer import DataPreparerFactory
from azureml.train.automl.runtime._entrypoints.utils.common import get_parent_run
from azureml.train.automl.runtime._code_generation.utilities import generate_model_code_and_notebook

# Minimum parameter needed to initiate a training
required_params = [ForecastConstant.model, ForecastConstant.output_dir,
                   ForecastConstant.report_interval, ForecastConstant.config_json]
# get the logger default logger as placeholder.
logger = logging.getLogger(__name__)


def get_model(model_name: str, metadata: Dict[str, str]) -> DNNForecastWrapper:
    """Return a `DNNForcastWrapper` corresponding to the passed in model_name.

    :param model_name:  name of the model to train
    :return: gets a wrapped model for Automl DNN Training.
    """
    model_dict = {ForecastConstant.Deep4Cast: Deep4CastWrapper,
                  ForecastConstant.ForecastTCN: ForecastTCNWrapper}
    return model_dict[model_name](metadata)


def run(
    mltable_data_json: Optional[str] = None,
    **kwargs: Any
) -> None:
    """Entry point for runner.py with error classification."""
    try:
        _run(mltable_data_json, **kwargs)
    except Exception as e:
        current_run = Run.get_context()
        logger.error("TCN runner script terminated with an exception of type: {}".format(type(e)))
        run_lifecycle_utilities.fail_run(current_run, e)
        raise


def _run(
    mltable_data_json: Optional[str] = None,
    **kwargs: Any
) -> DNNForecastWrapper:
    """Start the DNN training based on the passed in parameters.

    :return:
    """
    # get command-line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument(DNNForecastWrapper.get_arg_parser_name(ForecastConstant.model), type=str,
                        help='model name', default=ForecastConstant.ForecastTCN)
    parser.add_argument('--output_dir', type=str, help='output directory', default="./outputs")
    parser.add_argument(DNNForecastWrapper.get_arg_parser_name(ForecastConstant.num_epochs), type=int,
                        default=25,
                        help='number of epochs to train')
    parser.add_argument(DNNForecastWrapper.get_arg_parser_name(ForecastConstant.primary_metric), type=str,
                        default="normalized_root_mean_squared_error", help='primary metric')
    parser.add_argument(DNNForecastWrapper.get_arg_parser_name(ForecastConstant.report_interval), type=int,
                        default=1, help='number of epochs to report score')
    parser.add_argument(DNNForecastWrapper.get_arg_parser_name(ForecastConstant.config_json), type=str,
                        default=ForecastConstant.config_json_default,
                        help='json representation of dataset and training settings from automl SDK')
    parser.add_argument(DNNForecastWrapper.get_arg_parser_name(ForecastConstant.parent_run_override), type=str,
                        default=None,
                        help=('The name of parent run, containing the '
                              'featurized data. Used for testing purposes only')
                        )
    args, unknown = parser.parse_known_args()
    os.makedirs(args.output_dir, exist_ok=True)
    args_dict = vars(args)
    params = DNNParams(required_params, args_dict, None)

    config_file = params.get_value(ForecastConstant.config_json)

    current_run = Run.get_context()
    dnn_settings, automl_settings_obj, datasets_definition_json = _parse_settings_file(config_file)
    if mltable_data_json is not None:
        datasets_definition_json = mltable_data_json

    metadata = _time_series_training_utilities._get_metadata_dict(
        model_name=constants.ModelClassNames.ForecastingModelClassNames.TCNForecaster,
        is_distributed=dnn_settings[ForecastConstant.CONSUME_DIST_FEATURIZATION_OUTPUT],
        run_id=current_run.id
    )
    model = get_model(params.get_value(ForecastConstant.model), metadata)

    DistributedHelper.initialize()

    if dnn_settings[ForecastConstant.CONSUME_DIST_FEATURIZATION_OUTPUT]:
        train_featurized_dataset, valid_featurized_dataset, expr_store, apply_log_transform_for_label, \
            raw_data_sample = _get_distributed_featurization_output(current_run, args.__parent_run_override)
    else:
        X, y, X_train, y_train, X_valid, y_valid, featurizer, apply_log_transform_for_label, raw_data_sample = \
            _get_training_data(dnn_settings, automl_settings_obj, datasets_definition_json)
    # Set the log transform option on the model if its not set by the config
    if ForecastConstant.apply_log_transform_for_label not in dnn_settings:
        dnn_settings[ForecastConstant.apply_log_transform_for_label] = apply_log_transform_for_label

    # Initialize model with config settings
    model.init_model(dnn_settings)
    model.raw_data_sample = raw_data_sample
    assert ForecastConstant.primary_metric in model.automl_settings
    num_epochs = params.get_value(ForecastConstant.num_epochs)
    logging_utilities.log_system_info(logger, prefix_message="[RunId:{}]".format(current_run.id))

    telemetry_logger = SystemResourceUsageTelemetryFactory.get_system_usage_telemetry(interval=10)

    telemetry_logger.send_usage_telemetry_log(
        prefix_message="[RunId:{}][Starting DNN Training]".format(current_run.id),
    )

    logging_utilities.log_system_info(logger, prefix_message="[RunId:{}]".format(current_run.id))

    telemetry_logger.send_usage_telemetry_log(
        prefix_message="[RunId:{}][Before DNN Train]".format(current_run.id),
    )

    if dnn_settings[ForecastConstant.CONSUME_DIST_FEATURIZATION_OUTPUT]:
        model._distributed_train(
            num_epochs,
            train_featurized_dataset,
            valid_featurized_dataset,
            expr_store,
            automl_settings_obj
        )
    else:
        model.train_model(
            num_epochs, X=X, y=y, X_train=X_train, y_train=y_train, X_valid=X_valid,
            y_valid=y_valid, featurizer=featurizer)

    enable_code_generation = automl_settings_obj.enable_code_generation
    logger.info("Code generation enabled: {}".format(enable_code_generation))
    if enable_code_generation:
        generate_model_code_and_notebook(current_run)

    telemetry_logger.send_usage_telemetry_log(
        prefix_message="[RunId:{}][After DNN Train completed]".format(current_run.id),
    )
    return model


def _get_distributed_featurization_output(current_run: Run, run_override: Optional[str] = None) -> Tuple[
        TabularDataset, TabularDataset, ExperimentStore, str]:
    """Get the output from the distirbuted feautirzation phase."""
    workspace = current_run.experiment.workspace
    default_datastore = workspace.get_default_datastore()

    with logging_utilities.log_activity(logger=logger, activity_name='LoadExperimentStore'):
        if run_override:
            logger.warning("Reading the data from the overridden run ID.")
        run_id = run_override if run_override else get_parent_run(current_run).id
        cache_store = LazyAzureBlobCacheStore(default_datastore, run_id)
        expr_store = ExperimentStore(cache_store, read_only=True)
        expr_store.load()

    with logging_utilities.log_activity(logger=logger, activity_name='FetchTabularDataset'):
        train_featurized_dataset: TabularDataset = expr_store.data.partitioned.get_featurized_train_dataset(workspace)
        valid_featurized_dataset: TabularDataset = expr_store.data.partitioned.get_featurized_valid_dataset(workspace)

    data_snapshot = expr_store.metadata.raw_data_snapshot_str

    with logging_utilities.log_activity(logger=logger, activity_name='LoadingLogTransformDecision'):
        apply_log_transform_for_label = expr_store.metadata.timeseries.apply_log_transform_for_label

    return (
        train_featurized_dataset,
        valid_featurized_dataset,
        expr_store,
        apply_log_transform_for_label,
        data_snapshot
    )


def _downcast_dataframe_types(df: pd.DataFrame) -> pd.DataFrame:
    """Safely downcast integer and float dataframe types to conserve memory."""
    float_cols = df.select_dtypes('float').columns
    int_cols = df.select_dtypes('integer').columns

    for float_col in float_cols:
        df[float_col] = pd.to_numeric(df[float_col], downcast='float')

    for int_col in int_cols:
        df[int_col] = pd.to_numeric(df[int_col], downcast='integer')

    return df


def _get_training_data(
    settings: dict,
    automl_settings_obj: AzureAutoMLSettings,
    datasets_definition_json: str,
) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame], Optional[pd.DataFrame], Optional[pd.DataFrame],
           Optional[pd.DataFrame], Optional[pd.DataFrame], TimeSeriesTransformer, bool, Optional[pd.DataFrame]]:
    """Get the training data the form of tuples from dictionary.

    :param settings: Settings for the forecasting problem.
    :param automl_settings_obj: AutoML settings.
    :param datasets_definition_json: datasets definitions.
    :return: A tuple with transformed train and validation data & the trained featurizer.
    """
    X, y, X_train, y_train, X_valid, y_valid, featurizer, apply_log_transform_for_label, raw_data_sample = \
        _featurize_raw_data(settings[ForecastConstant.automl_settings], automl_settings_obj,
                            datasets_definition_json)

    return X, y, X_train, y_train, X_valid, y_valid, featurizer, apply_log_transform_for_label, raw_data_sample


def _featurize_raw_data(automl_settings: dict, automl_settings_obj: AzureAutoMLSettings,
                        datasets_definition_json: str) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame],
                                                                Optional[pd.DataFrame], Optional[pd.DataFrame],
                                                                Optional[pd.DataFrame], Optional[pd.DataFrame],
                                                                Optional[pd.DataFrame]]:
    """Featurize the raw the data."""
    X_transformed, y_transformed, X_train_transformed, y_train_transformed, X_valid_transformed, y_valid_transformed, \
        featurizer = None, None, None, None, None, None, None
    apply_log_transform_for_label = True

    X, y, X_train, y_train, X_valid, y_valid, raw_data_sample = _get_raw_data(
        automl_settings_obj, datasets_definition_json)

    # In the above _get_raw_data function, the time series identifier column names will be detected by the
    # timeseries id detection data guardrail and stored in the automl_settings_obj.
    # Here we store it in automl_settings because that is used in data featurization.
    automl_settings[ForecastConstant.automl_constants.TimeSeries.GRAIN_COLUMN_NAMES] = \
        automl_settings_obj.grain_column_names

    if X_train is not None:
        # train the featurizer and transform training data
        X_train_transformed, y_train_transformed, featurizer, apply_log_transform_for_label = \
            _wrapper_util.train_featurizer_and_transform(X_train, y_train, automl_settings)
        # featurize test data.
        X_valid_transformed, y_valid_transformed = _wrapper_util.transform_data(featurizer, X_valid, y_valid)
    elif X is not None:
        # train the featurizer and transform the full data
        X_transformed, y_transformed, featurizer, apply_log_transform_for_label = \
            _wrapper_util.train_featurizer_and_transform(X, y, automl_settings)

    return (X_transformed, y_transformed, X_train_transformed, y_train_transformed, X_valid_transformed,
            y_valid_transformed, featurizer, apply_log_transform_for_label, raw_data_sample)


def _get_raw_data(automl_settings_obj: AzureAutoMLSettings, datasets_definition_json: str) -> Tuple[
        Optional[pd.DataFrame], Optional[np.ndarray], Optional[pd.DataFrame], Optional[np.ndarray],
        Optional[pd.DataFrame], Optional[np.ndarray], Optional[pd.DataFrame]]:
    """Fetch the raw data for the experiment."""
    data_preparer = DataPreparerFactory.get_preparer(datasets_definition_json)
    # Read data from the source and create various panda frames
    raw_experiment_data = data_preparer.prepare_raw_experiment_data(automl_settings_obj)

    # frequency fixing and data cleaning of raw data.
    X_full, y_full, X_valid, y_valid = _wrapper_util.preprocess_raw_data(raw_experiment_data, automl_settings_obj)
    raw_data_sample = X_full[-1:].copy()
    X, y, X_train, y_train = None, None, None, None
    if X_valid is not None:
        X_train, y_train = X_full, y_full
    else:
        X, y = X_full, y_full

    return X, y, X_train, y_train, X_valid, y_valid, raw_data_sample


def _parse_settings_file(file_name: str) -> Tuple[dict, AzureAutoMLSettings, Any]:
    """Create dprep dataset dict and training setting dict.

    :param file_name: file containing the dataset dprep and other training parameters such as
                      lookback, horizon and time column name.
    :return:
    """
    params = json.load(open(file_name, encoding='utf-8-sig'))
    clean_settings = clean_general_settings_json_parse(params['general.json'])
    general_setting_dict = json.loads(clean_settings)
    settings = get_parameters_from_general_settings(general_setting_dict)
    automl_settings = settings[ForecastConstant.automl_settings]
    automl_settings_obj = _wrapper_util.get_automl_base_settings(automl_settings)

    # JOS settings as a dictionary may or may not contain keys SDK uses during featurization and training
    # as a short term fix, the grain_column_names will be set here to ensure this setting is always
    # present in the settings passed to AutoML core SDK. As a long term fix we should figure out
    # how to use the automl_settings_obj which correctly sets all attributes, not matter what is sent by
    # JOS.
    settings[ForecastConstant.grain_column_names] = automl_settings_obj.grain_column_names
    settings[ForecastConstant.enable_future_regressors] = automl_settings_obj._enable_future_regressors
    return settings, automl_settings_obj, params[ForecastConstant.dataset_definition_key]


def clean_general_settings_json_parse(orig_string: str) -> str:
    """Convert word/char into JSON parse form.

    :param orig_string: the original string to convert.
    :return:
    """
    ret_string = orig_string
    replace = {"None": "null", "True": "true", "False": "false", "'": "\""}
    for item in replace:
        ret_string = ret_string.replace(item, replace[item])
    return ret_string


def get_parameters_from_general_settings(general_setting_dict: dict) -> dict:
    """Collect parameter for training from setting.

    :param general_setting_dict: dictionary of parameters from automl settings.
    :return:
    """
    settings = {}
    if ForecastConstant.Horizon in general_setting_dict:
        if isinstance(general_setting_dict.get(ForecastConstant.Horizon, ForecastConstant.max_horizon_default), int):
            settings[ForecastConstant.Horizon] = int(general_setting_dict[ForecastConstant.Horizon])
        else:
            settings[ForecastConstant.Horizon] = ForecastConstant.auto
    if ForecastConstant.Lookback in general_setting_dict:
        settings[ForecastConstant.Lookback] = int(general_setting_dict[ForecastConstant.Lookback])
        settings[ForecastConstant.n_layers] = max(int(math.log2(settings[ForecastConstant.Lookback])), 1)

    settings[ForecastConstant.CONSUME_DIST_FEATURIZATION_OUTPUT] = \
        general_setting_dict.get('use_distributed') is True

    settings[ForecastConstant.primary_metric] = general_setting_dict.get(ForecastConstant.primary_metric,
                                                                         ForecastConstant.default_primary_metric)

    automl_settings = general_setting_dict.copy()
    for item_excluded in ForecastConstant.EXCLUDE_AUTOML_SETTINGS:
        if item_excluded in automl_settings:
            del automl_settings[item_excluded]

    # This dataset settings dictionary is used as the ts_param_dict internally when the
    # TimeseriesDataset calls suggest_featurization_timeseries. To ensure the settings
    # are "valid" we must inject an empty grain column names here as well. Grain column
    # names might not be set by JOS when passed to the SDK at runtime. This object should
    # really use the same helper method as AutoML uses to create the ts_param_dict in the
    # short term. In the longer term we should consider using a strongly typed object which
    # requires or defaults all expected parameters.
    if ForecastConstant.grain_column_names not in automl_settings:
        automl_settings[ForecastConstant.grain_column_names] = None
    assert ForecastConstant.primary_metric in automl_settings
    settings[ForecastConstant.automl_settings] = automl_settings
    return settings
