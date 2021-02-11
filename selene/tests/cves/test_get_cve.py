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

from gvm.protocols.next import InfoType as GvmInfoType

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
                cve(id: "CVE-2020-2222") {
                    id
                    name
                    updateTime
                    description
                    products
                    nvtRefs {
                        id
                        name
                    }
                    certRefs {
                        name
                        title
                        type
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        cve = json['data']['cve']

        self.assertEqual(cve['name'], 'CVE-2020-2222')
        self.assertEqual(cve['id'], 'CVE-2020-2222')
        self.assertEqual(
            cve['description'],
            'bar baz boing',
        )

        self.assertEqual(
            cve['products'],
            [
                'cpe:/a:foo:bar:2.235.1:',
                'cpe:/a:foo:bar:2.244.1:',
            ],
        )

        self.assertIsNotNone(cve['nvtRefs'])
        nvts = cve['nvtRefs']
        self.assertEqual(nvts[0]['id'], '1.3.6.1.4.1.25623.1.0.123456')
        self.assertEqual(nvts[0]['name'], 'blee')
        self.assertEqual(nvts[1]['id'], '1.3.6.1.4.1.25623.1.0.654321')
        self.assertEqual(nvts[1]['name'], 'bloo')


class CVEGetEntityTestCase(SeleneTestCase):
    gmp_name = 'info'
    selene_name = 'cve'
    test_get_entity = make_test_get_entity(
        gmp_name,
        selene_name=selene_name,
        info_type=GvmInfoType.CVE,
    )
