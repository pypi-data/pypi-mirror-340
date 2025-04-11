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
import json
import posixpath
from os.path import basename
from pathlib import Path
from typing import Optional

import click
import requests

from efpclient.errors import CliError, ResponseError
from efpclient.swagger_client import Item

from efpclient import logger, swagger
from efpclient.configuration import ConfigurationMap
from efpclient.swagger import handle_not_successful
from efpclient.swagger_client.rest import ApiException
from efpclient.utils import json_str

FILE_DOWNLOAD_CHUNK_SIZE = 10 * 1024  # 10 KB


@click.command('list')
@click.pass_obj
def list_spoolers(conf: dict):
    """ List spoolers owned by the authenticated user. """
    try:
        logger.debug(f'Calling spoolers')
        response = swagger.get(conf).spoolers()
        logger.info('Service replied with code 200')
        # Response contains a list of Spooler objects, we need to convert all of them to dict
        logger.echo(json_str(list(v.to_dict() for v in response)))
    except ApiException as e:
        handle_not_successful(e, [401, 400])


@click.command('jobs')
@click.option('-u', '--uri', 'uri', type=str, required=True,
              help='URI of the spooler to which the jobs belong.')
@click.option('-g', '--grid', 'grid', type=str, default='',
              help='HPC scheduler or VDI session manager to use. Not specifying this value means the default is used.')
@click.option('-c', '--cluster', 'cluster', type=str, default='',
              help='Cluster to use. Not specifying this value means the default is used.')
@click.pass_obj
def spooler_jobs(conf: dict, uri: str, grid: str, cluster: str):
    """ List jobs by spooler URI, same as 'jobs spooler' command. """
    try:
        logger.debug(f'Calling jobs_by_spooler with spooler: {uri}, grid: {grid}, cluster: {cluster}')
        response = swagger.get(conf).jobs_by_spooler(uri, grid=grid, cluster=cluster)
        logger.info('Service replied with code 200')
        # Response contains a list of Job objects, we need to convert all of them to dict
        logger.echo(json_str(list(v.to_dict() for v in response)))
    except ApiException as e:
        handle_not_successful(e, [401, 400])


@click.command('files')
@click.option('-u', '--uri', 'uri', type=str, required=True,
              help='URI of the spooler whose files you want to list.')
@click.option('-p', '--sub-path', 'sub_path', type=str, default='/',
              help='Sub-path that you want to visit inside the spooler. The root (/) path is used if it is empty.')
@click.pass_obj
def spooler_files(conf: dict, uri: str, sub_path: str):
    """ List files in spooler given its URI. """
    try:
        logger.debug(f'Calling spooler_files with spooler: {uri}, sub_path: {sub_path}')
        response = swagger.get(conf).spooler_files(uri, sub=sub_path)
        logger.info('Service replied with code 200')
        # Response contains a list of Item objects, we need to convert all of them to dict
        logger.echo(json_str(list(v.to_dict() for v in response)))
    except ApiException as e:
        handle_not_successful(e, [401, 400])


@click.command('download')
@click.option('-u', '--uri', 'uri', type=str, required=True,
              help="URI of the spooler to download from.")
@click.option('-f', '--filename', 'filename', type=str, required=True,
              help="Name of file to download.")
@click.option('-p', '--sub-path', 'sub_path', type=str, default='/',
              help='Sub-path where the file resides inside the spooler. The root (/) path is used if it is empty.')
@click.option('-o', '--output', 'output', type=str,
              help="Path to file where to write downloaded content. The same value given to filename is used if it is empty.")
@click.pass_obj
def spooler_download(conf: dict, uri: str, filename: str, sub_path: str, output: str):
    """ Download a file from a spooler. """
    try:
        logger.debug(f'Calling spooler_files with spooler: {uri}, sub_path: {sub_path} to get the download url')
        items: list[Item] = swagger.get(conf).spooler_files(uri, sub=sub_path)
        logger.debug('Service replied with code 200, searching file to download in the retrieved list')
        for item in items:
            if item.name == filename and item.url:
                logger.debug(f'File {filename} found in sub-path {sub_path}, downloading')
                with requests.session() as session:
                    headers = {'Referer': conf[ConfigurationMap.PORTAL_URL.name],
                               'Authorization': f'Bearer {conf[ConfigurationMap.TOKEN.name]}'}
                    verify = conf[ConfigurationMap.CA_BUNDLE.name] if conf[ConfigurationMap.SSL_VERIFY.name].lower() == 'true' else False

                    response = session.get(item.url, headers=headers, verify=verify, stream=True)
                    if response.status_code != 200:
                        logger.warn(f'Response status code from {item.url} is {response.status_code}, unable to download the file. '
                                    f'Response text is:')
                        logger.warn(f'{response.text}', indent=4)
                    else:
                        outfile = output if output else filename
                        logger.debug(f'Got response 200 from {item.url}, saving content to {outfile}')
                        with open(outfile, mode="wb") as file:
                            for chunk in response.iter_content(chunk_size=FILE_DOWNLOAD_CHUNK_SIZE):
                                file.write(chunk)

                        logger.echo(f'Content saved to {outfile}')

                    return

        raise CliError(f'Cannot find file {filename} in sub-path {sub_path} of spooler {uri}')
    except ApiException as e:
        handle_not_successful(e, [401, 400])


