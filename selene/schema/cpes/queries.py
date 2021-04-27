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

import graphene

from graphql import ResolveInfo
from gvm.protocols.next import InfoType as GvmInfoType

from selene.schema.cpes.fields import CPE

from selene.schema.parser import FilterString

from selene.schema.relay import (
    EntityConnectionField,
    Entities,
    get_filter_string_for_pagination,
)

from selene.schema.utils import get_gmp, require_authentication, XmlElement


class GetCPE(graphene.Field):
    """Gets a single CPE information.

    Args:
        id (str): ID of the CPE information being queried

    Example:

        .. code-block::

            query {
                cpe(id: "cpe:/a:vendor:product:etc") {
                    id
                    name
                    updateTime
                    title
                    nvdId
                    maxCvss
                    cveRefs
                    status
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "cpe": {
                        "id": "cpe:/a:vendor:product:etc",
                        "name": "cpe:/a:vendor:product:etc"
                        "title": "Vendor product etc"
                        "nvdId": "123456"
                        "maxCvss": 5.6
                        "cveRefs": 1
                        "status": "FINAL"
                    }
                }
            }

    """

    def __init__(self):
        super().__init__(
            CPE,
            cpe_id=graphene.String(required=True, name='id'),
            resolver=self.resolve,
        )

    @staticmethod
    @require_authentication
    def resolve(_root, info, cpe_id: str):
        gmp = get_gmp(info)

        xml = gmp.get_info(str(cpe_id), info_type=GvmInfoType.CPE)
        return xml.find('info')


class GetCPEs(EntityConnectionField):
    """Gets a list of CPE information with pagination

    Args:
        filter_string (str, optional): Optional filter string to be
            used with query.

    Example:

        .. code-block::

            query {
                cpes (filterString: "name~Foo rows=2") {
                    nodes {
                        id
                        name
                    }
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "cpes": {
                        "nodes": [
                            {
                                "id": "CPE-2020-12345",
                                "name": "Foo"
                            },
                            {
                                "id": "CPE-2020-12346",
                                "name": "Foo Bar"
                            },
                        ]
                    }
                }
            }

    """

    entity_type = CPE

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

        xml: XmlElement = gmp.get_info_list(
            filter=filter_string.filter_string, info_type=GvmInfoType.CPE
        )

        requested = None
        cpe_elements = []
        info_elements = xml.findall('info')
        for element in info_elements:
            if element.get('id'):
                cpe_elements.append(element)
            else:
                requested = element
        counts = xml.find('info_count')

        return Entities(cpe_elements, counts, requested)
