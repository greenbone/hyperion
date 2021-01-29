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
class UserSettingsTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                userSettings {
                    id
                    name
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_user_settings(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_settings',
            '''
            <get_settings_response>
                <setting id="75d23ba8-3d23-11ea-858e-b7c2cb43e815">
                    <name>a</name>
                    <comment>b</comment>
                    <value>1</value>
                </setting>
                <setting id="aaa8dccc-3eab-11ea-a303-fff496f2cccb">
                    <name>b</name>
                    <comment>c</comment>
                    <value>2</value>
                </setting>
            </get_settings_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                userSettings {
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

        settings = json['data']['userSettings']

        self.assertEqual(len(settings), 2)

        setting1 = settings[0]
        setting2 = settings[1]

        self.assertEqual(setting1['name'], 'a')
        self.assertEqual(setting1['id'], '75d23ba8-3d23-11ea-858e-b7c2cb43e815')
        self.assertEqual(setting1['comment'], 'b')
        self.assertEqual(setting1['value'], '1')

        self.assertEqual(setting2['name'], 'b')
        self.assertEqual(setting2['id'], 'aaa8dccc-3eab-11ea-a303-fff496f2cccb')
        self.assertEqual(setting2['comment'], 'c')
        self.assertEqual(setting2['value'], '2')
