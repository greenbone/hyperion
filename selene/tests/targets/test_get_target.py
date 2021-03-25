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

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory

from selene.tests.entity import make_test_get_entity


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class TargetTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                target(id: "08b69003-5fc2-4037-a479-93b440211c73") {
                    id
                    name
                    comment
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_target_no_tasks(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_target',
            '''
            <get_target_response>
                <target id="08b69003-5fc2-4037-a479-93b440211c73">
                    <name>foo</name>
                    <comment>bar</comment>
                    <hosts>192.168.10.90</hosts>
                    <exclude_hosts>192.168.10.9</exclude_hosts>
                    <max_hosts>1</max_hosts>
                    <ssh_credential id="33d0cd82-57c6-11e1-8ed1-4061823cc51a">
                        <name>baz</name>
                        <port>42</port>
                        <trash>0</trash>
                    </ssh_credential>
                    <smb_credential id="33d0cd82-57c6-11e1-8ed1-4061823cc51b">
                        <name>baz</name>
                        <trash>0</trash>
                    </smb_credential>
                    <esxi_credential id="33d0cd82-57c6-11e1-8ed1-4061823cc51c">
                        <name>qux</name>
                        <trash>0</trash>
                    </esxi_credential>
                    <snmp_credential id="33d0cd82-57c6-11e1-8ed1-4061823cc51d">
                        <name>quux</name>
                        <trash>0</trash>
                    </snmp_credential>
                    <port_list id="33d0cd82-57c6-11e1-8ed1-406186ea4fc5">
                        <name>All IANA assigned TCP 2012-02-10</name>
                        <trash>0</trash>
                    </port_list>
                    <allow_simultaneous_ips>1</allow_simultaneous_ips>
                    <reverse_lookup_only>0</reverse_lookup_only>
                    <reverse_lookup_unify>0</reverse_lookup_unify>
                    <alive_tests>Scan Config Default</alive_tests>
                    <tasks>
                        <task id="ef778231-6b56-480f-8e1e-e89a09bc03bd">
                            <name>task1</name>
                        </task>
                    </tasks>
                </target>
            </get_target_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                target(id: "08b69003-5fc2-4037-a479-93b440211c73") {
                    id
                    name
                    comment
                    hosts
                    maxHosts
                    excludeHosts
                    sshCredential {
                        id
                        name
                        port
                    }
                    smbCredential {
                        id
                        name
                    }
                    esxiCredential {
                        id
                        name
                    }
                    snmpCredential {
                        id
                        name
                    }
                    portList {
                        id
                        name
                    }
                    allowSimultaneousIPs
                    reverseLookupOnly
                    reverseLookupUnify
                    aliveTests
                    portRange
                    tasks {
                        id
                        name
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        target = json['data']['target']

        self.assertEqual(target['id'], '08b69003-5fc2-4037-a479-93b440211c73')
        self.assertEqual(target['hosts'], ['192.168.10.90'])
        self.assertEqual(target['excludeHosts'], ['192.168.10.9'])
        self.assertEqual(target['maxHosts'], 1)
        self.assertEqual(
            target['sshCredential']['id'],
            '33d0cd82-57c6-11e1-8ed1-4061823cc51a',
        )
        self.assertEqual(target['sshCredential']['name'], 'baz')
        self.assertEqual(target['sshCredential']['port'], 42)
        self.assertEqual(
            target['smbCredential']['id'],
            '33d0cd82-57c6-11e1-8ed1-4061823cc51b',
        )
        self.assertEqual(target['smbCredential']['name'], 'baz')
        self.assertEqual(
            target['esxiCredential']['id'],
            '33d0cd82-57c6-11e1-8ed1-4061823cc51c',
        )
        self.assertEqual(target['esxiCredential']['name'], 'qux')
        self.assertEqual(
            target['snmpCredential']['id'],
            '33d0cd82-57c6-11e1-8ed1-4061823cc51d',
        )
        self.assertEqual(target['snmpCredential']['name'], 'quux')
        self.assertEqual(
            target['portList']['id'], '33d0cd82-57c6-11e1-8ed1-406186ea4fc5'
        )
        self.assertEqual(
            target['portList']['name'], 'All IANA assigned TCP 2012-02-10'
        )
        self.assertEqual(target['name'], 'foo')
        self.assertEqual(target['aliveTests'], 'Scan Config Default')
        self.assertEqual(target['allowSimultaneousIPs'], True)
        self.assertEqual(target['reverseLookupOnly'], False)
        self.assertEqual(target['reverseLookupUnify'], False)
        self.assertEqual(target['portRange'], None)

        task = target['tasks'][0]

        self.assertEqual(task['name'], 'task1')
        self.assertEqual(task['id'], 'ef778231-6b56-480f-8e1e-e89a09bc03bd')

    def test_get_target(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_target',
            '''
            <get_target_response>
                <target id="08b69003-5fc2-4037-a479-93b440211c73">
                    <name>foo</name>
                    <comment>bar</comment>
                    <hosts>192.168.10.90</hosts>
                    <exclude_hosts>192.168.10.9</exclude_hosts>
                    <max_hosts>1</max_hosts>
                    <ssh_credential id="33d0cd82-57c6-11e1-8ed1-4061823cc51a">
                        <name>baz</name>
                        <port>42</port>
                        <trash>0</trash>
                    </ssh_credential>
                    <smb_credential id="33d0cd82-57c6-11e1-8ed1-4061823cc51b">
                        <name>baz</name>
                        <trash>0</trash>
                    </smb_credential>
                    <esxi_credential id="33d0cd82-57c6-11e1-8ed1-4061823cc51c">
                        <name>qux</name>
                        <trash>0</trash>
                    </esxi_credential>
                    <snmp_credential id="33d0cd82-57c6-11e1-8ed1-4061823cc51d">
                        <name>quux</name>
                        <trash>0</trash>
                    </snmp_credential>
                    <port_list id="33d0cd82-57c6-11e1-8ed1-406186ea4fc5">
                        <name>All IANA assigned TCP 2012-02-10</name>
                        <trash>0</trash>
                    </port_list>
                    <allow_simultaneous_ips>1</allow_simultaneous_ips>
                    <reverse_lookup_only>0</reverse_lookup_only>
                    <reverse_lookup_unify>0</reverse_lookup_unify>
                    <alive_tests>Scan Config Default</alive_tests>
                    <tasks/>
                </target>
            </get_target_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                target(id: "08b69003-5fc2-4037-a479-93b440211c73") {
                    id
                    name
                    tasks {
                        id
                        name
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        tasks = json['data']['target']['tasks']

        self.assertIsNone(tasks)


class TargetGetEntityTestCase(SeleneTestCase):
    gmp_name = 'target'
    test_get_entity = make_test_get_entity(gmp_name, tasks=True)
