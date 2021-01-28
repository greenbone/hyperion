# -*- coding: utf-8 -*-
# Copyright (C) 2020 Greenbone Networks GmbH
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

from gvm.protocols.latest import (
    AliveTest as GvmAliveTest,
)

from selene.schema.base import BaseObjectType
from selene.schema.entity import EntityObjectType
from selene.schema.port_list.fields import PortList
from selene.schema.utils import (
    get_int_from_element,
    get_text_from_element,
    get_boolean_from_element,
)


class AliveTest(graphene.Enum):
    class Meta:
        enum = GvmAliveTest


class TargetCredential(BaseObjectType):
    pass


class TargetSSHCredential(TargetCredential):
    port = graphene.Int()

    def resolve_port(root, _info):
        return get_int_from_element(root, 'port')


class Target(EntityObjectType):
    """Target ObjectType"""

    hosts = graphene.List(graphene.String)
    exclude_hosts = graphene.List(graphene.String)
    max_hosts = graphene.Int()

    port_list = graphene.Field(PortList)
    ssh_credential = graphene.Field(TargetSSHCredential)
    smb_credential = graphene.Field(TargetCredential)
    esxi_credential = graphene.Field(TargetCredential)
    snmp_credential = graphene.Field(TargetCredential)

    alive_tests = graphene.String(description="Which alive test to use.")
    reverse_lookup_only = graphene.Boolean(
        description="Whether to scan only hosts that have names."
    )
    reverse_lookup_unify = graphene.Boolean(
        description=(
            "Whether to scan only one IP when "
            "multiple IPs have the same name."
        )
    )
    port_range = graphene.String()

    def resolve_hosts(root, _info):
        hosts = get_text_from_element(root, 'hosts')
        if hosts is None:
            return []
        return hosts.split(',')

    def resolve_exclude_hosts(root, _info):
        ehosts = get_text_from_element(root, 'exclude_hosts')
        if ehosts is None:
            return []
        return ehosts.split(',')

    def resolve_max_hosts(root, _info):
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

    def resolve_alive_tests(root, _info):
        return get_text_from_element(root, 'alive_tests')

    def resolve_reverse_lookup_only(root, _info):
        return get_boolean_from_element(root, "reverse_lookup_only")

    def resolve_reverse_lookup_unify(root, _info):
        return get_boolean_from_element(root, "reverse_lookup_unify")

    def resolve_port_range(root, _info):
        return get_text_from_element(root, "port_range")
