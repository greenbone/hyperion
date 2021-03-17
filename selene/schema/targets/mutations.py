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

import graphene

from graphql import GraphQLError

from gvm.protocols.next import get_alive_test_from_string

from selene.schema.entities import (
    create_delete_by_ids_mutation,
    create_delete_by_filter_mutation,
    create_export_by_ids_mutation,
    create_export_by_filter_mutation,
)

from selene.schema.utils import (
    require_authentication,
    get_gmp,
)


class CreateTargetInput(graphene.InputObjectType):
    """Input object for createTarget

    Args:
        name (str): Name of the target.
        hosts (str, optional): String of comma-separated host addresses to scan
        exclude_hosts (str, optional): String of comma-separated hosts addresses
            to exclude from scan.
        comment (str, optional): Comment for the target.
        ssh_credential_id (UUID, optional): UUID of a ssh credential
            to use on target.
        ssh_credential_port(int, optional): The port to use for ssh credential.
        smb_credential_id (UUID, optional): UUID of a smb credential to use on
            target.
        snmp_credential_id (UUID, optional): UUID of a snmp credential to use
            on target.
        esxi_credential_id (UUID, optional): UUID of a esxi credential to use
            on target.
        alive_test (str, optional): Which alive test to use.
        allow_simultaneous_ips (bool, optional): Whether to scan multiple
            IPs of the same host simultaneously.
        reverse_lookup_only (bool, optional): Whether to scan only hosts that
            have names.
        reverse_lookup_unify (bool, optional): Whether to scan only one IP
            when multiple IPs have the same name.
        port_list_id (UUID): UUID of the port list to use on target.
        port_range (str, optional): Comma separated list of port ranges for the
            target (allowing whitespace)
        hosts_filter (str, optional): Filter to select target host from
            assets hosts
    """

    name = graphene.String(required=True, description="Target name.")
    hosts = graphene.String(
        description="String of comma-separated hosts addresses to scan."
    )
    exclude_hosts = graphene.String(
        description=(
            "String of comma-separated hosts addresses to exclude from scan."
        )
    )
    comment = graphene.String(description="Comment for the target.")
    ssh_credential_id = graphene.UUID(
        description="UUID of a ssh credential to use on target."
    )
    ssh_credential_port = graphene.Int(
        description="The port to use for ssh credential."
    )
    smb_credential_id = graphene.UUID(
        description="UUID of a smb credential to use on target."
    )
    snmp_credential_id = graphene.UUID(
        description="UUID of a snmp credential to use on target."
    )
    esxi_credential_id = graphene.UUID(
        description="UUID of a esxi credential to use on target."
    )
    alive_test = graphene.String(description="Which alive test to use.")
    allow_simultaneous_ips = graphene.Boolean(
        name="allowSimultaneousIPs",
        description=(
            "Whether to scan multiple IPs of the same host simultaneously."
        ),
    )
    reverse_lookup_only = graphene.Boolean(
        description="Whether to scan only hosts that have names."
    )
    reverse_lookup_unify = graphene.Boolean(
        description=(
            "Whether to scan only one IP when "
            "multiple IPs have the same name."
        )
    )
    port_list_id = graphene.UUID(
        description="UUID of the port list to use on target."
    )
    port_range = graphene.String(
        description=(
            "Comma separated list of port ranges for "
            "the target (allowing whitespace)"
        )
    )
    hosts_filter = graphene.String(
        description="Filter to select target host from assets hosts."
    )


class CreateTarget(graphene.Mutation):
    """Creates a target

    Args:
        input (CreateTargetInput): Input object for CreateTarget.
    """

    class Arguments:
        input_object = CreateTargetInput(required=True, name='input')

    target_id = graphene.UUID(name='id')

    @require_authentication
    def mutate(root, info, input_object):
        name = input_object.name
        comment = input_object.comment

        if (
            input_object.alive_test is not None
            and input_object.alive_test.lower() != 'scan config default'
        ):
            # must be lower case to work; gsa sends lower case
            alive_test = get_alive_test_from_string(input_object.alive_test)
        else:
            alive_test = None

        if input_object.hosts is not None:
            hosts = [host.strip() for host in input_object.hosts.split(',')]
        else:
            hosts = None

        if input_object.exclude_hosts is not None:
            exclude_hosts = [
                host.strip() for host in input_object.exclude_hosts.split(',')
            ]
        else:
            exclude_hosts = None

        if input_object.ssh_credential_id is not None:
            ssh_credential_id = str(input_object.ssh_credential_id)
            ssh_credential_port = input_object.ssh_credential_port
        else:
            ssh_credential_id = None
            ssh_credential_port = None

        if input_object.smb_credential_id is not None:
            smb_credential_id = str(input_object.smb_credential_id)
        else:
            smb_credential_id = None

        if input_object.snmp_credential_id is not None:
            snmp_credential_id = str(input_object.snmp_credential_id)
        else:
            snmp_credential_id = None

        if input_object.esxi_credential_id is not None:
            esxi_credential_id = str(input_object.esxi_credential_id)
        else:
            esxi_credential_id = None

        allow_simultaneous_ips = input_object.allow_simultaneous_ips

        reverse_lookup_only = input_object.reverse_lookup_only

        reverse_lookup_unify = input_object.reverse_lookup_unify

        if (
            input_object.port_list_id is None
            and input_object.port_range is None
        ):
            raise GraphQLError(
                "PortListID or PortRange field required."
            ) from None

        if input_object.port_list_id is not None:
            port_list_id = str(input_object.port_list_id)
        else:
            port_list_id = None

        asset_hosts_filter = input_object.hosts_filter

        gmp = get_gmp(info)

        resp = gmp.create_target(
            name,
            alive_test=alive_test,
            hosts=hosts,
            exclude_hosts=exclude_hosts,
            comment=comment,
            ssh_credential_id=ssh_credential_id,
            ssh_credential_port=ssh_credential_port,
            smb_credential_id=smb_credential_id,
            snmp_credential_id=snmp_credential_id,
            esxi_credential_id=esxi_credential_id,
            allow_simultaneous_ips=allow_simultaneous_ips,
            reverse_lookup_only=reverse_lookup_only,
            reverse_lookup_unify=reverse_lookup_unify,
            port_list_id=port_list_id,
            port_range=input_object.port_range,
            asset_hosts_filter=asset_hosts_filter,
        )

        return CreateTarget(target_id=resp.get('id'))


