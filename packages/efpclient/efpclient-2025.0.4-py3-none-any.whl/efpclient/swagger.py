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

from efpclient import swagger_client, logger
from efpclient.configuration import ConfigurationMap
from efpclient.errors import MissingTokenError
from efpclient.swagger_client import DefaultApi
from efpclient.swagger_client.rest import ApiException
from efpclient.utils import json_str


def get(conf: dict) -> DefaultApi:
    """ Get a new Swagger client instance.

    :param conf: the configuration dictionary
    :returns: the Swagger client instance
    """
    if not conf[ConfigurationMap.TOKEN.name]:
        raise MissingTokenError

    logger.debug('Creating Swagger client instance...')
    swagger_conf = swagger_client.Configuration()
    swagger_conf.host = conf[ConfigurationMap.PORTAL_URL.name]
    if conf[ConfigurationMap.SSL_VERIFY.name].lower() == 'true':
        swagger_conf.ssl_ca_cert = conf[ConfigurationMap.CA_BUNDLE.name]
    else:
        swagger_conf.verify_ssl = False
    swagger = swagger_client.DefaultApi(swagger_client.ApiClient(swagger_conf))
    swagger.api_client.set_default_header(header_name='Authorization',
                                          header_value=f'Bearer {conf[ConfigurationMap.TOKEN.name]}')
    logger.debug('Swagger client instance successfully created')

    return swagger


def handle_not_successful(e: ApiException, statuses: list):
    """ Handle not successful responses coming from Swagger client calls.

    :param e: the :class:`ApiException` thrown by a Swagger client call
    :param statuses: list of ``int`` representing HTTP status codes to manage
    """
    if e.status in statuses:
        logger.info(f'Service replied with code {e.status}')
        try:
            logger.echo(json_str(json.loads(e.body)))
        except ValueError:
            logger.echo(e.body)
    else:
        raise ApiException(e, e.status, e.reason)
