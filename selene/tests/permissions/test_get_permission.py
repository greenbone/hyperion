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

# pylint: disable=line-too-long

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory
from selene.tests.entity import make_test_get_entity


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class GetPermissionTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                permission(
                    id: "6fe1f935-d8eb-4b78-a1d7-1fce90af227c",
                ) {
                    name
                    id
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_permission(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_permission',
            '''
            <get_permissions_response status="200" status_text="OK">
            <permission id="ecade4f9-cc42-4f51-b5db-7cbcf90fc8b6">
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
            </get_permissions_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                permission(
                    id: "6fe1f935-d8eb-4b78-a1d7-1fce90af227c",
                ) {
                    # inherited entity fields
                    id
                    owner
                    name
                    comment
                    writable
                    inUse
                    creationTime
                    modificationTime
                    permissions
                    {
                        name
                    }
                    userTags
                    {
                        count
                        tags {
                            value
                            comment
                        }
                    }
                    # new fields
                    resource
                    {
                    id
                    name
                    type
                    trash
                    deleted
                    permissions
                    {
                        name
                    }
                    }
                    subject
                    {
                        id
                        name
                        type
                        trash
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        permission = json['data']['permission']

        # Entity fields
        self.assertEqual(permission['name'], 'get_tasks')
        self.assertEqual(
            permission['id'], "ecade4f9-cc42-4f51-b5db-7cbcf90fc8b6"
        )
        self.assertEqual(permission['owner'], 'myuser')
        self.assertEqual(permission['comment'], None)
        self.assertEqual(permission['writable'], True)
        self.assertEqual(permission['inUse'], False)
        self.assertEqual(
            permission['creationTime'], "2020-11-09T09:44:23+00:00"
        )
        self.assertEqual(
            permission['modificationTime'], "2020-11-09T09:44:23+00:00"
        )
        self.assertEqual(permission['permissions'], [{"name": "Everything"}])
        self.assertEqual(permission['userTags'], None)
        # Resource and Subject field
        self.assertEqual(
            permission['resource'],
            {
                "id": "df479236-1803-4e46-9014-2981ba9e15b1",
                "name": "task Clone 1",
                "type": "task",
                "trash": False,
                "deleted": False,
                "permissions": None,
            },
        )
        self.assertEqual(
            permission['subject'],
            {
                "id": "f8d47c31-e63f-4d3b-a5e8-0aa2f56ba2a0",
                "name": "myuser",
                "type": "user",
                "trash": False,
            },
        )

        mock_gmp.gmp_protocol.get_permission.assert_called_with(
            "6fe1f935-d8eb-4b78-a1d7-1fce90af227c"
        )


class PermissionGetEntityTestCase(SeleneTestCase):
    gmp_name = 'permission'
    selene_name = 'permission'
    test_get_entity = make_test_get_entity(gmp_name, selene_name=selene_name)
