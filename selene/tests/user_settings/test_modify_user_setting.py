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

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class ModifyUserSettingTestCase(SeleneTestCase):
    def setUp(self):
        self.xml = '''
        <modify_setting_response
            status="200"
            status_text="OK"
        />
        '''

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            mutation {
                modifyUserSetting(
                    id: "578a1c14-e2dc-45ef-a591-89d31391d007"
                    value: "30"
                ) {
                    ok
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_modify_setting(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('modify_setting', self.xml)

        self.login('foo', 'bar')

        response = self.query(
            '''
            mutation {
                modifyUserSetting(
                    id: "578a1c14-e2dc-45ef-a591-89d31391d007"
                    value: "30"
                ) {
                    ok
                }
            }
            '''
        )

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_setting.assert_called_with(
            setting_id='578a1c14-e2dc-45ef-a591-89d31391d007', value='30'
        )

    def test_modify_setting_without_id(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('modify_setting', self.xml)

        self.login('foo', 'bar')

        response = self.query(
            '''
            mutation {
                modifyUserSetting(
                    value: "30"
                ) {
                    ok
                }
            }
            '''
        )

        self.assertResponseHasErrors(response)

    def test_modify_setting_without_value(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('modify_setting', self.xml)

        self.login('foo', 'bar')

        response = self.query(
            '''
            mutation {
                modifyUserSetting(
                    id: "578a1c14-e2dc-45ef-a591-89d31391d007"
                ) {
                    ok
                }
            }
            '''
        )

        self.assertResponseHasErrors(response)
