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
class OverrideTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                override(id: "08b69003-5fc2-4037-a479-93b440211c73") {
                    id
                    text
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_override(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_override',
            '''
            <get_override_response>
                <override id="08b69003-5fc2-4037-a479-93b440211c73">
                    <text>Han shot first</text>
                    <owner><name>Han</name></owner>
                    <creation_time>2020-06-30T09:16:25Z</creation_time>
                    <modification_time>2020-07-30T09:16:25Z</modification_time>
                    <writable>1</writable>
                    <in_use>1</in_use>
                    <active>1</active>
                    <orphan>0</orphan>
                    <nvt><name>Greedo</name></nvt>
                    <hosts>123.456.789.1,123.456.789.2</hosts>
                    <severity>5.5</severity>
                    <new_severity>10</new_severity>
                </override>
            </get_override_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                override(id: "08b69003-5fc2-4037-a479-93b440211c73") {
                    id
                    text
                    owner
                    creationTime
                    modificationTime
                    writable
                    inUse
                    active
                    orphan
                    name
                    hosts
                    severity
                    newSeverity
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        override = json['data']['override']

        self.assertEqual(override['id'], '08b69003-5fc2-4037-a479-93b440211c73')
        self.assertEqual(override['text'], 'Han shot first')
        self.assertEqual(override['owner'], 'Han')
        self.assertEqual(override['creationTime'], '2020-06-30T09:16:25+00:00')
        self.assertEqual(
            override['modificationTime'], '2020-07-30T09:16:25+00:00'
        )
        self.assertEqual(override['writable'], True)
        self.assertEqual(override['inUse'], True)
        self.assertEqual(override['active'], True)
        self.assertEqual(override['orphan'], False)
        self.assertEqual(override['name'], 'Greedo')
        self.assertListEqual(
            override['hosts'], ['123.456.789.1', '123.456.789.2']
        )
        self.assertEqual(override['severity'], 5.5)
        self.assertEqual(override['newSeverity'], 10)

    def test_get_override_with_no_hosts(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_override',
            '''
            <get_override_response>
                <override id="08b69003-5fc2-4037-a479-93b440211c73">
                    <text>Han shot first</text>
                    <owner><name>Han</name></owner>
                    <creation_time>2020-06-30T09:16:25Z</creation_time>
                    <modification_time>2020-07-30T09:16:25Z</modification_time>
                    <writable>1</writable>
                    <in_use>1</in_use>
                    <active>1</active>
                    <orphan>0</orphan>
                    <nvt><name>Greedo</name></nvt>
                    <severity>5.5</severity>
                    <new_severity>10</new_severity>
                </override>
            </get_override_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                override(id: "08b69003-5fc2-4037-a479-93b440211c73") {
                    hosts
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        override = json['data']['override']

        self.assertListEqual(override['hosts'], [])
