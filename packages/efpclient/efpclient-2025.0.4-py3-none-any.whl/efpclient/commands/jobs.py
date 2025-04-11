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


@click.command('mine')
@click.option('-g', '--grid', 'grid', type=str, default='',
              help='HPC scheduler or VDI session manager to use. Not specifying this value means the default is used.')
@click.option('-c', '--cluster', 'cluster', type=str, default='',
              help='Cluster to use. Not specifying this value means the default is used.')
@click.pass_obj
def my_jobs(conf: dict, grid: str, cluster: str):
    """ List jobs belonging to user performing the request. """
    try:
        logger.debug(f'Calling my_jobs with grid: {grid}, cluster: {cluster}')
        response = swagger.get(conf).my_jobs(grid=grid, cluster=cluster)
        logger.info('Service replied with code 200')
        # Response contains a list of Job objects, we need to convert all of them to dict
        logger.echo(json_str(list(v.to_dict() for v in response)))
    except ApiException as e:
        handle_not_successful(e, [401, 400])


@click.command('all')
@click.option('-g', '--grid', 'grid', type=str, default='',
              help='HPC scheduler or VDI session manager to use. Not specifying this value means the default is used.')
@click.option('-c', '--cluster', 'cluster', type=str, default='',
              help='Cluster to use. Not specifying this value means the default is used.')
@click.pass_obj
def all_jobs(conf: dict, grid: str, cluster: str):
    """ List all jobs available. """
    try:
        logger.debug(f'Calling all_jobs with grid: {grid}, cluster: {cluster}')
        response = swagger.get(conf).all_jobs(grid=grid, cluster=cluster)
        logger.info('Service replied with code 200')
        # Response contains a list of Job objects, we need to convert all of them to dict
        logger.echo(json_str(list(v.to_dict() for v in response)))
    except ApiException as e:
        handle_not_successful(e, [401, 400])


@click.command('host')
@click.option('-n', '--name', 'hostname', type=str, required=True, help='Name of the host to which the jobs belong.')
@click.option('-g', '--grid', 'grid', type=str, default='',
              help='HPC scheduler or VDI session manager to use. Not specifying this value means the default is used.')
@click.option('-c', '--cluster', 'cluster', type=str, default='',
              help='Cluster to use. Not specifying this value means the default is used.')
@click.pass_obj
def jobs_by_host(conf: dict, hostname: str, grid: str, cluster: str):
    """ List jobs by host name, same as 'hosts jobs' command. """
    try:
        logger.debug(f'Calling jobs_by_host with hostname: {hostname}, grid: {grid}, cluster: {cluster}')
        response = swagger.get(conf).jobs_by_host(hostname, grid=grid, cluster=cluster)
        logger.info('Service replied with code 200')
        # Response contains a list of Job objects, we need to convert all of them to dict
        logger.echo(json_str(list(v.to_dict() for v in response)))
    except ApiException as e:
        handle_not_successful(e, [401, 400])


@click.command('spooler')
@click.option('-u', '--uri', 'spooler_uri', type=str, required=True,
              help='URI of the spooler to which the jobs belong.')
@click.option('-g', '--grid', 'grid', type=str, default='',
              help='HPC scheduler or VDI session manager to use. Not specifying this value means the default is used.')
@click.option('-c', '--cluster', 'cluster', type=str, default='',
              help='Cluster to use. Not specifying this value means the default is used.')
@click.pass_obj
def jobs_by_spooler(conf: dict, spooler_uri: str, grid: str, cluster: str):
    """ List jobs by spooler URI, same as 'spoolers jobs' command. """
    try:
        logger.debug(f'Calling jobs_by_spooler with spooler: {spooler_uri}, grid: {grid}, cluster: {cluster}')
        response = swagger.get(conf).jobs_by_spooler(spooler_uri, grid=grid, cluster=cluster)
        logger.info('Service replied with code 200')
        # Response contains a list of Job objects, we need to convert all of them to dict
        logger.echo(json_str(list(v.to_dict() for v in response)))
    except ApiException as e:
        handle_not_successful(e, [401, 400])


