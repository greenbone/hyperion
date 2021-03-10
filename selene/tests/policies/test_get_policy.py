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

from selene.tests import SeleneTestCase, GmpMockFactory

from selene.tests.entity import make_test_get_entity

CWD = Path(__file__).absolute().parent


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class GetPolicyTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
               policy (id: "daba56c8-73ec-11df-a475-002264764cea",
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

    def test_get_policy(self, mock_gmp: GmpMockFactory):
        policy_xml_path = CWD / 'example-policy.xml'
        policy_xml_str = policy_xml_path.read_text()

        mock_gmp.mock_response('get_policy', policy_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
               policy (id: "daba56c8-73ec-11df-a475-002264764cea",
               ) {
                    name
                    type
                    id
                    trash
                    familyCount
                    familyGrowing
                    usageType
                    maxNvtCount
                    nvtGrowing
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

        policy = json['data']['policy']

        self.assertEqual(policy['id'], "daba56c8-73ec-11df-a475-002264764cea")
        self.assertEqual(policy['name'], 'foo')
        self.assertEqual(policy['type'], 0)
        self.assertEqual(policy['trash'], 0)
        self.assertEqual(policy['familyCount'], 2)
        self.assertEqual(policy['usageType'], 'scan')
        self.assertEqual(policy['maxNvtCount'], 249)
        self.assertEqual(policy['knownNvtCount'], 3)
        self.assertEqual(policy['predefined'], True)
        self.assertEqual(
            policy['families'],
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
            policy['nvtPreferences'],
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
            policy['scannerPreferences'],
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
                    "alternativeValues": None,
                },
            ],
        )
        self.assertEqual(
            policy['tasks'],
            [
                {
                    "id": "49d082ec-73f5-4b3a-75b5-3b9d9e38d079",
                    "name": "some_name",
                }
            ],
        )
        self.assertEqual(
            policy['nvtSelectors'],
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

        self.assertEqual(policy['nvtGrowing'], False)
        self.assertEqual(policy['familyGrowing'], True)


class PolicyGetEntityTestCase(SeleneTestCase):
    gmp_name = 'config'
    gmp_cmd = 'get_policy'
    selene_name = 'policy'
    test_get_entity = make_test_get_entity(
        gmp_name,
        selene_name=selene_name,
        gmp_cmd=gmp_cmd,
        audits=True,
    )
