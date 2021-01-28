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
class CreateHostTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            mutation {
                createHost(input: {
                    name: "foo",
                }) {
                    id
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_create_host(self, mock_gmp: GmpMockFactory):
        host_id = uuid4()

        mock_gmp.mock_response(
            'create_host',
            f'''
            <create_host_response id="{host_id}" status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            mutation {
                createHost(input: {
                    name: "foo",
                    comment: "bar",
                }) {
                    id
                }
            }
            '''
        )

        self.assertResponseNoErrors(response)

        json = response.json()

        uuid = json['data']['createHost']['id']

        self.assertEqual(uuid, str(host_id))

        mock_gmp.gmp_protocol.create_host.assert_called_with(
            "foo",
            comment="bar",
        )
