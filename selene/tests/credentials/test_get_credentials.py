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

from selene.tests.pagination import (
    make_test_counts,
    make_test_after_first,
    make_test_page_info,
    make_test_before_last,
    make_test_after_first_before_last,
)
from selene.tests.entity import make_test_get_entities

from selene.schema.credentials.queries import GetCredentials


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class CredentialsTestCase(SeleneTestCase):
    def setUp(self):
        self.xml = '''
            <get_credentials_response>
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
            </get_credentials_response>
            '''

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                credentials{
                    nodes {
                        id
                        name
                    }
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_credentials(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_credentials', self.xml)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                credentials {
                    nodes {
                        id
                        name
                        allowInsecure
                        login
                        type
                        authAlgorithm
                        privacyAlgorithm
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        credentials = json['data']['credentials']['nodes']

        self.assertEqual(len(credentials), 2)

        credential1 = credentials[0]
        credential2 = credentials[1]

        # Credential 1

        self.assertEqual(
            credential1['id'], "daba56c8-73ec-11df-a475-002264764cea"
        )
        self.assertEqual(credential1['name'], 'foo')
        self.assertFalse(credential1['allowInsecure'])
        self.assertEqual(credential1['login'], 'username')
        self.assertEqual(credential1['type'], 'USERNAME_PASSWORD')
        self.assertIsNone(credential1['authAlgorithm'])
        self.assertIsNone(credential1['privacyAlgorithm'])

        # Credential 2

        self.assertEqual(
            credential2['id'], "472b4d2c-0c22-4d60-9aa2-e03d4e3b3e92"
        )
        self.assertEqual(credential2['name'], 'lorem')
        self.assertFalse(credential2['allowInsecure'])
        self.assertEqual(credential2['login'], 'username')
        self.assertEqual(credential2['type'], 'SNMP')
        self.assertEqual(credential2['authAlgorithm'], 'SHA1')
        self.assertEqual(credential2['privacyAlgorithm'], 'AES')

    def test_get_filtered_credentials(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_credentials', self.xml)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                credentials (
                    filterString: "lorem",
                ) {
                    nodes {
                        id
                        name
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        credentials = json['data']['credentials']['nodes']

        self.assertEqual(len(credentials), 2)

        credential1 = credentials[0]
        credential2 = credentials[1]

        self.assertEqual(
            credential1['id'], 'daba56c8-73ec-11df-a475-002264764cea'
        )
        self.assertEqual(credential1['name'], 'foo')

        self.assertEqual(
            credential2['id'], '472b4d2c-0c22-4d60-9aa2-e03d4e3b3e92'
        )
        self.assertEqual(credential2['name'], 'lorem')


class CredentialsPaginationTestCase(SeleneTestCase):
    gmp_name = 'credential'
    selene_name = 'credential'
    test_pagination_with_after_and_first = make_test_after_first(
        gmp_name, selene_name=selene_name
    )
    test_counts = make_test_counts(gmp_name, selene_name=selene_name)
    test_page_info = make_test_page_info(
        gmp_name, selene_name=selene_name, query=GetCredentials
    )
    test_pagination_with_before_and_last = make_test_before_last(
        gmp_name, selene_name=selene_name
    )
    test_after_first_before_last = make_test_after_first_before_last(
        gmp_name, selene_name=selene_name
    )


class CredentialGetEntitiesTestCase(SeleneTestCase):
    gmp_name = 'credential'
    test_get_entities = make_test_get_entities(gmp_name)
