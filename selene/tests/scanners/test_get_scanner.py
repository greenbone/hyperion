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

from selene.tests.entity import make_test_get_entity

CWD = Path(__file__).absolute().parent


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class ScannerTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                scanner(id: "08b69003-5fc2-4037-a479-93b440211c73") {
                    id
                    name
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_scanner(self, mock_gmp: GmpMockFactory):
        scanner_xml_path = CWD / 'example-scanner.xml'
        scanner_xml_str = scanner_xml_path.read_text()

        mock_gmp.mock_response('get_scanner', scanner_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                scanner(id: "08b69003-5fc2-4037-a479-93b440211c73"){
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
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        scanner = json['data']['scanner']

        self.assertEqual(scanner['id'], '08b69003-5fc2-4037-a479-93b440211c73')
        self.assertEqual(scanner['name'], 'OpenVAS Default')

        self.assertEqual(scanner['type'], "OPENVAS_SCANNER_TYPE")

        self.assertEqual(
            scanner['host'], '/home/sdiedrich/install/var/run/ospd-openvas.sock'
        )
        self.assertEqual(scanner['port'], '0')

        self.assertIsNone(scanner['configs'])

        tasks = scanner['tasks']
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0]['name'], '012345')

        self.assertIsNone(scanner['credential']['name'])

        info = scanner['info']

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

    def test_get_scanner_with_certificate(self, mock_gmp: GmpMockFactory):
        scanner_xml_path = CWD / 'example-scanner-2.xml'
        scanner_xml_str = scanner_xml_path.read_text()

        mock_gmp.mock_response('get_scanner', scanner_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                scanner(id: "08b69003-5fc2-4037-a479-93b440211c73"){
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
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        scanner = json['data']['scanner']

        self.assertEqual(scanner['id'], '6b2db524-9fb0-45b8-9b56-d958f84cb546')
        self.assertEqual(scanner['name'], 'OSP Scanner-openvas')

        self.assertEqual(scanner['type'], "OSP_SCANNER_TYPE")

        self.assertEqual(scanner['host'], '127.0.0.1')
        self.assertEqual(scanner['port'], '2346')

        configs = scanner['configs']
        self.assertEqual(len(configs), 3)
        self.assertEqual(configs[0]['name'], 'Base 2')

        self.assertIsNone(scanner['tasks'])

        credential = scanner['credential']
        self.assertEqual(
            credential['name'], 'Credential for Scanner OSP Scanner-openvas'
        )

        ca_pub = scanner['caPub']
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


class ScannerGetEntityTestCase(SeleneTestCase):
    gmp_name = 'scanner'
    test_get_entity = make_test_get_entity(gmp_name)
