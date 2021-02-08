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

from gvm.protocols.next import get_alive_test_from_string

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class ModifyTargetTestCase(SeleneTestCase):
    def setUp(self):
        self.target_id = uuid4()
        self.ssh_credential_id = uuid4()
        self.snmp_credential_id = uuid4()
        self.esxi_credential_id = uuid4()
        self.smb_credential_id = uuid4()
        self.port_list_id = uuid4()

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            f'''
            mutation {{
                modifyTarget(input: {{
                    id: "{self.target_id}",
                }}) {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_modify_target(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'modify_target',
            '''
            <modify_target_response status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyTarget(input: {{
                    id: "{self.target_id}",
                    name: "bar",
                    hosts: "127.0.0.1, 192.168.10.130",
                    sshCredentialId: "{self.ssh_credential_id}",
                    sshCredentialPort: 33,
                    smbCredentialId: "{self.smb_credential_id}",
                    snmpCredentialId: "{self.snmp_credential_id}",
                    esxiCredentialId: "{self.esxi_credential_id}",
                    aliveTest: "icmp ping",
                    allowSimultaneousIps: false,
                    reverseLookupUnify: false,
                }}) {{
                    ok
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['modifyTarget']['ok']

        self.assertEqual(ok, True)

        mock_gmp.gmp_protocol.modify_target.assert_called_with(
            str(self.target_id),
            alive_test=get_alive_test_from_string('icmp ping'),
            hosts=['127.0.0.1', '192.168.10.130'],
            exclude_hosts=None,
            comment=None,
            ssh_credential_id=str(self.ssh_credential_id),
            ssh_credential_port=33,
            smb_credential_id=str(self.smb_credential_id),
            snmp_credential_id=str(self.snmp_credential_id),
            esxi_credential_id=str(self.esxi_credential_id),
            allow_simultaneous_ips=False,
            name="bar",
            reverse_lookup_only=None,
            reverse_lookup_unify=False,
            port_list_id=None,
        )

    def test_nullify_config_default_alive_test(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'modify_target',
            '''
            <modify_target_response status="200" status_text="OK" />
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyTarget(input: {{
                    id: "{self.target_id}",
                    name: "bar",
                    aliveTest: "scan config default",
                }}) {{
                    ok
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['modifyTarget']['ok']

        self.assertEqual(ok, True)

        mock_gmp.gmp_protocol.modify_target.assert_called_with(
            str(self.target_id),
            alive_test=None,
            hosts=None,
            exclude_hosts=None,
            comment=None,
            ssh_credential_id=None,
            name="bar",
            ssh_credential_port=None,
            smb_credential_id=None,
            snmp_credential_id=None,
            esxi_credential_id=None,
            allow_simultaneous_ips=None,
            reverse_lookup_only=None,
            reverse_lookup_unify=None,
            port_list_id=None,
        )

    def test_modify_target_port_list(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'modify_target',
            '''
            <modify_target_response status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyTarget(input: {{
                    id: "{self.target_id}",
                    name: "bar",
                    sshCredentialPort: 22,
                    portListId: "{str(self.port_list_id)}"
                }}) {{
                    ok
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['modifyTarget']['ok']

        self.assertEqual(ok, True)

        mock_gmp.gmp_protocol.modify_target.assert_called_with(
            str(self.target_id),
            alive_test=None,
            hosts=None,
            exclude_hosts=None,
            comment=None,
            name="bar",
            ssh_credential_id=None,
            ssh_credential_port=None,
            smb_credential_id=None,
            snmp_credential_id=None,
            esxi_credential_id=None,
            allow_simultaneous_ips=None,
            reverse_lookup_only=None,
            reverse_lookup_unify=None,
            port_list_id=str(self.port_list_id),
        )
