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
import logging
import traceback
from typing import Any

import click

OFF = 2 * logging.ERROR

# Java logging levels are supported and mapped accordingly
_levels_map = {
    'finest': logging.DEBUG,
    'finer': logging.DEBUG,
    'fine': logging.DEBUG,
    'config': logging.DEBUG,
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warn': logging.WARN,
    'warning': logging.WARN,
    'error': logging.ERROR,
    'severe': logging.ERROR,
    'off': OFF
}

level = logging.WARN  # pylint: disable=invalid-name


def _indent(msg: str, quantity: int = 4):
    if quantity <= 0:
        return msg

    if msg:
        out = ''
        for line in msg.splitlines(keepends=True):
            out += (quantity * ' ') + line
        return out

    return None


def echo(msg: str, indent: int = 0):
    """ Print a message to standard output without any coloring unless log level is 'off'.

    :param msg: message to be printed
    :param indent: message indentation (default: 0)
    """
    if level != OFF:
        click.echo(_indent(msg, indent))


def debug(msg: str, indent: int = 0):
    """ Print a colored message to standard output if log level is 'debug'.

    :param msg: message to be printed
    :param indent: message indentation (default: 0)
    """
    if level <= logging.DEBUG:
        click.secho(_indent(msg, indent), fg='bright_magenta')


def info(msg: str, indent: int = 0):
    """ Print a colored message to standard output if log level is 'info'.

    :param msg: message to be printed
    :param indent: message indentation (default: 0)
    """
    if level <= logging.INFO:
        click.secho(_indent(msg, indent), fg='cyan')


def warn(msg: str, indent: int = 0):
    """ Print a colored message to standard output if log level is 'warn'.

    :param msg: message to be printed
    :param indent: message indentation (default: 0)
    """
    if level <= logging.WARN:
        click.secho(_indent(msg, indent), fg='yellow', err=True)


def error(msg: str, e: Exception = None, indent: int = 0):
    """ Print a colored message to standard output if log level is 'error'.

    :param msg: message to be printed
    :param e: the :class:`Exception` for which to print the stack trace (default: None)
    :param indent: message indentation (default: 0)
    """
    if level <= logging.ERROR:
        click.secho(_indent(msg, indent), fg='red', err=True)
        if e:
            click.secho(_indent('Traceback (most recent call last):', indent), fg='red')
            tb = traceback.format_tb(e.__traceback__)
            for s in tb:
                click.secho(_indent(s, indent), fg='red', nl=False, err=True)


def map_level(conf_level: Any) -> int:
    """ Map a log level as defined in the configuration to the internal (``logging`` library compliant) log level.
    This is needed to transparently support Java log levels from the legacy 'efclient' configuration.

    :param conf_level: the configuration level, either ``str`` or ``int``
    :returns the mapped log level, as defined by the ``logging`` library
    """
    if isinstance(conf_level, str) and _levels_map.get(conf_level.lower()):
        return _levels_map[conf_level.lower()]

    if isinstance(conf_level, int):
        return conf_level

    return logging.WARN
