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
import configparser
from importlib import metadata

import click
import urllib3
from requests.exceptions import RequestException
from urllib3.exceptions import MaxRetryError

from efpclient import configuration
from efpclient import logger
from efpclient.commands.admin import logged_users, logout_user, licenses_usage
from efpclient.commands.clusters import all_clusters
from efpclient.commands.hosts import all_hosts, host_jobs, host_info
from efpclient.commands.jobs import all_jobs, my_jobs, jobs_by_host, jobs_by_spooler
from efpclient.commands.jobs import job_info, suspend_job, resume_job, cancel_job, kill_job
from efpclient.commands.queues import all_queues
from efpclient.commands.services import list_services, describe_service, submit_service
from efpclient.commands.spoolers import spooler_jobs, delete_spooler, spooler_files, spooler_download, spooler_upload, list_spoolers
from efpclient.commands.token import create_token
from efpclient.configuration import ConfigurationMap
from efpclient.errors import ResponseError, ConfigurationError, MissingTokenError, CliError
from efpclient.swagger_client.rest import ApiException


try:
    __version__ = metadata.version('efpclient')
except metadata.PackageNotFoundError:
    __version__ = 'dev'

urllib3.disable_warnings()


# Main group
@click.version_option(f'{__version__}', '-v', '--version', prog_name='NI SP Software EF Portal Client')
@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.option('-c', '--conf', 'conf_filename', type=str,
              help='Path to configuration file. Without this option, the configuration file '
                   '<user.home>/.efpclient.conf or the legacy <user.home>/.efclient.conf (if it exists) '
                   'will be used by default.')
@click.option('-u', '--url', ConfigurationMap.PORTAL_URL.cli_param_name, type=str,
              help='EF Portal base URL to connect to.')
@click.option('-s', '--ssl-verify', ConfigurationMap.SSL_VERIFY.cli_param_name, flag_value='true', type=str,
              help='Enable SSL certificates verification.')
@click.option('-b', '--ca-bundle', ConfigurationMap.CA_BUNDLE.cli_param_name, type=str,
              help='CA certificate bundle file to use when SSL certificates verification is enabled.')
@click.option('-l', '--log', ConfigurationMap.LOG_INFO.cli_param_name, is_flag=True, type=bool,
              help='Enable logging at INFO level. Without neither this option nor -d|--debug, level is WARN by default.')
@click.option('-d', '--debug', ConfigurationMap.LOG_DEBUG.cli_param_name, is_flag=True, type=bool,
              help='Enable logging at DEBUG level. Without neither this option nor -l|--log, level is WARN by default.')
@click.pass_context
def _cli(ctx: click.Context, conf_filename: str, **kwargs: dict):
    """ Command Line Interface to interact with EF Portal """
    ctx.obj = configuration.load(conf_filename, kwargs)


# Subgroups
@_cli.group('token')
def _token():
    """ Authentication token commands group. """


@_cli.group('jobs')
def _jobs():
    """ Jobs related commands group. """


@_cli.group('hosts')
def _hosts():
    """ Hosts related commands group. """


@_cli.group('clusters')
def _clusters():
    """ Clusters related commands group. """


@_cli.group('queues')
def _queues():
    """ Queues related commands group. """


@_cli.group('spoolers')
def _spoolers():
    """ Spoolers related commands group. """


@_cli.group('services')
def _services():
    """ Services related commands group. """


@_cli.group('admin')
def _admin():
    """ Administration related commands group. """


# Bind commands to corresponding subgroups
_token.add_command(create_token)
_jobs.add_command(my_jobs)
_jobs.add_command(all_jobs)
_jobs.add_command(jobs_by_host)
_jobs.add_command(jobs_by_spooler)
_jobs.add_command(job_info)
_jobs.add_command(suspend_job)
_jobs.add_command(resume_job)
_jobs.add_command(cancel_job)
_jobs.add_command(kill_job)
_hosts.add_command(all_hosts)
_hosts.add_command(host_jobs)
_hosts.add_command(host_info)
_clusters.add_command(all_clusters)
_queues.add_command(all_queues)
_spoolers.add_command(list_spoolers)
_spoolers.add_command(spooler_jobs)
_spoolers.add_command(spooler_files)
_spoolers.add_command(spooler_download)
_spoolers.add_command(spooler_upload)
_spoolers.add_command(delete_spooler)
_services.add_command(list_services)
_services.add_command(describe_service)
_services.add_command(submit_service)
_admin.add_command(logged_users)
_admin.add_command(logout_user)
_admin.add_command(licenses_usage)


def run():
    """ The CLI entrypoint """
    try:
        configuration.init()
        _cli()  # pylint: disable=no-value-for-parameter

        return 0
    except ConfigurationError as ce:
        logger.error(f'Configuration error: {ce}')
    except MissingTokenError:
        logger.error('Token is missing in client configuration, unable to perform the requested action')
    except (RequestException, MaxRetryError) as re:
        logger.error(f'Networking error: {re}')
    except ResponseError as rpe:
        logger.error(f'Unexpected response from service: {rpe}')
    except ApiException as ae:
        logger.error(f'Error calling EF Portal REST endpoint: {ae}')
    except CliError as ce:
        logger.echo(f'Error: {ce}')
    except OSError as ose:
        logger.error(f'Error managing file or directory: {ose}')
    except configparser.Error as cpe:
        logger.error(f'Error parsing configuration file: {cpe}')
    except ValueError as ve:
        logger.error(f'Value error: {ve}')
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error(f'Unexpected error: {e}', e)

    return 1
