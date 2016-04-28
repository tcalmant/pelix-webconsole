#!/usr/bin/env python
# -- Content-Encoding: UTF-8 --
"""
Core module for the Pelix Web Console.

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
import mimetypes
import os

try:
    from urllib.parse import urlencode, urlsplit
except ImportError:
    from urllib import urlencode, urlsplit

# Setuptools
import pkg_resources

# iPOPO Decorators
from pelix.ipopo.decorators import ComponentFactory, Provides, RequiresMap, \
    Instantiate, Property, Validate

import pelix.http
import pelix.shell

import pelix_webconsole
from pelix_webconsole.utils import BasicPage

# ------------------------------------------------------------------------------

# Documentation strings format
__docformat__ = "restructuredtext en"

# Version
__version_info__ = (0, 0, 1)
__version__ = ".".join(str(x) for x in __version_info__)

# Overview page
OVERVIEW_ID = "overview"

# ------------------------------------------------------------------------------


@ComponentFactory()
@RequiresMap('_pages', pelix_webconsole.SERVICE_PAGE_PROVIDER,
             pelix_webconsole.PROP_PAGE_ID, optional=True)
@Provides(pelix.http.HTTP_SERVLET)
@Property('_path', pelix.http.HTTP_SERVLET_PATH, '/console')
@Instantiate('web-console-servlet')
class WebConsoleServlet(object):
    """
    Web Console servlet
    """
    def __init__(self):
        """
        Sets up members
        """
        self._pages = None
        self._path = None
        self._context = None

    @Validate
    def validate(self, context):
        """
        Component validated

        :param context: Bundle Context
        """
        self._context = context

    def do_GET(self, request, response):
        """
        Handle a GET request

        :param request: Request bean
        :param response: Response bean
        """
        servlet_path = self._path.split('/')
        path_info = urlsplit(request.get_path())
        path = path_info.path.split('/')[len(servlet_path):]

        if not path or not path[0]:
            response.set_response(302)
            response.set_header(
                "location", '/'.join(servlet_path + ["index.html"]))
            response.end_headers()
            return

        if path[0] == 'api':
            # REST API call
            if path[1] == 'v1':
                # Dispatch the request
                if path[2] == 'pages':
                    return self.send_pages(response)
                elif path[2] == 'page':
                    return self.send_page(
                        path[3], '/'.join(path[4:]), response)
                else:
                    return response.send_content(
                        404, "<p>Unknown API entry</p>")
            else:
                return response.send_content(404, "<p>Unknown API version</p>")
        else:
            # Static file, use pkg_resources
            file_subpath = os.path.join("_static", os.path.sep.join(path))
            try:
                # Use setuptools when possible
                data = pkg_resources.resource_string(__name__, file_subpath)
            except IOError:
                # File not found
                response.send_content(404, "<h1>File not found</h1>\n"
                                           "<p>{0}</p>".format(file_subpath))
            else:
                response.send_content(
                    200, data, mimetypes.guess_type(file_subpath))

    def send_pages(self, response):
        """
        Sends the list of known pages

        :param response: Response bean
        """
        # The internal 'overview' page
        pages = {"main": OVERVIEW_ID,
                 "pages": [OVERVIEW_ID],
                 "names": [OVERVIEW_ID.title()]}

        # Prepare the list of pages
        for page_id in sorted(self._pages):
            pages['pages'].append(page_id)
            pages['names'].append(self._pages[page_id].get_title())

        # Send the response as a JSON object
        response.send_content(200, json.dumps(pages), "application/json")

    def send_page(self, page_id, sub_url, response):
        """
        Sends the content of the requested page

        :param page_id: Page ID
        :param sub_url: Sub URL to give to the page
        :param response: Response bean
        """
        try:
            self._pages[page_id].handle(sub_url, response)
        except KeyError:
            if page_id == OVERVIEW_ID:
                self.send_overview(response)
            else:
                content = """<html>
<head>
<title>Pelix Web Console</title>
</head>
<body>
<h1>Page not found: {title}</h1>
</html>
""".format(title=page_id)
                response.send_content(404, content)

    def send_overview(self, response):
        """
        Sends the overview page

        :param response: Response bean
        """
        framework = self._context.get_bundle(0)
        fw_props = framework.get_properties()
        props_rows = '\n'.join(
            "<tr>\n"
            "  <td>{0}</td>\n"
            "  <td>{1}</td>\n"
            "</tr>".format(BasicPage.escape(key),
                           BasicPage.escape(fw_props[key]))
            for key in sorted(fw_props))

        environment = os.environ
        env_rows = '\n'.join(
            "<tr>\n"
            "  <td>{0}</td>\n"
            "  <td>{1}</td>\n"
            "</tr>".format(BasicPage.escape(key),
                           BasicPage.escape(environment[key]))
            for key in sorted(environment))

        install_folder = os.path.dirname(pelix.__file__)

        content = """
<h1>Framework Overview</h1>
<h2>Pelix</h2>
<div class="table-responsive">
<table class="table table-striped table-hover">
<thead>
    <th>Key</th>
    <th>Value</th>
</thead>
<tbody>
<tr>
    <td>Framework Version</td>
    <td>{version}</td>
</tr>
<tr>
    <td>Framework Installation Folder</td>
    <td>{install_folder}</td>
</tr>
</tbody>
</table>
</div>

<h2>Framework Properties</h2>
<div class="table-responsive">
<table class="table table-striped table-hover">
<thead>
    <th>Key</th>
    <th>Value</th>
</thead>
<tbody>
{props_rows}
</tbody>
</table>
</div>

<h2>Environment Variables</h2>
<div class="table-responsive">
<table class="table table-striped table-hover">
<thead>
    <th>Key</th>
    <th>Value</th>
</thead>
<tbody>
{env_rows}
</tbody>
</table>
</div>""".format(props_rows=props_rows, env_rows=env_rows,
                 version=pelix.__version__, install_folder=install_folder)

        # Send the response as HTML
        response.send_content(200, content)