@click.command('info')
@click.option('-i', '--id', 'job_id', type=str, required=True, help='Id of the job to look for.')
@click.option('-g', '--grid', 'grid', type=str, default='',
              help='HPC scheduler or VDI session manager to use. Not specifying this value means the default is used.')
@click.option('-c', '--cluster', 'cluster', type=str, default='',
              help='Cluster to use. Not specifying this value means the default is used.')
@click.pass_obj
def job_info(conf: dict, job_id: str, grid: str, cluster: str):
    """ Get job info for a given job id. """
    try:
        logger.debug(f'Calling job_info with job_id: {job_id}, grid: {grid}, cluster: {cluster}')
        response = swagger.get(conf).job_info(job_id, grid=grid, cluster=cluster)
        logger.info('Service replied with code 200')
        logger.echo(json_str(response.to_dict()))
    except ApiException as e:
        handle_not_successful(e, [401, 400])


@click.command('suspend')
@click.option('-i', '--id', 'job_id', type=str, required=True, help='Id of the job to suspend.')
@click.option('-g', '--grid', 'grid', type=str, default='',
              help='HPC scheduler or VDI session manager to use. Not specifying this value means the default is used.')
@click.option('-c', '--cluster', 'cluster', type=str, default='',
              help='Cluster to use. Not specifying this value means the default is used.')
@click.pass_obj
def suspend_job(conf: dict, job_id: str, grid: str, cluster: str):
    """ Suspend a job specifying its id. """
    try:
        logger.debug(f'Calling suspend_job with job_id: {job_id}, grid: {grid}, cluster: {cluster}')
        response = swagger.get(conf).suspend_job(job_id, grid=grid, cluster=cluster)
        logger.info('Service replied with code 200')
        logger.echo(json_str(response.to_dict()))
    except ApiException as e:
        handle_not_successful(e, [401, 400])


@click.command('resume')
@click.option('-i', '--id', 'job_id', type=str, required=True, help='Id of the job to resume.')
@click.option('-g', '--grid', 'grid', type=str, default='',
              help='HPC scheduler or VDI session manager to use. Not specifying this value means the default is used.')
@click.option('-c', '--cluster', 'cluster', type=str, default='',
              help='Cluster to use. Not specifying this value means the default is used.')
@click.pass_obj
def resume_job(conf: dict, job_id: str, grid: str, cluster: str):
    """ Resume a job specifying its id. """
    try:
        logger.debug(f'Calling resume_job with job_id: {job_id}, grid: {grid}, cluster: {cluster}')
        response = swagger.get(conf).resume_job(job_id, grid=grid, cluster=cluster)
        logger.info('Service replied with code 200')
        logger.echo(json_str(response.to_dict()))
    except ApiException as e:
        handle_not_successful(e, [401, 400])


@click.command('cancel')
@click.option('-i', '--id', 'job_id', type=str, required=True, help='Id of the job to cancel.')
@click.option('-g', '--grid', 'grid', type=str, default='',
              help='HPC scheduler or VDI session manager to use. Not specifying this value means the default is used.')
@click.option('-c', '--cluster', 'cluster', type=str, default='',
              help='Cluster to use. Not specifying this value means the default is used.')
@click.pass_obj
def cancel_job(conf: dict, job_id: str, grid: str, cluster: str):
    """ Cancel a job specifying its id. """
    try:
        logger.debug(f'Calling cancel_job with job_id: {job_id}, grid: {grid}, cluster: {cluster}')
        response = swagger.get(conf).cancel_job(job_id, grid=grid, cluster=cluster)
        logger.info('Service replied with code 200')
        logger.echo(json_str(response.to_dict()))
    except ApiException as e:
        handle_not_successful(e, [401, 400])


@click.command('kill')
@click.option('-i', '--id', 'job_id', type=str, required=True, help='Id of the job to cancel.')
@click.option('-g', '--grid', 'grid', type=str, default='',
              help='HPC scheduler or VDI session manager to use. Not specifying this value means the default is used.')
@click.option('-c', '--cluster', 'cluster', type=str, default='',
              help='Cluster to use. Not specifying this value means the default is used.')
@click.pass_obj
def kill_job(conf: dict, job_id: str, grid: str, cluster: str):
    """ Cancel a job specifying its id, alias for 'cancel' command. """
    cancel_job(conf, job_id, grid, cluster)
