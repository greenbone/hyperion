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

# pylint: disable=no-self-argument, no-member

from uuid import UUID

import graphene

from selene.schema.entities import (
    create_export_by_filter_mutation,
    create_export_by_ids_mutation,
    create_delete_by_ids_mutation,
    create_delete_by_filter_mutation,
)
from selene.schema.utils import (
    get_gmp,
    require_authentication,
)


class DeleteReport(graphene.Mutation):
    """Deletes a report

    Args:
        id (UUID): UUID of task to delete.

    Returns:
        ok (Boolean)
    """

    class Arguments:
        report_id = graphene.String(required=True, name='id')

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, report_id):
        gmp = get_gmp(info)
        gmp.delete_report(report_id)
        return DeleteReport(ok=True)


# Explicit classes needed, else we get error
# 'AssertionError: Found different types with the same name in the
#   schema: DeleteByIds, DeleteByIds.'

DeleteByIdsClass = create_delete_by_ids_mutation(entity_name='report')


class DeleteReportsByIds(DeleteByIdsClass):
    """Deletes a list of reports

    Args:
        ids (List(UUID)): List of UUIDs of reports to delete.

    Returns:
        ok (Boolean)
    """


DeleteByFilterClass = create_delete_by_filter_mutation(entity_name='report')


class DeleteReportsByFilter(DeleteByFilterClass):
    """Deletes a filtered list of reports
    Args:
        filterString (str): Filter string for report list to delete.
    Returns:
        ok (Boolean)
    """


class ImportReport(graphene.Mutation):
    """Imports a XML-formatted report. Call with importReport.

    Args:
        report (str)
        task_id (str)
        task_name (str)
        task_comment (str)
        in_assets (Boolean)

    Returns:
        id (UUID)

    """

    class Arguments:
        report = graphene.String(required=True)

        task_id = graphene.UUID()
        task_name = graphene.String()
        task_comment = graphene.String()
        in_assets = graphene.String()

    report_id = graphene.UUID(name='id')

    @require_authentication
    def mutate(
        root,
        info,
        report: str,
        task_id: str = UUID,
        task_name: str = None,
        task_comment: str = None,
        in_assets: bool = None,
    ):
        gmp = get_gmp(info)

        resp = gmp.import_report(
            report,
            task_id=str(task_id),
            task_name=str(task_name),
            task_comment=str(task_comment),
            in_assets=in_assets,
        )
        return ImportReport(report_id=resp.get('id'))


# Explicit classes needed, else we get error
# 'AssertionError: Found different types with the same name in the
#   schema: ExportByIds, ExportByIds.'

ExportByIdsClass = create_export_by_ids_mutation(
    entity_name='report', with_details=True
)


class ExportReportsByIds(ExportByIdsClass):
    pass


ExportByFilterClass = create_export_by_filter_mutation(
    entity_name='report', with_details=True
)


class ExportReportsByFilter(ExportByFilterClass):
    pass
