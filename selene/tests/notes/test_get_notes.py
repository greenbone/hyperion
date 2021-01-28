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

from selene.schema.notes.queries import GetNotes


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class NoteTestCase(SeleneTestCase):
    def setUp(self):
        self.xml = '''
            <get_note_response>
                <note id="08b69003-5fc2-4037-a479-93b440211c73">
                    <text>foo</text>
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
                <note id="6b2db524-9fb0-45b8-9b56-d958f84cb546">
                    <text>bar</text>
                    <owner><name>Lorem</name></owner>
                    <creation_time>2020-06-30T09:16:25Z</creation_time>
                    <modification_time>2020-07-30T09:16:25Z</modification_time>
                    <writable>1</writable>
                    <in_use>1</in_use>
                    <active>1</active>
                    <orphan>0</orphan>
                    <hosts>123.456.789.3,123.456.789.4</hosts>
                    <severity>5.5</severity>
                </note>
                <note_count>
                    20
                    <filtered>2</filtered>
                </note_count>
                <notes max="10" start="1"/>
            </get_note_response>
            '''

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                notes {
                    nodes {
                        id
                        text
                    }
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_notes(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_notes', self.xml)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                notes {
                    nodes {
                        id
                        text
                        creationTime
                        modificationTime
                        active
                        inUse
                        orphan
                        writable
                        hosts
                        owner
                        severity
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        notes = json['data']['notes']['nodes']

        self.assertEqual(len(notes), 2)

        note1 = notes[0]
        note2 = notes[1]

        self.assertEqual(note1['id'], '08b69003-5fc2-4037-a479-93b440211c73')
        self.assertEqual(note1['text'], 'foo')
        self.assertEqual(note1['creationTime'], '2020-06-30T09:16:25+00:00')
        self.assertEqual(note1['modificationTime'], '2020-07-30T09:16:25+00:00')
        self.assertEqual(note1['active'], True)
        self.assertEqual(note1['owner'], 'Foo')
        self.assertEqual(note1['inUse'], True)
        self.assertEqual(note1['orphan'], False)
        self.assertEqual(note1['writable'], True)
        self.assertListEqual(note1['hosts'], ['123.456.789.1', '123.456.789.2'])
        self.assertEqual(note1['severity'], 5.5)

        self.assertEqual(note2['id'], '6b2db524-9fb0-45b8-9b56-d958f84cb546')
        self.assertEqual(note2['text'], 'bar')
        self.assertEqual(note2['creationTime'], '2020-06-30T09:16:25+00:00')
        self.assertEqual(note2['modificationTime'], '2020-07-30T09:16:25+00:00')
        self.assertEqual(note2['active'], True)
        self.assertEqual(note2['owner'], 'Lorem')
        self.assertEqual(note2['inUse'], True)
        self.assertEqual(note2['orphan'], False)
        self.assertEqual(note2['writable'], True)
        self.assertEqual(note2['hosts'], ['123.456.789.3', '123.456.789.4'])
        self.assertEqual(note2['severity'], 5.5)

    def test_get_filtered_notes(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_notes', self.xml)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                notes (
                    filterString: "lorem",
                ) {
                    nodes {
                        id
                        text
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        notes = json['data']['notes']['nodes']

        self.assertEqual(len(notes), 2)

        note1 = notes[0]
        note2 = notes[1]

        self.assertEqual(note1['id'], '08b69003-5fc2-4037-a479-93b440211c73')
        self.assertEqual(note1['text'], 'foo')

        self.assertEqual(note2['id'], '6b2db524-9fb0-45b8-9b56-d958f84cb546')
        self.assertEqual(note2['text'], 'bar')


class NotesPaginationTestCase(SeleneTestCase):
    entity_name = 'note'
    test_pagination_with_after_and_first = make_test_after_first(
        entity_name, details=True
    )
    test_counts = make_test_counts(entity_name)
    test_page_info = make_test_page_info(entity_name, query=GetNotes)
    test_pagination_with_before_and_last = make_test_before_last(
        entity_name, details=True
    )
    test_edges = make_test_edges(entity_name)
    test_after_first_before_last = make_test_after_first_before_last(
        entity_name, details=True
    )
