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

from pathlib import Path

from unittest.mock import patch

from selene.schema.scan_configs.fields import ScanConfigType

from selene.tests import SeleneTestCase, GmpMockFactory

from selene.tests.entity import make_test_get_entity

CWD = Path(__file__).absolute().parent


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

    def test_get_scan_config_none_fields(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_scan_config',
            '''
            <get_config_response status="200" status_text="OK">
                <config id="daba56c8-73ec-11df-a475-002264764cea">
                    <name>foo</name>
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
                    }
                    nvtPreferences{
                        nvt{
                            name
                        }
                        hrName
                    }
                    scannerPreferences{
                        hrName
                    }
                    tasks{
                        id
                    }
                    nvtSelectors{
                        name
                    }
               }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        scan_config = json['data']['scanConfig']

        self.assertIsNone(scan_config['type'])
        self.assertIsNone(scan_config['trash'])
        self.assertIsNone(scan_config['familyCount'])
        self.assertIsNone(scan_config['familyGrowing'])
        self.assertIsNone(scan_config['nvtCount'])
        self.assertIsNone(scan_config['nvtGrowing'])
        self.assertIsNone(scan_config['usageType'])
        self.assertIsNone(scan_config['maxNvtCount'])
        self.assertIsNone(scan_config['knownNvtCount'])
        self.assertIsNone(scan_config['predefined'])
        self.assertIsNone(scan_config['families'])
        self.assertIsNone(scan_config['nvtPreferences'])
        self.assertIsNone(scan_config['scannerPreferences'])
        self.assertIsNone(scan_config['tasks'])
        self.assertIsNone(scan_config['nvtSelectors'])

    def test_get_scan_config(self, mock_gmp: GmpMockFactory):
        scan_config_xml_path = CWD / 'example-scan-config.xml'
        scan_config_xml_str = scan_config_xml_path.read_text()

        mock_gmp.mock_response('get_scan_config', scan_config_xml_str)

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
                    nvtPreferences{
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
                        alternativeValues
                    }
                    scannerPreferences{
                        hrName
                        name
                        id
                        type
                        value
                        default
                        alternativeValues
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
        self.assertEqual(
            scan_config['type'],
            ScanConfigType.OPENVAS.name,  # pylint: disable=no-member
        )
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
            scan_config['nvtPreferences'],
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
                    "alternativeValues": None,
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
                    "alternativeValues": ["Paranoid", "Sneaky"],
                },
            ],
        )
        self.assertEqual(
            scan_config['scannerPreferences'],
            [
                {
                    "name": "auto_enable_dependencies",
                    "id": None,
                    "hrName": "auto_enable_dependencies",
                    "type": None,
                    "value": "1",
                    "default": "1",
                    "alternativeValues": None,
                },
                {
                    "name": "cgi_path",
                    "id": None,
                    "hrName": "cgi_path",
                    "type": None,
                    "value": "/cgi-bin:/scripts",
                    "default": "/cgi-bin:/scripts",
                    "alternativeValues": ["Paranoid", "Sneaky"],
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
    gmp_cmd = 'get_scan_config'
    test_get_entity = make_test_get_entity(
        gmp_name=gmp_name, selene_name=selene_name, gmp_cmd=gmp_cmd, tasks=True
    )
