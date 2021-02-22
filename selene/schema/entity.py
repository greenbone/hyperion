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

from selene.schema.parser import parse_uuid

from selene.schema.utils import (
    get_owner,
    get_boolean_from_element,
    get_datetime_from_element,
    get_int_from_element,
    get_text_from_element,
)

from selene.schema.tags.fields import Tag


class EntityUserTags(graphene.ObjectType):
    count = graphene.Int()
    tags = graphene.List(Tag)

    def resolve_count(root, _info):
        return get_int_from_element(root, 'count')

    def resolve_tags(root, _info):
        return root.findall('tag')


class EntityPermission(graphene.ObjectType):
    """Simple permission description."""

    name = graphene.String()

    def resolve_name(root, _info):
        return get_text_from_element(root, 'name')


class EntityObjectType(graphene.ObjectType):

    uuid = graphene.UUID(name='id')

    owner = graphene.String()
    name = graphene.String()
    comment = graphene.String()

    writable = graphene.Boolean()
    in_use = graphene.Boolean()

    creation_time = graphene.DateTime()
    modification_time = graphene.DateTime()

    permissions = graphene.List(EntityPermission)

    user_tags = graphene.Field(EntityUserTags)

    def resolve_uuid(root, _info):
        return parse_uuid(root.get('id'))

    def resolve_owner(root, _info):
        return get_owner(root)

    def resolve_name(root, _info):
        return get_text_from_element(root, 'name')

    def resolve_comment(root, _info):
        return get_text_from_element(root, 'comment')

    def resolve_writable(root, _info):
        return get_boolean_from_element(root, 'writable')

    def resolve_in_use(root, _info):
        return get_boolean_from_element(root, 'in_use')

    def resolve_creation_time(root, _info):
        return get_datetime_from_element(root, 'creation_time')

    def resolve_modification_time(root, _info):
        return get_datetime_from_element(root, 'modification_time')

    def resolve_permissions(root, _info):
        permissions = root.find('permissions')
        if permissions is None or len(permissions) == 0:
            return None
        return permissions.findall('permission')

    def resolve_user_tags(root, _info):
        return root.find('user_tags')
