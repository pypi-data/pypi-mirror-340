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
@click.pass_obj
def all_clusters(conf: dict):
    """ List all available clusters. """
    try:
        logger.debug('Calling clusters')
        response = swagger.get(conf).clusters()
        logger.info('Service replied with code 200')
        # Response contains a list of Cluster objects, we need to convert all of them to dict
        logger.echo(json_str(list(v.to_dict() for v in response)))
    except ApiException as e:
        handle_not_successful(e, [401, 400])
