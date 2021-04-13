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

# pylint: disable=no-self-argument, no-member

import graphene

from gvm.protocols.next import (
    AliveTest as GvmAliveTest,
)

from selene.schema.base import BaseObjectType
from selene.schema.entity import EntityObjectType
from selene.schema.port_list.fields import PortList
from selene.schema.utils import (
    csv_to_list,
    get_int_from_element,
    get_text_from_element,
    get_boolean_from_element,
)


class AliveTest(graphene.Enum):
    class Meta:
        enum = GvmAliveTest


class TargetCredential(BaseObjectType):
    """ A Credential referenced by a Target via name and id """


class TargetSSHCredential(TargetCredential):
    port = graphene.Int(description="SSH Port to connect with the credential")

    def resolve_port(root, _info):
        return get_int_from_element(root, 'port')


class TargetTask(BaseObjectType):
    """ A Task referenced by a Target via name and id """


class Target(EntityObjectType):
    """Target ObjectType"""

    hosts = graphene.List(
        graphene.String,
        description="List of IPs, host names or address ranges to scan as a "
        "target",
    )
    exclude_hosts = graphene.List(
        graphene.String,
        description="List of IPs, host names or address ranges to exclude while"
        " scanning",
    )
    host_count = graphene.Int(
        description="Number of hosts to target for a scan"
    )

    port_list = graphene.Field(
        PortList, description="Port list to use for the target"
    )

    ssh_credential = graphene.Field(TargetSSHCredential)
    smb_credential = graphene.Field(TargetCredential)
    esxi_credential = graphene.Field(TargetCredential)
    snmp_credential = graphene.Field(TargetCredential)

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
    tasks = graphene.List(
        TargetTask,
        description="List of tasks that use the target",
    )

    def resolve_hosts(root, _info):
        hosts = get_text_from_element(root, 'hosts')
        return csv_to_list(hosts)

    def resolve_exclude_hosts(root, _info):
        exclude_hosts = get_text_from_element(root, 'exclude_hosts')
        return csv_to_list(exclude_hosts)

    def resolve_host_count(root, _info):
        return get_int_from_element(root, 'max_hosts')

    def resolve_port_list(root, _info):
        return root.find("port_list")

    def resolve_ssh_credential(root, _info):
        return root.find('ssh_credential')

    def resolve_smb_credential(root, _info):
        return root.find('smb_credential')

    def resolve_esxi_credential(root, _info):
        return root.find('esxi_credential')

    def resolve_snmp_credential(root, _info):
        return root.find('snmp_credential')

    def resolve_alive_test(root, _info):
        return get_text_from_element(root, 'alive_tests')

    def resolve_allow_simultaneous_ips(root, _info):
        return get_boolean_from_element(root, "allow_simultaneous_ips")

    def resolve_reverse_lookup_only(root, _info):
        return get_boolean_from_element(root, "reverse_lookup_only")

    def resolve_reverse_lookup_unify(root, _info):
        return get_boolean_from_element(root, "reverse_lookup_unify")

    def resolve_tasks(root, _info):
        tasks = root.find('tasks')
        if len(tasks) == 0:
            return None
        return tasks.findall('task')
