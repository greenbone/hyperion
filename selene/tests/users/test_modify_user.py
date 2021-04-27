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
class ModifyUserTestCase(SeleneTestCase):
    def setUp(self):
        self.id1 = uuid4()
        self.sources_file = 'file'

        self.name = 'new name'
        self.comment = 'new comment'
        self.password = 'new password'
        self.hosts = ['these', 'are', 'some', 'new', 'hosts']
        self.ifaces = ['these', 'are', 'some', 'new', 'ifaces']
        self.hosts_allow = True
        self.ifaces_allow = True
        self.role_ids = [
            "1ba70e85-c6c7-428a-bcbc-d2581a7963f0",
            "2ba70e85-c6c7-428a-bcbc-d2581a7963f1",
        ]

        self.get_users_response = '''
        <get_users_response status="200" status_text="OK">
          <user id="0ba70e85-c6c7-428a-bcbc-d2581a7963f8">
            <owner>
              <name>myuser</name>
            </owner>
            <name>allmodtest1fr4</name>
            <comment>comment3</comment>
            <creation_time>2020-11-18T21:37:20Z</creation_time>
            <modification_time>2020-11-23T16:16:05Z</modification_time>
            <writable>1</writable>
            <in_use>0</in_use>
            <permissions>
              <permission>
                <name>Everything</name>
              </permission>
            </permissions>
            <hosts allow="0"/>
            <sources>
              <source>file</source>
            </sources>
            <ifaces allow="0">new, newss</ifaces>
            <role id="7a8cb5b4-b74d-11e2-8187-406186ea4fc5">
              <name>Admin</name>
            </role>
            <groups>
              <group id="6beaa7f8-1867-4864-9bc9-f9642fc1e755">
                <name>hyperion_test_group</name>
              </group>
            </groups>
          </user>
          <filters id="">
            <term>first=1 rows=10 sort=name</term>
            <keywords>
              <keyword>
                <column>first</column>
                <relation>=</relation>
                <value>1</value>
              </keyword>
              <keyword>
                <column>rows</column>
                <relation>=</relation>
                <value>10</value>
              </keyword>
              <keyword>
                <column>sort</column>
                <relation>=</relation>
                <value>name</value>
              </keyword>
            </keywords>
          </filters>
          <sort>
            <field>name<order>ascending</order></field>
          </sort>
          <users start="1" max="1000"/>
          <user_count>12<filtered>1</filtered><page>1</page></user_count>
        </get_users_response>
        '''

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            f'''
            mutation {{
                modifyUserSetName(input: {{
                    id: "{self.id1}",
                    name: "{self.name}",
                }}) {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_modify_user_set_name(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_user', self.get_users_response)

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyUserSetName(input: {{
                    id: "{self.id1}",
                    name: "{self.name}"
                }}) {{
                    ok
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['modifyUserSetName']['ok']

        self.assertEqual(ok, True)

        mock_gmp.gmp_protocol.get_user.assert_called_with(user_id=str(self.id1))

        mock_gmp.gmp_protocol.modify_user.assert_called_once()

    def test_modify_user_set_comment(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_user', self.get_users_response)

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyUserSetComment(input: {{
                    id: "{self.id1}",
                    comment: "{self.comment}"
                }}) {{
                    ok
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['modifyUserSetComment']['ok']

        self.assertEqual(ok, True)

        mock_gmp.gmp_protocol.get_user.assert_called_with(user_id=str(self.id1))

        mock_gmp.gmp_protocol.modify_user.assert_called_once()

    def test_modify_user_set_hosts(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_user', self.get_users_response)

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyUserSetHosts(input: {{
                    id: "{self.id1}",
                    hosts: "{self.hosts}"
                }}) {{
                    ok
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['modifyUserSetHosts']['ok']

        self.assertEqual(ok, True)

        mock_gmp.gmp_protocol.get_user.assert_called_with(user_id=str(self.id1))

        mock_gmp.gmp_protocol.modify_user.assert_called_once()

    def test_modify_user_set_ifaces(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_user', self.get_users_response)

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyUserSetIfaces(input: {{
                    id: "{self.id1}",
                    ifaces: "{self.ifaces}"
                }}) {{
                    ok
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['modifyUserSetIfaces']['ok']

        self.assertEqual(ok, True)

        mock_gmp.gmp_protocol.get_user.assert_called_with(user_id=str(self.id1))

        mock_gmp.gmp_protocol.modify_user.assert_called_once()

    def test_modify_user_set_password(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_user', self.get_users_response)

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyUserSetPassword(input: {{
                    id: "{self.id1}",
                    password: "{self.password}"
                }}) {{
                    ok
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['modifyUserSetPassword']['ok']

        self.assertEqual(ok, True)

        mock_gmp.gmp_protocol.get_user.assert_called_with(user_id=str(self.id1))

        mock_gmp.gmp_protocol.modify_user.assert_called_once()

    def test_modify_user_set_auth_src(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_user', self.get_users_response)

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyUserSetAuthSource(input: {{
                    id: "{self.id1}",
                    authSource: FILE,
                }}) {{
                    ok
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['modifyUserSetAuthSource']['ok']

        self.assertEqual(ok, True)

        mock_gmp.gmp_protocol.get_user.assert_called_with(user_id=str(self.id1))

        mock_gmp.gmp_protocol.modify_user.assert_called_once()

    def test_modify_user_set_ifaces_allow(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_user', self.get_users_response)

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyUserSetIfacesAllow(input: {{
                    id: "{self.id1}",
                    ifacesAllow: true,
                }}) {{
                    ok
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['modifyUserSetIfacesAllow']['ok']

        self.assertEqual(ok, True)

        mock_gmp.gmp_protocol.get_user.assert_called_with(user_id=str(self.id1))

        mock_gmp.gmp_protocol.modify_user.assert_called_once()

    def test_modify_user_set_hosts_allow(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_user', self.get_users_response)

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyUserSetHostsAllow(input: {{
                    id: "{self.id1}",
                    hostsAllow: true
                }}) {{
                    ok
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['modifyUserSetHostsAllow']['ok']

        self.assertEqual(ok, True)

        mock_gmp.gmp_protocol.get_user.assert_called_with(user_id=str(self.id1))

        mock_gmp.gmp_protocol.modify_user.assert_called_once()

    def test_modify_user_set_roles(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_user', self.get_users_response)

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyUserSetRoles(input: {{
                    id: "{self.id1}",
                    roleIds: ["1ba70e85-c6c7-428a-bcbc-d2581a7963f0",
                    "2ba70e85-c6c7-428a-bcbc-d2581a7963f1"]
                }}) {{
                    ok
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['modifyUserSetRoles']['ok']

        self.assertEqual(ok, True)

        mock_gmp.gmp_protocol.get_user.assert_called_with(user_id=str(self.id1))

        mock_gmp.gmp_protocol.modify_user.assert_called_once()

    def test_modify_user_set_groups(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_user', self.get_users_response)

        self.login('foo', 'bar')

        response = self.query(
            f'''
                mutation {{
                    modifyUserSetGroups(input: {{
                        id: "{self.id1}",
                        groupIds: ["1ba70e85-c6c7-428a-bcbc-d2581a7963f0",
                        "2ba70e85-c6c7-428a-bcbc-d2581a7963f1"]
                    }}) {{
                        ok
                    }}
                }}
                '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['modifyUserSetGroups']['ok']

        self.assertEqual(ok, True)

        mock_gmp.gmp_protocol.get_user.assert_called_with(user_id=str(self.id1))

        mock_gmp.gmp_protocol.modify_user.assert_called_once()
