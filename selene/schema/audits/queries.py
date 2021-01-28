# -*- coding: utf-8 -*-
# Copyright (C) 2019 Greenbone Networks GmbH
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

from selene.schema.audits.fields import Audit

from selene.schema.utils import get_gmp, require_authentication, XmlElement


class GetAudit(graphene.Field):
    """Gets a single audit.

    Args:
        id (UUID): UUID of the audit being queried

    Example:

        .. code-block::

            query {
                audit (auditId: "f5c40267-71ab-4cd7-b14b-3599a84522e8") {
                    name
                    comment
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "audit": {
                        "name": "modified",
                        "comment": "To be or not to be",
                    }
                }
            }

    """

    def __init__(self):
        super().__init__(
            Audit,
            audit_id=graphene.UUID(required=True, name='id'),
            resolver=self.resolve,
        )

    @staticmethod
    @require_authentication
    def resolve(_root, info, audit_id: UUID):
        gmp = get_gmp(info)

        xml = gmp.get_audit(str(audit_id))
        return xml.find('task')


class GetAudits(EntityConnectionField):
    """Gets a list of audits with pagination

    Args:
        filter_string (str, optional): Optional filter string to be
            used with query.

    Example:

        .. code-block::

            query {
                audits (filterString: "name~TLS rows=4") {
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
                    "audits": {
                        "nodes": [
                            {
                                "id": "1fb47870-47ce-4b9f-a8f9-8b4b19624c59",
                                "name": "TLS"
                            },
                            {
                                "id": "5d07b6eb-27f9-424a-a206-34babbba7b4d",
                                "name": "TLS Clone 1"
                            },
                            {
                                "id": "3e2dab9d-8abe-4eb6-a3c7-5171738ac520",
                                "name": "TLS Clone 2"
                            },
                            {
                                "id": "49415287-32e7-4451-9424-df4e44bffc6c",
                                "name": "TLS Clone 3"
                            }
                        ]
                    }
                }
            }

    """

    entity_type = Audit

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

        xml: XmlElement = gmp.get_audits(
            filter=filter_string.filter_string, details=True
        )

        audit_elements = xml.findall('task')
        counts = xml.find('task_count')
        requested = xml.find('tasks')

        return Entities(audit_elements, counts, requested)
