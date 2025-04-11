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
from os.path import basename
from pathlib import Path

import click

from efpclient import logger, swagger
from efpclient.commands import spoolers
from efpclient.configuration import ConfigurationMap
from efpclient.errors import ConfigurationError, CliError
from efpclient.swagger import handle_not_successful
from efpclient.swagger_client import Service, ServiceParam, ServiceRequest
from efpclient.swagger_client.rest import ApiException
from efpclient.utils import json_str

CLI_OPTION_ITEM = 'option'
CLI_HELP_ITEM = 'help'


# pylint: disable=too-few-public-methods
class ParsedService:
    """ Just a container class for a parsed EF Portal service. """
    def __init__(self, service_dict: dict, cli_options: dict, hidden_options: dict):
        self.service_dict = service_dict
        self.cli_options = cli_options
        self.hidden_options = hidden_options


@click.command('list')
@click.option('-d', '--sdf', ConfigurationMap.SDF_URI.cli_param_name, type=str,
              help='URI of the SDF containing services to list, e.g. /plugin_name/sdf.xml')
@click.pass_obj
def list_services(conf: dict, **kwargs: dict):
    """ List all services associated to given SDF. """
    sdf = _get_option_value(ConfigurationMap.SDF_URI, conf, **kwargs)
    try:
        logger.debug(f'Calling list_services with SDF {sdf}')
        response = swagger.get(conf).services(sdf)
        logger.info('Service replied with code 200')
        # Response contains a list of Service objects, we need to convert all of them to dict
        logger.echo(json_str(list(v.to_dict() for v in response)))
    except ApiException as e:
        handle_not_successful(e, [401, 400])


@click.command('describe')
@click.option('-d', '--sdf', ConfigurationMap.SDF_URI.cli_param_name, type=str,
              help='URI of the SDF containing the service to describe, e.g. /plugin_name/sdf.xml')
@click.option('-s', '--service', 'service_uri', type=str, required=True,
              help='URI of the service to describe, e.g. //sdf_name/service_name')
@click.option('-t', '--text', 'output_plaintext', is_flag=True, type=bool,
              help="Return the plain text version of service details, "
                   "useful to more easily see the command-line usage for 'submit' command.")
@click.pass_obj
def describe_service(conf: dict, **kwargs: dict):
    """ Describe a service given its URI. """
    sdf = _get_option_value(ConfigurationMap.SDF_URI, conf, **kwargs)
    uri = kwargs.get('service_uri')
    try:
        logger.debug(f'Calling get_service with SDF {sdf} and service uri {uri}')
        response = swagger.get(conf).get_service(sdf, str(uri))
        logger.info('Service replied with code 200')
        parsed_service = _process(response)
        if kwargs.get('output_plaintext'):
            _print_plaintext(parsed_service.service_dict)
        else:
            logger.echo(json_str(_help_for_json(parsed_service.service_dict)))
    except ApiException as e:
        handle_not_successful(e, [401, 400])


@click.command('submit', context_settings={'ignore_unknown_options': True})
@click.option('-d', '--sdf', ConfigurationMap.SDF_URI.cli_param_name, type=str,
              help='URI of the SDF containing the service to describe, e.g. /plugin_name/sdf.xml')
@click.option('-s', '--service', 'service_uri', type=str,
              help='URI of the service to describe, e.g. //sdf_name/service_name')
@click.option('-h', '--help', 'show_help', is_flag=True, type=bool,
              help='Show this message and exit.')
