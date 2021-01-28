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

from gvm.protocols.latest import AssetType

from selene.tests import SeleneTestCase, GmpMockFactory

from selene.tests.entity import make_test_get_entity

CWD = Path(__file__).absolute().parent


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class OperatingSystemTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                operatingSystem(id: "05d1edfa-3df8-11ea-9651-7b09b3acce77") {
                    id
                    name
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_operating_system(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_asset',
            '''
            <get_assets_response>
                <asset id="75d23ba8-3d23-11ea-858e-b7c2cb43e815">
                    <name>cpe:/h:hp:jetdirect</name>
                </asset>
            </get_assets_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                operatingSystem(id: "75d23ba8-3d23-11ea-858e-b7c2cb43e815") {
                    id
                    name
                    owner
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        operating_system = json['data']['operatingSystem']

        self.assertEqual(operating_system['name'], 'cpe:/h:hp:jetdirect')
        self.assertEqual(
            operating_system['id'], '75d23ba8-3d23-11ea-858e-b7c2cb43e815'
        )
        self.assertIsNone(operating_system['owner'])

    def test_complex_operating_system(self, mock_gmp: GmpMockFactory):
        operating_system_xml_path = CWD / 'example-os.xml'
        operating_system_xml_str = operating_system_xml_path.read_text()

        mock_gmp.mock_response('get_asset', operating_system_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                operatingSystem(id: "291a7547-c817-4b46-88f2-32415d825335") {
                    id
                    name
                    operatingSystemInformation {
                        latestSeverity
                        highestSeverity
                        averageSeverity
                        title
                        installs
                        hostCount
                        hosts {
                            severity
                            id
                            name
                        }
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        operating_system = json['data']['operatingSystem']

        self.assertEqual(operating_system['name'], 'cpe:/h:hp:jetdirect')
        self.assertEqual(
            operating_system['id'], '33c639d9-08ef-4f3c-853f-103ab15fb8c1'
        )

        os_infos = operating_system['operatingSystemInformation']

        self.assertEqual(os_infos['latestSeverity'], 10.0)
        self.assertEqual(os_infos['highestSeverity'], 10.0)
        self.assertEqual(os_infos['averageSeverity'], 10.0)
        self.assertIsNone(os_infos['title'])
        self.assertEqual(os_infos['installs'], 1)
        self.assertEqual(os_infos['hostCount'], 1)
        host = os_infos['hosts'][0]
        self.assertEqual(host['severity'], 10.0)
        self.assertEqual(host['id'], "5725be9b-f911-440b-a450-9f6c8ea0aa8e")
        self.assertEqual(host['name'], '185.190.68.10')


class OperatingSystemGetEntityTestCase(SeleneTestCase):
    gmp_name = 'asset'
    selene_name = 'operatingSystem'
    test_get_entity = make_test_get_entity(
        gmp_name, selene_name=selene_name, asset_type=AssetType.OPERATING_SYSTEM
    )
