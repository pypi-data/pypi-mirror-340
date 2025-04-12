# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""SDK utilities dealing with the runtime environment."""
import logging
import os
import platform
import re
from typing import Any, Dict, Optional, Union

from packaging.requirements import Requirement, InvalidRequirement

from azureml.automl.core.shared.exceptions import ClientException
from azureml.automl.core import package_utilities
from azureml.core import Environment, RunConfiguration, Workspace
from azureml.core.conda_dependencies import CondaDependencies
import azureml.train.automl
from azureml.train.automl._constants_azureml import EnvironmentSettings
from ._azureautomlsettings import AzureAutoMLSettings
from .constants import Environments, PYPI_INDEX
from . import constants

logger = logging.getLogger(__name__)

NON_PROD_ENVIRONMENTS = {
    "AzureML-AutoML": "AutoML-Non-Prod",
    "AzureML-AutoML-GPU": "AutoML-Non-Prod-GPU",
    "AzureML-AutoML-DNN": "AutoML-Non-Prod-DNN",
    "AzureML-AutoML-DNN-GPU": "AutoML-Non-Prod-DNN-GPU",
    "AzureML-AutoML-DNN-Forecasting-GPU": "AutoML-Non-Prod-DNN-Forecasting-GPU",
    "AzureML-AutoML-DNN-Vision-GPU": "AutoML-DNN-Vision-GPU-NonProd",
    "AzureML-AutoML-DNN-Text-GPU": "AutoML-DNN-Text-GPU-Candidate"
}


class _Package:
    """A class to identify packages."""

    def __init__(self, name: str, regex: str, is_conda: bool, required_version: Optional[str] = None):
        """
        Create a package representation.

        :param name: The name of the package.
        :type name: str
        :param regex: The regex to search for in conda dependencies.
        :type regex: str
        :param is_conda: The flag to determine if package should be a conda package.
        :type is_conda: bool
        :param required_version: The version specifier. Should follow PEP 440.
        :type required_version: str
        """
        self.name = name
        self.regex = regex
        self.is_conda = is_conda

        if required_version is not None:
            try:
                specifier = Requirement(name + required_version).specifier
                if len(specifier) < 1:
                    # ensure version specifier is complete. If length is 0 then only a number was provided
                    raise ClientException.create_without_pii(
                        "Invalid version specifier. Ensure version follows PEP 440 standards.")
            except (InvalidRequirement):
                # allow conda's '=' version matching clause, different from pip's '=='
                conda_version_matching_regex = r"^\=[\.0-9]+$"
                is_conda_double_equals = is_conda and re.search(conda_version_matching_regex, required_version)
                if not is_conda_double_equals:
                    raise ClientException.create_without_pii(
                        "Invalid version specifier. Ensure version follows PEP 440 standards.")
        self.required_version = required_version


