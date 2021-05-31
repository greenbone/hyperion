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

from selene.schema.utils import get_gmp, require_authentication


class ModifyUserSetting(graphene.Mutation):
    """
    Modifies a setting selected by UUID of the current user.
    This covers most settings except timezone and password.
    """

    class Arguments:
        setting_id = graphene.UUID(
            required=True,
            name='id',
            description='UUID of the user setting to modify',
        )
        value = graphene.String(
            required=True, description='Value to set for the user setting'
        )

    ok = graphene.Boolean()

    @staticmethod
    @require_authentication
    def mutate(_root, info, setting_id, value):
        gmp = get_gmp(info)
        gmp.modify_user_setting(setting_id=str(setting_id), value=value)
        return ModifyUserSetting(ok=True)


class ModifyUserSettingByName(graphene.Mutation):
    """
    Modifies a setting selected by name of the current user.
    Currently this only applies to "Timezone" and "Password".
    """

    class Arguments:
        setting_name = graphene.String(
            required=True,
            name='name',
            description='Name of the user setting to modify',
        )
        value = graphene.String(
            required=True, description='Value to set for the user setting'
        )

    ok = graphene.Boolean()

    @staticmethod
    @require_authentication
    def mutate(_root, info, setting_name, value):
        gmp = get_gmp(info)
        gmp.modify_user_setting(name=setting_name, value=value)
        return ModifyUserSetting(ok=True)
