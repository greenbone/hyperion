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

# pylint: disable=no-member

from uuid import uuid4

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class CreateRoleTestCase(SeleneTestCase):
    def setUp(self):
        self.id1 = uuid4()

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            mutation {
                createRole( input: {
                        name: "some_name",
                        comment: "some_comment",
                        users: ["myuser","another_user"]}) {
                    id
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_create_role(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'create_role',
            f'''
            <create_role_response status="201"
             status_text="OK, resource created"
             id="{self.id1}"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            mutation {
                createRole( input: {
                        name: "some_name",
                        comment: "some_comment",
                        users: ["myuser","another_user"]}) {
                    id
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        created_role_id = json['data']['createRole']['id']

        self.assertEqual(created_role_id, str(self.id1))

        mock_gmp.gmp_protocol.create_role.assert_called_with(
            name="some_name",
            comment="some_comment",
            users=["myuser", "another_user"],
        )