@click.argument('submit_options', nargs=-1, type=click.UNPROCESSED)
@click.pass_obj
def submit_service(conf: dict, submit_options: tuple, **kwargs: dict):
    """ Submit a service given its URI and options. """
    sdf = _get_option_value(ConfigurationMap.SDF_URI, conf, **kwargs)
    uri = kwargs.get('service_uri')
    show_help = kwargs.get('show_help')
    if not uri:
        if show_help:
            logger.echo(f'{click.get_current_context().get_help()}\n')
        else:
            logger.echo('Usage: efpclient services submit [OPTIONS] [SUBMIT_OPTIONS]...')
            logger.echo("Try 'efpclient services submit -h' for help.\n")

        raise CliError("Missing option '-s' / '--service'")

    if show_help:
        logger.echo(f'{click.get_current_context().get_help()}\n')
        try:
            parsed_service = _process(swagger.get(conf).get_service(sdf, str(uri)), choice_label=True)
            options = parsed_service.service_dict.get('options')
            if options:
                logger.echo('Service options:')
                _print_options_help(options)

            return
        except ApiException:
            logger.echo(f'Unable to get options for service {uri}')
            return

    try:
        logger.debug(f'Calling get_service with SDF {sdf} and service uri {uri} to fetch options details')
        client = swagger.get(conf)
        parsed_service = _process(client.get_service(sdf, str(uri)))
        logger.debug('Service replied with code 200')

        # Iterate over options given at command line and try to find a match with those defined by the service
        # In case of a match, we act accordingly to the option type
        logger.debug(f'Start parsing service specific options {submit_options}')
        params, filepaths = _parse_options(submit_options, parsed_service.cli_options, str(uri))

        # Process hidden options, if any. They are not exposed to the user, but their values
        # need to be sent to the service anyway
        for key in parsed_service.hidden_options:
            value = parsed_service.hidden_options[key]
            logger.debug(f'Found hidden option {key}, setting its value to: {value}')
            params.append(ServiceParam(key, [value]))

        spooler_uri = None
        if filepaths:
            logger.info('One or more options of type sfu or mfu specified, performing file upload before submit')
            response = spoolers.upload_files(conf, filepaths)
            if response:
                spooler_uri = json.loads(response.text)['uri']

        body = ServiceRequest(sdf=sdf, uri=uri, options=params, spooler_uri=spooler_uri)
        logger.debug(f'Calling submit_service with body:\n{body}')
        response = client.submit_service(body)
        logger.info('Service replied with code 200')
        logger.echo(json_str(response.to_dict()))

    except ApiException as e:
        handle_not_successful(e, [401, 400])


def _process(service: Service, choice_label: bool = False) -> ParsedService:
    service_dict = service.to_dict()
    cli_options = {}
    hidden_options = {}

    for option in service_dict.get('options'):
        opt_id = option.get('id')
        opt_type = option.get('type')
        opt_value = option.get('value')
        opt_label = option.get('label')
        opt_name = f'--opt-{opt_id}'
        opt_help = f'{opt_label if opt_label else "No description found"}.'

        if opt_type == 'boolean':
            opt_help += f' Specify this option to set the value: {opt_value}' if opt_value \
                else ' This option does not set any specific value.'

            option[CLI_OPTION_ITEM] = opt_name
            option[CLI_HELP_ITEM] = opt_help
            cli_options[opt_name] = {'id': opt_id, 'type': opt_type, 'value': opt_value}
        elif opt_type in ('list', 'radio'):
            choices = []
            # We assume at least one choice available
            for choice in option.get('choices'):
                value = choice.get('value')
                if value:
                    if choice_label:
                        label = choice.get('label') if choice.get('label') else 'No description found'
                        choices.append(f'{value}   "{label}"')
                    else:
                        choices.append(f'{value}')

            opt_help += f' Default value is: {opt_value}.' if opt_value else ''
            opt_help += ' Valid values to choose from are'
            opt_help += ' (description in quotes): ' if choice_label else ': '
            # Use a custom separator to avoid screwing any service defined text later on, since
            # we will format values differently based on chosen output mode.
            opt_help += f'{"@@".join(choices)}'

            option[CLI_OPTION_ITEM] = f'{opt_name} VALUE_1|VALUE_2|...'
            option[CLI_HELP_ITEM] = opt_help
            cli_options[opt_name] = {'id': opt_id, 'type': opt_type, 'choices': choices}
        elif opt_type in ('file', 'sfu'):
            option[CLI_OPTION_ITEM] = f'{opt_name} FILENAME'
            option[CLI_HELP_ITEM] = f'{opt_help} Specify a single local file to upload.'
            cli_options[opt_name] = {'id': opt_id, 'type': opt_type}
        elif opt_type == 'mfu':
            option[CLI_OPTION_ITEM] = f'{opt_name} FILENAME_1,FILENAME_2,...'
            option[CLI_HELP_ITEM] = (f'{opt_help} '
                                     f'Specify one or more local files to upload, using a comma separated list.')
            cli_options[opt_name] = {'id': opt_id, 'type': opt_type}
        elif opt_type == 'hidden':
            # Fill just the hidden_options dict since we need hidden values on submit
            hidden_options[opt_id] = opt_value
        else:
            # All other types of options are treated as text options (text, textarea, date, rfb, ...)
            opt_help += f' Default value is: {opt_value}' if opt_value else ''

            option[CLI_OPTION_ITEM] = f'{opt_name} TEXT'
            option[CLI_HELP_ITEM] = f'{opt_help}'
            cli_options[opt_name] = {'id': opt_id, 'type': opt_type}

    return ParsedService(service_dict, cli_options, hidden_options)


