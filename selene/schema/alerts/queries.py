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

from graphql import ResolveInfo

import graphene

from selene.schema.base import SingleObjectQuery

from selene.schema.alerts.fields import Alert

from selene.schema.parser import FilterString

from selene.schema.relay import (
    EntityConnectionField,
    Entities,
    get_filter_string_for_pagination,
)

from selene.schema.utils import get_gmp, require_authentication, XmlElement


class GetAlert(SingleObjectQuery):
    """Get a single alert

    Example:

        query {
            alert(id: "08b69003-5fc2-4037-a479-93b440211c73"){
                name
                id
            }
        }

    Response:

        {
            "data": {
                "alert": {
                    "name": "foo",
                    "id": "08b69003-5fc2-4037-a479-93b440211c73"
                }
            }
        }

    """

    object_type = Alert
    kwargs = {
        'alert_id': graphene.UUID(
            required=True,
            name='id',
            description="UUID of the to be requested alert",
        ),
    }

    @staticmethod
    @require_authentication
    def resolve(_root, info, alert_id: UUID):
        gmp = get_gmp(info)

        xml = gmp.get_alert(str(alert_id), tasks=True)
        return xml.find('alert')


class GetAlerts(EntityConnectionField):
    """Get a list of alerts with pagination

    Example:

        query {
            alerts (filterString: "foo"){
                nodes {
                    name
                    id
                }
            }
        }

    Response:

        {
            "data": {
                "alerts": {
                    "nodes": [
                        {
                            "name": "foo",
                            "id": "08b69003-5fc2-4037-a479-93b440211c73"
                        },
                        {
                            "name": "bar",
                            "id": "6b2db524-9fb0-45b8-9b56-d958f84cb546"
                        }
                    ]
                }
            }
        }

    """

    entity_type = Alert

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

        xml: XmlElement = gmp.get_alerts(
            filter=filter_string.filter_string, tasks=True
        )

        alert_elements = xml.findall('alert')
        counts = xml.find('alert_count')
        requested = xml.find('alerts')

        return Entities(alert_elements, counts, requested)
