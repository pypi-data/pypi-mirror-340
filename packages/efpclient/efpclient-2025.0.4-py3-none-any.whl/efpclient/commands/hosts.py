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
import click

from efpclient import logger, swagger
from efpclient.swagger import handle_not_successful
from efpclient.swagger_client.rest import ApiException
from efpclient.utils import json_str


@click.command('all')
@click.option('-g', '--grid', 'grid', type=str, default='',
              help='HPC scheduler or VDI session manager to use. Not specifying this value means the default is used.')
@click.option('-c', '--cluster', 'cluster', type=str, default='',
              help='Cluster to use. Not specifying this value means the default is used.')
@click.pass_obj
def all_hosts(conf: dict, grid: str, cluster: str):
    """ List all available hosts. """
    try:
        logger.debug(f'Calling hosts with grid: {grid}, cluster: {cluster}')
        response = swagger.get(conf).hosts(grid=grid, cluster=cluster)
        logger.info('Service replied with code 200')
        # Response contains a list of Host objects, we need to convert all of them to dict
        logger.echo(json_str(list(v.to_dict() for v in response)))
    except ApiException as e:
        handle_not_successful(e, [401, 400])


@click.command('jobs')
@click.option('-n', '--name', 'hostname', type=str, required=True, help='Name of the host to which the jobs belong.')
@click.option('-g', '--grid', 'grid', type=str, default='',
              help='HPC scheduler or VDI session manager to use. Not specifying this value means the default is used.')
@click.option('-c', '--cluster', 'cluster', type=str, default='',
              help='Cluster to use. Not specifying this value means the default is used.')
@click.pass_obj
def host_jobs(conf: dict, hostname: str, grid: str, cluster: str):
    """ List jobs by host name, same as 'jobs host' command. """
    try:
        logger.debug(f'Calling jobs_by_host with hostname: {hostname}, grid: {grid}, cluster: {cluster}')
        response = swagger.get(conf).jobs_by_host(hostname, grid=grid, cluster=cluster)
        logger.info('Service replied with code 200')
        # Response contains a list of Job objects, we need to convert all of them to dict
        logger.echo(json_str(list(v.to_dict() for v in response)))
    except ApiException as e:
        handle_not_successful(e, [401, 400])


@click.command('info')
@click.option('-n', '--name', 'hostname', type=str, required=True, help='Name of the host to look for.')
@click.option('-g', '--grid', 'grid', type=str, default='',
              help='HPC scheduler or VDI session manager to use. Not specifying this value means the default is used.')
@click.option('-c', '--cluster', 'cluster', type=str, default='',
              help='Cluster to use. Not specifying this value means the default is used.')
@click.pass_obj
def host_info(conf: dict, hostname: str, grid: str, cluster: str):
    """ Get host info for a given host name. """
    try:
        logger.debug(f'Calling get_host with hostname: {hostname}, grid: {grid}, cluster: {cluster}')
        response = swagger.get(conf).get_host(hostname, grid=grid, cluster=cluster)
        logger.info('Service replied with code 200')
        logger.echo(json_str(response.to_dict()))
    except ApiException as e:
        handle_not_successful(e, [401, 400])
