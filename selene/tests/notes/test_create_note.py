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


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class NoteTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            mutation {
                createNote (input: {text: "Test Note",
                                    nvtOid: "1.3.6.1.4.1.25623.1.0.112826"}) {
                    id
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_create_note(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'create_note',
            '''
            <create_note_response status="201" status_text="OK,
            resource created" id="e1438fb2-ab2c-4f4a-ad6b-de97005256e8"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            mutation {
                createNote (input: {text: "Test Note",
                                    nvtOid: "1.3.6.1.4.1.25623.1.0.112826",
                                    daysActive: 2,
                                    hosts: ["127.0.0.1"],
                                    resultId:
                                      "74555f56-6d00-47c2-b229-54bdf8c3fe9e",
                                    port: "general/tcp",
                                    severity: 0.0,
                                    taskId:
                                      "c05a764c-bea6-4555-b24e-fbd9c741501c"}) {
                    id
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        note_id = json['data']['createNote']['id']
        self.assertEqual(note_id, 'e1438fb2-ab2c-4f4a-ad6b-de97005256e8')

        mock_gmp.gmp_protocol.create_note.assert_called_with(
            "Test Note",
            "1.3.6.1.4.1.25623.1.0.112826",
            days_active=2,
            hosts=["127.0.0.1"],
            port="general/tcp",
            result_id="74555f56-6d00-47c2-b229-54bdf8c3fe9e",
            severity=0.0,
            task_id="c05a764c-bea6-4555-b24e-fbd9c741501c",
        )

    def test_create_note_minimal(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'create_note',
            '''
            <create_note_response status="201" status_text="OK,
            resource created" id="e1438fb2-ab2c-4f4a-ad6b-de97005256e8"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            mutation {
                createNote (input: {text: "Test Note",
                                    nvtOid: "1.3.6.1.4.1.25623.1.0.112826"}) {
                    id
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        note_id = json['data']['createNote']['id']
        self.assertEqual(note_id, 'e1438fb2-ab2c-4f4a-ad6b-de97005256e8')
        mock_gmp.gmp_protocol.create_note.assert_called_with(
            "Test Note",
            "1.3.6.1.4.1.25623.1.0.112826",
            days_active=None,
            hosts=None,
            port=None,
            result_id=None,
            severity=None,
            task_id=None,
        )
