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

from uuid import uuid4

from pathlib import Path

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory

CWD = Path(__file__).absolute().parent


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class TagTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        tag_id = uuid4()
        response = self.query(
            f'''
            query {{
                tag(id: "{tag_id}") {{
                    id
                    name
                    value
                    comment
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_tag(self, mock_gmp: GmpMockFactory):
        tag_id = uuid4()
        mock_gmp.mock_response(
            'get_tag',
            f'''
            <get_tags_response>
                <tag id="{tag_id}">
                    <name>cat</name>
                    <comment>dog</comment>
                    <value>goat</value>
                </tag>
            </get_tags_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            query {{
                tag(id: "{tag_id}") {{
                    id
                    name
                    value
                    comment
                }}
            }}
            '''
        )
        json = response.json()

        self.assertResponseNoErrors(response)

        tag = json['data']['tag']

        self.assertEqual(tag['id'], str(tag_id))
        self.assertEqual(tag['name'], 'cat')
        self.assertEqual(tag['comment'], 'dog')
        self.assertEqual(tag['value'], 'goat')
