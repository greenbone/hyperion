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
                modifyLdapAuthenticationSettings(
                    authDn: "hello",
                    enable: true,
                    host: "localhost",
                    certificate: "-----BEGIN CERTIFICATE-----"
                    ) {
                    ok
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_modify_ldap_settings(self, mock_gmp: GmpMockFactory):
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
            mutation {
                modifyLdapAuthenticationSettings(
                    authDn: "hello",
                    enable: true,
                    host: "localhost",
                    certificate: "-----BEGIN CERTIFICATE-----"
                    ) {
                    ok
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        self.assertTrue(json['data']['modifyLdapAuthenticationSettings']['ok'])

        mock_gmp.gmp_protocol.modify_auth.assert_called_with(
            'method:ldap_connect',
            {
                'enable': 'true',
                'authdn': 'hello',
                'ldaphost': 'localhost',
                'cacert': '-----BEGIN CERTIFICATE-----',
            },
        )
