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

# pylint: disable=line-too-long

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory

from selene.tests.entity import make_test_get_entity


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class GetScanConfigTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
               scanConfig (id: "daba56c8-73ec-11df-a475-002264764cea",
               ) {
                    name
                    type
            	    id
            	    trash
               }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_scan_config(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_config',
            '''
            <get_config_response status="200" status_text="OK">
                <config id="daba56c8-73ec-11df-a475-002264764cea">
                    <name>foo</name>
                    <type>0</type>
                    <usage_type>scan</usage_type>
                    <predefined>1</predefined>
                    <trash>0</trash>
                    <family_count>2<growing>1</growing></family_count>
                    <nvt_count>3<growing>0</growing></nvt_count>
                    <type>0</type>
                    <usage_type>scan</usage_type>
                    <families>
                    <family>
                        <name>Port scanners</name>
                        <nvt_count>2</nvt_count>
                        <max_nvt_count>9</max_nvt_count>
                        <growing>0</growing>
                    </family>
                    <family>
                        <name>Service detection</name>
                        <nvt_count>1</nvt_count>
                        <max_nvt_count>240</max_nvt_count>
                        <growing>0</growing>
                    </family>
                    </families>
                    <max_nvt_count>249</max_nvt_count>
                    <known_nvt_count>3</known_nvt_count>
                    <preferences>
                        <preference>
                            <nvt oid="1.3.6.1.4.1.25623.1.0.100315">
                                <name>Ping Host</name>
                            </nvt>
                            <id>13</id>
                            <hr_name>Log failed nmap calls</hr_name>
                            <name>Log failed nmap calls</name>
                            <type>checkbox</type>
                            <value>no</value>
                            <default>no</default>
                        </preference>
                        <preference>
                            <nvt oid="1.3.6.1.4.1.25623.1.0.100315">
                                <name>Ping Host</name>
                            </nvt>
                            <id>14</id>
                            <hr_name>nmap timing policy</hr_name>
                            <name>nmap timing policy</name>
                            <type>radio</type>
                            <value>Normal</value>
                            <alt>Paranoid</alt>
                            <alt>Sneaky</alt>
                            <default>Normal</default>
                        </preference>
                    </preferences>
                    <tasks>
                        <task id="49d082ec-73f5-4b3a-75b5-3b9d9e38d079">
                            <name>some_name</name>
                        </task>
                    </tasks>
                    <nvt_selectors>
                        <nvt_selector>
                            <name>f187d4cf-a157-471c-81a6-74990b5da181</name>
                            <include>1</include>
                            <type>2</type>
                            <family_or_nvt>1.3.6.1.4.1.25623.1.0.100315</family_or_nvt>
                        </nvt_selector>
                        <nvt_selector>
                            <name>f187d4cf-a157-471c-81a6-74990b5da181</name>
                            <include>1</include>
                            <type>2</type>
                            <family_or_nvt>1.3.6.1.4.1.25623.1.0.14259</family_or_nvt>
                        </nvt_selector>
                    </nvt_selectors>
                </config>
            </get_config_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
               scanConfig (id: "daba56c8-73ec-11df-a475-002264764cea",
               ) {
                    name
                    type
            	    id
            	    trash
                    familyCount
                    familyGrowing
                    nvtCount
                    nvtGrowing
                    usageType
                    maxNvtCount
                    knownNvtCount
                    predefined
                    families{
                        name
                        nvtCount
                        maxNvtCount
                        growing
                    }
                    preferences{
                        nvt{
                            name
                            id
                        }
                        hrName
                        name
                        id
                        type
                        value
                        default
                        alt
                    }
                    tasks{
                        id
                        name
                    }
                    nvtSelectors{
                        name
                        include
                        type
                        familyOrNvt
                    }
               }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        scan_config = json['data']['scanConfig']

        self.assertEqual(
            scan_config['id'], "daba56c8-73ec-11df-a475-002264764cea"
        )
        self.assertEqual(scan_config['name'], 'foo')
        self.assertEqual(scan_config['type'], 0)
        self.assertEqual(scan_config['trash'], 0)
        self.assertEqual(scan_config['familyCount'], 2)
        self.assertEqual(scan_config['usageType'], 'scan')
        self.assertEqual(scan_config['maxNvtCount'], 249)
        self.assertEqual(scan_config['knownNvtCount'], 3)
        self.assertEqual(scan_config['predefined'], True)
        self.assertEqual(
            scan_config['families'],
            [
                {
                    "name": "Port scanners",
                    "nvtCount": 2,
                    "maxNvtCount": 9,
                    "growing": False,
                },
                {
                    "name": "Service detection",
                    "nvtCount": 1,
                    "maxNvtCount": 240,
                    "growing": False,
                },
            ],
        )
        self.assertEqual(
            scan_config['preferences'],
            [
                {
                    "name": "Log failed nmap calls",
                    "id": 13,
                    "nvt": {
                        "name": "Ping Host",
                        "id": "1.3.6.1.4.1.25623.1.0.100315",
                    },
                    "hrName": "Log failed nmap calls",
                    "type": "checkbox",
                    "value": "no",
                    "default": "no",
                    "alt": None,
                },
                {
                    "name": "nmap timing policy",
                    "id": 14,
                    "nvt": {
                        "name": "Ping Host",
                        "id": "1.3.6.1.4.1.25623.1.0.100315",
                    },
                    "hrName": "nmap timing policy",
                    "type": "radio",
                    "value": "Normal",
                    "default": "Normal",
                    "alt": ["Paranoid", "Sneaky"],
                },
            ],
        )
        self.assertEqual(
            scan_config['tasks'],
            [
                {
                    "id": "49d082ec-73f5-4b3a-75b5-3b9d9e38d079",
                    "name": "some_name",
                }
            ],
        )
        self.assertEqual(
            scan_config['nvtSelectors'],
            [
                {
                    "name": "f187d4cf-a157-471c-81a6-74990b5da181",
                    "include": True,
                    "type": 2,
                    "familyOrNvt": "1.3.6.1.4.1.25623.1.0.100315",
                },
                {
                    "name": "f187d4cf-a157-471c-81a6-74990b5da181",
                    "include": True,
                    "type": 2,
                    "familyOrNvt": "1.3.6.1.4.1.25623.1.0.14259",
                },
            ],
        )

        self.assertEqual(scan_config['nvtGrowing'], False)
        self.assertEqual(scan_config['familyGrowing'], True)


class ScanConfigGetEntityTestCase(SeleneTestCase):
    gmp_name = 'config'
    selene_name = 'scanConfig'
    test_get_entity = make_test_get_entity(
        gmp_name, selene_name=selene_name, tasks=True
    )