@click.command('upload')
@click.option('-u', '--uri', 'uri', type=str, required=True,
              help="URI of the spooler where to upload files.")
@click.option('-p', '--sub-path', 'sub_path', type=str, default='/',
              help='Sub-path where to upload files inside the spooler. The root (/) path is used if it is empty.')
@click.option('-f', '--file', 'filepaths', type=str, required=True, multiple=True,
              help="Path to local file to upload. Use it multiple times to upload more than one file at once.")
@click.pass_obj
def spooler_upload(conf: dict, uri: str, sub_path: str, filepaths: list):
    """ Upload one or more local files into a spooler. """
    response = upload_files(conf, filepaths, spooler_uri=uri, sub_path=sub_path)
    if response:
        logger.echo(json_str(json.loads(response.text)))


@click.command('delete')
@click.option('-u', '--uri', 'uri', type=str, required=True, help='URI of the spooler to delete.')
@click.pass_obj
def delete_spooler(conf: dict, uri: str):
    """ Delete a spooler given its URI. """
    try:
        logger.debug(f'Calling delete_spooler with spooler {uri}')
        response = swagger.get(conf).delete_spooler(uri)
        logger.info('Service replied with code 200')
        logger.echo(json_str(response.to_dict()))
    except ApiException as e:
        handle_not_successful(e, [401, 400])


def upload_files(conf: dict, filepaths: list, spooler_uri: str = None, sub_path: str = '/') -> Optional[requests.Response]:
    """ Upload one or more local files into an either new or existing spooler.

    :param conf: the configuration dictionary
    :param filepaths: ``list`` of ``str`` containing local  file paths to upload
    :param spooler_uri: URI of the spooler where to upload the file. If missing, a new spooler will be created
    :param sub_path: spooler sub-path where to upload the file. Default: ``/``
    :returns: the :class:`requests.Response` coming from the API, or ``None`` if ``filepaths`` is empty or a managed error occurred
    :raises: :class:`ResponseError` if a not managed error occurs
    """
    with requests.session() as session:
        headers = {'Referer': conf[ConfigurationMap.PORTAL_URL.name],
                   'Authorization': f'Bearer {conf[ConfigurationMap.TOKEN.name]}',
                   'path': sub_path}
        verify = conf[ConfigurationMap.CA_BUNDLE.name] if conf[ConfigurationMap.SSL_VERIFY.name].lower() == 'true' else False
        if spooler_uri:
            headers['spooler'] = spooler_uri

        response = None
        for filepath in filepaths:
            filename = basename(Path(filepath))
            endpoint = posixpath.join(conf[ConfigurationMap.PORTAL_URL.name], f'rest/system/spoolers/upload/{filename}')
            logger.debug(f'Calling endpoint {endpoint} using headers '
                         f'{f"{{spooler: {spooler_uri}, path: {sub_path}}}" if spooler_uri else f"{{path: {sub_path}}}"}')
            with open(filepath, 'rb') as data:
                logger.info(f'Uploading file {filepath} {f"into spooler {spooler_uri}" if spooler_uri else "into a new spooler"}, '
                            f'this may take a while...')
                response = session.post(endpoint, headers=headers, verify=verify, data=data)
                if response.status_code != 200:
                    _handle_not_successful_upload(response, [401, 400])
                    return None

                logger.info('Service replied with code 200')

        # All responses are the same when they all succeed, so just take the spooler uri from the last one
        # ...or return None if nothing was done
        return response


def _handle_not_successful_upload(response: requests.Response, statuses: list):
    """ Handle not successful responses coming from requests POST calls to the upload endpoint.

    :param response: the :class:`requests.Response` coming from the upload endpoint
    :param statuses: list of ``int`` representing HTTP status codes to manage
    """
    if response.status_code in statuses:
        logger.info(f'Service replied with code {response.status_code}')
        try:
            logger.echo(json_str(json.loads(response.text)))
        except ValueError:
            logger.echo(response.text)
    else:
        raise ResponseError(f'Service replied with code {response.status_code} and text:\n{response.text}')