class ModifyTargetInput(graphene.InputObjectType):
    """Input object for modifyTarget

    Args:
        id (UUID) – ID of target to modify.
        name (str, optional): Name of the target.
        hosts (str, optional): String of comma-separated
            hosts addresses to scan.
        exclude_hosts (str, optional): String of comma-separated
            of hosts addresses to exclude from scan.
        comment (str, optional): Comment for the target.
        ssh_credential_id (UUID, optional): UUID of a ssh credential
            to use on target.
        ssh_credential_port(int, optional): The port to use for ssh credential.
        smb_credential_id (UUID, optional): UUID of a smb credential to use on
            target.
        snmp_credential_id (UUID, optional): UUID of a snmp credential to use
            on target.
        esxi_credential_id (UUID, optional): UUID of a esxi credential to use
            on target.
        alive_test (str, optional): Which alive test to use.
        allow_simultaneous_ips (bool, optional): Whether to scan multiple
            IPs of the same host simultaneously.
        reverse_lookup_only (bool, optional): Whether to scan only hosts that
            have names.
        reverse_lookup_unify (bool, optional): Whether to scan only one IP
            when multiple IPs have the same name.
        port_list_id (UUID, optional): UUID of the port list to use on target.
        port_range (str, optional): Comma separated list of port ranges for the
            target (allowing whitespace)
    """

    target_id = graphene.UUID(
        required=True, description="ID of target to modify.", name='id'
    )
    name = graphene.String(description="Target name.")
    hosts = graphene.String(
        description="String of comma-separated hosts addresses to scan."
    )
    exclude_hosts = graphene.String(
        description=(
            "String of comma-separated hosts " "addresses to exclude from scan."
        )
    )
    comment = graphene.String(description="Comment for the target.")
    ssh_credential_id = graphene.UUID(
        description="UUID of a ssh credential to use on target."
    )
    ssh_credential_port = graphene.Int(
        description="The port to use for ssh credential."
    )
    smb_credential_id = graphene.UUID(
        description="UUID of a smb credential to use on target."
    )
    snmp_credential_id = graphene.UUID(
        description="UUID of a snmp credential to use on target."
    )
    esxi_credential_id = graphene.UUID(
        description="UUID of a esxi credential to use on target."
    )
    alive_test = graphene.String(description="Which alive test to use.")
    allow_simultaneous_ips = graphene.Boolean(
        description=(
            "Whether to scan multiple IPs of the same host simultaneously."
        )
    )
    reverse_lookup_only = graphene.Boolean(
        description="Whether to scan only hosts that have names."
    )
    reverse_lookup_unify = graphene.Boolean(
        description=(
            "Whether to scan only one IP when "
            "multiple IPs have the same name."
        )
    )
    port_list_id = graphene.UUID(
        description="UUID of the port list to use on target."
    )


