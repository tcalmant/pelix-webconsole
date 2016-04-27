#!/usr/bin/env python
# -- Content-Encoding: UTF-8 --
"""
Pelix Web Console: bundles pages

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
@Instantiate('web-console-bundles')
class BundlesPage(BasicPage):
    """
    Bundles page for the Web Console
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
        self._id = "bundles"
        self._title = "Bundles"

        self._context = context

    def handle(self, sub_url, response):
        """
        Prepares the content of the bundles page

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

        # Normalize bundles data
        bundles_info = [
            {"id": bundle.get_bundle_id(),
             "link": self.make_bundle_link(bundle, bundle.get_symbolic_name()),
             "version": str(bundle.get_version()),
             "state": self._utils.bundlestate_to_str(bundle.get_state())}
            for bundle in self._context.get_bundles()]

        rows = [
            "<tr>\n"
            "  <td>{id}</td>\n"
            "  <td>{link}</td>\n"
            "  <td>{version}</td>\n"
            "  <td>{state}</td>\n"
            "</tr>".format(**bundle_info) for bundle_info in bundles_info]

        page = """
<h1>Bundles</h1>
<div class="table-responsive">
<table class="table table-striped table-hover">
<thead>
    <th>ID</th>
    <th>Name</th>
    <th>Version</th>
    <th>State</th>
</thead>
<tbody>
{rows}
</tbody>
</table>
</div>
""".format(rows='\n'.join(rows))
        response.send_content(200, page)

    def _details(self, bundle_id, response):
        """
        Prints the details of a bundle

        :param bundle_id: ID of the bundle
        :param response: Response bean
        """
        try:
            bundle = self._context.get_bundle(bundle_id)
        except constants.BundleException:
            return response.send_content(
                404, "Bundle not found: {0}".format(bundle_id))

        services = bundle.get_registered_services() or []
        provided_svc_rows = [
            "<tr>\n"
            "  <td>{svc_id}</td>\n"
            "  <td>{spec}</td>\n"
            "  <td>{rank}</td>\n"
            "</tr>".format(
                svc_id=svc_ref.get_property(constants.SERVICE_ID),
                spec=self.make_service_link(
                    svc_ref,
                    ";".join(svc_ref.get_property(constants.OBJECTCLASS))),
                rank=svc_ref.get_property(constants.SERVICE_RANKING))
            for svc_ref in services]

        services = bundle.get_services_in_use()
        consumed_svc_rows = [
            "<tr>\n"
            "  <td>{svc_id}</td>\n"
            "  <td>{spec}</td>\n"
            "  <td>{bundle}</td>\n"
            "  <td>{rank}</td>\n"
            "</tr>".format(
                svc_id=svc_ref.get_property(constants.SERVICE_ID),
                spec=self.make_service_link(
                    svc_ref,
                    ";".join(svc_ref.get_property(constants.OBJECTCLASS))),
                bundle=self.make_bundle_link(svc_ref.get_bundle()),
                rank=svc_ref.get_property(constants.SERVICE_RANKING))
            for svc_ref in services]

        page = """
<h1>Bundle {name} ({bid})</h1>
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
            <td>{bid}</td>
        </tr>
        <tr>
            <td>Name</td>
            <td>{name}</td>
        </tr>
        <tr>
            <td>Version</td>
            <td>{version}</td>
        </tr>
        <tr>
            <td>State</td>
            <td>{state}</td>
        </tr>
        <tr>
            <td>Location</td>
            <td>{location}</td>
        </tr>
    </tbody>
    </table>
</div>

<h2>Provided Services</h2>
<div class="table-responsive">
    <table class="table table-striped table-hover">
    <thead>
        <th>ID</th>
        <th>Specifications</th>
        <th>Ranking</th>
    </thead>
    <tbody>
    {provided_svc_rows}
    </tbody>
    </table>
</div>

<h2>Consumed Services</h2>
<div class="table-responsive">
    <table class="table table-striped table-hover">
    <thead>
        <th>ID</th>
        <th>Specifications</th>
        <th>Bundle</th>
        <th>Ranking</th>
    </thead>
    <tbody>
    {consumed_svc_rows}
    </tbody>
    </table>
</div>
        """.format(
            name=bundle.get_symbolic_name(), bid=bundle.get_bundle_id(),
            version=bundle.get_version(), location=bundle.get_location(),
            provided_svc_rows='\n'.join(provided_svc_rows),
            consumed_svc_rows='\n'.join(consumed_svc_rows),
            state=self._utils.bundlestate_to_str(bundle.get_state()))
        response.send_content(200, page)
