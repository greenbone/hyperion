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

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class ModifyAuthTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        """
        Test the authentication requirement
        """
        response = self.query(
            '''
            mutation {
                modifyAuth(
                    groupName: "method:ldap_connect",
                    authConfSettings: [{key: "enable", value: "false"}]
                ) {
                    ok
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_modify_auth(self, mock_gmp: GmpMockFactory):
        """
        Test a correct mutation query to modify a authentication setting
        """
        mock_gmp.mock_response(
            'modify_auth',
            '<modify_auth_response status="200" status_text="OK"/>',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            mutation ModifyAuth {
                modifyAuth(
                    groupName: "method:ldap_connect",
                    authConfSettings: [{key: "enable", value: "false"}]
                ) {
                    ok
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        self.assertTrue(json['data']['modifyAuth']['ok'])

        mock_gmp.gmp_protocol.modify_auth.assert_called_with(
            'method:ldap_connect', {'enable': 'false'}
        )

    def test_modify_auth_without_group_name(self, _mock_gmp: GmpMockFactory):
        """
        Test a mutation query where the groupName is missing.
        """
        self.login('foo', 'bar')

        response = self.query(
            '''
            mutation ModifyAuth {
                modifyAuth(
                    authConfSettings: [{key: "enable", value: "false"}]
                ) {
                    ok
                }
            }
            '''
        )

        self.assertResponseHasErrors(response)

    def test_modify_auth_without_settings(self, _mock_gmp: GmpMockFactory):
        """
        Test a mutation query where the authConfSettings are missing.
        """
        self.login('foo', 'bar')

        response = self.query(
            '''
            mutation ModifyAuth {
                modifyAuth(
                    groupName: "method:ldap_connect"
                ) {
                    ok
                }
            }
            '''
        )

        self.assertResponseHasErrors(response)
