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

# pylint: disable=no-member

from uuid import uuid4

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class CreateUserTestCase(SeleneTestCase):
    def setUp(self):
        self.id1 = uuid4()
        self.response_xml = f'''
            <create_user_response status="201"
             status_text="OK, resource created"
             id="{self.id1}"/>
            '''

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            mutation {
                createUser( input:{
                        name: "user1",
                        password: "pass",
                        hosts: ["123.45.67.89","22.22.22.22"],
                        hostsAllow: true,
                        ifaces: ["iface1", "iface2"],
                        ifacesAllow: true,
                        roleIds: ["5be3c376-7577-4bad-bde6-3d07fb9ad027",
                                  "881a3894-3312-4bce-8260-3f5cd09664a6"],
                    }
                ) {
                    id
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_create_user(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('create_user', self.response_xml)

        self.login('foo', 'bar')

        response = self.query(
            '''
            mutation {
                createUser( input:{
                        name: "user1",
                        password: "pass",
                        hosts: ["123.45.67.89","22.22.22.22"],
                        hostsAllow: true,
                        ifaces: ["iface1", "iface2"],
                        ifacesAllow: true,
                        roleIds: ["5be3c376-7577-4bad-bde6-3d07fb9ad027",
                                  "881a3894-3312-4bce-8260-3f5cd09664a6"],
                    }
                ) {
                    id
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        created_user_id = json['data']['createUser']['id']

        self.assertEqual(created_user_id, str(self.id1))

        mock_gmp.gmp_protocol.create_user.assert_called_with(
            name="user1",
            password="pass",
            hosts=["123.45.67.89", "22.22.22.22"],
            hosts_allow=True,
            ifaces=["iface1", "iface2"],
            ifaces_allow=True,
            role_ids=[
                "5be3c376-7577-4bad-bde6-3d07fb9ad027",
                "881a3894-3312-4bce-8260-3f5cd09664a6",
            ],
        )
