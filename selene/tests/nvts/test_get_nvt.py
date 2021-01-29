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
class NVTTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                nvt(id: "1.3.6.1.4.1.25623.1.0.814313") {
                    id
                    name
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_nvt(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_info',
            '''
            <get_info_response>
                <info id="1.3.6.1.4.1.25623.1.0.814313">
                    <name>foo</name>
                </info>
            </get_info_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                nvt(id: "1.3.6.1.4.1.25623.1.0.814313") {
                    id
                    name
                    owner
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        nvt = json['data']['nvt']

        self.assertEqual(nvt['id'], '1.3.6.1.4.1.25623.1.0.814313')
        self.assertEqual(nvt['name'], 'foo')
        self.assertIsNone(nvt['owner'])

    def test_complex_nvt(self, mock_gmp: GmpMockFactory):
        nvt_xml_path = CWD / 'example-nvt.xml'
        nvt_xml_str = nvt_xml_path.read_text()

        mock_gmp.mock_response('get_info', nvt_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                nvt(id: "1.3.6.1.4.1.25623.1.0.117130") {
                    id
                    name
                    creationTime
                    modificationTime
                    category
                    family
                    cvssBase
                    qod {
                        value
                        type
                    }
                    severities {
                        score
                        severitiesList {
                            date
                            origin
                            score
                            type
                            vector
                        }
                    }
                    refs{
                        warning
                        refList{
                            id
                            type
                        }
                    }
                    tags {
                        cvssBaseVector
                        summary
                        insight
                        impact
                        affected
                        vuldetect
                    }
                    preferenceCount
                    timeout
                    defaultTimeout
                    solution{
                        type
                        method
                        description
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        nvt = json['data']['nvt']

        self.assertEqual(nvt['name'], 'test')
        self.assertEqual(nvt['id'], '1.3.6.1.4.1.25623.1.0.117130')

        self.assertEqual(nvt['category'], 3)
        self.assertEqual(nvt['family'], 'Some family')
        self.assertEqual(nvt['cvssBase'], 4.9)
        self.assertEqual(
            nvt['qod'],
            {"value": 80, "type": "remote_banner"},
        )
        self.assertEqual(
            nvt['severities'],
            {
                "score": 49,
                "severitiesList": [
                    {
                        "date": "2020-12-23T06:28:09+00:00",
                        "origin": None,
                        "score": 49,
                        "type": "cvss_base_v2",
                        "vector": "AV:N/AC:M/Au:S/C:P/I:N/A:P",
                    }
                ],
            },
        )
        self.assertEqual(
            nvt['refs'],
            {
                "warning": None,
                "refList": [
                    {"id": "54321", "type": "cert-bund"},
                    {"id": "12345", "type": "dfn-cert"},
                    {"id": "CVE-2014-0682", "type": "cve"},
                    {"id": "http://test.test", "type": "url"},
                ],
            },
        )
        self.assertIsNotNone(nvt['tags'])
        tags = nvt['tags']
        self.assertEqual(tags['cvssBaseVector'], 'vec')
        self.assertEqual(tags['summary'], 'sum')
        self.assertEqual(tags['insight'], 'ins')
        self.assertEqual(tags['impact'], 'imp')
        self.assertEqual(tags['affected'], 'aff')
        self.assertEqual(tags['vuldetect'], 'vul')
        self.assertEqual(nvt['preferenceCount'], -1)
        self.assertEqual(nvt['timeout'], None)
        self.assertEqual(nvt['defaultTimeout'], None)
        self.assertEqual(
            nvt['solution'],
            {
                "type": "WillNotFix",
                "method": "",
                "description": "Sorry.",
            },
        )


class NVTGetEntityTestCase(SeleneTestCase):
    gmp_name = 'info'
    selene_name = 'nvt'
    test_get_entity = make_test_get_entity(
        gmp_name,
        selene_name=selene_name,
        info_type=GvmInfoType.NVT,
    )
