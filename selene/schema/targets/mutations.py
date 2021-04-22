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

# pylint: disable=no-self-argument

import graphene

from selene.errors import InvalidRequest

from selene.schema.entities import (
    create_delete_by_ids_mutation,
    create_delete_by_filter_mutation,
    create_export_by_ids_mutation,
    create_export_by_filter_mutation,
)

from selene.schema.targets.fields import AliveTest

from selene.schema.utils import (
    require_authentication,
    get_gmp,
)


class SSHTargetCredentialInput(graphene.InputObjectType):
    ssh_id = graphene.UUID(
        name="id", description="UUID of a ssh credential to use on target"
    )
    port = graphene.Int(description="The port to use for ssh credential")


class TargetCredentialInput(graphene.InputObjectType):
    credential_id = graphene.UUID(
        name="id", description="UUID of a credential to use on target"
    )


class TargetCredentialsInput(graphene.InputObjectType):
    ssh = graphene.Field(
        SSHTargetCredentialInput,
        description="SSH credential to use on target",
    )
    smb = graphene.Field(
        TargetCredentialInput,
        description="SMB credential to use on target",
    )
    snmp = graphene.Field(
        TargetCredentialInput,
        description="SNMP credential to use on target",
    )
    esxi = graphene.Field(
        TargetCredentialInput,
        description="ESXi credential to use on target",
    )


class CreateTargetInput(graphene.InputObjectType):
    """Input object for createTarget"""

    name = graphene.String(required=True, description="Target name.")
    hosts = graphene.List(
        graphene.String,
        required=True,
        description="List of hosts to scan",
    )
    exclude_hosts = graphene.List(
        graphene.String, description="List of hosts to exclude from scan"
    )
    port_list_id = graphene.UUID(
        required=True, description="UUID of the port list to use on target"
    )
    comment = graphene.String(description="Comment for the target")
    credentials = graphene.Field(
        TargetCredentialsInput, description="Credentials to use for the target"
    )
    esxi_credential_id = graphene.UUID(
        description="UUID of a esxi credential to use on target"
    )
    alive_test = graphene.Field(
        AliveTest,
        description="Which alive test to use",
        required=True,
    )
    allow_simultaneous_ips = graphene.Boolean(
        name="allowSimultaneousIPs",
        description=(
            "Whether to scan multiple IPs of the same host simultaneously"
        ),
    )
    reverse_lookup_only = graphene.Boolean(
        description="Whether to scan only hosts that have names"
    )
    reverse_lookup_unify = graphene.Boolean(
        description=(
            "Whether to scan only one IP when "
            "multiple IPs have the same name"
        )
    )


class CreateTarget(graphene.Mutation):
    """Create a target"""

    class Arguments:
        input_object = CreateTargetInput(
            required=True,
            name='input',
            description='Input ObjectType for creating a new target',
        )

    target_id = graphene.UUID(name='id')

    @require_authentication
    def mutate(_root, info, input_object):
        name = input_object.name
        comment = input_object.comment

        alive_test = AliveTest.get(input_object.alive_test)

        hosts = input_object.hosts
        exclude_hosts = input_object.exclude_hosts

        if (
            input_object.credentials is not None
            and input_object.credentials.ssh is not None
        ):
            if (
                input_object.credentials.ssh.port
                and not input_object.credentials.ssh.ssh_id
            ):
                raise InvalidRequest(
                    "Setting a SSH credential port requires a SSH credential id"
                )

            ssh_credential_id = str(input_object.credentials.ssh.ssh_id)
            ssh_credential_port = input_object.credentials.ssh.port
        else:
            ssh_credential_id = None
            ssh_credential_port = None

        if (
            input_object.credentials is not None
            and input_object.credentials.smb is not None
        ):
            smb_credential_id = str(input_object.credentials.smb.credential_id)
        else:
            smb_credential_id = None

        if (
            input_object.credentials is not None
            and input_object.credentials.snmp is not None
        ):
            snmp_credential_id = str(
                input_object.credentials.snmp.credential_id
            )
        else:
            snmp_credential_id = None

        if (
            input_object.credentials is not None
            and input_object.credentials.esxi is not None
        ):
            esxi_credential_id = str(
                input_object.credentials.esxi.credential_id
            )
        else:
            esxi_credential_id = None

        allow_simultaneous_ips = input_object.allow_simultaneous_ips

        reverse_lookup_only = input_object.reverse_lookup_only

        reverse_lookup_unify = input_object.reverse_lookup_unify

        port_list_id = str(input_object.port_list_id)

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
        )

        return CreateTarget(target_id=resp.get('id'))


