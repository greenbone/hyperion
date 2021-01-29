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

import string

from uuid import uuid4

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class ExportPermissionsByIdsTestCase(SeleneTestCase):
    def setUp(self):
        self.id1 = uuid4()
        self.id2 = uuid4()
        self.permission_mock_xml = f'''
            <get_permissions_response status="200" status_text="OK">
            <permission id="{self.id1}">
                <owner>
                <name>myuser</name>
                </owner>
                <name>get_tasks</name>
                <comment/>
                <creation_time>2020-11-09T09:44:23Z</creation_time>
                <modification_time>2020-11-09T09:44:23Z</modification_time>
                <writable>1</writable>
                <in_use>0</in_use>
                <permissions>
                <permission>
                    <name>Everything</name>
                </permission>
                </permissions>
                <resource id="df479236-1803-4e46-9014-2981ba9e15b1">
                <name>task Clone 1</name>
                <type>task</type>
                <trash>0</trash>
                <deleted>0</deleted>
                </resource>
                <subject id="f8d47c31-e63f-4d3b-a5e8-0aa2f56ba2a0">
                <name>myuser</name>
                <type>user</type>
                <trash>0</trash>
                </subject>
            </permission>
            <permission id="{self.id2}">
                <owner>
                <name>myuser</name>
                </owner>
                <name>create_agent</name>
                <comment/>
                <creation_time>2020-11-09T09:44:23Z</creation_time>
                <modification_time>2020-11-09T09:44:23Z</modification_time>
                <writable>1</writable>
                <in_use>0</in_use>
                <permissions>
                <permission>
                    <name>Everything</name>
                </permission>
                </permissions>
                <resource id="df479236-1803-4e46-9014-2981ba9e15b1">
                <name>task Clone 1</name>
                <type>task</type>
                <trash>0</trash>
                <deleted>0</deleted>
                </resource>
                <subject id="f8d47c31-e63f-4d3b-a5e8-0aa2f56ba2a0">
                <name>myuser</name>
                <type>user</type>
                <trash>0</trash>
                </subject>
            </permission>
            </get_permissions_response>
            '''

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            f'''
            mutation {{
                exportPermissionsByIds(ids: ["{self.id1}", "{self.id2}"]) {{
                   exportedEntities
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_export_permissions_by_ids(self, mock_gmp: GmpMockFactory):
        self.login('foo', 'bar')

        mock_gmp.mock_response('get_permissions', self.permission_mock_xml)

        response = self.query(
            f'''
            mutation {{
                exportPermissionsByIds(ids: ["{self.id1}", "{self.id2}"]) {{
                   exportedEntities
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        permissions_xml = json['data']['exportPermissionsByIds'][
            'exportedEntities'
        ]

        self.assertEqual(
            self.permission_mock_xml.translate(
                str.maketrans('', '', string.whitespace)
            ),
            permissions_xml.translate(str.maketrans('', '', string.whitespace)),
        )
        mock_gmp.gmp_protocol.get_permissions.assert_called_with(
            filter=f'uuid= uuid={self.id1} uuid={self.id2} ',
        )

    def test_export_empty_ids_array(self, mock_gmp: GmpMockFactory):
        self.login('foo', 'bar')

        mock_gmp.mock_response('get_permissions', self.permission_mock_xml)

        response = self.query(
            '''
            mutation {
                exportPermissionsByIds(ids: []) {
                   exportedEntities
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        permissions_xml = json['data']['exportPermissionsByIds'][
            'exportedEntities'
        ]

        self.assertEqual(
            self.permission_mock_xml.translate(
                str.maketrans('', '', string.whitespace)
            ),
            permissions_xml.translate(str.maketrans('', '', string.whitespace)),
        )

        mock_gmp.gmp_protocol.get_permissions.assert_called_with(
            filter='uuid= ',
        )
