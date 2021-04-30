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

import string

import graphene

from selene.schema.entity import EntityObjectType

from selene.schema.utils import get_text_from_element


class BaseRoleType(EntityObjectType):
    pass


class Role(BaseRoleType):
    users = graphene.List(graphene.String)

    @staticmethod
    def resolve_users(root, _info):
        user_string = get_text_from_element(root, 'users')
        if not user_string:
            return None
        # get rid of all whitespace
        user_string = user_string.translate(
            str.maketrans('', '', string.whitespace)
        )
        return user_string.split(',')
