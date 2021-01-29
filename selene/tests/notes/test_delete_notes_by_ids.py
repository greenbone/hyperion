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

from uuid import uuid4

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class DeleteNotesByIdsTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            mutation {
                deleteNotesByIds(
                    ids: ["e1438fb2-ab2c-4f4a-ad6b-de97005256e8"]
                ) {
                   ok
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_delete_notes(self, mock_gmp: GmpMockFactory):
        self.login('foo', 'bar')

        id1 = uuid4()
        id2 = uuid4()

        mock_gmp.mock_response(
            'get_notes',
            f'''
            <get_notes_response status="200" status_text="OK">
                <note id="{id1}">
                    <text>Foo Clone 1</text>
                </note>
                <note id="{id2}">
                    <text>Foo Clone 2</text>
                </note>
            </get_notes_response>
            ''',
        )

        response = self.query(
            f'''
            mutation {{
                deleteNotesByIds(ids: ["{id1}", "{id2}"]) {{
                    ok
                }}
            }}
            '''
        )
        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['deleteNotesByIds']['ok']

        self.assertTrue(ok)

        mock_gmp.gmp_protocol.get_notes.assert_called_with(
            filter=f'uuid={id1} uuid={id2} '
        )

        mock_gmp.gmp_protocol.delete_note.assert_any_call(note_id=str(id1))

        mock_gmp.gmp_protocol.delete_note.assert_any_call(note_id=str(id2))

    def test_delete_notes_invalid(self, mock_gmp: GmpMockFactory):
        self.login('foo', 'bar')

        id1 = uuid4()
        id2 = uuid4()

        # Only one of the requested notes is found.
        mock_gmp.mock_response(
            'get_notes',
            f'''
            <get_notes_response status="200" status_text="OK">
                <note id="{id1}">
                    <text>Foo Clone 1</text>
                </note>
            </get_notes_response>
            ''',
        )

        response = self.query(
            f'''
            mutation {{
                deleteNotesByIds(ids: ["{id1}", "{id2}"]) {{
                    ok
                }}
            }}
            '''
        )
        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['deleteNotesByIds']['ok']

        self.assertFalse(ok)

        mock_gmp.gmp_protocol.get_notes.assert_called_with(
            filter=f'uuid={id1} uuid={id2} '
        )