def modify_run_configuration(settings: AzureAutoMLSettings,
                             run_config: RunConfiguration,
                             logger: Union[logging.Logger, logging.LoggerAdapter]) -> RunConfiguration:  # type: ignore
    """
    Modify the run configuration with the correct version of AutoML and pip feed.
    Install pytorch, pytorch-transformer and cudatoolkit=10 in remote environment.
    GPU support enabled for CUDA driver version >= 384.81.
    Currently supports Linux which is the OS for remote compute, though Windows should work too.
    """
    from azureml.core.conda_dependencies import CondaDependencies, DEFAULT_SDK_ORIGIN
    import azureml.train.automl

    installed_packages = package_utilities._all_dependencies()

    # The meta package might not be installed on user's machine, but client will be, so we can use that for looking
    # up the version.
    automl_regex = r"azureml\S*automl\S*"
    automl_meta_pkg = "azureml-train-automl"

    defaults_regex = r"azureml\S*defaults"
    defaults_pkg = "azureml-defaults"

    prophet_pkg = "prophet"
    prophet_regex = "prophet==1.1.4"

    holidays_pkg = "holidays"
    holidays_regex = "holidays==0.29"

    joblib_pkg = "joblib"
    joblib_regex = "joblib==1.2.0"

    git_setuptools_pkg = "setuptools-git"
    git_setuptools_regex = r"setuptools-git==1.2"

    numpy_pkg = "numpy"
    numpy_regex = r"numpy>=1.16.0,<1.17.0"

    pandas_pkg = "pandas"
    pandas_regex = r"pandas==1.3.5"

    psutil_pkg = "psutil"
    psutil_regex = r"psutil([\=\<\>\~0-9\.\s]+|\Z)"

    sklearn_pkg = "scikit-learn"
    sklearn_regex = r"scikit-learn<=1.5.1,>=1.0.0"

    pytorch_pkg = "pytorch"
    pytorch_regex = r"pytorch=1\.4\.0"

    cudatoolkit_pkg = "cudatoolkit"
    cudatoolkit_regex = r"cudatoolkit=10\.1\.243"

    xgboost_pkg = "xgboost"
    xgboost_regex = r"xgboost<=1\.5\.2"

    # Adding inference schema generation package so we can reuse same env for inferencing as well
    inference_schema_pkg = "inference-schema"
    inference_schema_regex = r"inference-schema([\=\<\>\~0-9\.\s]+|\Z)"

    pytorch_transformers_pkg = "pytorch-transformers"  # includes BERT, XLNet, GPT-2 etc.
    pytorch_transformers_regex = r"pytorch-transformers==1.0.0"

    spacy_pkg = "spacy"  # tokenizer required by BiLSTM text DNN model
    spacy_regex = r"spacy==3.7.4"

    # download english tokenizer model
    spacy_english_model_url = "https://aka.ms/automl-resources/packages/en_core_web_sm-3.7.1.tar.gz"
    spacy_english_model_regex = "en_core_web_sm"

    urllib3_pkg = "urllib3"
    urllib3_regex = r"urllib3==1.26.7"

    azurecore_pkg = "azure-core"
    azurecore_regex = r"azure-core==1.24.1"

    boto3_pkg = "boto3"
    boto3_regex = "==1.15.18"

    botocore_pkg = "botocore"
    botocore_regex = "==1.18.18"
    # tar ball from github.com/NVIDIA/apex for half-precision floating point arithmetic
    # apex_url = "https://aka.ms/automl-resources/packages/apex.tar.gz"
    # apex_regex = "apex"

    # full version (including patch for automl pacakge)
    automl_version = azureml.train.automl.SELFVERSION  # type: Optional[str]

    # major, minor version for automl dependencies
    candidates = ['a', 'b', 'r']
    is_sdk_candidate = any([candidate_match for candidate_match in candidates
                            if candidate_match in azureml.train.automl.VERSION])
    is_gated_build = re.match('0[.]1[.]0[.]\\d+', azureml.train.automl.VERSION) is not None
    is_patch_build = (".post" in azureml.train.automl.VERSION)
    if is_sdk_candidate or is_gated_build or is_patch_build:
        automl_generic_version = azureml.train.automl.VERSION  # type: Optional[str]
    else:
        automl_generic_version = "{}.*".format(azureml.train.automl.VERSION)
    automl_pin_generic_version = "=={}".format(automl_generic_version)  # type: Optional[str]

    if automl_version and automl_version == "0.1.0.0":
        warning_message = (
            "You are running a developer or editable installation of required packages. Your "
            "changes will not be run on your remote compute. Latest versions of "
            "azureml-core and azureml-train-automl will be used unless you have "
            "specified an alternative index or version to use."
        )
        logger.warning(warning_message)
        logging.warning(warning_message)
        automl_pin_generic_version = None
        automl_generic_version = None
        automl_version = None

    required_package_list = [
        # If automl version is not an editable install use that version otherwise automl_pin_generic_Version will be
        # none, taking latest pypi. If we pin to meta pacakge only, take generic version to ensure no package not found
        # issues with a patch.
        _Package(automl_meta_pkg, automl_regex, False, automl_pin_generic_version),
        _Package(defaults_pkg, defaults_regex, False, automl_pin_generic_version),
        _Package(pandas_pkg, pandas_regex, True, "==1.3.5"),
        _Package(psutil_pkg, psutil_regex, True, ">5.0.0,<6.0.0"),
        _Package(sklearn_pkg, sklearn_regex, True, "==1.5.1"),
        _Package(numpy_pkg, numpy_regex, True, "==1.23.5"),
        _Package(xgboost_pkg, xgboost_regex, False, "==1.5.2"),
        _Package(inference_schema_pkg, inference_schema_regex, False),
        _Package(prophet_pkg, prophet_regex, False, "==1.1.4"),
        _Package(holidays_pkg, holidays_regex, True, "==0.29"),
        _Package(joblib_pkg, joblib_regex, False, "==1.2.0"),
        _Package(git_setuptools_pkg, git_setuptools_regex, True),
        _Package(urllib3_pkg, urllib3_regex, False),
        _Package(azurecore_pkg, azurecore_regex, False),
        _Package(boto3_pkg, boto3_regex, False, "==1.20.19"),
        _Package(botocore_pkg, botocore_regex, False, "==1.23.19"),
        # _Package(apex_url, apex_regex, False),  # disabled until fix for fused kernels available
    ]

    if settings.enable_dnn:
        required_package_list.extend([
            _Package(pytorch_pkg, pytorch_regex, True, "==1.11.0"),  # supported for Linux - OS for remote compute
            _Package(cudatoolkit_pkg, cudatoolkit_regex, True, "==10.1.243"),
            _Package(pytorch_transformers_pkg, pytorch_transformers_regex, False, "==1.0.0"),
            _Package(spacy_pkg, spacy_regex, False, "==3.7.4"),
            _Package(spacy_english_model_url, spacy_english_model_regex, False),
        ])
    else:
        logger.debug("Skipping DNN packages since enable_dnn=False.")

    dependencies = run_config.environment.python.conda_dependencies
    dependencies.add_channel("pytorch")
    # dependencies.set_pip_option('--global-option="--cpp_ext" --global-option="--cuda_ext"')

    # if debug flag sets an sdk_url use it
    if settings.sdk_url is not None:
        dependencies.set_pip_option("--index-url " + settings.sdk_url)
        dependencies.set_pip_option("--extra-index-url " + DEFAULT_SDK_ORIGIN)

    # if debug_flag sets packages, use those in remote run
    if settings.sdk_packages is not None:
        for package in settings.sdk_packages:
            dependencies.add_pip_package(package)

    # azureml-defaults is auto-added to run configuration but its version is not pinned
    # we will remove this package and add it again with correct version pinned.
    dependencies.remove_pip_package(defaults_pkg)

    all_pkgs_str = " ".join(dependencies.pip_packages) + " " + " ".join(dependencies.conda_packages)
    dependencies.add_conda_package('pip==22.3.1')

    # include required packages
    for p in required_package_list:
        if not re.findall(p.regex, all_pkgs_str):
            logger.info("Package {} missing from dependencies file.".format(p.name))
            # when picking version - check if we require a specific version first
            # if not, then use what is installed. If the package doesn't require a version
            # and doesnt have an installed version don't pin.
            if p.required_version is not None:
                version_str = p.required_version
                logger.info("Using pinned version: {}{}".format(p.name, version_str))
            elif p.name in installed_packages:
                ver = installed_packages[p.name]
                version_str = "=={}".format(ver)
                logger.info("Using installed version: {}{}".format(p.name, version_str))
            else:
                version_str = ""

            if p.is_conda:
                dependencies.add_conda_package(p.name + version_str)
            else:
                dependencies.add_pip_package(p.name + version_str)

            # If azureml-train-automl is added by the SDK, we need to ensure we do not pin to an editable installation.
            # If automl_version is none we will reset the version to not pin for all azureml-* packages except defaults
            # (handled below).
            if p.name == automl_meta_pkg and automl_version is None:
                dependencies.add_pip_package(automl_meta_pkg)
            if p.name == defaults_pkg and automl_version is None:
                dependencies.add_pip_package(defaults_pkg)

    # If we installed from a channel that isn't pypi we'll need to pick up the index. We'll assume
    # if the user added an index to their dependencies they know what they are doing and we won't modify anything.
    source_url = CondaDependencies.sdk_origin_url()
    if source_url != DEFAULT_SDK_ORIGIN and 'index-url' not in dependencies.serialize_to_string():
        dependencies.set_pip_option("--index-url " + source_url)
        dependencies.set_pip_option("--extra-index-url " + DEFAULT_SDK_ORIGIN)

    dependencies.set_python_version(platform.python_version())

    run_config.environment.python.conda_dependencies = dependencies
    return run_config


