#!/usr/bin/env python
# -- Content-Encoding: UTF-8 --
"""
Pelix Web Console: services pages

:author: Thomas Calmant
:copyright: Copyright 2015, Thomas Calmant
:license: Apache License 2.0
:version: 0.0.1

..

    Copyright 2016 Thomas Calmant

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

# Standard library
import json

# iPOPO Decorators
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, \
    Instantiate
import pelix.constants as constants
import pelix.shell

from pelix_webconsole.utils import BasicPage

# ------------------------------------------------------------------------------

# Documentation strings format
__docformat__ = "restructuredtext en"

# Version
__version_info__ = (0, 0, 1)
__version__ = ".".join(str(x) for x in __version_info__)

# ------------------------------------------------------------------------------


@ComponentFactory()
@Requires('_utils', pelix.shell.SERVICE_SHELL_UTILS)
@Instantiate('web-console-services')
class ServicesPage(BasicPage):
    """
    Services page for the Web Console
    """
    def __init__(self):
        """
        Sets up members
        """
        BasicPage.__init__(self)
        self._utils = None
        self._context = None

    @Validate
    def validate(self, context):
        """
        Component validated

        :param context: Bundle Context
        """
        self._id = "services"
        self._title = "Services"
        self._context = context

    def handle(self, sub_url, response):
        """
        Prepares the content of the services page

        :param sub_url: Request sub-URL
        :param response: Response bean
        """
        parts = [part for part in sub_url.split('/') if part]
        if parts:
            return response.send_content(500, "Arguments are not supported")

        # Normalize service data
        services_info = [
            {"id": ref.get_property(constants.SERVICE_ID),
             "specifications": ref.get_property(constants.OBJECTCLASS),
             "providerId": ref.get_bundle().get_bundle_id(),
             "properties": {
                 str(key): str(value)
                 for key, value in ref.get_properties().items()}
             } for ref in self._context.get_all_service_references(None)]

        response.send_content(200, json.dumps(services_info),
                              mime_type="application/json")
