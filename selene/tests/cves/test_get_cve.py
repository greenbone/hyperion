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

    def test_get_cve_none_cases(self, mock_gmp: GmpMockFactory):
        cve_id = 'CVE-1999-0001'
        mock_gmp.mock_response(
            'get_cve',
            f'''
            <get_info_response>
                <info id="{cve_id}">
                    <name>foo</name>
                </info>
            </get_info_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            query {{
                cve(id: "{cve_id}") {{
                    id
                    name
                    owner
                    products
                    score
                    cvssVector
                    cvssV2Vector {{
                        vector
                    }}
                    cvssV3Vector {{
                        vector
                    }}
                    nvtRefs {{
                        id
                    }}
                    certRefs {{
                        name
                    }}
                    refs {{
                        source
                    }}
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        cve = json['data']['cve']

        self.assertEqual(cve['id'], cve_id)
        self.assertEqual(cve['name'], 'foo')
        self.assertIsNone(cve['owner'])
        self.assertIsNone(cve['score'])
        self.assertIsNone(cve['cvssVector'])
        self.assertIsNone(cve['cvssV2Vector'])
        self.assertIsNone(cve['cvssV3Vector'])
        self.assertIsNone(cve['nvtRefs'])
        self.assertIsNone(cve['certRefs'])
        self.assertIsNone(cve['refs'])
        self.assertIsNone(cve['products'])

        mock_gmp.gmp_protocol.get_cve.assert_called_with(cve_id)

    def test_get_cve_products_empty(self, mock_gmp: GmpMockFactory):
        cve_id = 'CVE-1999-0001'
        mock_gmp.mock_response(
            'get_cve',
            f'''
            <get_info_response>
                <info id="{cve_id}">
                    <name>foo</name>
                    <cve><products/></cve>
                </info>
            </get_info_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            query {{
                cve(id: "{cve_id}") {{
                    products
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        cve = json['data']['cve']

        self.assertIsNone(cve['products'])

        mock_gmp.gmp_protocol.get_cve.assert_called_with(cve_id)

    def test_complex_cve(self, mock_gmp: GmpMockFactory):
        cve_xml_path = CWD / 'example-cve.xml'
        cve_xml_str = cve_xml_path.read_text()

        mock_gmp.mock_response('get_cve', cve_xml_str)

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
                    score
                    cvssVector
                    cvssV2Vector {
                        accessVector
                        accessComplexity
                        authentication
                        confidentiality
                        integrity
                        availability
                        baseScore
                        vector
                    }
                    cvssV3Vector {
                        attackVector
                        attackComplexity
                        privilegesRequired
                        userInteraction
                        scope
                        confidentiality
                        integrity
                        availability
                        baseScore
                        vector
                    }
                    nvtRefs {
                        id
                        name
                    }
                    certRefs {
                        name
                        title
                        type
                    }
                    refs {
                        source
                        link
                        reference
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
        self.assertEqual(cve['description'], 'bar baz boing')
        self.assertIsNotNone(cve['cvssV2Vector'])

        cvss_v2_vector = cve['cvssV2Vector']
        self.assertEqual(cvss_v2_vector['accessVector'], 'NETWORK')
        self.assertEqual(cvss_v2_vector['accessComplexity'], 'MEDIUM')
        self.assertEqual(cvss_v2_vector['authentication'], 'SINGLE')
        self.assertEqual(cvss_v2_vector['confidentiality'], 'NONE')
        self.assertEqual(cvss_v2_vector['integrity'], 'PARTIAL')
        self.assertEqual(cvss_v2_vector['availability'], 'NONE')
        self.assertEqual(cvss_v2_vector['baseScore'], 3.5)
        self.assertEqual(cvss_v2_vector['vector'], 'AV:N/AC:M/Au:S/C:N/I:P/A:N')

        cvss_v3_vector = cve['cvssV3Vector']
        self.assertEqual(cvss_v3_vector['attackVector'], 'NETWORK')
        self.assertEqual(cvss_v3_vector['attackComplexity'], 'LOW')
        self.assertEqual(cvss_v3_vector['privilegesRequired'], 'LOW')
        self.assertEqual(cvss_v3_vector['userInteraction'], 'REQUIRED')
        self.assertEqual(cvss_v3_vector['scope'], 'CHANGED')
        self.assertEqual(cvss_v3_vector['confidentiality'], 'LOW')
        self.assertEqual(cvss_v3_vector['integrity'], 'LOW')
        self.assertEqual(cvss_v3_vector['availability'], 'NONE')
        self.assertEqual(cvss_v3_vector['baseScore'], 5.4)
        self.assertEqual(
            cvss_v3_vector['vector'],
            'CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:L/I:L/A:N',
        )
        self.assertEqual(
            cve['cvssVector'], 'CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:L/I:L/A:N'
        )

        self.assertEqual(cve['score'], 54)

        self.assertEqual(
            cve['products'],
            ['cpe:/a:foo:bar:2.235.1:', 'cpe:/a:foo:bar:2.244.1:'],
        )

        self.assertIsNotNone(cve['nvtRefs'])
        nvts = cve['nvtRefs']
        self.assertEqual(nvts[0]['id'], '1.3.6.1.4.1.25623.1.0.123456')
        self.assertEqual(nvts[0]['name'], 'blee')
        self.assertEqual(nvts[1]['id'], '1.3.6.1.4.1.25623.1.0.654321')
        self.assertEqual(nvts[1]['name'], 'bloo')

        self.assertIsNotNone(cve['refs'])
        refs = cve['refs']
        self.assertEqual(refs[0]['source'], 'MLIST')
        self.assertEqual(refs[0]['link'], 'link1')
        self.assertEqual(refs[0]['reference'], 'ref1')
        self.assertEqual(refs[1]['source'], 'CONFIRM')
        self.assertEqual(refs[1]['link'], 'link2')
        self.assertEqual(refs[1]['reference'], 'ref2')


class CVEGetEntityTestCase(SeleneTestCase):
    gmp_name = 'info'
    selene_name = 'cve'
    gmp_cmd = 'get_cve'
    test_get_entity = make_test_get_entity(
        gmp_name=gmp_name, selene_name=selene_name, gmp_cmd=gmp_cmd
    )
