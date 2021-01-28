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
class GetRoleTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                role(
                    id: "6fe1f935-d8eb-4b78-a1d7-1fce90af227c",
                ) {
                    name
                    id
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_role(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_role',
            '''
            <get_roles_response status="200" status_text="OK">
            <role id="5be3c376-7577-4bad-bde6-3d07fb9ad027">
                <owner>
                    <name>myuser</name>
                </owner>
                <name>test</name>
                <comment>test</comment>
                <creation_time>2020-09-04T12:53:52Z</creation_time>
                <modification_time>2020-11-10T13:19:36Z</modification_time>
                <writable>1</writable>
                <in_use>0</in_use>
                <permissions>
                <permission>
                    <name>Everything</name>
                </permission>
                </permissions>
                <users>hyperion_test_user, myuser</users>
            </role>
            </get_roles_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                role(
                    id: "5be3c376-7577-4bad-bde6-3d07fb9ad027",
                ) {
                    name
                    id
                    users
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        role = json['data']['role']

        self.assertEqual(role['name'], 'test')
        self.assertEqual(role['id'], "5be3c376-7577-4bad-bde6-3d07fb9ad027")
        self.assertEqual(role['users'], ['hyperion_test_user', 'myuser'])


class RoleGetEntityTestCase(SeleneTestCase):
    gmp_name = 'role'
    selene_name = 'role'
    test_get_entity = make_test_get_entity(gmp_name, selene_name=selene_name)
