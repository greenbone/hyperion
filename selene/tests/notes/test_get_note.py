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
class NoteTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                note(id: "08b69003-5fc2-4037-a479-93b440211c73") {
                    id
                    text
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_note(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_note',
            '''
            <get_note_response>
                <note id="08b69003-5fc2-4037-a479-93b440211c73">
                    <text>Hello World</text>
                    <owner><name>Foo</name></owner>
                    <creation_time>2020-06-30T09:16:25Z</creation_time>
                    <modification_time>2020-07-30T09:16:25Z</modification_time>
                    <writable>1</writable>
                    <in_use>1</in_use>
                    <active>1</active>
                    <orphan>0</orphan>
                    <hosts>123.456.789.1,123.456.789.2</hosts>
                    <severity>5.5</severity>
                </note>
            </get_note_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                note(id: "08b69003-5fc2-4037-a479-93b440211c73") {
                    id
                    text
                    owner
                    creationTime
                    modificationTime
                    writable
                    inUse
                    active
                    orphan
                    hosts
                    severity
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        note = json['data']['note']

        self.assertEqual(note['id'], '08b69003-5fc2-4037-a479-93b440211c73')
        self.assertEqual(note['text'], 'Hello World')
        self.assertEqual(note['owner'], 'Foo')
        self.assertEqual(note['creationTime'], '2020-06-30T09:16:25+00:00')
        self.assertEqual(note['modificationTime'], '2020-07-30T09:16:25+00:00')
        self.assertEqual(note['writable'], True)
        self.assertEqual(note['inUse'], True)
        self.assertEqual(note['active'], True)
        self.assertEqual(note['orphan'], False)
        self.assertListEqual(note['hosts'], ['123.456.789.1', '123.456.789.2'])
        self.assertEqual(note['severity'], 5.5)

    def test_get_note_without_hosts(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_note',
            '''
            <get_note_response>
                <note id="08b69003-5fc2-4037-a479-93b440211c73">
                    <text>Hello World</text>
                </note>
            </get_note_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                note(id: "08b69003-5fc2-4037-a479-93b440211c73") {
                    hosts
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        note = json['data']['note']

        self.assertListEqual(note['hosts'], [])
