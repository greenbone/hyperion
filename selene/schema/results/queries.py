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

import graphene

from graphql import ResolveInfo

from selene.schema.parser import FilterString
from selene.schema.relay import (
    EntityConnectionField,
    Entities,
    get_filter_string_for_pagination,
)
from selene.schema.utils import (
    get_gmp,
    require_authentication,
    XmlElement,
)
from selene.schema.results.fields import Result


class GetResult(graphene.Field):
    """Gets a single report.

    Args:
        id (UUID): UUID of the result being queried

    Example:

        .. code-block::

            query {
                result (id: "e501545c-0c4d-47d9-a9f8-28da34c6b958") {
                    name
                    comment
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "result": {
                        "name": "Some Result",
                        "comment": "May the 4th",
                    }
                }
            }

    """

    def __init__(self):
        super().__init__(
            Result,
            result_id=graphene.UUID(required=True, name='id'),
            resolver=self.resolve,
        )

    @staticmethod
    @require_authentication
    def resolve(_root, info, result_id: UUID):
        gmp = get_gmp(info)

        xml = gmp.get_result(str(result_id))
        return xml.find('result')


class GetResults(EntityConnectionField):
    """Gets a list of reports with pagination

    Args:
        filter_string (str, optional): Optional filter string to be
            used with query.

    Example:

        .. code-block::

            query {
                results (filterString: "name~Result rows=4") {
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
                    "results": {
                        "nodes": [
                            {
                                "id": "1fb47870-47ce-4b9f-a8f9-8b4b19624c59",
                                "name": "Some Result"
                            },
                            {
                                "id": "5d07b6eb-27f9-424a-a206-34babbba7b4d",
                                "name": "Another Result"
                            },
                            {
                                "id": "3e2dab9d-8abe-4eb6-a3c7-5171738ac520",
                                "name": "More Result(s)"
                            }
                        ]
                    }
                }
            }

    """

    entity_type = Result

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

        xml: XmlElement = gmp.get_results(filter=filter_string.filter_string)

        result_elements = xml.findall('result')
        counts = xml.find('result_count')
        requested = xml.find('results')

        return Entities(result_elements, counts, requested)
