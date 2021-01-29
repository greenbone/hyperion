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

# from datetime import datetime, timezone
from pathlib import Path

from unittest.mock import patch

from gvm.protocols.latest import InfoType as GvmInfoType

from selene.tests import SeleneTestCase, GmpMockFactory

from selene.tests.entity import make_test_get_entity

CWD = Path(__file__).absolute().parent


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class CVETestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                cve(id: "CVE-1999-0001") {
                    id
                    name
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_cve(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_info',
            '''
            <get_info_response>
                <info id="CVE-1999-0001">
                    <name>foo</name>
                </info>
            </get_info_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                cve(id: "CVE-1999-0001") {
                    id
                    name
                    owner
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        cve = json['data']['cve']

        self.assertEqual(cve['id'], 'CVE-1999-0001')
        self.assertEqual(cve['name'], 'foo')
        self.assertIsNone(cve['owner'])

    def test_complex_cve(self, mock_gmp: GmpMockFactory):
        cve_xml_path = CWD / 'example-cve.xml'
        cve_xml_str = cve_xml_path.read_text()

        mock_gmp.mock_response('get_info', cve_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                cve(id: "CVE-1999-0001") {
                    id
                    name
                    updateTime
                    description
                    products
                    cvssV2Vector {
                        accessVector
                        accessComplexity
                        authentication
                        confidentiality
                        integrity
                        availability
                        baseScore
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        cve = json['data']['cve']

        self.assertEqual(cve['name'], 'CVE-1999-0001')
        self.assertEqual(cve['id'], 'CVE-1999-0001')
        self.assertEqual(
            cve['description'],
            'ip_input.c in BSD-derived TCP/IP implementations allows remote '
            'attackers to cause a denial of service (crash or hang) via '
            'crafted packets.',
        )
        self.assertIsNotNone(cve['cvssV2Vector'])

        cvss_v2_vector = cve['cvssV2Vector']
        self.assertEqual(cvss_v2_vector['accessVector'], 'NETWORK')
        self.assertEqual(cvss_v2_vector['accessComplexity'], 'LOW')
        self.assertEqual(cvss_v2_vector['authentication'], 'NONE')
        self.assertEqual(cvss_v2_vector['confidentiality'], 'NONE')
        self.assertEqual(cvss_v2_vector['integrity'], 'NONE')
        self.assertEqual(cvss_v2_vector['availability'], 'PARTIAL')
        self.assertEqual(cvss_v2_vector['baseScore'], 5)

        self.assertEqual(
            cve['products'],
            [
                'cpe:/o:bsdi:bsd_os:3.1',
                'cpe:/o:freebsd:freebsd:1.0',
                'cpe:/o:freebsd:freebsd:1.1',
                'cpe:/o:freebsd:freebsd:1.1.5.1',
                'cpe:/o:freebsd:freebsd:1.2',
                'cpe:/o:freebsd:freebsd:2.0',
                'cpe:/o:freebsd:freebsd:2.0.1',
                'cpe:/o:freebsd:freebsd:2.0.5',
                'cpe:/o:freebsd:freebsd:2.1.5',
                'cpe:/o:freebsd:freebsd:2.1.6',
                'cpe:/o:freebsd:freebsd:2.1.6.1',
                'cpe:/o:freebsd:freebsd:2.1.7',
                'cpe:/o:freebsd:freebsd:2.1.7.1',
                'cpe:/o:freebsd:freebsd:2.2',
                'cpe:/o:freebsd:freebsd:2.2.2',
                'cpe:/o:freebsd:freebsd:2.2.3',
                'cpe:/o:freebsd:freebsd:2.2.4',
                'cpe:/o:freebsd:freebsd:2.2.5',
                'cpe:/o:freebsd:freebsd:2.2.6',
                'cpe:/o:freebsd:freebsd:2.2.8',
                'cpe:/o:freebsd:freebsd:3.0',
                'cpe:/o:openbsd:openbsd:2.3',
                'cpe:/o:openbsd:openbsd:2.4',
            ],
        )


class CVEGetEntityTestCase(SeleneTestCase):
    gmp_name = 'info'
    selene_name = 'cve'
    test_get_entity = make_test_get_entity(
        gmp_name,
        selene_name=selene_name,
        info_type=GvmInfoType.CVE,
    )
