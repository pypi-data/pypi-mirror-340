"""
    Copyright 2025 NI SP Software GmbH

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
import copy
import os
import platform
import shutil
import stat
import urllib.parse
from configparser import ConfigParser, NoSectionError, NoOptionError
from enum import Enum
from importlib import resources
from pathlib import Path
from typing import Iterable, Any

import click

from efpclient import logger
from efpclient.errors import ConfigurationError

RESOURCE_CONF_FILENAME = 'efpclient.conf'
EFP_CLIENT_CONF_FILENAME = '.efpclient.conf'
LEGACY_EF_CLIENT_CONF_FILENAME = '.efclient.conf'
LEGACY_EF_CLIENT_CONF_FAKE_SECTION_NAME = 'LEGACY_EF_CLIENT'


class ConfigurationType(Enum):
    """ Configuration file types """
    EFP_CLIENT = 1
    LEGACY_EF_CLIENT = 2


class ConfigurationMap(Enum):
    """ Defines all global configuration parameter, mapping relevant data in a tuple.

    Each tuple contains the following data, in order (can be None if not applicable):
        - conf section name
        - conf param name
        - cli param name
        - env variable name
        - efclient equivalent param name
        - default value
    """
    # Add new values here to support more configuration params.
    PORTAL_URL = ('portal', 'url', 'portal_url', 'EFP_CLIENT_PORTAL_URL', None, None)
    SDF_URI = ('portal', 'sdf', 'sdf_uri', 'EFP_CLIENT_SDF', None, None)
    LEGACY_URL = (None, None, None, None, 'URL', None)
    LOG_INFO = (None, None, 'log_info', None, None, False)
    LOG_DEBUG = (None, None, 'log_debug', None, None, False)
    LOG_LEVEL = ('output', 'log-level', None, 'EFP_CLIENT_LOG_LEVEL', 'logging.level', 'warn')
    AUTH_USERNAME = ('authentication', 'username', 'username', 'EFP_CLIENT_AUTH_USERNAME', 'cred._username', None)
    AUTH_PASSWORD = ('authentication', 'password', None, 'EFP_CLIENT_AUTH_PASSWORD', 'cred._password', None)
    HTTP_BASIC_AUTH = ('authentication', 'http-basic-auth', 'http_basic_auth', 'EFP_CLIENT_HTTP_BASIC_AUTH', None, 'false')
    TOKEN = ('authentication', 'token', None, 'EFP_CLIENT_TOKEN', 'cred._token', None)
    SSL_VERIFY = ('security', 'ssl-verify', 'ssl_verify', 'EFP_CLIENT_SSL_VERIFY', None, 'false')
    CA_BUNDLE = ('security', 'ca-bundle', 'ca_bundle', 'EFP_CLIENT_CA_BUNDLE', None, None)

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, conf_section_name: str, conf_param_name: str, cli_param_name: str,
                 env_var_name: str, efclient_param_name: str, default_value: Any):
        self.conf_section_name = conf_section_name
        self.conf_param_name = conf_param_name
        self.cli_param_name = cli_param_name
        self.env_var_name = env_var_name
        self.efclient_param_name = efclient_param_name
        self.default_value = default_value


# We need this since UNNAMED_SECTION is available in Python>=3.13 configparser only
def _inject_fake_section(conf_fp: Iterable[str]) -> Iterable[str]:
    yield f'[{LEGACY_EF_CLIENT_CONF_FAKE_SECTION_NAME}]\n'
    yield from conf_fp


def _get_conf_dir() -> Path:
    return Path.home()


def _get_conf_file() -> (Path, ConfigurationType):
    conf_file = _get_conf_dir() / EFP_CLIENT_CONF_FILENAME
    legacy_conf_file = _get_conf_dir() / LEGACY_EF_CLIENT_CONF_FILENAME

    # If both new and legacy conf file exist, return the new one
    if conf_file.is_file() and legacy_conf_file.is_file():
        return conf_file, ConfigurationType.EFP_CLIENT

    # If legacy confile exists, return it
    if legacy_conf_file.is_file():
        return legacy_conf_file, ConfigurationType.LEGACY_EF_CLIENT

    return conf_file, ConfigurationType.EFP_CLIENT


def _get_value_from_conf_file(parser: ConfigParser, section: str, option: str):
    try:
        return parser.get(section, option)
    except NoSectionError:
        logger.debug(f'No section [{section}] found in the configuration file, ignoring option {option}')
    except NoOptionError:
        logger.debug(f'No option {option} found in section [{section}] of the configuration file, ignoring option')

    return None


# Priority order is (higher priority value overrides the lower ones):
# - CLI parameter
# - Environment variable
# - Configuration file or legacy configuration file (.efclient.conf)
# - Default value
def _get_conf_value(item: ConfigurationMap, parser: ConfigParser, cli_args: dict,
                    conf_type: ConfigurationType = None) -> Any:
    if item.cli_param_name and cli_args.get(item.cli_param_name):
        logger.debug(f'Taking {item.name} value from command line parameter')
        return cli_args.get(item.cli_param_name)

    if item.env_var_name and os.environ.get(item.env_var_name):
        logger.debug(f'Taking {item.name} value from environment variable {item.env_var_name}')
        return os.environ.get(item.env_var_name)

    if (item.conf_section_name and item.conf_param_name
            and (not conf_type or conf_type == ConfigurationType.EFP_CLIENT)
            and _get_value_from_conf_file(parser, item.conf_section_name, item.conf_param_name)):
        logger.debug(f'Taking {item.name} value from configuration file')
        return _get_value_from_conf_file(parser, item.conf_section_name, item.conf_param_name)

    if (item.efclient_param_name
            and (not conf_type or conf_type == ConfigurationType.LEGACY_EF_CLIENT)
            and _get_value_from_conf_file(parser, LEGACY_EF_CLIENT_CONF_FAKE_SECTION_NAME, item.efclient_param_name)):
        logger.debug(f'Taking {item.name} value from legacy configuration file')
        return _get_value_from_conf_file(parser, LEGACY_EF_CLIENT_CONF_FAKE_SECTION_NAME, item.efclient_param_name)

    logger.debug(f'No value found in any configuration for {item.name}, using default value')
    return item.default_value


def _configure_logger_level(parser: ConfigParser, cli_args: dict):
    is_info = _get_conf_value(ConfigurationMap.LOG_INFO, parser, cli_args)
    is_debug = _get_conf_value(ConfigurationMap.LOG_DEBUG, parser, cli_args)
    level = _get_conf_value(ConfigurationMap.LOG_LEVEL, parser, cli_args)
    if is_debug:
        logger.level = logger.map_level('debug')
    elif is_info:
        logger.level = logger.map_level('info')
    else:
        logger.level = logger.map_level(level)


def _redact(conf: dict) -> dict:
    conf_cp = copy.deepcopy(conf)
    if conf_cp[ConfigurationMap.AUTH_PASSWORD.name]:
        conf_cp[ConfigurationMap.AUTH_PASSWORD.name] = '******'
    if conf_cp[ConfigurationMap.TOKEN.name]:
        conf_cp[ConfigurationMap.TOKEN.name] = '******'

    return conf_cp


def _has_wrong_permissions(conf_file: Path) -> bool:
    # Check for 600 permissions
    return not os.stat(conf_file).st_mode == 0o100600


def _infer_from_legacy_conf(legacy_url: str) -> (str, str):
    url = urllib.parse.urlparse(legacy_url)
    if not url.scheme or not url.netloc or not url.path:
        raise ConfigurationError(f'Invalid URL {legacy_url} defined in legacy configuration file')

    path = url.path
    context = path
    if '/' in context:
        while os.path.dirname(context) != '/':
            context = os.path.dirname(context)

    portal_url = f'{url.scheme}://{url.netloc}{context}'
    sdf = path.replace(context, '')
    if not sdf:
        raise ConfigurationError(f'Missing SDF in URL {legacy_url} defined in legacy configuration file')

    return portal_url, sdf


def init():
    """ Init the configuration system by creating a new configuration file if it does not exist. """
    user_conf_dir = _get_conf_dir()
    user_conf_file, _ = _get_conf_file()
    if not user_conf_file.is_file():
        try:
            os.makedirs(user_conf_dir, exist_ok=True)
            with resources.as_file(resources.files('efpclient.resources') / RESOURCE_CONF_FILENAME) as default_conf_file:
                shutil.copyfile(default_conf_file, user_conf_file)
                # Set 600 permissions
                os.chmod(user_conf_file, stat.S_IRUSR | stat.S_IWUSR)
        except OSError as e:
            logger.warn(f'Error creating default configuration file {user_conf_file}: {e}')


def load(conf_filename: str, cli_args: dict) -> dict:
    """ Load the global configuration using a priority mechanism
    (CLI parameters, environment variables, configuration file).

    :param conf_filename: the configuration file name
    :param cli_args: dict containing global CLI arguments
    :returns dict containing the configuration
    """
    conf = {}
    parser = ConfigParser()

    # Load the configuration file
    if conf_filename:
        conf_file = Path(conf_filename)
        conf_type = ConfigurationType.EFP_CLIENT
        # Assume new EF Portal specs
        with open(conf_file, 'r', encoding='utf-8') as cf:
            parser.read_file(cf)
    else:
        conf_file, conf_type = _get_conf_file()
        if conf_type == ConfigurationType.LEGACY_EF_CLIENT:
            # Uncomment the following to force case-sensitive parameters (see URL in efclient.conf)
            # parser.optionxform = str
            with open(conf_file, 'r', encoding='utf-8') as cf:
                parser.read_file(_inject_fake_section(cf))
        else:
            # Assume new EF Portal specs
            with open(conf_file, 'r', encoding='utf-8') as cf:
                parser.read_file(cf)

    # Configure logger level first
    _configure_logger_level(parser, cli_args)

    logger.info(f'Using configuration file {conf_file}')
    logger.debug('Checking configuration file permissions')
    if platform.system() == 'Windows':
        # Python is not able to os.chmod() files properly on Windows, so we would have warnings
        # also using newly created configuration files
        logger.info('Skipping configuration file permissions check on Windows')
    elif _has_wrong_permissions(conf_file):
        logger.warn(f'Configuration file {conf_file} has wrong permissions! It should be 600 for security reasons')

    # Populate the configuration dictionary
    for item in ConfigurationMap:
        conf[item.name] = _get_conf_value(item, parser, cli_args, conf_type)

    if conf[ConfigurationMap.LEGACY_URL.name]:
        logger.debug(f'Found parameter {ConfigurationMap.LEGACY_URL.efclient_param_name} with value '
                     f'{conf[ConfigurationMap.LEGACY_URL.name]} in legacy configuration file')
        portal_url, sdf = _infer_from_legacy_conf(conf[ConfigurationMap.LEGACY_URL.name])
        conf[ConfigurationMap.PORTAL_URL.name] = portal_url
        conf[ConfigurationMap.SDF_URI.name] = sdf
        logger.debug(f'Inferred values from {ConfigurationMap.LEGACY_URL.name}: '
                     f'{ConfigurationMap.PORTAL_URL.name}: {portal_url}, {ConfigurationMap.SDF_URI.name}: {sdf}')

    logger.debug(f'Loaded global conf: {_redact(conf)}')

    # Check for required conf values
    if not conf[ConfigurationMap.PORTAL_URL.name]:
        logger.echo(f'{click.get_current_context().get_help()}\n')
        raise ConfigurationError(f'Required parameter {ConfigurationMap.PORTAL_URL.conf_param_name} is not defined')

    # Validation checks
    # See Note in https://requests.readthedocs.io/en/latest/user/advanced/#ssl-cert-verification
    if conf[ConfigurationMap.CA_BUNDLE.name] and not Path(conf[ConfigurationMap.CA_BUNDLE.name]).is_file():
        raise ConfigurationError(f'CA bundle {conf[ConfigurationMap.CA_BUNDLE.name]} must exist and be a file')

    return conf
