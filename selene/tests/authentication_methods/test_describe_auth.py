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
                ldapAuthenticationSettings {
                    authDn
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_describe_auth_ldap(self, mock_gmp: GmpMockFactory):
        """
        Test query
        """
        auth_xml_path = CWD / 'example-describe-auth.xml'
        auth_xml_str = auth_xml_path.read_text()

        mock_gmp.mock_response('describe_auth', auth_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                ldapAuthenticationSettings {
                    authDn
                    enable
                    host
                    caCertificate {
                        md5Fingerprint
                        issuer
                        activationTime
                        expirationTime
                        certificate
                        timeStatus
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.describe_auth.assert_called_with()

        ldap_settings = json['data']['ldapAuthenticationSettings']

        self.assertEqual(ldap_settings['authDn'], 'userid=%s,dc=example,dc=org')
        self.assertEqual(ldap_settings['enable'], True)
        self.assertEqual(ldap_settings['host'], '127.0.0.1')

        ca_certificate = ldap_settings['caCertificate']

        self.assertEqual(
            ca_certificate['md5Fingerprint'],
            'a4:dd:68:50:9c:7b:ff:b5:ca:46:ee:ac:0a:14:a3:fd',
        )
        self.assertEqual(ca_certificate['issuer'], 'C=AU,ST=Some-State,O=Rando')
        self.assertEqual(
            ca_certificate['activationTime'], '2021-04-01T13:56:33+00:00'
        )
        self.assertEqual(
            ca_certificate['expirationTime'], '2026-03-31T13:56:33+00:00'
        )
        self.assertEqual(
            ca_certificate['certificate'],
            '-----BEGIN CERTIFICATE-----MIIDazCCAlOgA-----END CERTIFICATE-----',
        )
        self.assertEqual(ca_certificate['timeStatus'], 'valid')

    def test_describe_auth_radius(self, mock_gmp: GmpMockFactory):
        """
        Test query
        """
        auth_xml_path = CWD / 'example-describe-auth.xml'
        auth_xml_str = auth_xml_path.read_text()

        mock_gmp.mock_response('describe_auth', auth_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                radiusAuthenticationSettings {
                    enable
                    host
                    secretKey
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.describe_auth.assert_called_with()

        radius_settings = json['data']['radiusAuthenticationSettings']

        self.assertEqual(radius_settings['enable'], False)
        self.assertEqual(radius_settings['secretKey'], 'testing123')
        self.assertEqual(radius_settings['host'], '127.0.0.1')
