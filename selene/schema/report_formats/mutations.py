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

import graphene

from selene.schema.utils import get_gmp, require_authentication

from selene.schema.entities import (
    create_delete_by_ids_mutation,
    create_delete_by_filter_mutation,
)


class DeleteReportFormat(graphene.Mutation):
    """Deletes a reportFormat

    Args:
        id (UUID): UUID of Report Format to delete.

    Returns:
        ok (Boolean)
    """

    class Arguments:
        report_format_id = graphene.UUID(required=True, name='id')

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, report_format_id):
        gmp = get_gmp(info)
        gmp.delete_report_format(str(report_format_id))
        return DeleteReportFormat(ok=True)


class ImportReportFormat(graphene.Mutation):
    """Imports a XML-formatted report_format. Call with importReportFormat.

    Args:
        report_format (str)


    Returns:
        id (UUID)

    """

    class Arguments:
        report_format = graphene.String(required=True)

    report_format_id = graphene.UUID(name='id')

    @require_authentication
    def mutate(
        root,
        info,
        report_format: str,
    ):
        gmp = get_gmp(info)

        resp = gmp.import_report_format(
            report_format=report_format,
        )
        return ImportReportFormat(report_format_id=resp.get('id'))


class ModifyReportFormatInput(graphene.InputObjectType):
    """Input object for modifyReportFormat.

    Arguments:
        report_format_id: UUID of report format to modify.
        active (bool): Whether the report format is active.
        name (str): The name of the report format.
        summary (str): A summary of the report format.
        param_name (str): The name of the param.
        param_value (str): The value of the param.
    """

    report_format_id = graphene.UUID(
        name='id', required=True, description="UUID of report format to modify."
    )
    active = graphene.Boolean(
        description="Whether the report format is active."
    )
    name = graphene.String(description="The name of the report format.")
    summary = graphene.String(description="A summary of the report format.")
    param_name = graphene.String(description="The name of the param.")
    param_value = graphene.String(description="The value of the param.")


class ModifyReportFormat(graphene.Mutation):
    class Arguments:
        input_object = ModifyReportFormatInput(required=True, name='input')

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, input_object):
        gmp = get_gmp(info)

        gmp.modify_report_format(
            str(input_object.report_format_id),
            active=input_object.active,
            name=input_object.name,
            summary=input_object.summary,
            param_name=input_object.param_name,
            param_value=input_object.param_value,
        )

        return ModifyReportFormat(ok=True)


# Explicit classes needed, else we get error
# 'AssertionError: Found different types with the same name in the
#   schema: DeleteByIds, DeleteByIds.'


DeleteByIdsClass = create_delete_by_ids_mutation(entity_name='report_format')


class DeleteReportFormatsByIds(DeleteByIdsClass):
    """Deletes a list of report_formats

    Args:
        ids (List(UUID)): List of UUIDs of report_formats to delete.
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.

    Returns:
        ok (Boolean)

    Example

        mutation {
            deleteReportFormatsByIds(
                ids: ["5f8e7b31-35ea-4b43-9797-6d77f058906b"],
                ultimate: false)
            {
                ok
            }
        }

        Response
        {
            "data": {
                "deleteReportFormatsByIds": {
                    "ok": true
                }
            }
        }
    """


DeleteByFilterClass = create_delete_by_filter_mutation(
    entity_name='report_format'
)


class DeleteReportFormatsByFilter(DeleteByFilterClass):
    """Deletes a filtered list of report_formats

    Args:
        filterString (str): Filter string for report_format list to delete.
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.

    Returns:
        ok (Boolean)

    Example

        mutation {
            deleteReportFormatByFilter(
                filterString:"name~Clone",
                ultimate: false)
            {
                ok
            }
        }

        Response
        {
            "data": {
                "deleteReportFormatByFilter": {
                    "ok": true
                }
            }
        }
    """
