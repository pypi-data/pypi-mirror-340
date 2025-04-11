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


@click.command('users')
@click.pass_obj
def logged_users(conf: dict):
    """ List all users currently logged in. """
    try:
        logger.debug('Calling users')
        response = swagger.get(conf).users()
        logger.info('Service replied with code 200')
        # Response contains a list of Session objects, we need to convert all of them to dict
        logger.echo(json_str(list(v.to_dict() for v in response)))
    except ApiException as e:
        handle_not_successful(e, [401, 400])


@click.command('logout')
@click.option('-u', '--username', 'username', type=str, required=True, help='Name of user to logout')
@click.pass_obj
def logout_user(conf: dict, username: str):
    """ Logout user by specifying his name. """
    try:
        logger.debug(f'Calling logout with username {username}')
        response = swagger.get(conf).logout(username)
        logger.info('Service replied with code 200')
        logger.echo(json_str(response.to_dict()))
    except ApiException as e:
        handle_not_successful(e, [401, 400])


@click.command('licenses')
@click.pass_obj
def licenses_usage(conf: dict):
    """ List current license status and usage. """
    try:
        logger.debug('Calling licenses')
        response = swagger.get(conf).licenses()
        logger.info('Service replied with code 200')
        # Response contains a list of License objects, we need to convert all of them to dict
        logger.echo(json_str(list(v.to_dict() for v in response)))
    except ApiException as e:
        handle_not_successful(e, [401, 400])
