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

# pylint: disable=no-self-argument

import graphene

from gvm.protocols.latest import AssetType as GvmAssetType

from selene.schema.entities import (
    create_delete_by_ids_mutation,
    create_delete_by_filter_mutation,
    create_export_by_ids_mutation,
    create_export_by_filter_mutation,
)
from selene.schema.utils import get_gmp, require_authentication


class CreateHostInput(graphene.InputObjectType):
    """Input object for createHost.

    Args:
        name (str): Name of the host.
            Must be an IPv4 or IPv6 address as string.
        comment (str, optional): Comment for the host.
    """

    name = graphene.String(
        required=True,
        description=(
            "Name of the host. Must be an IPv4 or IPv6 address as string."
        ),
    )
    comment = graphene.String(description="Comment for the host.")


class CreateHost(graphene.Mutation):
    class Arguments:
        input_object = CreateHostInput(required=True, name='input')

    host_id = graphene.UUID(name='id')

    @require_authentication
    def mutate(root, info, input_object):
        gmp = get_gmp(info)

        resp = gmp.create_host(
            input_object.name,
            comment=input_object.comment,
        )

        return CreateHost(host_id=resp.get('id'))


class DeleteHost(graphene.Mutation):
    """Deletes a host

    Args:
        id (UUID): UUID of host to delete.

    Returns:
        ok (Boolean)
    """

    class Arguments:
        host_id = graphene.UUID(required=True, name='id')

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, host_id):
        gmp = get_gmp(info)
        gmp.delete_asset(asset_id=str(host_id))
        return DeleteHost(ok=True)


class DeleteHostsByReport(graphene.Mutation):
    """Deletes a list of hosts from a report
    Args:
        reportID (str): Report ID for host list to delete.
    Returns:
        ok (Boolean)
    """

    class Arguments:
        report_id = graphene.String(
            required=True,
            description='report_id for host list to delete.',
            name='id',
        )

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, report_id):
        gmp = get_gmp(info)
        gmp.delete_asset(report_id=str(report_id))
        return DeleteHostsByReport(ok=True)


#   schema: DeleteByIds, DeleteByIds.'

DeleteByIdsClass = create_delete_by_ids_mutation(
    entity_name='asset', asset_type=GvmAssetType.HOST
)


class DeleteHostsByIds(DeleteByIdsClass):
    """Deletes a list of hosts

    Args:
        ids (List(UUID)): List of UUIDs of host to delete.
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.

    Returns:
        ok (Boolean)

    Example

        mutation {
            deleteHostsByIds(
                ids: ["5f8e7b31-35ea-4b43-9797-6d77f058906b"],
                ultimate: false)
            {
                ok
            }
        }

        Response
        {
            "data": {
                "deleteHostsByIds": {
                    "ok": true
                }
            }
        }
    """


DeleteByFilterClass = create_delete_by_filter_mutation(
    entity_name='asset', asset_type=GvmAssetType.HOST
)


class DeleteHostsByFilter(DeleteByFilterClass):
    """Deletes a filtered list of host

    Args:
        filterString (str): Filter string for host list to delete.
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.

    Returns:
        ok (Boolean)

    Example

        mutation {
            deleteHostByFilter(
                filterString:"name~Clone",
                ultimate: false)
            {
                ok
            }
        }

        Response
        {
            "data": {
                "deleteHostByFilter": {
                    "ok": true
                }
            }
        }
    """


# Explicit classes needed, else we get error
# 'AssertionError: Found different types with the same name in the
#   schema: ExportByIds, ExportByIds.'

ExportByIdsClass = create_export_by_ids_mutation(
    entity_name='asset', asset_type=GvmAssetType.HOST
)


class ExportHostsByIds(ExportByIdsClass):
    pass


ExportByFilterClass = create_export_by_filter_mutation(
    entity_name='asset', asset_type=GvmAssetType.HOST
)


class ExportHostsByFilter(ExportByFilterClass):
    pass


class ModifyHostInput(graphene.InputObjectType):
    """Input object for modifyHost.

    Args:
        id (UUID): UUID of host to modify.
        comment (str, optional): The comment on the host.
    """

    host_id = graphene.UUID(
        required=True, description="UUID of host to modify.", name='id'
    )
    comment = graphene.String(description="Host comment.")


class ModifyHost(graphene.Mutation):

    """Modifies an existing host. Call with modifyHost.

    Args:
        input (ModifyHostInput): Input object for ModifyHost

    Returns:
        ok (Boolean)
    """

    class Arguments:
        input_object = ModifyHostInput(required=True, name='input')

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, input_object):

        host_id = str(input_object.host_id)
        comment = input_object.comment

        gmp = get_gmp(info)

        gmp.modify_asset(
            host_id,
            comment=comment,
        )

        return ModifyHost(ok=True)
