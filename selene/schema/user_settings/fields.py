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

import graphene

from selene.schema.utils import get_text_from_element


class UserSetting(graphene.ObjectType):
    comment = graphene.String()
    value = graphene.String()
    # allow uuid to be a string until the uuid of the "Notes Top Dashboard
    # Configuration" is fixed
    uuid = graphene.String(name='id')
    name = graphene.String()

    @staticmethod
    def resolve_uuid(root, _info):
        entity_id = root.get('id')
        return entity_id

    @staticmethod
    def resolve_name(root, _info):
        return get_text_from_element(root, 'name')

    @staticmethod
    def resolve_comment(root, _info):
        return get_text_from_element(root, 'comment')

    @staticmethod
    def resolve_value(root, _info):
        return get_text_from_element(root, 'value')