def modify_run_configuration_curated(settings: AzureAutoMLSettings,
                                     run_config: RunConfiguration,
                                     workspace: Workspace,
                                     logger: Union[logging.Logger, logging.LoggerAdapter]  # type: ignore
                                     ) -> RunConfiguration:

    curated_env = Environment.get(workspace, Environments.AUTOML_DNN, "1")
    curated_env.name = "AutoML-SDK"

    curated_env_pkgs = [
        "azureml-core",
        "azureml-pipeline-core",
        "azureml-telemetry",
        "azureml-defaults",
        "azureml-interpret",
        "azureml-automl-core",
        "azureml-automl-runtime",
        "azureml-train-automl-client",
        "azureml-train-automl-runtime"
    ]

    if is_prod():
        for pkg in curated_env_pkgs:
            curated_env.python.conda_dependencies.add_pip_package("{}=={}".format(pkg, azureml.train.automl.VERSION))
        extra_index = CondaDependencies.sdk_origin_url().rstrip("/")
        if extra_index != PYPI_INDEX:
            curated_env.python.conda_dependencies.add_pip_package("--extra-index-url " + extra_index)
    logger.info("Modified environment to: {}".format(curated_env))
    run_config.environment = curated_env
    run_config.environment.name = "AutoML_Fallback"
    return run_config


