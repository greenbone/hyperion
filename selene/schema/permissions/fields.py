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

import graphene

from gvm.protocols.next import (
    PermissionSubjectType as GvmPermissionSubjectType,
    EntityType as GvmEntityType,
)

from selene.schema.parser import parse_uuid

from selene.schema.entity import EntityObjectType, EntityPermission

from selene.schema.utils import get_boolean_from_element, get_text_from_element

# Needed for gmp command in CreatePermission mutation
class PermissionEntityType(graphene.Enum):
    class Meta:
        enum = GvmEntityType


# Needed for gmp command in CreatePermission mutation
class PermissionSubjectType(graphene.Enum):
    class Meta:
        enum = GvmPermissionSubjectType


class PermissionSubject(graphene.ObjectType):
    """The subject the permission applies to."""

    uuid = graphene.UUID(name='id')
    name = graphene.String()
    subject_type = graphene.String(name='type')
    trash = graphene.Boolean()

    @staticmethod
    def resolve_uuid(root, _info):
        return parse_uuid(root.get('id'))

    @staticmethod
    def resolve_name(root, _info):
        return get_text_from_element(root, 'name')

    @staticmethod
    def resolve_subject_type(root, _info):
        return get_text_from_element(root, 'type')

    @staticmethod
    def resolve_trash(root, _info):
        return get_boolean_from_element(root, 'trash')


class PermissionResource(graphene.ObjectType):
    """The resource the permission applies to."""

    uuid = graphene.UUID(name='id')
    name = graphene.String()
    permission_type = graphene.String(name='type')
    trash = graphene.Boolean()
    deleted = graphene.Boolean()
    permissions = graphene.List(EntityPermission)

    @staticmethod
    def resolve_uuid(root, _info):
        return parse_uuid(root.get('id'))

    @staticmethod
    def resolve_name(root, _info):
        return get_text_from_element(root, 'name')

    @staticmethod
    def resolve_permission_type(root, _info):
        return get_text_from_element(root, 'type')

    @staticmethod
    def resolve_trash(root, _info):
        return get_boolean_from_element(root, 'trash')

    @staticmethod
    def resolve_deleted(root, _info):
        return get_boolean_from_element(root, 'deleted')

    @staticmethod
    def resolve_permissions(root, _info):
        permissions = root.find('permissions')
        if permissions is None or permissions and len(permissions) == 0:
            return None
        return root.findall('permissions')


class Permission(EntityObjectType):
    resource = graphene.Field(PermissionResource)
    subject = graphene.Field(PermissionSubject)

    @staticmethod
    def resolve_resource(root, _info):
        return root.find('resource')

    @staticmethod
    def resolve_subject(root, _info):
        return root.find('subject')