class ModifyTarget(graphene.Mutation):
    """Modifies a target

    Args:
        input (ModifyTargetInput): Input object for ModifyTarget.
    """

    class Arguments:
        input_object = ModifyTargetInput(required=True, name='input')

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, input_object):
        target_id = str(input_object.target_id)
        name = input_object.name
        comment = input_object.comment

        if (
            input_object.alive_test is not None
            and input_object.alive_test.lower() != 'scan config default'
        ):
            alive_test = get_alive_test_from_string(input_object.alive_test)
        else:
            alive_test = None

        if input_object.hosts is not None:
            hosts = [host.strip() for host in input_object.hosts.split(',')]
        else:
            hosts = None

        if input_object.exclude_hosts is not None:
            exclude_hosts = [
                host.strip() for host in input_object.exclude_hosts.split(',')
            ]
        else:
            exclude_hosts = None

        if input_object.ssh_credential_id is not None:
            ssh_credential_id = str(input_object.ssh_credential_id)
            ssh_credential_port = input_object.ssh_credential_port
        else:
            ssh_credential_id = None
            ssh_credential_port = None

        if input_object.smb_credential_id is not None:
            smb_credential_id = str(input_object.smb_credential_id)
        else:
            smb_credential_id = None

        if input_object.snmp_credential_id is not None:
            snmp_credential_id = str(input_object.snmp_credential_id)
        else:
            snmp_credential_id = None

        if input_object.esxi_credential_id is not None:
            esxi_credential_id = str(input_object.esxi_credential_id)
        else:
            esxi_credential_id = None

        if input_object.port_list_id is not None:
            port_list_id = str(input_object.port_list_id)
        else:
            port_list_id = None

        allow_simultaneous_ips = input_object.allow_simultaneous_ips

        reverse_lookup_only = input_object.reverse_lookup_only

        reverse_lookup_unify = input_object.reverse_lookup_unify

        gmp = get_gmp(info)

        gmp.modify_target(
            target_id,
            name=name,
            alive_test=alive_test,
            hosts=hosts,
            exclude_hosts=exclude_hosts,
            comment=comment,
            ssh_credential_id=ssh_credential_id,
            ssh_credential_port=ssh_credential_port,
            smb_credential_id=smb_credential_id,
            snmp_credential_id=snmp_credential_id,
            esxi_credential_id=esxi_credential_id,
            allow_simultaneous_ips=allow_simultaneous_ips,
            reverse_lookup_only=reverse_lookup_only,
            reverse_lookup_unify=reverse_lookup_unify,
            port_list_id=port_list_id,
        )

        return ModifyTarget(ok=True)


class DeleteTarget(graphene.Mutation):
    """Deletes a target

    Args:
        id (UUID): UUID of target to delete.

    Returns:
        ok (Boolean)
    """

    class Arguments:
        target_id = graphene.UUID(required=True, name='id')
        ultimate = graphene.Boolean(name='ultimate')

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, target_id, ultimate):
        gmp = get_gmp(info)
        gmp.delete_target(str(target_id), ultimate=ultimate)
        return DeleteTarget(ok=True)


class CloneTarget(graphene.Mutation):
    """Clone a target

    Args:
        id (UUID): UUID of target to clone.

    Example:

        .. code-block::

            mutation {
                cloneTarget(
                    id: "b992601e-e0df-4078-b4b1-39e04f92f4cc",
                ) {
                    id
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "cloneTarget": {
                    "id": "a569f3df-0f8d-4001-aeef-08cdee0cdf49"
                    }
                }
            }
    """

    class Arguments:
        target_id = graphene.UUID(required=True, name='id')

    # it is really awkward to reuse the same variable
    # name here, but it seems working ...?!
    target_id = graphene.UUID(name='id')

    @require_authentication
    def mutate(root, info, target_id):
        gmp = get_gmp(info)
        elem = gmp.clone_target(str(target_id))
        return CloneTarget(target_id=elem.get('id'))


# Explicit classes needed, else we get error
# 'AssertionError: Found different types with the same name in the
#   schema: ExportByIds, ExportByIds.'

ExportByIdsClass = create_export_by_ids_mutation(entity_name='target')


class ExportTargetsByIds(ExportByIdsClass):
    pass


ExportByFilterClass = create_export_by_filter_mutation(entity_name='target')


class ExportTargetsByFilter(ExportByFilterClass):
    pass


#   schema: DeleteByIds, DeleteByIds.'


DeleteByIdsClass = create_delete_by_ids_mutation(entity_name='target')


class DeleteTargetsByIds(DeleteByIdsClass):
    """Deletes a list of targets

    Args:
        ids (List(UUID)): List of UUIDs of targets to delete.
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.

    Returns:
        ok (Boolean)

    Example

        mutation {
            deleteTargetsByIds(
                ids: ["5f8e7b31-35ea-4b43-9797-6d77f058906b"],
                ultimate: false)
            {
                ok
            }
        }

        Response
        {
            "data": {
                "deleteTargetByIds": {
                    "ok": true
                }
            }
        }
    """


DeleteByFilterClass = create_delete_by_filter_mutation(entity_name='target')


class DeleteTargetsByFilter(DeleteByFilterClass):
    """Deletes a filtered list of targets

    Args:
        filterString (str): Filter string for target list to delete.
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.

    Returns:
        ok (Boolean)

    Example

        mutation {
            deleteTargetsByFilter(
                filterString:"name~Clone",
                ultimate: false)
            {
                ok
            }
        }

        Response
        {
            "data": {
                "deleteTargetByFilter": {
                    "ok": true
                }
            }
        }
    """
