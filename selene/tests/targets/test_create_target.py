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

from gvm.protocols.latest import get_alive_test_from_string

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class CreateTargetTestCase(SeleneTestCase):
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
                createTarget(input: {{
                    name: "foo",
                    portListId: "{self.port_list_id}"
                }}) {{
                    id
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_create_target(self, mock_gmp: GmpMockFactory):

        mock_gmp.mock_response(
            'create_target',
            f'''
            <create_target_response
                id="{self.target_id}"
                status="200"
                status_text="OK"
            />
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                createTarget(input: {{
                    name: "bar",
                    hosts: "127.0.0.1, 192.168.10.130",
                    sshCredentialId: "{self.ssh_credential_id}",
                    sshCredentialPort: 33,
                    smbCredentialId: "{self.smb_credential_id}",
                    snmpCredentialId: "{self.snmp_credential_id}",
                    esxiCredentialId: "{self.esxi_credential_id}",
                    excludeHosts: "1.3.3.7, lorem",
                    aliveTest: "icmp ping",
                    reverseLookupUnify: false,
                    portListId: "{self.port_list_id}"
                }}) {{
                    id
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        uuid = json['data']['createTarget']['id']

        self.assertEqual(uuid, str(self.target_id))

        mock_gmp.gmp_protocol.create_target.assert_called_with(
            "bar",
            alive_test=get_alive_test_from_string('icmp ping'),
            hosts=['127.0.0.1', '192.168.10.130'],
            exclude_hosts=['1.3.3.7', 'lorem'],
            comment=None,
            ssh_credential_id=str(self.ssh_credential_id),
            ssh_credential_port=33,
            smb_credential_id=str(self.smb_credential_id),
            snmp_credential_id=str(self.snmp_credential_id),
            esxi_credential_id=str(self.esxi_credential_id),
            reverse_lookup_only=None,
            reverse_lookup_unify=False,
            port_list_id=str(self.port_list_id),
            port_range=None,
            asset_hosts_filter=None,
        )

    def test_nullify_config_default_alive_test(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'create_target',
            f'''
            <create_target_response
                id="{self.target_id}"
                status="200"
                status_text="OK"
            />
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                createTarget(input: {{
                    name: "bar",
                    aliveTest: "scan config default",
                    portListId: "{self.port_list_id}"
                }}) {{
                    id
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        uuid = json['data']['createTarget']['id']

        self.assertEqual(uuid, str(self.target_id))

        mock_gmp.gmp_protocol.create_target.assert_called_with(
            "bar",
            alive_test=None,
            hosts=None,
            exclude_hosts=None,
            comment=None,
            ssh_credential_id=None,
            ssh_credential_port=None,
            smb_credential_id=None,
            snmp_credential_id=None,
            esxi_credential_id=None,
            reverse_lookup_only=None,
            reverse_lookup_unify=None,
            port_list_id=str(self.port_list_id),
            port_range=None,
            asset_hosts_filter=None,
        )

    def test_nullify_ssh_cred_port(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'create_target',
            f'''
            <create_target_response
                id="{self.target_id}"
                status="200"
                status_text="OK"
            />
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                createTarget(input: {{
                    name: "bar",
                    sshCredentialPort: 22,
                    portListId: "{self.port_list_id}"
                }}) {{
                    id
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        uuid = json['data']['createTarget']['id']

        self.assertEqual(uuid, str(self.target_id))

        mock_gmp.gmp_protocol.create_target.assert_called_with(
            "bar",
            alive_test=None,
            hosts=None,
            exclude_hosts=None,
            comment=None,
            ssh_credential_id=None,
            ssh_credential_port=None,
            smb_credential_id=None,
            snmp_credential_id=None,
            esxi_credential_id=None,
            reverse_lookup_only=None,
            reverse_lookup_unify=None,
            port_list_id=str(self.port_list_id),
            port_range=None,
            asset_hosts_filter=None,
        )

    def test_create_target_missing_portrange_and_id(
        self, mock_gmp: GmpMockFactory
    ):

        mock_gmp.mock_response(
            'create_target',
            f'''
            <create_target_response
                id="{self.target_id}"
                status="200"
                status_text="OK"
            />
            ''',
        )

        self.login('foo', 'bar')

        # with self.assertRaises(GraphQLError):
        response = self.query(
            f'''
                mutation {{
                    createTarget(input: {{
                        name: "bar",
                        hosts: "127.0.0.1, 192.168.10.130",
                        sshCredentialId: "{self.ssh_credential_id}",
                        sshCredentialPort: 33,
                        smbCredentialId: "{self.smb_credential_id}",
                        snmpCredentialId: "{self.snmp_credential_id}",
                        esxiCredentialId: "{self.esxi_credential_id}",
                        excludeHosts: "1.3.3.7, lorem",
                        aliveTest: "icmp ping",
                        reverseLookupUnify: false,
                    }}) {{
                        id
                    }}
                }}
                '''
        )

        self.assertResponseHasErrorMessage(
            response, 'PortListID or PortRange field required.'
        )

    def test_create_target_portrange(self, mock_gmp: GmpMockFactory):

        mock_gmp.mock_response(
            'create_target',
            f'''
            <create_target_response
                id="{self.target_id}"
                status="200"
                status_text="OK"
            />
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                createTarget(input: {{
                    name: "bar",
                    hosts: "127.0.0.1, 192.168.10.130",
                    sshCredentialId: "{self.ssh_credential_id}",
                    sshCredentialPort: 33,
                    smbCredentialId: "{self.smb_credential_id}",
                    snmpCredentialId: "{self.snmp_credential_id}",
                    esxiCredentialId: "{self.esxi_credential_id}",
                    excludeHosts: "1.3.3.7, lorem",
                    aliveTest: "icmp ping",
                    reverseLookupUnify: false,
                    portRange: "T: 1, 3-4, 7-10"
                }}) {{
                    id
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        uuid = json['data']['createTarget']['id']

        self.assertEqual(uuid, str(self.target_id))

        mock_gmp.gmp_protocol.create_target.assert_called_with(
            "bar",
            alive_test=get_alive_test_from_string('icmp ping'),
            hosts=['127.0.0.1', '192.168.10.130'],
            exclude_hosts=['1.3.3.7', 'lorem'],
            comment=None,
            ssh_credential_id=str(self.ssh_credential_id),
            ssh_credential_port=33,
            smb_credential_id=str(self.smb_credential_id),
            snmp_credential_id=str(self.snmp_credential_id),
            esxi_credential_id=str(self.esxi_credential_id),
            reverse_lookup_only=None,
            reverse_lookup_unify=False,
            port_list_id=None,
            port_range="T: 1, 3-4, 7-10",
            asset_hosts_filter=None,
        )

    def test_create_target_with_hosts_filter(self, mock_gmp: GmpMockFactory):

        mock_gmp.mock_response(
            'create_target',
            f'''
            <create_target_response
                id="{self.target_id}"
                status="200"
                status_text="OK"
            />
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                createTarget(input: {{
                    name: "bar",
                    sshCredentialId: "{self.ssh_credential_id}",
                    sshCredentialPort: 33,
                    smbCredentialId: "{self.smb_credential_id}",
                    snmpCredentialId: "{self.snmp_credential_id}",
                    esxiCredentialId: "{self.esxi_credential_id}",
                    excludeHosts: "1.3.3.7, lorem",
                    aliveTest: "icmp ping",
                    reverseLookupUnify: false,
                    portListId: "{self.port_list_id}"
                    hostsFilter: "uuid=12345",
                }}) {{
                    id
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        uuid = json['data']['createTarget']['id']

        self.assertEqual(uuid, str(self.target_id))

        mock_gmp.gmp_protocol.create_target.assert_called_with(
            "bar",
            alive_test=get_alive_test_from_string('icmp ping'),
            hosts=None,
            exclude_hosts=['1.3.3.7', 'lorem'],
            comment=None,
            ssh_credential_id=str(self.ssh_credential_id),
            ssh_credential_port=33,
            smb_credential_id=str(self.smb_credential_id),
            snmp_credential_id=str(self.snmp_credential_id),
            esxi_credential_id=str(self.esxi_credential_id),
            reverse_lookup_only=None,
            reverse_lookup_unify=False,
            port_list_id=str(self.port_list_id),
            port_range=None,
            asset_hosts_filter="uuid=12345",
        )
