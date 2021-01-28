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

# from datetime import datetime, timezone
from pathlib import Path

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory

from selene.tests.entity import make_test_get_entity

CWD = Path(__file__).absolute().parent


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class TLSCertificateTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                tlsCertificate(id: "05d1edfa-3df8-11ea-9651-7b09b3acce77") {
                    id
                    name
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_tls_certificate(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_tls_certificate',
            '''
            <get_tls_certificates_response>
                <tls_certificate id="75d23ba8-3d23-11ea-858e-b7c2cb43e815">
                    <name>foo</name>
                </tls_certificate>
            </get_tls_certificates_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                tlsCertificate(id: "75d23ba8-3d23-11ea-858e-b7c2cb43e815") {
                    id
                    name
                    owner
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        tls_certificate = json['data']['tlsCertificate']

        self.assertEqual(tls_certificate['name'], 'foo')
        self.assertEqual(
            tls_certificate['id'], '75d23ba8-3d23-11ea-858e-b7c2cb43e815'
        )
        self.assertIsNone(tls_certificate['owner'])

    def test_complex_tls_certificate(self, mock_gmp: GmpMockFactory):
        tls_certificate_xml_path = CWD / 'example-tls-certificate.xml'
        tls_certificate_xml_str = tls_certificate_xml_path.read_text()

        mock_gmp.mock_response('get_tls_certificate', tls_certificate_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                tlsCertificate(id: "291a7547-c817-4b46-88f2-32415d825335") {
                    id
                    name
                    certificateFormat
                    certificate
                    sha256Fingerprint
                    md5Fingerprint
                    trust
                    valid
                    timeStatus
                    activationTime
                    expirationTime
                    subjectDn
                    issuerDn
                    serial
                    lastSeen
                    sources {
                        id
                        timestamp
                        tlsVersions
                        location {
                            id
                            hostIp
                            hostId
                            port
                        }
                        origin {
                            id
                            originType
                            originId
                            originData
                        }
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        tls_certificate = json['data']['tlsCertificate']

        self.assertEqual(tls_certificate['name'], 'xyz')
        self.assertEqual(
            tls_certificate['id'], 'b34292d9-ef91-41fc-8832-5f70b0ad88a7'
        )
        self.assertEqual(tls_certificate['certificate'], 'boo')
        self.assertEqual(tls_certificate['certificateFormat'], 'DER')
        self.assertEqual(tls_certificate['sha256Fingerprint'], 'foo')
        self.assertEqual(tls_certificate['md5Fingerprint'], 'moo')
        self.assertEqual(tls_certificate['trust'], False)
        self.assertEqual(tls_certificate['valid'], True)
        self.assertEqual(tls_certificate['timeStatus'], 'valid')
        self.assertEqual(
            tls_certificate['activationTime'], '2014-01-15T13:26:06+00:00'
        )
        self.assertEqual(
            tls_certificate['expirationTime'], '2034-01-11T13:26:06+00:00'
        )

        self.assertEqual(tls_certificate['subjectDn'], 'xyz')
        self.assertEqual(tls_certificate['issuerDn'], 'CN=EM2_CA')
        self.assertEqual(tls_certificate['serial'], 'moo')
        self.assertEqual(
            tls_certificate['lastSeen'], '2017-06-05T21:10:07+00:00'
        )

        sources = tls_certificate['sources']
        source = sources[0]

        self.assertEqual(source['id'], '77465cc9-466d-42a4-9ad9-b186304fb414')
        self.assertEqual(source['timestamp'], '2017-06-05T21:10:07+00:00')
        self.assertEqual(
            source['tlsVersions'], ['TLSv1.2', 'TLSv1.1', 'TLSv1.0']
        )

        location = source['location']
        origin = source['origin']

        self.assertEqual(location['id'], '4e44ba5a-0497-46f3-bee5-4059f5d4424a')
        self.assertEqual(location['hostIp'], '194.81.203.113')
        self.assertEqual(location['hostId'], None)
        self.assertEqual(location['port'], 8194)

        self.assertEqual(origin['id'], 'e9d19408-8265-43c3-ab74-c00dd6844639')
        self.assertEqual(origin['originType'], 'Report')
        self.assertEqual(
            origin['originId'], 'fc4a54fd-28a1-4182-9bde-4d012ac7a69a'
        )
        self.assertEqual(origin['originData'], '1.3.6.1.4.1.25623.1.0.103692')


class TLSCertificateGetEntityTestCase(SeleneTestCase):
    gmp_name = 'tls_certificate'
    selene_name = 'tlsCertificate'
    test_get_entity = make_test_get_entity(gmp_name, selene_name=selene_name)
