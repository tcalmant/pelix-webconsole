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

    @staticmethod
    def make_show_page_link(page_id, sub_page, text):
        """
        Prepares a link to call the JavaScript method "showSubPage"

        :param page_id: ID of the page to show
        :param sub_page: Sub-URL of the page to show
        :param text: Link text
        :return: The link string
        """
        return "<a href=\"javascript:GlobalPagesIDs['{0}']" \
            ".showSubPage('{1}')\">{2}</a>".format(page_id, sub_page, text)

    def make_bundle_link(self, bundle, text=None):
        """
        Prepares an HTML link to the details of the given bundle

        :param bundle: A Bundle object
        :param text: Optional link text
        :return: An HTML link string
        """
        bid = bundle.get_bundle_id()
        if not text:
            text = "{0} ({1})".format(bundle.get_symbolic_name(), bid)

        return self.make_show_page_link(
            "bundles", "details/{0}".format(bid), text)

    def make_service_link(self, svc_ref, text=None):
        """
        Prepares an HTML link to the details of the given service

        :param svc_ref: A ServiceReference object
        :param text: Optional link text
        :return: An HTML link string
        """
        sid = svc_ref.get_property(constants.SERVICE_ID)
        if not text:
            text = "{0} ({1})".format(
                ";".join(svc_ref.get_property(constants.OBJECTCLASS)), sid)

        return self.make_show_page_link(
            "services", "details/{0}".format(sid), text)
