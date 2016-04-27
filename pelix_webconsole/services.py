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
        parts = sub_url.split('/')
        if parts:
            try:
                if parts[0] == 'details':
                    return self._details(int(parts[1]), response)
            except IndexError:
                return response.send_content(500, "Argument missing")

        # Normalize service data
        references = self._context.get_all_service_references(None)
        services_info = [
            {"id": ref.get_property(constants.SERVICE_ID),
             "specs": self.make_service_link(
                 ref, ";".join(ref.get_property(constants.OBJECTCLASS))),
             "bundle": self.make_bundle_link(ref.get_bundle()),
             "rank": ref.get_property(constants.SERVICE_RANKING)}
            for ref in references]

        rows = ["<tr>\n"
                "  <td>{id}</td>\n"
                "  <td>{specs}</td>\n"
                "  <td>{bundle}</td>\n"
                "  <td>{rank}</td>\n"
                "</tr>".format(**svc_info)
                for svc_info in services_info]

        page = """
<h1>Services</h1>
<div class="table-responsive">
    <table class="table table-striped table-hover">
    <thead>
        <th>ID</th>
        <th>Specifications</th>
        <th>Bundle</th>
        <th>Ranking</th>
    </thead>
    <tbody>
    {rows}
    </tbody>
    </table>
</div>
    """.format(rows='\n'.join(rows))
        response.send_content(200, page)

    def _details(self, svc_id, response):
        """
        Prints the details of a service

        :param svc_id: ID of the service
        :param response: Response bean
        """
        svc_ref = self._context.get_service_reference(
            None, "({0}={1})".format(constants.SERVICE_ID, svc_id))
        if svc_ref is None:
            return response.send_content(
                404, "Service not found: {0}".format(svc_id))

        # Service properties (escaped)
        props = svc_ref.get_properties()
        props_rows = [
            "<tr>\n"
            "  <td>{0}</td>\n"
            "  <td>{1}</td>\n"
            "</tr>".format(self.escape(key), self.escape(props[key]))
            for key in sorted(props)]

        # Consuming bundles
        bundles_rows = [
            "<tr>\n"
            "  <td>{0}</td>\n"
            "</tr>".format(self.make_bundle_link(bundle))
            for bundle in svc_ref.get_using_bundles()]

        page = """
    <h1>Service {sid}</h1>
    <h2>Basic Information</h2>
    <div class="table-responsive">
        <table class="table table-striped table-hover">
        <thead>
            <th>Property</th>
            <th>Value</th>
        </thead>
        <tbody>
            <tr>
                <td>ID</td>
                <td>{sid}</td>
            </tr>
            <tr>
                <td>Rank</td>
                <td>{rank}</td>
            </tr>
            <tr>
                <td>Specifications</td>
                <td>{specs}</td>
            </tr>
            <tr>
                <td>Bundle</td>
                <td>{bundle_link}</td>
            </tr>
        </tbody>
        </table>
    </div>

    <h2>Service Properties</h2>
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

    <h2>Bundles using this service</h2>
    <div class="table-responsive">
        <table class="table table-striped table-hover">
        <thead>
            <th>Bundles</th>
        </thead>
        <tbody>
        {bundles_rows}
        </tbody>
        </table>
    </div>
            """.format(
            sid=svc_id, rank=svc_ref.get_property(constants.SERVICE_RANKING),
            specs=";".join(svc_ref.get_property(constants.OBJECTCLASS)),
            bundle_link=self.make_bundle_link(svc_ref.get_bundle()),
            props_rows='\n'.join(props_rows),
            bundles_rows='\n'.join(bundles_rows))
        response.send_content(200, page)