def is_prod():
    # Should this query pip for the version?
    index = CondaDependencies.sdk_origin_url().rstrip("/")
    if_runtime_non_prod = False
    try:
        # If we're testing runtime candidate we'll have prod client and non-prod runtime
        from azureml.train.automl.runtime import VERSION as RUNTIME_VERSION
        if_runtime_non_prod = RUNTIME_VERSION.startswith("0")
    except ImportError:
        pass
    return not azureml.train.automl.VERSION.startswith("0") and not if_runtime_non_prod and index == PYPI_INDEX


def validate_non_prod_env_exists(ws):
    NON_PROD_MISMATCH_WARNING = "Detected non-production version of AutoML is installed. The locally installed " \
                                "version does not match the version in the environment. " \
                                "The local version is {}. The environment is {}."
    NON_PROD_MISSING_WARNING = "Detected non-production version of AutoML is installed and no non-production " \
                               "environment was pre-registered for this workspace. Falling back " \
                               "to using deprecated environment logic. Please run the automl_generate_non_prod " \
                               "script to create the proper environments. If you did not intend to use a " \
                               "non-production version of AutoML, please reinstall via " \
                               "'pip install -I --upgrade azureml-train-automl'"
    for env_name in NON_PROD_ENVIRONMENTS:
        try:
            env = Environment.get(ws, NON_PROD_ENVIRONMENTS[env_name])
            if (env.python.conda_dependencies and not
                any([azureml.train.automl.VERSION in x for x in env.python.conda_dependencies.pip_packages])) or \
                    (env.docker.base_dockerfile and not (azureml.train.automl.VERSION in env.docker.base_dockerfile)):
                logger.warning(NON_PROD_MISMATCH_WARNING.format(azureml.automl.core.VERSION, env))
                """
                Uncomment this once we version the envs for concurrent runs in the same workspace
                raise ClientException()._with_error(
                    AzureMLError.create(AutoMLInternal,
                                        error_details=error_details
                                        .format(azureml.automl.core.VERSION, env))
                )
                """
        except Exception as e:
            if 'NotFound' in str(e):
                logger.warning(NON_PROD_MISSING_WARNING)
                """
                Uncomment this once we version the envs for concurrent runs in the same workspace
                raise ClientException()._with_error(
                    AzureMLError.create(AutoMLInternal, error_details=error_details)
                )
                """
            else:
                raise


def get_curated_environment_scenario(settings_dict: Dict[str, Any], task: str) -> Optional[str]:
    """
    Get the curated environment label from automl settings first then try to get it from system env.

    :param settings_dict: A dict contains automl settings.
    :param task: The AutoML task type.
    :return: A string represent the scenario. None if nothing can be found.
    """
    # Internal parameter for curated environment scenarios
    force_curated_environment = settings_dict.get('force_curated_environment',
                                                  os.environ.get("FORCE_CURATED_ENVIRONMENT", False))
    if EnvironmentSettings.SCENARIO in settings_dict:
        scenario = settings_dict.get(EnvironmentSettings.SCENARIO)
        logging.warning("{} is an internal parameter that should not be used for regular experiments.".format(
            EnvironmentSettings.SCENARIO
        ))
    else:
        scenario = os.environ.get(EnvironmentSettings.SCENARIO_ENV_VAR)
        if scenario is None:
            if task in constants.Tasks.ALL_IMAGE:
                scenario = constants.Scenarios.VISION
            elif task in constants.Tasks.ALL_TEXT:
                if settings_dict.get('enable_distributed_dnn_training_ort_ds', False):
                    scenario = constants.Scenarios.TEXT_DNN_PTCA
                else:
                    scenario = constants.Scenarios.TEXT_DNN
            elif is_prod() or force_curated_environment:
                scenario = constants.Scenarios.AUTOML
            else:
                scenario = constants.Scenarios._NON_PROD
    settings_dict.pop(EnvironmentSettings.SCENARIO, None)

    return scenario


