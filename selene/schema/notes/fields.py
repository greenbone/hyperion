# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Greenbone Networks GmbH
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

from selene.schema.parser import parse_uuid
from selene.schema.severity import SeverityType

from selene.schema.resolver import find_resolver

from selene.schema.utils import (
    get_owner,
    get_boolean_from_element,
    get_datetime_from_element,
    get_text_from_element,
)

from selene.schema.nvts.fields import NVT
from selene.schema.permissions.fields import Permission
from selene.schema.results.queries import Result
from selene.schema.tasks.fields import Task


class Note(graphene.ObjectType):
    class Meta:
        default_resolver = find_resolver

    uuid = graphene.UUID(name='id')

    creation_time = graphene.DateTime()
    modification_time = graphene.DateTime()
    end_time = graphene.DateTime()

    writable = graphene.Boolean()
    in_use = graphene.Boolean()
    active = graphene.Boolean()
    orphan = graphene.Boolean()

    owner = graphene.String()
    text = graphene.String()
    hosts = graphene.List(graphene.String)
    port = graphene.String()
    severity = SeverityType()
    threat = graphene.String()

    permissions = graphene.List(Permission)
    nvt = graphene.Field(NVT)
    task = graphene.Field(Task)
    result = graphene.Field(Result)

    def resolve_uuid(root, _info):
        return parse_uuid(root.get('id'))

    def resolve_permissions(root, _info):
        permissions = root.find('permissions')
        if len(permissions) == 0:
            return None
        return permissions.findall('permission')

    def resolve_owner(root, _info):
        return get_owner(root)

    def resolve_creation_time(root, _info):
        return get_datetime_from_element(root, 'creation_time')

    def resolve_modification_time(root, _info):
        return get_datetime_from_element(root, 'modification_time')

    def resolve_end_time(root, _info):
        return get_datetime_from_element(root, 'end_time')

    def resolve_writable(root, _info):
        return get_boolean_from_element(root, 'writable')

    def resolve_in_use(root, _info):
        return get_boolean_from_element(root, 'in_use')

    def resolve_active(root, _info):
        return get_boolean_from_element(root, 'active')

    def resolve_orphan(root, _info):
        return get_boolean_from_element(root, 'orphan')

    def resolve_text(root, _info):
        return get_text_from_element(root, 'text')

    def resolve_hosts(root, _info):
        hosts = get_text_from_element(root, 'hosts')
        if hosts is None:
            return []
        return hosts.split(',')

    def resolve_port(root, _info):
        return get_text_from_element(root, 'port')

    def resolve_severity(root, _info):
        return get_text_from_element(root, 'severity')

    def resolve_threat(root, _info):
        return get_text_from_element(root, 'threat')
