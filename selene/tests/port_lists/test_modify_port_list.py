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
class ModifyPortListTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        port_list_id = str(uuid4())

        response = self.query(
            f'''
            mutation {{
                modifyPortList(input: {{
                    id: "{port_list_id}"
                    name: "bar"
                    comment: "port range"
                }}) {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_modify_port_list(self, mock_gmp: GmpMockFactory):
        port_list_id = str(uuid4())

        mock_gmp.mock_response(
            'modify_port_list',
            '''
            <modify_port_list_response
            status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyPortList(input: {{
                    id: "{port_list_id}"
                    name: "bar"
                    comment: "port range"
                }}) {{
                    ok
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['modifyPortList']['ok']

        self.assertEqual(ok, True)

        mock_gmp.gmp_protocol.modify_port_list.assert_called_with(
            port_list_id=str(port_list_id), name="bar", comment="port range"
        )
