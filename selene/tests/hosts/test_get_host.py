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

from gvm.protocols.next import AssetType

from selene.tests import SeleneTestCase, GmpMockFactory

from selene.tests.entity import make_test_get_entity

CWD = Path(__file__).absolute().parent


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class HostTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                host(id: "05d1edfa-3df8-11ea-9651-7b09b3acce77") {
                    id
                    name
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_host(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_asset',
            '''
            <get_assets_response>
                <asset id="75d23ba8-3d23-11ea-858e-b7c2cb43e815">
                    <name>a</name>
                </asset>
            </get_assets_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                host(id: "75d23ba8-3d23-11ea-858e-b7c2cb43e815") {
                    id
                    name
                    owner
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        host = json['data']['host']

        self.assertEqual(host['name'], 'a')
        self.assertEqual(host['id'], '75d23ba8-3d23-11ea-858e-b7c2cb43e815')
        self.assertIsNone(host['owner'])

    def test_complex_host(self, mock_gmp: GmpMockFactory):
        host_xml_path = CWD / 'example-host.xml'
        host_xml_str = host_xml_path.read_text()

        mock_gmp.mock_response('get_asset', host_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                host(id: "291a7547-c817-4b46-88f2-32415d825335") {
                    id
                    name
                    severity
                    identifiers {
                        id
                        name
                        value
                        creationTime
                        modificationTime
                        sourceId
                        sourceName
                        sourceType
                        sourceData
                        sourceDeleted
                        osId
                        osTitle
                    }
                    details {
                        name
                        value
                        source {
                            id
                            name
                            type
                            description
                        }
                        extra
                    }
                    routes {
                        hosts {
                            id
                            ip
                            distance
                            sameSource
                        }
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        host = json['data']['host']

        self.assertEqual(host['name'], 'xyzxy')
        self.assertEqual(host['id'], 'd8c5fc4f-c01b-48aa-854b-cfe4bc9fb8c6')
        self.assertEqual(host['severity'], 7.5)

        identifiers = host['identifiers']
        identifier = identifiers[1]

        self.assertEqual(
            identifier['id'], 'd2f59ef2-5ae4-4a74-857b-2a639955d28c'
        )
        self.assertEqual(identifier['name'], 'ip')
        self.assertEqual(identifier['value'], '0.0.0.0')
        self.assertEqual(
            identifier['creationTime'], '2020-06-19T09:34:48+00:00'
        )
        self.assertEqual(
            identifier['modificationTime'], '2020-06-19T09:34:48+00:00'
        )
        self.assertEqual(
            identifier['sourceId'], '3404b586-40be-4a7d-a964-c23c435d9abc'
        )
        self.assertEqual(identifier['sourceType'], 'Report Host')
        self.assertIsNone(identifier['sourceData'])
        self.assertFalse(identifier['sourceDeleted'])
        self.assertIsNone(identifier['sourceName'])
        self.assertIsNone(identifier['osId'])
        self.assertIsNone(identifier['osTitle'])

        self.assertEqual(identifiers[2]['sourceData'], 'CMDB-Parser')

        details = host['details']
        detail = details[0]

        self.assertEqual(detail['name'], 'best_os_cpe')
        self.assertEqual(
            detail['value'], 'cpe:/o:red hat:enterprise_linux_server:7.6'
        )
        self.assertEqual(
            detail['source']['id'], '3404b586-40be-4a7d-a964-c23c435d9abc'
        )
        self.assertEqual(detail['source']['type'], 'Report')
        self.assertIsNone(detail['source']['name'])
        self.assertIsNone(detail['source']['description'])
        self.assertIsNone(detail['extra'])

        self.assertIsNone(host['routes'])


class HostGetEntityTestCase(SeleneTestCase):
    gmp_name = 'asset'
    selene_name = 'host'
    test_get_entity = make_test_get_entity(
        gmp_name, selene_name=selene_name, asset_type=AssetType.HOST
    )
