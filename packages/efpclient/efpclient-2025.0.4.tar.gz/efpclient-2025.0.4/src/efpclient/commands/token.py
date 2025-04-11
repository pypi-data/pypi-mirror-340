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
import posixpath
import re
from datetime import datetime
from getpass import getpass
from typing import Any

import click
import requests
from requests.auth import HTTPBasicAuth

from efpclient import logger
from efpclient.configuration import ConfigurationMap
from efpclient.utils import json_str


def _get_token(session: requests.Session, portal_url: str, user: str, password: str, *,
               http_basic_auth: bool = False, verify: Any = False) -> (dict, str):
    endpoint = posixpath.join(portal_url, 'eftoken/eftoken.xml?_uri=//eftoken/eftoken')

    logger.debug(f'Get new token calling endpoint {endpoint}')
    data = {'EF_OUTPUT_MODE': 'rest'} if http_basic_auth else {'_username': user, '_password': password, 'EF_OUTPUT_MODE': 'rest'}
    auth = HTTPBasicAuth(user, password) if http_basic_auth else None
    r = session.post(endpoint, headers={'Referer': portal_url}, data=data, auth=auth, verify=verify)
    if r.status_code != 200:
        logger.warn(f'Response status code from {endpoint} is {r.status_code}')

    logger.debug(f'Got response {r.status_code} from {endpoint} with text:')
    logger.debug(f'{r.text}', indent=4)

    # Perform logout to free the license token before moving forward
    if r.status_code != 403:
        _logout(session, portal_url, auth=auth, verify=verify)

    token = {}
    for line in r.text.splitlines():
        if re.search('^token=\\w+$|^user=\\w+$|^expiration=\\d+$', line, re.ASCII):
            items = line.split('=')
            key = items[0]
            value = str(datetime.fromtimestamp(int(items[1]) / 1000)) if key == 'expiration' else items[1]
            token[key] = value

    return token, r.text


def _logout(session: requests.Session, portal_url: str, *, auth: HTTPBasicAuth = None, verify: Any = False):
    endpoint = posixpath.join(portal_url, 'eftoken/eftoken.xml?_uri=//com.enginframe.system/logout')

    logger.debug(f'Perform logout calling endpoint {endpoint}')
    r = session.post(endpoint, headers={'Referer': portal_url}, verify=verify, auth=auth)
    if r.status_code != 200:
        logger.warn(f'Response status code from {endpoint} is {r.status_code}')
        logger.warn('Response text is:')
        logger.warn(f'{r.text}', indent=4)
    else:
        logger.debug('Logout performed successfully')


@click.command('create')
@click.option('-u', '--username', ConfigurationMap.AUTH_USERNAME.cli_param_name,
              envvar=ConfigurationMap.AUTH_USERNAME.env_var_name, type=str,
              help='Username used to authenticate while getting a new token.')
@click.option('-t', '--token-only', 'output_token_only', is_flag=True, type=bool,
              help='Return only the token id of the new token (useful for shell scripting integration).')
@click.option('-b', '--http-basic', ConfigurationMap.HTTP_BASIC_AUTH.cli_param_name, flag_value='true', type=str,
              help='Enable HTTP Basic Authentication to authenticate while getting a new token.')
@click.option('-x', '--text', 'output_plaintext', is_flag=True, type=bool,
              help='Return the plain text version of the new token, if any valid, '
                   'as given by the EF Portal token service.')
@click.pass_obj
def create_token(conf: dict, **kwargs: dict):
    """
    Create a new token to authenticate to EF Portal services.\n
    A valid token is required to use all other commands offered by this client.
    """
    portal_url = conf[ConfigurationMap.PORTAL_URL.name]

    with requests.session() as session:
        # Get token
        cli_user = kwargs.get(ConfigurationMap.AUTH_USERNAME.cli_param_name)
        user = cli_user if cli_user else conf[ConfigurationMap.AUTH_USERNAME.name]
        if not user:
            user = input(f'[{portal_url}] Enter the username to authenticate: ')

        password = conf[ConfigurationMap.AUTH_PASSWORD.name]
        if not password:
            password = getpass(f'[{portal_url}] Enter the password to authenticate: ')

        cli_http_auth = kwargs.get(ConfigurationMap.HTTP_BASIC_AUTH.cli_param_name)
        http_basic_auth = (cli_http_auth if cli_http_auth else conf[ConfigurationMap.HTTP_BASIC_AUTH.name]).lower() == 'true'

        verify = conf[ConfigurationMap.CA_BUNDLE.name] if conf[ConfigurationMap.SSL_VERIFY.name].lower() == 'true' else False

        token, service_out = _get_token(session, portal_url, user, password, http_basic_auth=http_basic_auth, verify=verify)

        if kwargs.get('output_token_only') and kwargs.get('output_plaintext'):
            logger.warn('Both --text and --token-only options given, using --token-only')

        if kwargs.get('output_token_only'):
            out = token['token'] if token.get('token') else ''
        elif kwargs.get('output_plaintext'):
            out = service_out if len(token) > 0 else ''
        else:
            out = json_str(token)

        logger.echo(out)