class ModifyTargetInput(graphene.InputObjectType):
    """Input object for modifyTarget"""

    target_id = graphene.UUID(
        required=True, description="ID of target to modify", name='id'
    )
    name = graphene.String(description="Target name")
    hosts = graphene.List(
        graphene.String,
        description="List of hosts to scan",
    )
    exclude_hosts = graphene.List(
        graphene.String, description="List of hosts to exclude from scan"
    )
    comment = graphene.String(description="Comment for the target")
    credentials = graphene.Field(
        TargetCredentialsInput,
        description="Credentials to set on the target",
    )
    alive_test = graphene.Field(
        AliveTest, description="Which alive test to use"
    )
    allow_simultaneous_ips = graphene.Boolean(
        name="allowSimultaneousIPs",
        description=(
            "Whether to scan multiple IPs of the same host simultaneously"
        ),
    )
    reverse_lookup_only = graphene.Boolean(
        description="Whether to scan only hosts that have names"
    )
    reverse_lookup_unify = graphene.Boolean(
        description=(
            "Whether to scan only one IP when "
            "multiple IPs have the same name"
        )
    )
    port_list_id = graphene.UUID(
        description="UUID of the port list to use on target"
    )


class ModifyTarget(graphene.Mutation):
    """Modify a target"""

    class Arguments:
        input_object = ModifyTargetInput(
            required=True,
            name='input',
            description='Input ObjectType to modify a target',
        )

    ok = graphene.Boolean()

    @require_authentication
    def mutate(_root, info, input_object):
        target_id = str(input_object.target_id)
        name = input_object.name
        comment = input_object.comment

        if input_object.alive_test is not None:
            alive_test = AliveTest.get(input_object.alive_test)
        else:
            alive_test = None

        if input_object.hosts is not None:
            hosts = input_object.hosts
        else:
            hosts = None

        if input_object.exclude_hosts:
            exclude_hosts = input_object.exclude_hosts
        else:
            exclude_hosts = None

        if (
            input_object.credentials is not None
            and input_object.credentials.ssh is not None
        ):
            if (
                input_object.credentials.ssh.port
                and not input_object.credentials.ssh.ssh_id
            ):
                raise InvalidRequest(
                    "Setting a SSH credential port requires a SSH credential id"
                )

            ssh_credential_id = str(input_object.credentials.ssh.ssh_id)
            ssh_credential_port = input_object.credentials.ssh.port
        else:
            ssh_credential_id = None
            ssh_credential_port = None

        if (
            input_object.credentials is not None
            and input_object.credentials.smb is not None
        ):
            smb_credential_id = str(input_object.credentials.smb.credential_id)
        else:
            smb_credential_id = None

        if (
            input_object.credentials is not None
            and input_object.credentials.snmp is not None
        ):
            snmp_credential_id = str(
                input_object.credentials.snmp.credential_id
            )
        else:
            snmp_credential_id = None

        if (
            input_object.credentials is not None
            and input_object.credentials.esxi is not None
        ):
            esxi_credential_id = str(
                input_object.credentials.esxi.credential_id
            )
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
    """Delete a target"""

    class Arguments:
        target_id = graphene.UUID(
            required=True,
            name='id',
            description='ID of the target to be deleted',
        )

    ok = graphene.Boolean()

    @require_authentication
    def mutate(_root, info, target_id):
        gmp = get_gmp(info)
        gmp.delete_target(str(target_id))
        return DeleteTarget(ok=True)


class CloneTarget(graphene.Mutation):
    """Clone a target"""

    class Arguments:
        target_id = graphene.UUID(
            required=True,
            name='id',
            description="ID of the target to be cloned",
        )

    target_id = graphene.UUID(name='id', description='UUID of the new target')

    @require_authentication
    def mutate(_root, info, target_id):
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
    """Delete a list of targets"""


DeleteByFilterClass = create_delete_by_filter_mutation(entity_name='target')


class DeleteTargetsByFilter(DeleteByFilterClass):
    """Delete a filtered list of targets

    Example

        mutation {
            deleteTargetsByFilter(filterString:"name~Clone") {
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
