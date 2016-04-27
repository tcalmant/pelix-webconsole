#!/usr/bin/env python
# -- Content-Encoding: UTF-8 --
"""
Pelix Web Console root package

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

# Module version
__version_info__ = (0, 0, 1)
__version__ = ".".join(str(x) for x in __version_info__)

# Documentation strings format
__docformat__ = "restructuredtext en"

# ------------------------------------------------------------------------------

SERVICE_PAGE_PROVIDER = "pelix.webconsole.page"
"""
Pelix Web Console Page provider service:

* handle(sub_url, response): Handles a page request
* get_id(): Returns the page ID
* get_title(): Returns the page title
"""

PROP_PAGE_ID = "pelix.webconsole.page.id"
"""
The ID of the page provided by the service
"""

PROP_PAGE_TITLE = "pelix.webconsole.page.title"
"""
The title of the page provided by the service
"""
