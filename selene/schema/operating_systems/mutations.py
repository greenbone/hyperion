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

import graphene

from gvm.protocols.next import AssetType as GvmAssetType

from selene.schema.utils import get_gmp, require_authentication
from selene.schema.entities import (
    create_delete_by_filter_mutation,
    create_delete_by_ids_mutation,
    create_export_by_ids_mutation,
    create_export_by_filter_mutation,
)


class DeleteOperatingSystem(graphene.Mutation):
    """Deletes a operating system

    Args:
        id (UUID): UUID of operating system to delete.

    Returns:
        ok (Boolean)
    """

    class Arguments:
        operating_system_id = graphene.UUID(required=True, name='id')

    ok = graphene.Boolean()

    @staticmethod
    @require_authentication
    def mutate(_root, info, operating_system_id):
        gmp = get_gmp(info)
        gmp.delete_asset(asset_id=str(operating_system_id))
        return DeleteOperatingSystem(ok=True)


class DeleteOperatingSystemsByReport(graphene.Mutation):
    """Deletes a list of  operating systems from a report
    Args:
        reportID (str): Report ID for operating systems list to delete.
    Returns:
        ok (Boolean)
    """

    class Arguments:
        report_id = graphene.String(
            required=True,
            description='report_id for asset list to delete.',
            name='id',
        )

    ok = graphene.Boolean()

    @staticmethod
    @require_authentication
    def mutate(_root, info, report_id):
        gmp = get_gmp(info)
        gmp.delete_asset(report_id=str(report_id))
        return DeleteOperatingSystemsByReport(ok=True)


#   schema: DeleteByIds, DeleteByIds.'

DeleteByIdsClass = create_delete_by_ids_mutation(
    entity_name='asset', asset_type=GvmAssetType.OPERATING_SYSTEM
)


class DeleteOperatingSystemsByIds(DeleteByIdsClass):
    """Deletes a list of operating_systems

    Args:
        ids (List(UUID)): List of UUIDs of operating_systems to delete.
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.

    Returns:
        ok (Boolean)

    Example

        mutation {
            deleteOperatingSystemsByIds(
                ids: ["5f8e7b31-35ea-4b43-9797-6d77f058906b"],
                ultimate: false)
            {
                ok
            }
        }

        Response
        {
            "data": {
                "deleteOperatingSystemsByIds": {
                    "ok": true
                }
            }
        }
    """


DeleteByFilterClass = create_delete_by_filter_mutation(
    entity_name='asset', asset_type=GvmAssetType.OPERATING_SYSTEM
)


class DeleteOperatingSystemsByFilter(DeleteByFilterClass):
    """Deletes a filtered list of operating_systems

    Args:
        filterString (str): Filter string for operating_system list to delete.
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.

    Returns:
        ok (Boolean)

    Example

        mutation {
            deleteOperatingSystemByFilter(
                filterString:"name~Clone",
                ultimate: false)
            {
                ok
            }
        }

        Response
        {
            "data": {
                "deleteOperatingSystemByFilter": {
                    "ok": true
                }
            }
        }
    """


# Explicit classes needed, else we get error
# 'AssertionError: Found different types with the same name in the
#   schema: ExportByIds, ExportByIds.'

ExportByIdsClass = create_export_by_ids_mutation(
    entity_name='asset', asset_type=GvmAssetType.OPERATING_SYSTEM
)


class ExportOperatingSystemsByIds(ExportByIdsClass):
    pass


ExportByFilterClass = create_export_by_filter_mutation(
    entity_name='asset', asset_type=GvmAssetType.OPERATING_SYSTEM
)


class ExportOperatingSystemsByFilter(ExportByFilterClass):
    pass


class ModifyOperatingSystemInput(graphene.InputObjectType):
    """Input object for modifyOperatingSystem.

    Args:
        id (UUID): UUID of the operating system to modify.
        comment (str, optional): The comment on the asset.
    """

    operating_system_id = graphene.UUID(
        required=True, description="UUID of asset to modify.", name='id'
    )
    comment = graphene.String(description="OperatingSystem comment.")


class ModifyOperatingSystem(graphene.Mutation):

    """Modifies an existing the operating system.
       Call with modifyOperatingSystem.

    Args:
        input (ModifyOperatingSystemInput): Input object for
                                            ModifyOperatingSystem

    Returns:
        ok (Boolean)
    """

    class Arguments:
        input_object = ModifyOperatingSystemInput(required=True, name='input')

    ok = graphene.Boolean()

    @staticmethod
    @require_authentication
    def mutate(_root, info, input_object):

        operating_system_id = str(input_object.operating_system_id)
        comment = input_object.comment

        gmp = get_gmp(info)

        gmp.modify_asset(operating_system_id, comment=comment)

        return ModifyOperatingSystem(ok=True)
