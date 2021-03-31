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

from selene.schema.base import BaseObjectType, NameObjectTypeMixin

from selene.schema.utils import (
    get_owner,
    get_boolean_from_element,
    get_datetime_from_element,
    get_int_from_element,
    get_text_from_element,
)

from selene.schema.tags.fields import Tag


class EntityUserTags(graphene.ObjectType):
    count = graphene.Int(description='Number of tags')
    tags = graphene.List(Tag, description='List of tags')

    def resolve_count(root, _info):
        return get_int_from_element(root, 'count')

    def resolve_tags(root, _info):
        return root.findall('tag')


class EntityPermission(NameObjectTypeMixin, graphene.ObjectType):
    """Simple permission description"""


class CreationModifactionObjectTypeMixin:

    creation_time = graphene.DateTime(
        description='Date and time the entity has been created'
    )
    modification_time = graphene.DateTime(
        description='Date and time the entity was last modified '
    )

    def resolve_creation_time(root, _info):
        return get_datetime_from_element(root, 'creation_time')

    def resolve_modification_time(root, _info):
        return get_datetime_from_element(root, 'modification_time')


class OwnerObjectTypeMixin:
    owner = graphene.String(description='Name of the user owning the entity')

    def resolve_owner(root, _info):
        return get_owner(root)


class CommentObjectTypeMixin:

    comment = graphene.String(description='Additional comment about the entity')

    def resolve_comment(root, _info):
        return get_text_from_element(root, 'comment')


class PermissionObjectTypeMixin:

    permissions = graphene.List(
        EntityPermission,
        description='Permissions of the current user on the entity',
    )

    def resolve_permissions(root, _info):
        permissions = root.find('permissions')
        if permissions is None or len(permissions) == 0:
            return None
        return permissions.findall('permission')


class UserTagsObjectTypeMixin:

    user_tags = graphene.Field(
        EntityUserTags, description='Tags connected to the entity by the user'
    )

    def resolve_user_tags(root, _info):
        return root.find('user_tags')


class AccessObjectTypeMixin:

    writable = graphene.Boolean(
        description='False if the current user is not allowed to change the'
        ' entity'
    )
    in_use = graphene.Boolean(
        description='True if the entity is used elsewhere and can not be'
        ' modified'
    )

    def resolve_writable(root, _info):
        return get_boolean_from_element(root, 'writable')

    def resolve_in_use(root, _info):
        return get_boolean_from_element(root, 'in_use')


class SimpleEntityObjectType(
    OwnerObjectTypeMixin,
    CommentObjectTypeMixin,
    CreationModifactionObjectTypeMixin,
    BaseObjectType,
):
    """A simple Entity object type without permissions, user tags, in use and
    writeable fields"""


class EntityObjectType(
    UserTagsObjectTypeMixin,
    PermissionObjectTypeMixin,
    AccessObjectTypeMixin,
    SimpleEntityObjectType,
):
    """An common object type for Entities"""
