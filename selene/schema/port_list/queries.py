# -*- coding: utf-8 -*-
# Copyright (C) 2020-2021 Greenbone Networks GmbH
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

# pylint: disable=no-self-argument, no-member

from uuid import UUID

import graphene

from graphql import ResolveInfo

from selene.schema.parser import FilterString
from selene.schema.port_list.fields import PortList

from selene.schema.relay import (
    EntityConnectionField,
    Entities,
    get_filter_string_for_pagination,
)

from selene.schema.utils import (
    require_authentication,
    get_gmp,
    XmlElement,
)


class GetPortList(graphene.Field):
    """Get a single portlist

    Example:

        .. code-block::

            query {
                portList (id: "4a4717fe-57d2-11e1-9a26-406186ea4fc5") {
                    id
                    name
                    portRanges [
                        {
                           start
                           end
                           type
                        }
                    ]
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "port_list": {
                        "id": "4a4717fe-57d2-11e1-9a26-406186ea4fc5"
                        "name": "All IANA assigned TCP and UDP",
                        "portRanges": [
                            {
                                "type": TCP,
                            }
                        ]
                    }
                }
            }

    """

    def __init__(self):
        super().__init__(
            PortList,
            port_list_id=graphene.UUID(
                required=True, name='id', description="ID of the port list"
            ),
            resolver=self.resolve,
        )

    @staticmethod
    @require_authentication
    def resolve(_root, info: ResolveInfo, port_list_id: UUID):
        gmp = get_gmp(info)

        xml: XmlElement = gmp.get_port_list(str(port_list_id))
        return xml.find('port_list')


class GetPortLists(EntityConnectionField):
    """Get a list of port lists with pagination

    Example:

        .. code-block::

            query {
                portLists(filterString: "all IANA"){
                    nodes{
                        name
                        id
                    }
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "portLists": {
                        "nodes": [
                            {
                                "name": "All IANA assigned TCP",
                                "id": "33d0cd82-57c6-11e1-8ed1-406186ea4fc5",
                            },
                            {
                                "name": "All IANA assigned TCP and UDP",
                                "id": "4a4717fe-57d2-11e1-9a26-406186ea4fc5",
                            },
                        ]
                    }
                }
            }

    """

    entity_type = PortList

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

        # details are required for port ranges
        xml: XmlElement = gmp.get_port_lists(
            filter=filter_string.filter_string, details=True
        )

        port_list_elements = xml.findall('port_list')
        counts = xml.find('port_list_count')
        requested = xml.find('port_lists')

        return Entities(port_list_elements, counts, requested)
