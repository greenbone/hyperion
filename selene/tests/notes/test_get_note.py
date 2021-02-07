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

# from selene.tests.entity import make_test_get_entity

CWD = Path(__file__).absolute().parent


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

    def test_query_name_in_note(self, _mock_gmp: GmpMockFactory):

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                note(id: "5221d57f-3e62-4114-8e19-135a79b6b102") {
                    name
                }
            }
            '''
        )

        self.assertResponseHasErrorMessage(
            response, 'Cannot query field "name" on type "Note".'
        )

    def test_get_note(self, mock_gmp: GmpMockFactory):
        note_xml_path = CWD / 'example-note.xml'
        note_xml_str = note_xml_path.read_text()

        mock_gmp.mock_response('get_note', note_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                note(id: "a4793d3d-b9a7-4b79-8dab-f1ecce14aee6") {
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
                    endTime
                    severity
                    nvt {
                        id
                        name
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        note = json['data']['note']

        self.assertEqual(note['id'], 'a4793d3d-b9a7-4b79-8dab-f1ecce14aee6')
        self.assertEqual(note['text'], 'wetert')
        self.assertEqual(note['active'], True)
        self.assertEqual(note['orphan'], False)
        self.assertListEqual(note['hosts'], ['127.0.0.1', '1.3.3.7'])
        self.assertEqual(note['severity'], 0.1)

        self.assertEqual(note['endTime'], '2021-03-07T11:13:55+01:00')
        self.assertIsNotNone(note['nvt'])
        nvt = note['nvt']
        self.assertEqual(nvt['id'], '1.3.6.1.4.1.25623.1.0.117130')
        self.assertEqual(
            nvt['name'],
            'Cisco WebEx Meetings Server Unauthorized Meeting Actions '
            'Vulnerability (Cisco-SA-20140129-CVE-2014-0682)',
        )

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


class NoteGetEntityTestCase(SeleneTestCase):
    gmp_name = 'note'
    # test_get_entity = make_test_get_entity(
    #     gmp_name,
    # )
