# -*- coding: utf-8 -*-
# Copyright (C) 2019-2021 Greenbone Networks GmbH
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

from selene.schema.utils import get_gmp, require_authentication, XmlElement
from selene.schema.report_formats.fields import ReportFormat
from selene.schema.relay import (
    EntityConnectionField,
    Entities,
    FilterString,
    get_filter_string_for_pagination,
)


class GetReportFormat(graphene.Field):
    """Gets a single report format.

    Args:
        id (UUID): UUID of the report format being queried

    Example:

        .. code-block::

            query {
                report_format(id: "e9b98e26-9fff-4ee8-9378-bc44fe3d6f2b"){
                    id
                    name
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "reportFormat": {
                        "name": "foo",
                        "id": "e9b98e26-9fff-4ee8-9378-bc44fe3d6f2b"
                    }
                }
            }

    """

    def __init__(self):
        super().__init__(
            ReportFormat,
            report_format_id=graphene.UUID(required=True, name='id'),
            resolver=self.resolve,
        )

    @staticmethod
    @require_authentication
    def resolve(_root, info, report_format_id: UUID):
        gmp = get_gmp(info)

        xml = gmp.get_report_format(str(report_format_id))
        return xml.find('report_format')


class GetReportFormats(EntityConnectionField):

    entity_type = ReportFormat

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

        xml: XmlElement = gmp.get_report_formats(
            filter_string=filter_string.filter_string
        )

        report_format_elements = xml.findall('report_format')
        counts = xml.find('report_format_count')
        requested = xml.find('report_formats')

        return Entities(report_format_elements, counts, requested)
