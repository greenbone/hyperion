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

from selene.schema.oval_definitions.fields import OvalDefinition

from selene.schema.parser import FilterString

from selene.schema.relay import (
    EntityConnectionField,
    Entities,
    get_filter_string_for_pagination,
)

from selene.schema.utils import get_gmp, require_authentication, XmlElement


class GetOvalDefinition(graphene.Field):
    """Gets a single OvalDefinition information.

    Args:
        id (str): ID of the Oval Definition information being queried

    Example:

        .. code-block::

            query {
                ovalDefinition(id: "oval:org.mitre.oval:def:12345") {
                    id
                    name
                    title
                    cveRefs
                    status
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "ovalDefinition": {
                        "id": "oval:org.mitre.oval:def:12345",
                        "name": "Foo"
                        "title": "Vendor product etc"
                        "cveRefs": 1
                        "status": "FINAL"
                    }
                }
            }

    """

    def __init__(self):
        super().__init__(
            OvalDefinition,
            oval_definition_id=graphene.String(required=True, name='id'),
            resolver=self.resolve,
        )

    @staticmethod
    @require_authentication
    def resolve(_root, info, oval_definition_id: str):
        gmp = get_gmp(info)

        xml = gmp.get_info(
            str(oval_definition_id), info_type=GvmInfoType.OVALDEF
        )
        return xml.find('info')


class GetOvalDefinitions(EntityConnectionField):
    """Gets a list of Oval Definition information with pagination

    Args:
        filter_string (str, optional): Optional filter string to be
            used with query.

    Example:

        .. code-block::

            query {
                ovalDefinitions (filterString: "name~Foo") {
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
                    "ovalDefinitions": {
                        "nodes": [
                            {
                                "id": "oval:org.mitre.oval:def:12345",
                                "name": "Foo"
                            },
                        ]
                    }
                }
            }

    """

    entity_type = OvalDefinition

    @staticmethod
    @require_authentication
    def resolve_entities(  # pylint: disable=arguments-differ
        _root,
        info: ResolveInfo,
        filter_string: FilterString = None,
        details: bool = True,
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
            filter=filter_string.filter_string,
            info_type=GvmInfoType.OVALDEF,
            details=details,
        )

        requested = None
        oval_definition_elements = []
        info_elements = xml.findall('info')
        for element in info_elements:
            if element.get('id'):
                oval_definition_elements.append(element)
            else:
                requested = element
        counts = xml.find('info_count')

        return Entities(oval_definition_elements, counts, requested)
