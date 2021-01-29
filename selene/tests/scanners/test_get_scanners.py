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

from pathlib import Path

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory

from selene.tests.pagination import (
    make_test_counts,
    make_test_after_first,
    make_test_page_info,
    make_test_edges,
    make_test_before_last,
    make_test_after_first_before_last,
)

from selene.tests.entity import make_test_get_entities

from selene.schema.scanners.queries import GetScanners

CWD = Path(__file__).absolute().parent


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class ScannersTestCase(SeleneTestCase):
    def setUp(self):
        self.xml = '''
            <get_scanners_response>
                <scanner id="08b69003-5fc2-4037-a479-93b440211c73">
                    <name>a</name>
                    <type>2</type>
                </scanner>
                <scanner id="6b2db524-9fb0-45b8-9b56-d958f84cb546">
                    <name>b</name>
                    <type>1</type>
                </scanner>
            </get_scanners_response>
            '''

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                scanners {
                    nodes {
                        id
                        name
                        type
                    }
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_scanners(self, mock_gmp: GmpMockFactory):
        scanners_xml_path = CWD / 'example-scanner-list.xml'
        scanners_xml_str = scanners_xml_path.read_text()

        mock_gmp.mock_response('get_scanners', scanners_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                scanners {
                    nodes {
                        id
                        name
                        type
                        host
                        port
                        configs {
                            name
                        }
                        tasks {
                            name
                        }
                        credential {
                            name
                        }
                        caPub {
                            certificate
                            info {
                                activationTime
                                expirationTime
                                issuer
                                md5Fingerprint
                                timeStatus
                            }
                        }
                        info{
                            scanner{
                                name
                                version
                            }
                            daemon{
                                name
                                version
                            }
                            protocol{
                                name
                                version
                            }
                            description
                            params {
                                id
                                name
                                default
                                description
                                type
                                mandatory
                            }
                        }
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        scanners = json['data']['scanners']['nodes']

        self.assertEqual(len(scanners), 2)

        scanner1 = scanners[0]
        scanner2 = scanners[1]

        # scanner 1
        self.assertEqual(scanner1['id'], '08b69003-5fc2-4037-a479-93b440211c73')
        self.assertEqual(scanner1['name'], 'OpenVAS Default')

        self.assertEqual(scanner1['type'], "OPENVAS_SCANNER_TYPE")

        self.assertEqual(
            scanner1['host'],
            '/home/sdiedrich/install/var/run/ospd-openvas.sock',
        )
        self.assertEqual(scanner1['port'], '0')

        self.assertIsNone(scanner1['configs'])

        tasks = scanner1['tasks']
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0]['name'], '012345')

        self.assertIsNone(scanner1['credential']['name'])

        info = scanner1['info']

        self.assertIsNotNone(info['description'])

        scanner_info = info['scanner']
        self.assertEqual(scanner_info['name'], 'openvas')
        self.assertEqual(scanner_info['version'], 'OpenVAS 7.0.0')

        daemon_info = info['daemon']
        self.assertEqual(daemon_info['name'], 'OSPd OpenVAS')
        self.assertEqual(daemon_info['version'], '20.8a1')

        protocol_info = info['protocol']
        self.assertEqual(protocol_info['name'], 'OSP')
        self.assertEqual(protocol_info['version'], '1.2')

        params = info['params']
        self.assertEqual(len(params), 19)

        self.assertEqual(params[0]['id'], "debug_mode")
        self.assertEqual(params[0]['name'], "Debug Mode")
        self.assertEqual(params[0]['default'], "0")
        self.assertEqual(
            params[0]['description'],
            "Whether to get extra scan debug information.",
        )
        self.assertEqual(params[0]['type'], "osp_boolean")
        self.assertFalse(params[0]['mandatory'])

        # scanner 2
        self.assertEqual(scanner2['id'], '6b2db524-9fb0-45b8-9b56-d958f84cb546')
        self.assertEqual(scanner2['name'], 'OSP Scanner-openvas')

        self.assertEqual(scanner2['type'], "OSP_SCANNER_TYPE")

        self.assertEqual(scanner2['host'], '127.0.0.1')
        self.assertEqual(scanner2['port'], '2346')

        configs = scanner2['configs']
        self.assertEqual(len(configs), 3)
        self.assertEqual(configs[0]['name'], 'Base 2')

        self.assertIsNone(scanner2['tasks'])

        credential = scanner2['credential']
        self.assertEqual(
            credential['name'], 'Credential for Scanner OSP Scanner-openvas'
        )

        ca_pub = scanner2['caPub']
        self.assertIsNotNone(ca_pub['certificate'])

        info = ca_pub['info']
        self.assertEqual(info['activationTime'], '2019-07-19T13:28:23+00:00')
        self.assertEqual(info['expirationTime'], '2020-07-18T13:28:23+00:00')
        self.assertEqual(info['issuer'], 'CN=localhost')
        self.assertEqual(
            info['md5Fingerprint'],
            '09:9f:2e:5c:27:93:be:75:25:55:f9:57:15:44:3d:e0',
        )
        self.assertEqual(info['timeStatus'], 'valid')

    def test_get_filtered_scanners(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_scanners', self.xml)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                scanners (
                    filterString: "lorem",
                ) {
                    nodes {
                        id
                        name
                        type
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        scanners = json['data']['scanners']['nodes']

        self.assertEqual(len(scanners), 2)

        scanner1 = scanners[0]
        scanner2 = scanners[1]

        self.assertEqual(scanner1['name'], 'a')
        self.assertEqual(scanner1['type'], "OPENVAS_SCANNER_TYPE")
        self.assertEqual(scanner1['id'], '08b69003-5fc2-4037-a479-93b440211c73')
        self.assertEqual(scanner2['name'], 'b')
        self.assertEqual(scanner2['type'], "OSP_SCANNER_TYPE")
        self.assertEqual(scanner2['id'], '6b2db524-9fb0-45b8-9b56-d958f84cb546')


class ScannersPaginationTestCase(SeleneTestCase):
    entity_name = 'scanner'
    test_pagination_with_after_and_first = make_test_after_first(
        entity_name, details=True
    )
    test_counts = make_test_counts(entity_name)
    test_page_info = make_test_page_info(entity_name, query=GetScanners)
    test_pagination_with_before_and_last = make_test_before_last(
        entity_name, details=True
    )
    test_edges = make_test_edges(entity_name)
    test_after_first_before_last = make_test_after_first_before_last(
        entity_name, details=True
    )


class ScannerGetEntitiesTestCase(SeleneTestCase):
    gmp_name = 'scanner'
    test_get_entities = make_test_get_entities(gmp_name, details=True)
