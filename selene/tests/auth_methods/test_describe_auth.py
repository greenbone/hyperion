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

from pathlib import Path

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory

CWD = Path(__file__).absolute().parent


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class AuthTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        """
        Test the authentication requirement
        """
        response = self.query(
            '''
            query {
                auth {
                    name
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_describe_auth(self, mock_gmp: GmpMockFactory):
        """
        Test query
        """
        auth_xml_path = CWD / 'example-describe-auth.xml'
        auth_xml_str = auth_xml_path.read_text()

        mock_gmp.mock_response('describe_auth', auth_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query DescribeAuth {
                auth {
                    name
                    authConfSettings {
                        key
                        value
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.describe_auth.assert_called_with()

        # Query should return a list of 3 methods
        auth_list = json['data']['auth']
        self.assertEqual(len(auth_list), 3)
        self.assertEqual(
            auth_list[0],
            {
                "name": "method:file",
                "authConfSettings": [
                    {"key": "enable", "value": "true"},
                    {"key": "order", "value": "1"},
                ],
            },
        )
        self.assertEqual(auth_list[1]['name'], 'method:ldap_connect')
        self.assertEqual(auth_list[2]['name'], 'method:radius_connect')
