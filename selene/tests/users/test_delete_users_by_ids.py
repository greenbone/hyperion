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
class DeleteUsersByIdsTestCase(SeleneTestCase):
    def setUp(self):
        self.id1 = uuid4()
        self.id2 = uuid4()
        self.inheritor_id = uuid4()
        self.resp = f'''
         <get_users_response status="200" status_text="OK">
          <user id="{self.id1}">
            <owner>
              <name>myuser</name>
            </owner>
            <name>foobar</name>
            <comment/>
            <creation_time>2020-11-10T13:18:44Z</creation_time>
            <modification_time>2020-11-10T13:19:07Z</modification_time>
            <writable>1</writable>
            <in_use>0</in_use>
            <permissions>
              <permission>
                <name>Everything</name>
              </permission>
              <permission>
                <name>Another permission</name>
              </permission>
            </permissions>
            <hosts allow="0">192.123.168.66, 192.168.66.67-70, 192.168.66.68</hosts>
            <sources>
              <source>file</source>
              <source>another source</source>
            </sources>
            <ifaces allow="0">some-interface1, some-interface2</ifaces>
            <role id="7a8cb5b4-b74d-11e2-8187-406186ea4fc5">
              <name>Admin</name>
              <permissions>
                <permission>
                    <name>role perm1</name>
                </permission>
                <permission>
                    <name>role perm2</name>
                </permission>
              </permissions>   
            </role>
            <role id="5be3c376-7577-4bad-bde6-3d07fb9ad027">
              <name>test</name>
            </role>
            <groups>
              <group id="5be3c376-7577-4bad-bde6-3d07fb9ad027">
                <name>group1 name</name>
                <permissions>
                  <permission>
                    <name>role perm</name>
                  </permission>
                  <permission>
                    <name>role perm</name>
                  </permission>
                </permissions>
              </group>
              <group id="2be3c376-7577-4bad-bde6-3d07fb9ad027">
                <name>group2 name</name>
                <permissions>
                  <permission>
                    <name>role2 perm2</name>
                  </permission>
                  <permission>
                    <name>role2 perm2</name>
                  </permission>
                </permissions>
              </group>
            </groups>
          </user>
          <user id="{self.id2}">
            <owner>
              <name>myuser</name>
            </owner>
            <name>hyperion_test_user</name>
            <comment/>
            <creation_time>2020-11-10T13:18:44Z</creation_time>
            <modification_time>2020-11-10T13:19:07Z</modification_time>
            <writable>1</writable>
            <in_use>0</in_use>
            <permissions>
              <permission>
                <name>Everything</name>
              </permission>
              <permission>
                <name>Another permission</name>
              </permission>
            </permissions>
            <hosts allow="0">192.123.168.66, 192.168.66.67-70, 192.168.66.68</hosts>
            <sources>
              <source>file</source>
              <source>another source</source>
            </sources>
            <ifaces allow="0">some-interface1, some-interface2</ifaces>
            <role id="7a8cb5b4-b74d-11e2-8187-406186ea4fc5">
              <name>Admin</name>
              <permissions>
                <permission>
                    <name>role perm1</name>
                </permission>
                <permission>
                    <name>role perm2</name>
                </permission>
              </permissions>   
            </role>
            <role id="5be3c376-7577-4bad-bde6-3d07fb9ad027">
              <name>test</name>
            </role>
            <groups>
              <group id="5be3c376-7577-4bad-bde6-3d07fb9ad027">
                <name>group1 name</name>
                <permissions>
                  <permission>
                    <name>role perm</name>
                  </permission>
                  <permission>
                    <name>role perm</name>
                  </permission>
                </permissions>
              </group>
              <group id="2be3c376-7577-4bad-bde6-3d07fb9ad027">
                <name>group2 name</name>
                <permissions>
                  <permission>
                    <name>role2 perm2</name>
                  </permission>
                  <permission>
                    <name>role2 perm2</name>
                  </permission>
                </permissions>
              </group>
            </groups>
          </user>
        </get_users_response>
        '''

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            f'''
            mutation {{
                deleteUsersByIds(input: {{ids: ["{self.id1}", "{self.id2}"]}})
                {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_delete_users_by_ids(self, mock_gmp: GmpMockFactory):
        self.login('foo', 'bar')

        mock_gmp.mock_response('get_users', self.resp)

        response = self.query(
            f'''
            mutation {{
                deleteUsersByIds(input: {{ids: ["{self.id1}", "{self.id2}"],
                  inheritorId:"{self.inheritor_id}"}})
                {{
                    ok
                }}
            }}
            '''
        )
        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['deleteUsersByIds']['ok']
        self.assertTrue(ok)

        mock_gmp.gmp_protocol.get_users.assert_called_with(
            filter_string=f'uuid={self.id1} uuid={self.id2} '
        )

        mock_gmp.gmp_protocol.delete_user.assert_any_call(
            user_id=f'{self.id1}',
            inheritor_id=f'{self.inheritor_id }',
            inheritor_name=None,
        )
        mock_gmp.gmp_protocol.delete_user.assert_any_call(
            user_id=f'{self.id2}',
            inheritor_id=f'{self.inheritor_id}',
            inheritor_name=None,
        )

    def test_delete_by_ids_invalid(self, mock_gmp: GmpMockFactory):
        self.login('foo', 'bar')

        mock_gmp.mock_response(
            'get_users',
            f'''
            <get_users_response status="200" status_text="OK">
            <role id="{self.id1}">
            </role>
            </get_users_response>''',
        )

        response = self.query(
            f'''
            mutation {{
                deleteUsersByIds(input: {{ ids: ["{self.id1}", "{self.id2}"]}})
                {{
                    ok
                }}
            }}
            '''
        )
        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['deleteUsersByIds']['ok']
        self.assertFalse(ok)

        mock_gmp.gmp_protocol.get_users.assert_called_with(
            filter_string=f'uuid={self.id1} uuid={self.id2} '
        )
