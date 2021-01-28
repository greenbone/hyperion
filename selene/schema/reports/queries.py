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

from selene.schema.reports.fields import Report, ReportModel
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


class GetReport(graphene.Field):
    """Gets a single report.

    Args:
        id (UUID): UUID of the report being queried

    Example:

        .. code-block::

            query {
                report (
                    reportId: "e501545c-0c4d-47d9-a9f8-28da34c6b958"
                    reportFormatId: "e5dd545c-0c4d-47d9-a9f8-d8da34c6bdd8"
                ) {
                    name
                    comment
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "report": {
                        "name": "Some mighty Report",
                        "comment": "May the 4th",
                    }
                }
            }

    """

    def __init__(self):
        super().__init__(
            Report,
            report_id=graphene.UUID(required=True, name='id'),
            report_format_id=graphene.UUID(),
            delta_report_id=graphene.UUID(),
            resolver=self.resolve,
        )

    @staticmethod
    @require_authentication
    def resolve(
        _root,
        info,
        report_id: UUID,
        report_format_id: UUID = None,
        delta_report_id: UUID = None,
    ):
        gmp = get_gmp(info)
        report = ReportModel()
        xml: XmlElement = gmp.get_report(
            str(report_id),
            report_format_id=(
                str(report_format_id) if report_format_id is not None else None
            ),
            delta_report_id=(
                str(delta_report_id) if delta_report_id is not None else None
            ),
            details=True,
        )
        report.outer_report = xml.find('report')
        report.inner_report = report.outer_report.find('report')
        return report


class GetReports(EntityConnectionField):
    """Gets a list of reports with pagination

    Args:
        filter_string (str, optional): Optional filter string to be
            used with query.

    Example:

        .. code-block::

            query {
                reports (filterString: "name~Report rows=4") {
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
                    "reports": {
                        "nodes": [
                            {
                                "id": "1fb47870-47ce-4b9f-a8f9-8b4b19624c59",
                                "name": "Some Report"
                            },
                            {
                                "id": "5d07b6eb-27f9-424a-a206-34babbba7b4d",
                                "name": "Another Report"
                            },
                            {
                                "id": "3e2dab9d-8abe-4eb6-a3c7-5171738ac520",
                                "name": "More Report(s)"
                            }
                        ]
                    }
                }
            }

    """

    entity_type = Report

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

        xml: XmlElement = gmp.get_reports(filter=filter_string.filter_string)

        reports = []

        report_elements = xml.findall('report')
        for elem in report_elements:
            report = ReportModel()
            report.outer_report = elem
            report.inner_report = elem.find('report')
            reports.append(report)
        counts = xml.find('report_count')
        requested = xml.find('reports')

        return Entities(reports, counts, requested)
