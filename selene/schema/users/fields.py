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

import string

import graphene

from selene.schema.entity import EntityObjectType, EntityPermission
from selene.schema.base import BaseObjectType
from selene.schema.roles.fields import BaseRoleType

from selene.schema.utils import get_text_from_element


class UserRole(BaseRoleType):
    """The role of the user."""

    permissions = graphene.List(EntityPermission)

    @staticmethod
    def resolve_permissions(root, _info):
        permissions = root.find('permissions')
        if permissions is None:
            return None
        return permissions.findall("permission")


class UserGroup(BaseObjectType):
    permissions = graphene.List(EntityPermission)

    @staticmethod
    def resolve_permissions(root, _info):
        permissions = root.find('permissions')
        if permissions is None:
            return None
        return permissions.findall("permission")


class User(EntityObjectType):
    roles = graphene.List(UserRole, description="The roles of the user.")
    group_list = graphene.List(
        UserGroup, name="groups", description="The groups the user belongs to."
    )
    host_list = graphene.List(graphene.String)
    hosts_allow = graphene.Boolean(
        description='If True, allow only listed, otherwise forbid listed.'
    )
    iface_list = graphene.List(graphene.String)
    ifaces_allow = graphene.Boolean(
        description='If True, allow only listed, otherwise forbid listed.'
    )
    sources = graphene.List(
        graphene.String,
        description="Sources allowed for" "authentication for this user.",
    )

    @staticmethod
    def resolve_roles(root, _info):
        roles = root.findall('role')
        if not roles or roles is None:
            return None
        return roles

    @staticmethod
    def resolve_group_list(root, _info):
        groups = root.find("groups")
        if groups is None:
            return None
        return groups.findall("group")

    @staticmethod
    def resolve_host_list(root, _info):
        hosts_string = get_text_from_element(root, 'hosts')
        if not hosts_string:
            return None
        hosts_string = hosts_string.translate(
            str.maketrans('', '', string.whitespace)
        )
        return hosts_string.split(',')

    @staticmethod
    def resolve_hosts_allow(root, _info):
        hosts = root.find("hosts")
        return bool(int(hosts.get("allow")))

    @staticmethod
    def resolve_iface_list(root, _info):
        ifaces_string = get_text_from_element(root, 'ifaces')
        if not ifaces_string:
            return None
        ifaces_string = ifaces_string.translate(
            str.maketrans('', '', string.whitespace)
        )
        return ifaces_string.split(',')

    @staticmethod
    def resolve_ifaces_allow(root, _info):
        ifaces = root.find("ifaces")
        return bool(int(ifaces.get("allow")))

    @staticmethod
    def resolve_sources(root, _info):
        sources_list_xml = root.find('sources').findall('source')
        sources_list = []
        for source in sources_list_xml:
            sources_list.append(source.text)
        return sources_list
