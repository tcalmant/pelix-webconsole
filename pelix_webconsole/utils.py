#!/usr/bin/env python
# -- Content-Encoding: UTF-8 --
"""
Pelix Web Console: Utility methods and classes for page providers

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
try:
    from html import escape
except ImportError:
    from cgi import escape

# iPOPO Decorators
from pelix.ipopo.decorators import Provides, Property

import pelix.constants as constants
import pelix_webconsole

# ------------------------------------------------------------------------------

# Documentation strings format
__docformat__ = "restructuredtext en"

# Version
__version_info__ = (0, 0, 1)
__version__ = ".".join(str(x) for x in __version_info__)

# ------------------------------------------------------------------------------


@Provides(pelix_webconsole.SERVICE_PAGE_PROVIDER)
@Property('_id', pelix_webconsole.PROP_PAGE_ID)
@Property('_title', pelix_webconsole.PROP_PAGE_TITLE)
class BasicPage(object):
    """
    Mother class for page providers
    """
    def __init__(self):
        """
        Sets up members
        """
        # Properties
        self._id = None
        self._title = None

    def get_id(self):
        """
        Returns the ID of the page
        """
        return self._id

    def get_title(self):
        """
        Returns the title of the page
        """
        return self._title

    @staticmethod
    def escape(text):
        """
        Escapes the given text

        :param text: Some text
        :return: The HTML-escaped text
        """
        return escape(str(text), True)
