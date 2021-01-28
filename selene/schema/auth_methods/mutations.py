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

import graphene

from selene.schema.utils import (
    get_gmp,
    require_authentication,
)


class AuthConfSettingInput(graphene.InputObjectType):
    """
    Input object for authentication configuration settings in modifyAuth.
    """

    key = graphene.String(required=True, description='Name of the setting')
    value = graphene.String(required=True, description='Value of the setting')


class ModifyAuth(graphene.Mutation):
    """Modifies an alert

    Args:
        group_name (String): Name of the authentication method group to modify.
        auth_conf_settings (List): List of authentication config settings.
    """

    class Arguments:
        group_name = graphene.String(
            required=True,
            description='Name of the authentication method group to modify',
        )
        auth_conf_settings = graphene.List(
            AuthConfSettingInput,
            required=True,
            description='List of authentication config settings',
        )

    ok = graphene.Boolean()

    @staticmethod
    @require_authentication
    def mutate(_root, info, group_name: str, auth_conf_settings: list):
        gmp = get_gmp(info)

        settings_dict = {}
        for item in auth_conf_settings:
            settings_dict[item.key] = item.value

        gmp.modify_auth(group_name, settings_dict)

        return ModifyAuth(ok=settings_dict)
