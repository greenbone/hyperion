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
class GetCredentialTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
               credential (id: "daba56c8-73ec-11df-a475-002264764cea",
               ) {
                    name
            	    id
               }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_credential(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_credential',
            '''
            <get_credential_response status="200" status_text="OK">
                <credential id="daba56c8-73ec-11df-a475-002264764cea">
                    <owner>
                        <name>admin</name>
                    </owner>
                    <name>foo</name>
                    <comment/>
                    <creation_time>2020-08-06T11:27:19Z</creation_time>
                    <modification_time>2020-08-06T11:27:19Z</modification_time>
                    <writable>1</writable>
                    <in_use>1</in_use>
                    <permissions>
                        <permission>
                            <name>Everything</name>
                        </permission>
                    </permissions>
                    <user_tags>
                        <count>1</count>
                        <tag id="fb8b57d4-7c0a-40c0-bc39-c330816c4f79">
                            <name>credential:foo</name>
                            <value/>
                            <comment/>
                        </tag>
                    </user_tags>
                    <allow_insecure>0</allow_insecure>
                    <login>username</login>
                    <type>up</type>
                </credential>
            </get_credential_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
               credential (id: "daba56c8-73ec-11df-a475-002264764cea",
               ) {
                    id
                    name
                    allowInsecure
                    login
                    type
                    authAlgorithm
                    privacyAlgorithm
               }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        credential = json['data']['credential']

        self.assertEqual(
            credential['id'], "daba56c8-73ec-11df-a475-002264764cea"
        )
        self.assertEqual(credential['name'], 'foo')
        self.assertFalse(credential['allowInsecure'])
        self.assertEqual(credential['login'], 'username')
        self.assertEqual(credential['type'], 'USERNAME_PASSWORD')
        self.assertIsNone(credential['authAlgorithm'])
        self.assertIsNone(credential['privacyAlgorithm'])

    def test_get_credential_with_algorithm(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_credential',
            '''
            <get_credential_response status="200" status_text="OK">
                <credential id="472b4d2c-0c22-4d60-9aa2-e03d4e3b3e92">
                    <owner>
                        <name>admin</name>
                    </owner>
                    <name>lorem</name>
                    <comment/>
                    <creation_time>2020-08-10T14:14:44Z</creation_time>
                    <modification_time>2020-08-10T14:14:44Z</modification_time>
                    <writable>1</writable>
                    <in_use>0</in_use>
                    <permissions>
                        <permission>
                            <name>Everything</name>
                        </permission>
                    </permissions>
                    <allow_insecure>0</allow_insecure>
                    <login>username</login>
                    <type>snmp</type>
                    <auth_algorithm>sha1</auth_algorithm>
                    <privacy>
                        <algorithm>aes</algorithm>
                    </privacy>
                </credential>
            </get_credential_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
               credential (id: "472b4d2c-0c22-4d60-9aa2-e03d4e3b3e92",
               ) {
                    id
                    name
                    allowInsecure
                    login
                    type
                    authAlgorithm
                    privacyAlgorithm
               }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        credential = json['data']['credential']

        self.assertEqual(
            credential['id'], "472b4d2c-0c22-4d60-9aa2-e03d4e3b3e92"
        )
        self.assertEqual(credential['name'], 'lorem')
        self.assertFalse(credential['allowInsecure'])
        self.assertEqual(credential['login'], 'username')
        self.assertEqual(credential['type'], 'SNMP')
        self.assertEqual(credential['authAlgorithm'], 'SHA1')
        self.assertEqual(credential['privacyAlgorithm'], 'AES')

    def test_get_credential_with_scanners(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_credential',
            '''
            <get_credential_response status="200" status_text="OK">
                <credential id="daba56c8-73ec-11df-a475-002264764cea">
                    <owner>
                        <name>admin</name>
                    </owner>
                    <name>foo</name>
                    <comment/>
                    <creation_time>2020-08-06T11:27:19Z</creation_time>
                    <modification_time>2020-08-06T11:27:19Z</modification_time>
                    <writable>1</writable>
                    <in_use>1</in_use>
                    <permissions>
                        <permission>
                            <name>Everything</name>
                        </permission>
                    </permissions>
                    <user_tags>
                        <count>1</count>
                        <tag id="fb8b57d4-7c0a-40c0-bc39-c330816c4f79">
                            <name>credential:foo</name>
                            <value/>
                            <comment/>
                        </tag>
                    </user_tags>
                    <scanners>
                        <scanner id="08b69003-5fc2-4037-a479-93b440211c73">
                            <name>OpenVAS Default</name>
                        </scanner>
                    </scanners>
                    <allow_insecure>0</allow_insecure>
                    <login>username</login>
                    <type>up</type>
                </credential>
            </get_credential_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                credential (
                    id: "daba56c8-73ec-11df-a475-002264764cea",
                ) {
                    id
                    name
                    allowInsecure
                    login
                    type
                    authAlgorithm
                    privacyAlgorithm
                    scanners {
                        id
                        name
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        credential = json['data']['credential']

        self.assertEqual(
            credential['id'], "daba56c8-73ec-11df-a475-002264764cea"
        )
        self.assertEqual(credential['name'], 'foo')
        self.assertFalse(credential['allowInsecure'])
        self.assertEqual(credential['login'], 'username')
        self.assertEqual(credential['type'], 'USERNAME_PASSWORD')
        self.assertIsNone(credential['authAlgorithm'])
        self.assertIsNone(credential['privacyAlgorithm'])
        self.assertIsNotNone(credential['scanners'])
        scanners = credential['scanners']
        self.assertEqual(len(scanners), 1)
        scanner = credential['scanners'][0]
        self.assertEqual(scanner["id"], "08b69003-5fc2-4037-a479-93b440211c73")
        self.assertEqual(scanner["name"], "OpenVAS Default")

    def test_get_credential_with_targets(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_credential',
            '''
            <get_credential_response status="200" status_text="OK">
                <credential id="daba56c8-73ec-11df-a475-002264764cea">
                    <owner>
                        <name>admin</name>
                    </owner>
                    <name>foo</name>
                    <comment/>
                    <creation_time>2020-08-06T11:27:19Z</creation_time>
                    <modification_time>2020-08-06T11:27:19Z</modification_time>
                    <writable>1</writable>
                    <in_use>1</in_use>
                    <permissions>
                        <permission>
                            <name>Everything</name>
                        </permission>
                    </permissions>
                    <user_tags>
                        <count>1</count>
                        <tag id="fb8b57d4-7c0a-40c0-bc39-c330816c4f79">
                            <name>credential:foo</name>
                            <value/>
                            <comment/>
                        </tag>
                    </user_tags>
                    <allow_insecure>0</allow_insecure>
                    <login>username</login>
                    <type>up</type>
                    <targets>
                        <target id="a1f478c1-27d0-4d8c-959f-150625186421">
                            <name>foo</name>
                        </target>
                    </targets>
                </credential>
            </get_credential_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                credential (
                    id: "daba56c8-73ec-11df-a475-002264764cea",
                ) {
                    id
                    name
                    allowInsecure
                    login
                    type
                    authAlgorithm
                    privacyAlgorithm
                    targets {
                        id
                        name
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        credential = json['data']['credential']

        self.assertEqual(
            credential['id'], "daba56c8-73ec-11df-a475-002264764cea"
        )
        self.assertEqual(credential['name'], 'foo')
        self.assertFalse(credential['allowInsecure'])
        self.assertEqual(credential['login'], 'username')
        self.assertEqual(credential['type'], 'USERNAME_PASSWORD')
        self.assertIsNone(credential['authAlgorithm'])
        self.assertIsNone(credential['privacyAlgorithm'])
        self.assertIsNotNone(credential['targets'])
        targets = credential['targets']
        self.assertEqual(len(targets), 1)
        target = credential['targets'][0]
        self.assertEqual(target["id"], "a1f478c1-27d0-4d8c-959f-150625186421")
        self.assertEqual(target["name"], "foo")


class CredentialGetEntityTestCase(SeleneTestCase):
    gmp_name = 'credential'
    test_get_entity = make_test_get_entity(
        gmp_name, scanners=True, targets=True
    )
