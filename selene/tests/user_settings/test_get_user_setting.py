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

# pylint: disable=line-too-long

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class UserSettingTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                userSetting(id: "05d1edfa-3df8-11ea-9651-7b09b3acce77") {
                    id
                    name
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_user_setting(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_setting',
            '''
            <get_settings_response>
                <setting id="75d23ba8-3d23-11ea-858e-b7c2cb43e815">
                    <name>a</name>
                    <comment>b</comment>
                    <value>1</value>
                </setting>
            </get_settings_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                userSetting(id: "75d23ba8-3d23-11ea-858e-b7c2cb43e815") {
                    id
                    name
                    comment
                    value
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        setting = json['data']['userSetting']

        self.assertEqual(setting['name'], 'a')
        self.assertEqual(setting['id'], '75d23ba8-3d23-11ea-858e-b7c2cb43e815')
        self.assertEqual(setting['comment'], 'b')
        self.assertEqual(setting['value'], '1')
