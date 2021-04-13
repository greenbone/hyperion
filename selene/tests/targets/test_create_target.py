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

from selene.schema.targets.fields import AliveTest

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
                    hosts: ["127.0.0.1"],
                    portListId: "{self.port_list_id}"
                    aliveTest: ICMP_PING,
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
                    hosts: ["127.0.0.1", "192.168.10.130"],
                    sshCredentialId: "{self.ssh_credential_id}",
                    sshCredentialPort: 33,
                    smbCredentialId: "{self.smb_credential_id}",
                    snmpCredentialId: "{self.snmp_credential_id}",
                    esxiCredentialId: "{self.esxi_credential_id}",
                    excludeHosts: ["1.3.3.7", "lorem"],
                    aliveTest: ICMP_PING,
                    allowSimultaneousIPs: true,
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
            alive_test=AliveTest.ICMP_PING,  # pylint: disable=no-member
            hosts=['127.0.0.1', '192.168.10.130'],
            exclude_hosts=['1.3.3.7', 'lorem'],
            comment=None,
            ssh_credential_id=str(self.ssh_credential_id),
            ssh_credential_port=33,
            smb_credential_id=str(self.smb_credential_id),
            snmp_credential_id=str(self.snmp_credential_id),
            esxi_credential_id=str(self.esxi_credential_id),
            allow_simultaneous_ips=True,
            reverse_lookup_only=None,
            reverse_lookup_unify=False,
            port_list_id=str(self.port_list_id),
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
                    hosts: ["127.0.0.1"],
                    sshCredentialPort: 22,
                    portListId: "{self.port_list_id}"
                    aliveTest: ICMP_PING,
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
            alive_test=AliveTest.ICMP_PING,  # pylint: disable=no-member
            hosts=["127.0.0.1"],
            exclude_hosts=None,
            comment=None,
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

    def test_create_target_missing_port_list_id(self, mock_gmp: GmpMockFactory):

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
                        hosts: ["127.0.0.1", "192.168.10.130"],
                        sshCredentialId: "{self.ssh_credential_id}",
                        sshCredentialPort: 33,
                        smbCredentialId: "{self.smb_credential_id}",
                        snmpCredentialId: "{self.snmp_credential_id}",
                        esxiCredentialId: "{self.esxi_credential_id}",
                        excludeHosts: ["1.3.3.7", "lorem"],
                        aliveTest: ICMP_PING,
                        reverseLookupUnify: false,
                    }}) {{
                        id
                    }}
                }}
                '''
        )

        self.assertResponseHasErrors(response)

    def test_create_target_do_not_allow_simultaneous_ips(
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

        response = self.query(
            f'''
            mutation {{
                createTarget(input: {{
                    name: "bar",
                    hosts: ["127.0.0.1", "192.168.10.130"],
                    aliveTest: ICMP_PING,
                    allowSimultaneousIPs: false,
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
            alive_test=AliveTest.ICMP_PING,  # pylint: disable=no-member
            hosts=['127.0.0.1', '192.168.10.130'],
            exclude_hosts=None,
            comment=None,
            ssh_credential_id=None,
            ssh_credential_port=None,
            smb_credential_id=None,
            snmp_credential_id=None,
            esxi_credential_id=None,
            allow_simultaneous_ips=False,
            reverse_lookup_only=None,
            reverse_lookup_unify=None,
            port_list_id=str(self.port_list_id),
        )
