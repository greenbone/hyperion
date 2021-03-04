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

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class GetScanConfigNvtTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                scanConfigNvt (id:"1.3.6.1.4.1.25623.1.0.999999") {
                id
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_scan_config_nvt(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_nvt',
            '''
            <get_nvts_response status="200" status_text="OK">
            <nvt oid="1.3.6.1.4.1.25623.1.0.100315">
                <name>Some name</name>
                <creation_time>2009-10-26T09:02:32Z</creation_time>
                <modification_time>2020-05-11T05:36:14Z</modification_time>
                <category>1</category>
                <summary>Some summary</summary>
                <family>Some family</family>
                <cvss_base>5.0</cvss_base>
                <qod>
                    <value>80</value>
                    <type>remote_banner</type>
                </qod>
                <severities score="50">
                    <severity type="cvss_base_v2">
                        <origin>CVE-2011-9999</origin>
                        <date>2009-10-26T09:02:32Z</date>
                        <score>50</score>
                        <value>AV:N/AC:M/Au:N/C:N/I:P/A:P</value>
                    </severity>
                </severities>
                <refs>
                    <ref type="cve" id="CVE-2011-9999"/>
                    <ref type="bid" id="12345"/>
                    <ref type="url" id="http://test.test"/>
                </refs>
                <tags>cvss_base_vector=vec|summary=sum|insight=ins|
                    affected=aff|impact=imp|vuldetect=vul
                </tags>
                <preference_count>-1</preference_count>
                <timeout/>
                <default_timeout/>
                <solution type="VendorFix" method="">Just update.</solution>
            </nvt>
            </get_nvts_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                scanConfigNvt (id:"1.3.6.1.4.1.25623.1.0.100315") {
                    id
                    name
                    creationTime
                    modificationTime
                    category
                    summary
                    family
                    cvssBase
                    qod {
                        value
                        type
                    }
                    score
                    severities {
                        date
                        origin
                        score
                        type
                        vector
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

        json_response = response.json()
        self.assertResponseNoErrors(response)
        nvt = json_response['data']['scanConfigNvt']

        self.assertEqual(nvt['id'], "1.3.6.1.4.1.25623.1.0.100315")
        self.assertEqual(nvt['name'], 'Some name')
        self.assertEqual(nvt['creationTime'], '2009-10-26T09:02:32Z')
        self.assertEqual(nvt['modificationTime'], '2020-05-11T05:36:14Z')
        self.assertEqual(nvt['category'], 1)
        self.assertEqual(nvt['summary'], 'Some summary')
        self.assertEqual(nvt['family'], 'Some family')
        self.assertEqual(nvt['cvssBase'], 5.0)
        self.assertEqual(nvt['score'], 50)
        self.assertEqual(
            nvt['qod'],
            {"value": 80, "type": "remote_banner"},
        )
        self.assertEqual(
            nvt['severities'],
            [
                {
                    "date": "2009-10-26T09:02:32+00:00",
                    "origin": "CVE-2011-9999",
                    "score": 50,
                    "type": "cvss_base_v2",
                    "vector": "AV:N/AC:M/Au:N/C:N/I:P/A:P",
                }
            ],
        )
        self.assertEqual(
            nvt['refs'],
            {
                "warning": None,
                "refList": [
                    {"id": "CVE-2011-9999", "type": "cve"},
                    {"id": "12345", "type": "bid"},
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
                "type": "VendorFix",
                "method": "",
                "description": "Just update.",
            },
        )

        mock_gmp.gmp_protocol.get_nvt.assert_called_with(
            "1.3.6.1.4.1.25623.1.0.100315"
        )
