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

# pylint: disable=line-too-long

from uuid import uuid4

from unittest.mock import patch

from gvm.protocols.latest import get_hosts_ordering_from_string

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class CreateAuditTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            f'''
            mutation {{
                createAudit(input: {{
                    name: "foo",
                    scannerId: "{uuid4()}",
                    policyId: "{uuid4()}",
                    targetId: "{uuid4()}"
                }}) {{
                    id
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_create_audit(self, mock_gmp: GmpMockFactory):
        audit_id = str(uuid4())
        policy_id = str(uuid4())
        target_id = str(uuid4())
        scanner_id = str(uuid4())

        mock_gmp.mock_response(
            'create_audit',
            f'''
            <create_task_response id="{audit_id}" status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                createAudit(input: {{
                    name: "bar",
                    scannerId: "{scanner_id}",
                    policyId: "{policy_id}",
                    targetId: "{target_id}",
                    scannerType: 2,
                    hostsOrdering: "reverse",
                    maxChecks: 7,
                    maxHosts: 13,
                    sourceIface: "foo",
                    autoDelete: "keep",
                    autoDeleteData: 4,
                    inAssets: true,
                    applyOverrides: false
                }}) {{
                    id
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        uuid = json['data']['createAudit']['id']

        self.assertEqual(uuid, audit_id)

        mock_gmp.gmp_protocol.create_audit.assert_called_with(
            "bar",
            policy_id,
            target_id,
            scanner_id,
            alert_ids=None,
            alterable=None,
            comment=None,
            hosts_ordering=get_hosts_ordering_from_string('reverse'),
            observers=None,
            preferences={
                'auto_delete': 'keep',
                'auto_delete_data': 4,
                'max_checks': 7,
                'max_hosts': 13,
                'source_iface': 'foo',
                'in_assets': 'yes',
                'assets_apply_overrides': 'no',
            },
            schedule_id=None,
            schedule_periods=None,
        )

    def test_nullify_scanner_preferences(self, mock_gmp: GmpMockFactory):
        audit_id = str(uuid4())
        policy_id = str(uuid4())
        target_id = str(uuid4())
        scanner_id = str(uuid4())

        mock_gmp.mock_response(
            'create_audit',
            f'''
            <create_task_response id="{audit_id}" status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        # scanner_type = 3
        response = self.query(
            f'''
            mutation {{
                createAudit(input: {{
                    name: "bar",
                    scannerId: "{scanner_id}",
                    policyId: "{policy_id}",
                    targetId: "{target_id}",
                    scannerType: 3,
                    hostsOrdering: "random",
                    maxChecks: 7,
                    maxHosts: 13,
                    sourceIface: "foo",
                    autoDelete: "keep",
                    autoDeleteData: 4
                    }}) {{
                    id
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        uuid = json['data']['createAudit']['id']

        self.assertEqual(uuid, audit_id)

        mock_gmp.gmp_protocol.create_audit.assert_called_with(
            "bar",
            policy_id,
            target_id,
            scanner_id,
            alert_ids=None,
            alterable=None,
            comment=None,
            hosts_ordering=None,
            observers=None,
            preferences={'auto_delete': 'keep', 'auto_delete_data': 4},
            schedule_id=None,
            schedule_periods=None,
        )

        # scanner_type = None
        second_response = self.query(
            f'''
            mutation {{
                createAudit(input: {{
                    name: "bar",
                    scannerId: "{scanner_id}",
                    policyId: "{policy_id}",
                    targetId: "{target_id}",
                    hostsOrdering: "random",
                    maxChecks: 7,
                    maxHosts: 13,
                    sourceIface: "foo",
                    autoDelete: "keep",
                    autoDeleteData: 4
                    }}) {{
                    id
                }}
            }}
            '''
        )

        json = second_response.json()

        self.assertResponseNoErrors(second_response)

        uuid = json['data']['createAudit']['id']

        self.assertEqual(uuid, audit_id)

        mock_gmp.gmp_protocol.create_audit.assert_called_with(
            "bar",
            policy_id,
            target_id,
            scanner_id,
            alert_ids=None,
            alterable=None,
            comment=None,
            hosts_ordering=None,
            observers=None,
            preferences={'auto_delete': 'keep', 'auto_delete_data': 4},
            schedule_id=None,
            schedule_periods=None,
        )
