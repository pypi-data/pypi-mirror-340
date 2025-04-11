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
from typing import Any


class EFPClientJsonEncoder(json.JSONEncoder):
    """ Custom JSON encoder which strips empty items. """
    def default(self, o):
        return str(o)

    def encode(self, o):
        return super().encode(strip_empty_items(o))


def strip_empty_items(o: Any) -> Any:
    """ Recursively remove empty items from ``list`` and ``dict``.

     :param o: object from which to remove empty items
     :returns: the stripped object
     """
    if isinstance(o, dict):
        return dict((k, strip_empty_items(v)) for k, v in o.items() if v)

    if isinstance(o, list):
        return list(strip_empty_items(v) for v in o if v)

    return o


def json_str(data: Any) -> str:
    """ Serialize the given object in a JSON formatted string, stripping empty items.

    :param data: object to serialize
    :returns: the JSON formatted string
    """
    return json.dumps(data, indent=4, cls=EFPClientJsonEncoder)
