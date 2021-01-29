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

from selene.schema.schedules.fields import Schedule

from selene.schema.utils import (
    require_authentication,
    get_gmp,
    XmlElement,
)


class GetSchedule(graphene.Field):
    """Gets a single schedule.

    Args:
        id (UUID): UUID of the schedule being queried

    Example:

        .. code-block::

            query {
                schedule (id: "4a4717fe-57d2-11e1-9a26-406186ea4fc5") {
                    id
                    name
                    timezone
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "schedule": {
                        "id": "4a4717fe-57d2-11e1-9a26-406186ea4fc5"
                        "name": "Weekly schedule",
                        "timezone": UTC,
                    }
                }
            }

    """

    def __init__(self):
        super().__init__(
            Schedule,
            schedule_id=graphene.UUID(required=True, name='id'),
            tasks=graphene.Boolean(default_value=True),
            resolver=self.resolve,
        )

    @staticmethod
    @require_authentication
    def resolve(_root, info, schedule_id: UUID, tasks):
        gmp = get_gmp(info)

        xml = gmp.get_schedule(str(schedule_id), tasks=tasks)
        return xml.find('schedule')


class GetSchedules(EntityConnectionField):
    """Gets a list of schedules with pagination

    Args:
        filter_string (str, optional): Optional filter string to be
            used with query.

    Example:

        .. code-block::

            query {
                schedules(filterString: "weekly"){
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
                    "schedules": {
                        "nodes": [
                            {
                                "name": "Weekly schedule",
                                "id": "33d0cd82-57c6-11e1-8ed1-406186ea4fc5",
                            },
                            {
                                "name": "Last weekly tonight",
                                "id": "4a4717fe-57d2-11e1-9a26-406186ea4fc5",
                            },
                        ]
                    }
                }
            }

    """

    entity_type = Schedule

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

        xml: XmlElement = gmp.get_schedules(filter=filter_string.filter_string)

        schedule_elements = xml.findall('schedule')
        counts = xml.find('schedule_count')
        requested = xml.find('schedules')

        return Entities(schedule_elements, counts, requested)
