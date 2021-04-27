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

from selene.schema.utils import get_gmp, require_authentication

from selene.schema.entities import (
    create_delete_by_ids_mutation,
    create_delete_by_filter_mutation,
    create_export_by_ids_mutation,
    create_export_by_filter_mutation,
)

from selene.schema.severity import SeverityType


class CloneOverride(graphene.Mutation):
    """Clones an override

    Args:
        id (UUID): UUID of override to clone.

    Returns:
        ok (Boolean)
    """

    class Arguments:
        copy_id = graphene.UUID(
            required=True,
            name='id',
            description='UUID of the override to clone.',
        )

    override_id = graphene.UUID(name='id')

    @require_authentication
    def mutate(root, info, copy_id):
        gmp = get_gmp(info)
        resp = gmp.clone_override(str(copy_id))
        return CloneOverride(override_id=resp.get('id'))


class CreateOverrideInput(graphene.InputObjectType):
    """Input object for createOverride.

    Args:
        text (str): Text of the new override
        nvt_oid (str): The NVT of the override
        days_active (int): Days override will be active. -1 on always, 0 off
        hosts (str): A list of host addresses
        new_severity (float): Severity to which should be overridden
        port (str): Port to which the override applies
        result_id (UUID): ID of a result to which override applies
        severity (float): Severity to which override applies
        task_id (UUID): ID of a task to which override applies
    """

    text = graphene.String(
        required=True, description='Text of the new override'
    )
    nvt_oid = graphene.String(
        required=True, description='OID of the nvt to which override applies'
    )
    days_active = graphene.Int(
        description="Days override will be active. -1 on always, 0 off"
    )
    hosts = graphene.List(
        graphene.String, description="A list of host addresses"
    )
    new_severity = graphene.Field(
        SeverityType,
        required=True,
        description="Severity to which should be overridden",
    )
    port = graphene.String(description="Port to which the override applies")
    result_id = graphene.UUID(
        description="UUID of a result to which override applies"
    )
    severity = graphene.Float(description="Severity to which override applies")
    task_id = graphene.UUID(
        description="UUID of task to which override applies"
    )


class CreateOverride(graphene.Mutation):
    """Creates a new override. Call with createOverride.

    Args:
        input (CreateOverrideInput): Input object for CreateOverride
    """

    class Arguments:
        input_object = CreateOverrideInput(required=True, name='input')

    override_id = graphene.UUID(name='id')

    @require_authentication
    def mutate(root, info, input_object):
        text = input_object.text
        nvt_oid = input_object.nvt_oid
        days_active = input_object.days_active
        if input_object.hosts is not None:
            hosts = [str(host) for host in input_object.hosts]
        else:
            hosts = None
        new_severity = input_object.new_severity
        port = input_object.port
        result_id = (
            str(input_object.result_id)
            if input_object.result_id is not None
            else None
        )
        severity = input_object.severity
        task_id = (
            str(input_object.task_id)
            if input_object.task_id is not None
            else None
        )

        gmp = get_gmp(info)

        resp = gmp.create_override(
            text,
            nvt_oid,
            days_active=days_active,
            hosts=hosts,
            new_severity=new_severity,
            port=port,
            result_id=result_id,
            severity=severity,
            task_id=task_id,
        )

        return CreateOverride(override_id=resp.get('id'))


class ModifyOverrideInput(graphene.InputObjectType):
    """Input object for modifyOverride.

    Args:
        text (str): Text of the new override
        nvt (NVT): The NVT of the override
    """

    override_id = graphene.UUID(
        required=True, name='id', description='UUID of the override to modify'
    )
    text = graphene.String(description='Text of the override')
    days_active = graphene.Int(
        description="Days override will be active. -1 on always, 0 off"
    )
    hosts = graphene.List(
        graphene.String, description="A list of hosts addresses"
    )
    new_severity = graphene.Field(
        SeverityType,
        required=True,
        description="Severity to which should be overridden",
    )
    port = graphene.String(description="Port to which the override applies")
    result_id = graphene.UUID(
        description="UUID of a result to which override applies"
    )
    severity = graphene.Float(description="Severity to which override applies")
    task_id = graphene.UUID(
        description="UUID of task to which override applies"
    )


class ModifyOverride(graphene.Mutation):
    """Modifies an override. Call with modifyOverride.

    Args:
        input (ModifyOverrideInput): Input object for ModifyOverride
    """

    class Arguments:
        input_object = ModifyOverrideInput(required=True, name='input')

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, input_object):
        override_id = str(input_object.override_id)
        text = input_object.text
        days_active = input_object.days_active
        if input_object.hosts is not None:
            hosts = [str(host) for host in input_object.hosts]
        else:
            hosts = None
        new_severity = input_object.new_severity
        port = input_object.port
        result_id = (
            str(input_object.result_id)
            if input_object.result_id is not None
            else None
        )
        severity = input_object.severity
        task_id = (
            str(input_object.task_id)
            if input_object.task_id is not None
            else None
        )

        gmp = get_gmp(info)

        gmp.modify_override(
            override_id,
            text,
            days_active=days_active,
            hosts=hosts,
            new_severity=new_severity,
            port=port,
            result_id=result_id,
            severity=severity,
            task_id=task_id,
        )

        return ModifyOverride(ok=True)


class DeleteOverride(graphene.Mutation):
    """Deletes an override

    Args:
        id (UUID): UUID of override to delete.
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.

    Returns:
        ok (Boolean)
    """

    class Arguments:
        override_id = graphene.UUID(required=True, name='id')
        ultimate = graphene.Boolean(name='ultimate')

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, override_id, ultimate):
        gmp = get_gmp(info)
        gmp.delete_override(str(override_id), ultimate=ultimate)
        return DeleteOverride(ok=True)


# Explicit classes needed, else we get error
# 'AssertionError: Found different types with the same name in the
#   schema: ExportByIds, ExportByIds.'

ExportByIdsClass = create_export_by_ids_mutation(
    entity_name='override', with_details=True
)


class ExportOverridesByIds(ExportByIdsClass):
    pass


ExportByFilterClass = create_export_by_filter_mutation(
    entity_name='override', with_details=True
)


class ExportOverridesByFilter(ExportByFilterClass):
    pass


#   schema: DeleteByIds, DeleteByIds.'


DeleteByIdsClass = create_delete_by_ids_mutation(entity_name='override')


class DeleteOverridesByIds(DeleteByIdsClass):
    """Deletes a list of overrides

    Args:
        ids (List(UUID)): List of UUIDs of overrides to delete.
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.

    Returns:
        ok (Boolean)

    Example

        mutation {
            deleteOverridesByIds(
                ids: ["5f8e7b31-35ea-4b43-9797-6d77f058906b"],
                ultimate: false)
            {
                ok
            }
        }

        Response
        {
            "data": {
                "deleteOverridesByIds": {
                    "ok": true
                }
            }
        }
    """


DeleteByFilterClass = create_delete_by_filter_mutation(entity_name='override')


class DeleteOverridesByFilter(DeleteByFilterClass):
    """Deletes a filtered list of overrides

    Args:
        filterString (str): Filter string for override list to delete.
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.

    Returns:
        ok (Boolean)

    Example

        mutation {
            deleteOverridesByFilter(
                filterString:"name~Clone",
                ultimate: false)
            {
                ok
            }
        }

        Response
        {
            "data": {
                "deleteOverridesByFilter": {
                    "ok": true
                }
            }
        }
    """
