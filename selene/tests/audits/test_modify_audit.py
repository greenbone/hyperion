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

from gvm.protocols.next import get_hosts_ordering_from_string

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class ModifyAuditTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        audit_id = str(uuid4())
        response = self.query(
            f'''
            mutation {{
                modifyAudit(input: {{
                    id: "{audit_id}",
                    name: "foo",
                }}) {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_modify_audit(self, mock_gmp: GmpMockFactory):
        audit_id = str(uuid4())
        policy_id = str(uuid4())

        mock_gmp.mock_response(
            'modify_audit',
            '''
            <modify_task_response status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyAudit(input: {{
                    id: "{audit_id}",
                    name: "bar"
                    scannerType: 2,
                    applyOverrides: false,
                    inAssets: true,
                    policyId: "{policy_id}",
                    hostsOrdering: "reverse",
                    maxChecks: 7,
                    maxHosts: 13,
                    sourceIface: "foo",
                    autoDelete: "keep",
                    autoDeleteData: 4
                    }}) {{
                    ok
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['modifyAudit']['ok']

        self.assertEqual(ok, True)

        mock_gmp.gmp_protocol.modify_audit.assert_called_with(
            str(audit_id),
            alert_ids=None,
            alterable=None,
            comment=None,
            policy_id=policy_id,
            hosts_ordering=get_hosts_ordering_from_string('reverse'),
            name="bar",
            observers=None,
            preferences={
                'auto_delete': 'keep',
                'auto_delete_data': 4,
                'max_checks': 7,
                'max_hosts': 13,
                'source_iface': 'foo',
                'assets_apply_overrides': 'no',
                'in_assets': 'yes',
            },
            scanner_id=None,
            schedule_id=None,
            schedule_periods=None,
            target_id=None,
        )

    def test_nullify_scanner_preferences(self, mock_gmp: GmpMockFactory):
        audit_id = str(uuid4())
        policy_id = str(uuid4())
        mock_gmp.mock_response(
            'modify_audit',
            '''
            <modify_task_response status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        # scanner_type = 3
        response = self.query(
            f'''
            mutation {{
                modifyAudit(input:{{
                    id: "{audit_id}",
                    scannerType: 3,
                    hostsOrdering: "random",
                    policyId: "{policy_id}"
                    maxChecks: 7,
                    maxHosts: 13,
                    sourceIface: "foo",
                    autoDelete: "keep",
                    autoDeleteData: 4,
                    }}) {{
                    ok
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['modifyAudit']['ok']

        self.assertEqual(ok, True)

        mock_gmp.gmp_protocol.modify_audit.assert_called_with(
            str(audit_id),
            alert_ids=None,
            alterable=None,
            comment=None,
            policy_id=None,
            hosts_ordering=None,
            name=None,
            observers=None,
            preferences={'auto_delete': 'keep', 'auto_delete_data': 4},
            scanner_id=None,
            schedule_id=None,
            schedule_periods=None,
            target_id=None,
        )

        # scanner_type = None
        second_response = self.query(
            f'''
            mutation {{
                modifyAudit(input: {{
                    id: "{audit_id}",
                    hostsOrdering: "random",
                    policyId: "{policy_id}"
                    maxChecks: 7,
                    maxHosts: 13,
                    sourceIface: "foo",
                    autoDelete: "keep",
                    autoDeleteData: 4
                    }}) {{
                    ok
                }}
            }}
            '''
        )

        json = second_response.json()

        self.assertResponseNoErrors(second_response)

        ok = json['data']['modifyAudit']['ok']

        self.assertEqual(ok, True)

        mock_gmp.gmp_protocol.modify_audit.assert_called_with(
            str(audit_id),
            alert_ids=None,
            alterable=None,
            comment=None,
            policy_id=None,
            hosts_ordering=None,
            name=None,
            observers=None,
            preferences={'auto_delete': 'keep', 'auto_delete_data': 4},
            scanner_id=None,
            schedule_id=None,
            schedule_periods=None,
            target_id=None,
        )
