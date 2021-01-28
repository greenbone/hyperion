# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Greenbone Networks GmbH
#
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# pylint: disable=no-self-argument

from uuid import UUID

import graphene

from graphql import ResolveInfo

from selene.schema.parser import FilterString

from selene.schema.relay import (
    EntityConnectionField,
    Entities,
    get_filter_string_for_pagination,
)

from selene.schema.scanners.fields import Scanner

from selene.schema.utils import (
    get_gmp,
    require_authentication,
    XmlElement,
)


class GetScanner(graphene.Field):
    """Gets a single scanner.

    Args:
        id (UUID): UUID of the scanner being queried

    Example:

        .. code-block::

            query {
                scanner(scannerId: "08b69003-5fc2-4037-a479-93b440211c73"){
                    name
                    id
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "scanner": {
                        "name": "OpenVAS Default",
                        "id": "08b69003-5fc2-4037-a479-93b440211c73"
                    }
                }
            }

    """

    def __init__(self):
        super().__init__(
            Scanner,
            scanner_id=graphene.UUID(required=True, name='id'),
            resolver=self.resolve,
        )

    @staticmethod
    @require_authentication
    def resolve(_root, info, scanner_id: UUID):
        gmp = get_gmp(info)

        xml = gmp.get_scanner(str(scanner_id))
        return xml.find('scanner')


class GetScanners(EntityConnectionField):
    """Gets a list of scanners with pagination

    Args:
        filter_string (str, optional): Optional filter string to be
            used with query.

    Example:

        .. code-block::

            query {
                scanners (filterString: "openvas"){
                    nodes {
                        name
                        type
                        id
                    }
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "scanners": {
                        "nodes": [
                            {
                                "name": "OpenVAS Default",
                                "type": "OPENVAS_SCANNER_TYPE",
                                "id": "08b69003-5fc2-4037-a479-93b440211c73"
                            },
                            {
                                "name": "OSP Scanner-openvas",
                                "type": "OSP_SCANNER_TYPE",
                                "id": "6b2db524-9fb0-45b8-9b56-d958f84cb546"
                            }
                        ]
                    }
                }
            }

    """

    entity_type = Scanner

    @staticmethod
    @require_authentication
    def resolve_entities(  # pylint: disable=arguments-differ
        _root,
        info: ResolveInfo,
        filter_string: FilterString = None,
        after: str = None,
        before: str = None,
        first: int = None,
        last: int = None,
    ) -> Entities:
        gmp = get_gmp(info)

        filter_string = get_filter_string_for_pagination(
            filter_string, first=first, last=last, after=after, before=before
        )

        xml: XmlElement = gmp.get_scanners(
            filter=filter_string.filter_string, details=True
        )

        scanner_elements = xml.findall('scanner')
        counts = xml.find('scanner_count')
        requested = xml.find('scanners')

        return Entities(scanner_elements, counts, requested)