def _parse_options(submit_options: tuple, cli_options: dict, uri: str) -> (list, list):
    params = []
    filepaths = []

    options = iter(submit_options)
    option = next(options, None)
    while option:
        logger.debug(f'Parsing option {option}')
        if option in cli_options:
            opt = cli_options[option]
            opt_id = opt.get('id')
            opt_type = opt.get('type')
            if opt_type == 'boolean':
                opt_value = opt.get('value')
                logger.debug(f'Found matching boolean option {opt_id} with value: {opt_value}')
                params.append(ServiceParam(opt_id, [opt_value]))
            else:
                logger.debug('Option requires an argument, fetching it from command line')
                value = next(options, None)
                if not value:
                    raise CliError(f'Option \'{option}\' requires an argument')

                if opt_type in ('list', 'radio'):
                    opt_choices = opt.get('choices')
                    if value not in opt_choices:
                        raise CliError(f'Invalid value for option \'{option}\', '
                                       f'valid values are: {", ".join(opt_choices)}')

                    logger.debug(f'Found matching {opt_type} option {opt_id}, setting its value to: {value}')
                    params.append(ServiceParam(opt_id, [value]))
                elif opt_type in ('file', 'sfu'):
                    logger.debug(f'Found matching {opt_type} option {opt_id}, loading local file: {value}')
                    _add_file_to_request(value, opt_id, params, filepaths)
                elif opt_type == 'mfu':
                    logger.debug(f'Found matching {opt_type} option {opt_id}, start loading local files')
                    for filepath in value.split(','):
                        logger.debug(f'Loading file: {filepath}')
                        _add_file_to_request(filepath, opt_id, params, filepaths)
                else:
                    logger.debug(f'Found matching {opt_type} option {opt_id}, setting its value to: {value}')
                    params.append(ServiceParam(opt_id, [value]))
        else:
            raise CliError(f'No such option for service {uri}: {option}')

        option = next(options, None)

    return params, filepaths


def _add_file_to_request(filepath: str, opt_id: str, params: list, filepaths: list):
    filename = basename(Path(filepath))
    params.append(ServiceParam(opt_id, [filename]))
    filepaths.append(filepath)


def _get_option_value(conf_item: ConfigurationMap, conf: dict, **kwargs: dict) -> str:
    opt_value = kwargs.get(conf_item.cli_param_name)
    value = opt_value if opt_value else conf[conf_item.name]
    if not value:
        logger.echo(f'{click.get_current_context().get_help()}\n')
        raise ConfigurationError(f'Required parameter {conf_item.conf_param_name} is not defined')

    return str(value)


def _help_for_json(service_dict: dict) -> dict:
    for option in service_dict.get('options'):
        help_line = option.get('help')
        if help_line:
            option['help'] = help_line.replace('@@', ', ')

    return service_dict


def _print_plaintext(service: dict, parent: str = None, level: int = 0):
    lines = []

    for key in service.keys():
        if service[key]:
            if isinstance(service[key], list):
                logger.echo(f'{key}:', indent=4 * level)
                for entry in service[key]:
                    _print_plaintext(entry, key, (level + 1))
                    if not parent:
                        logger.echo('')
            elif parent == 'choices':
                lines.append(f'{key}: {service[key]}')
            else:
                if key == 'help':
                    help_line = (f'{key}: {service[key]}'
                                 .replace('values to choose from are:', f'values to choose from are:\n{" " * 6}-')
                                 .replace('@@', f'\n{" " * 6}- '))
                    logger.echo(help_line, indent=4 * level)
                else:
                    logger.echo(f'{key}: {service[key]}', indent=4 * level)

    if lines:
        logger.echo(', '.join(lines), indent=4 * level)


def _print_options_help(options: dict):
    for option in options:
        opt_name = option.get('option')
        if opt_name:
            logger.echo(f'{opt_name}', indent=2)
            opt_help = option.get('help')
            if opt_help:
                for line in opt_help.split('. '):
                    help_line = (line.strip()
                                 .replace('(description in quotes):', '(description in quotes):\n-')
                                 .replace('@@', '\n- '))
                    if help_line:
                        logger.echo(f'{help_line}', indent=6)
