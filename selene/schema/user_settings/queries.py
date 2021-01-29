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

from selene.schema.user_settings.fields import UserSetting
from selene.schema.utils import (
    require_authentication,
    get_gmp,
)


class GetUserSetting(graphene.Field):
    def __init__(self):
        super().__init__(
            UserSetting,
            user_setting_id=graphene.UUID(required=True, name='id'),
            resolver=self.resolve,
        )

    @staticmethod
    @require_authentication
    def resolve(_root, info, user_setting_id: graphene.UUID):
        gmp = get_gmp(info)

        xml = gmp.get_setting(str(user_setting_id))
        return xml.find('setting')


class GetUserSettings(graphene.List):
    def __init__(self):
        super().__init__(
            UserSetting, filter_string=graphene.String(), resolver=self.resolve
        )

    @staticmethod
    @require_authentication
    def resolve(_root, info, filter_string: str = None):
        gmp = get_gmp(info)

        xml = gmp.get_settings(filter=filter_string)
        return xml.findall('setting')
