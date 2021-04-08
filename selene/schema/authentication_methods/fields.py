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

import graphene

from selene.schema.utils import get_text_from_element


class AuthConfSetting(graphene.ObjectType):
    """
    Object class describing an authentication configuration setting
    """

    key = graphene.String(description='Name of the setting')
    value = graphene.String(description='Value of the setting')

    @staticmethod
    def resolve_key(root, _info):
        return get_text_from_element(root, 'key')

    @staticmethod
    def resolve_value(root, _info):
        return get_text_from_element(root, 'value')


class AuthMethodGroup(graphene.ObjectType):
    """
    Object class describing an authentication method.
    """

    name = graphene.String(description='Name of the authentication method')
    auth_conf_settings = graphene.List(
        AuthConfSetting,
        description='List of authentication configuration settings',
    )

    @staticmethod
    def resolve_name(root, _info):
        return root.attrib.get('name')

    @staticmethod
    def resolve_auth_conf_settings(root, _info):
        return root.findall('auth_conf_setting')
