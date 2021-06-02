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

from uuid import UUID

import graphene

from graphql import ResolveInfo

from selene.schema.parser import FilterString

from selene.schema.relay import (
    EntityConnectionField,
    Entities,
    get_filter_string_for_pagination,
)

from selene.schema.utils import get_gmp, require_authentication, XmlElement

from selene.schema.overrides.fields import Override


class GetOverride(graphene.Field):
    """Gets a single override.

    Args:
        id (UUID): UUID of the override being queried

    Example:

        .. code-block::

            query {
                override(id: "6e618e3a-bdfb-4495-9571-22c84b022b13"){
                    id
                    text
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "override": {
                        "id": "6e618e3a-bdfb-4495-9571-22c84b022b13",
                        "text": "Test Override"
                    }
                }
            }

    """

    def __init__(self):
        super().__init__(
            Override,
            override_id=graphene.UUID(required=True, name='id'),
            resolver=self.resolve,
        )

    @staticmethod
    @require_authentication
    def resolve(_root, info, override_id: UUID):
        gmp = get_gmp(info)

        xml = gmp.get_override(str(override_id))
        return xml.find('override')


class GetOverrides(EntityConnectionField):
    """Gets a list of overrides with pagination

    Args:
        filter_string (str, optional): Optional filter string to be
            used with query.

    Example:

        .. code-block::

            query {
                overrides (filterString: "Test"){
                    nodes {
                        id
                        text
                    }
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "overrides": {
                        "nodes": [
                            {
                                "id": "08b69003-5fc2-4037-a479-93b440211c73"
                                "text": "Test Override 1",
                            },
                            {
                                "id": "6b2db524-9fb0-45b8-9b56-d958f84cb546"
                                "text": "Test Override 2",
                            }
                        ]
                    }
                }
            }

    """

    entity_type = Override

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

        xml: XmlElement = gmp.get_overrides(
            filter_string=filter_string.filter_string, details=True
        )

        override_elements = xml.findall('override')
        counts = xml.find('override_count')
        requested = xml.find('overrides')

        return Entities(override_elements, counts, requested)
