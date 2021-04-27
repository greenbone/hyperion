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

from graphql import ResolveInfo

import graphene

from selene.schema.parser import FilterString

from selene.schema.relay import (
    EntityConnectionField,
    Entities,
    get_filter_string_for_pagination,
)
from selene.schema.targets.fields import Target
from selene.schema.utils import require_authentication, get_gmp, XmlElement


class GetTarget(graphene.Field):
    """Gets a single target.

    Args:
        id (UUID): UUID of the target being queried

    Example:

        .. code-block::

            query {
                target(targetId: "90da78c5-81fc-49cb-903d-c87d73716ff0"){
                    name
                    id
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "target": {
                        "name": "Simple Target",
                        "id": "90da78c5-81fc-49cb-903d-c87d73716ff0"
                    }
                }
            }

    """

    def __init__(self):
        super().__init__(
            Target,
            target_id=graphene.UUID(
                required=True,
                name='id',
                description='Target ID to request details for',
            ),
            resolver=self.resolve,
        )

    @staticmethod
    @require_authentication
    def resolve(_root, info, target_id: UUID):
        gmp = get_gmp(info)

        xml = gmp.get_target(str(target_id), tasks=True)
        return xml.find('target')


class GetTargets(EntityConnectionField):
    """Gets a list of targets with pagination

    Args:
        filter_string (str, optional): Optional filter string to be
            used with query.

    Example:

        .. code-block::

            query {
                targets(filterString: "Target"){
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
                    "targets": {
                        "nodes": [
                            {
                                "name": "Test Target",
                                "id": "9c661873-1ba1-4a76-819b-505a216d4137"
                            },
                            {
                                "name": "Simple Target",
                                "id": "90da78c5-81fc-49cb-903d-c87d73716ff0"
                            },
                        ]
                    }
                }
            }

    """

    entity_type = Target

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

        xml: XmlElement = gmp.get_targets(filter=filter_string.filter_string)

        target_elements = xml.findall('target')
        counts = xml.find('target_count')
        requested = xml.find('targets')

        return Entities(target_elements, counts, requested)
