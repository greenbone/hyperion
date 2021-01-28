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

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class ModifyRoleTestCase(SeleneTestCase):
    def setUp(self):
        self.id1 = uuid4()

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            f'''
            mutation {{
                modifyRole(input: {{
                    id: "{self.id1}"
                    name: "foo",
                    comment: "bar",
                    users: ["myuser","another user"],
                }}) {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_modify_role(self, mock_gmp: GmpMockFactory):

        mock_gmp.mock_response(
            'modify_role',
            '<modify_role_response status="200" status_text="OK"/>',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyRole(input: {{
                    id: "{self.id1}"
                    name: "foo",
                    comment: "bar",
                    users: ["myuser","another user"],
                }}) {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseNoErrors(response)

        json = response.json()

        ok = json['data']['modifyRole']['ok']

        self.assertEqual(ok, True)

        mock_gmp.gmp_protocol.modify_role.assert_called_with(
            role_id=f'{self.id1}',
            comment="bar",
            name="foo",
            users=["myuser", "another user"],
        )
