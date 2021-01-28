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

from selene.schema.vulnerabilities.fields import Vulnerability

from selene.schema.utils import (
    get_gmp,
    require_authentication,
    XmlElement,
)


class GetVulnerability(graphene.Field):
    """Gets a single vulnerability.

    Args:
        id (str): ID of the vulnerability being queried

    Example:

        .. code-block::

            query {
                vulnerability(id: "1.3.6.1.4.1.25623.1.0.814238"){
                    name
                    id
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "vulnerability": {
                        "name": "foo",
                        "id": "1.3.6.1.4.1.25623.1.0.814238"
                    }
                }
            }

    """

    def __init__(self):
        super().__init__(
            Vulnerability,
            vulnerability_id=graphene.String(required=True, name='id'),
            resolver=self.resolve,
        )

    @staticmethod
    @require_authentication
    def resolve(_root, info, vulnerability_id: UUID):
        gmp = get_gmp(info)

        xml = gmp.get_vulnerability(str(vulnerability_id))
        return xml.find('vuln')


class GetVulnerabilities(EntityConnectionField):
    """Gets a list of vulnerabilities with pagination

    Args:
        filter_string (str, optional): Optional filter string to be
            used with query.

    Example:

        .. code-block::

            query {
                vulnerabilities (filterString: "foo"){
                    nodes {
                        name
                        comment
                        id
                        value
                    }
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "vulnerabilities": {
                        "nodes": [
                            {
                                "name": "cat",
                                "id": "1.3.6.1.4.1.25623.1.0.814238",
                                "value": "goat",
                                "comment": "dog"
                            },
                            {
                                "name": "fooVulnerabilitie",
                                "id": "1.3.6.1.4.1.25623.1.0.814224",
                                "value": "bar",
                                "comment": "hello world"
                            }
                        ]
                    }
                }
            }

    """

    entity_type = Vulnerability

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

        xml: XmlElement = gmp.get_vulnerabilities(
            filter=filter_string.filter_string
        )

        vulnerability_elements = xml.findall('vuln')
        counts = xml.find('vuln_count')
        requested = xml.find('vulns')

        return Entities(vulnerability_elements, counts, requested)