def get_curated_environment_label(settings_dict: Dict[str, Any]) -> Optional[str]:
    """
    Get the curated environment label from automl settings first then try to get it from system env.

    :param settings_dict: A dict contains automl settings.
    :return: A string represent the label. None if nothing can be found.
    """
    if EnvironmentSettings.ENVIRONMENT_LABEL in settings_dict:
        environment_label = settings_dict.get(EnvironmentSettings.ENVIRONMENT_LABEL)
        logging.warning("{} is an internal parameter that should not be used for regular experiments.".format(
            EnvironmentSettings.ENVIRONMENT_LABEL
        ))
    else:
        environment_label = os.environ.get(EnvironmentSettings.ENVIRONMENT_LABEL_ENV_VAR)
    settings_dict.pop(EnvironmentSettings.ENVIRONMENT_LABEL, None)

    return environment_label


#
# we expect automl Dockerfile to have a structure
# that allows us to parse conda and pip CondaDependencies
# using marker comments
# roughly it looks like this:
# BEGIN_SECTION    -- things like FROM ENV COPY, etc
# # begin conda create
# # Create conda environment
# RUN conda create ...
#     # begin conda dependencies
#     pip=20.2.4 \
#     py-cpuinfo=5.0.0 \
#     ...
#     # end conda dependencies
#     ... more conda options here
# # end conda create
# ...
# # begin pip install
# RUN pip install {pin-to-extra-index} \
#                 # begin pypi dependencies
#                 '{pin-to-latest-pypi-version:"azureml-core=={}"}' \
#                 '{pin-to-latest-pypi-version:"azureml-mlflow=={}"}' \
#                 ... more pypi dependencies
#                 # end pypi dependencies
# # end pip install
_AUTOML_DOCKERFILE_GRAMMAR = \
    re.compile(r'(.*)'          # 0 section0
               r'(^\s*# begin conda create\s*$)'           # 1 begin conda create marker
               r'(.*)'                                     # 2 begin_conda create
               r'(^\s*# begin conda dependencies\s*$)'     # 3 begin conda dependencies marker
               r'(.*)'                                     # 4 conda dependencies
               r'(^\s*# end conda dependencies\s*$)'       # 5 end conda dependencies marker
               r'(.*)'                                     # 6 end_conda_create
               r'(^\s*# end conda create\s*$)'             # 7 end conda create marker
               r'(.*)'                                     # 8 section1
               r'(^\s*# begin pip install\s*$)'            # 9 begin pip install marker
               r'(.*)'                                     # 10 begin_pip_install
               r'(^\s*# begin pypi dependencies\s*$)'      # 11 begin pypi dependencies marker
               r'(.*)'                                     # 12 pypi dependencies
               r'(^\s*# end pypi dependencies\s*$)'        # 13 end pypi dependencies marker
               r'(.*)'                                     # 14 end_pip_install
               r'(^\s*# end pip install\s*$)'              # 15 end pip install marker
               r'(.*)',                                    # 16 section2
               re.MULTILINE | re.DOTALL)


def parse_automl_dockerfile(contents: str) -> Optional[Dict[str, str]]:
    """
    parses a Dockerfile content under the assumption if follows the dependencies marking convention
    """
    match = _AUTOML_DOCKERFILE_GRAMMAR.fullmatch(contents)
    if match:
        groups = match.groups()
        return {
            "section0": groups[0],
            "begin_conda_create": groups[2],
            "conda_dependencies": groups[4],
            "end_conda_create": groups[6],
            "section1": groups[8],
            "begin_pip_install": groups[10],
            "pypi_dependencies": groups[12],
            "end_pip_install": groups[14],
            "section2": groups[16]
        }
    return None
