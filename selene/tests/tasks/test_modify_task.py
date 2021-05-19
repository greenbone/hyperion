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

from selene.schema.utils import RESET_UUID

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class ModifyTaskTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        task_id = str(uuid4())
        target_id = str(uuid4())
        scanner_id = str(uuid4())
        scan_config_id = str(uuid4())
        schedule_id = str(uuid4())
        alert_ids = [str(uuid4()), str(uuid4())]

        response = self.query(
            f'''
            mutation {{
                modifyTask(input: {{
                    id: "{task_id}",
                    name: "foo",
                    comment: "Foo Bar",
                    targetId: "{target_id}",
                    scannerId: "{scanner_id}",
                    scanConfigId: "{scan_config_id}",
                    scheduleId: "{schedule_id}",
                    alterable: true,
                    alertIds: ["{'","'.join(alert_ids)}"],
                }}) {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_modify_task(self, mock_gmp: GmpMockFactory):
        task_id = str(uuid4())
        target_id = str(uuid4())
        scanner_id = str(uuid4())
        scan_config_id = str(uuid4())
        schedule_id = str(uuid4())
        alert_ids = [str(uuid4()), str(uuid4())]

        mock_gmp.mock_response(
            'modify_task',
            '''
            <modify_task_response status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyTask(input: {{
                    id: "{task_id}",
                    name: "bar"
                    comment: "Foo Bar",
                    targetId: "{target_id}",
                    scannerId: "{scanner_id}",
                    scanConfigId: "{scan_config_id}",
                    scheduleId: "{schedule_id}",
                    alterable: true,
                    alertIds: ["{'","'.join(alert_ids)}"],
                    preferences: {{
                        autoDeleteReports: 4
                        createAssets: true,
                        createAssetsApplyOverrides: false,
                        maxConcurrentNvts: 7,
                        maxConcurrentHosts: 13,
                    }}
                }}) {{
                    ok
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['modifyTask']['ok']

        self.assertEqual(ok, True)

        mock_gmp.gmp_protocol.modify_task.assert_called_with(
            task_id,
            alert_ids=alert_ids,
            alterable=True,
            comment="Foo Bar",
            config_id=scan_config_id,
            name="bar",
            observers=None,
            preferences={
                'auto_delete': 'keep',
                'auto_delete_data': 4,
                'max_checks': 7,
                'max_hosts': 13,
                'assets_apply_overrides': 'no',
                'in_assets': 'yes',
            },
            scanner_id=scanner_id,
            schedule_id=schedule_id,
            schedule_periods=None,
            target_id=target_id,
        )

    def test_modify_task_auto_delete_reports_none(
        self, mock_gmp: GmpMockFactory
    ):
        task_id = str(uuid4())
        target_id = str(uuid4())
        scanner_id = str(uuid4())
        scan_config_id = str(uuid4())
        schedule_id = str(uuid4())
        alert_ids = [str(uuid4()), str(uuid4())]

        mock_gmp.mock_response(
            'modify_task',
            '''
            <modify_task_response status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyTask(input: {{
                    id: "{task_id}",
                    name: "bar"
                    comment: "Foo Bar",
                    targetId: "{target_id}",
                    scannerId: "{scanner_id}",
                    scanConfigId: "{scan_config_id}",
                    scheduleId: "{schedule_id}",
                    alertIds: ["{'","'.join(alert_ids)}"],
                    alterable: true,
                    preferences: {{
                        createAssets: true,
                        createAssetsApplyOverrides: false,
                        maxConcurrentNvts: 7,
                        maxConcurrentHosts: 13,
                    }}
                }}) {{
                    ok
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['modifyTask']['ok']

        self.assertEqual(ok, True)

        mock_gmp.gmp_protocol.modify_task.assert_called_with(
            task_id,
            alert_ids=alert_ids,
            alterable=True,
            comment="Foo Bar",
            config_id=scan_config_id,
            name="bar",
            observers=None,
            preferences={
                'auto_delete': 'no',
                'max_checks': 7,
                'max_hosts': 13,
                'assets_apply_overrides': 'no',
                'in_assets': 'yes',
            },
            scanner_id=scanner_id,
            schedule_id=schedule_id,
            schedule_periods=None,
            target_id=target_id,
        )

    def test_modify_task_reset_schedule(self, mock_gmp: GmpMockFactory):
        task_id = str(uuid4())
        target_id = str(uuid4())
        scanner_id = str(uuid4())
        scan_config_id = str(uuid4())
        alert_ids = [str(uuid4()), str(uuid4())]

        mock_gmp.mock_response(
            'modify_task',
            '''
            <modify_task_response status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyTask(input: {{
                    id: "{task_id}",
                    name: "bar"
                    comment: "Foo Bar",
                    targetId: "{target_id}",
                    scannerId: "{scanner_id}",
                    scanConfigId: "{scan_config_id}",
                    alterable: true,
                    alertIds: ["{'","'.join(alert_ids)}"],
                    preferences: {{
                        autoDeleteReports: 4
                        createAssets: true,
                        createAssetsApplyOverrides: false,
                        maxConcurrentNvts: 7,
                        maxConcurrentHosts: 13,
                    }}
                }}) {{
                    ok
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['modifyTask']['ok']

        self.assertEqual(ok, True)

        mock_gmp.gmp_protocol.modify_task.assert_called_with(
            task_id,
            alert_ids=alert_ids,
            alterable=True,
            comment="Foo Bar",
            config_id=scan_config_id,
            name="bar",
            observers=None,
            preferences={
                'auto_delete': 'keep',
                'auto_delete_data': 4,
                'max_checks': 7,
                'max_hosts': 13,
                'assets_apply_overrides': 'no',
                'in_assets': 'yes',
            },
            scanner_id=scanner_id,
            schedule_id=RESET_UUID,
            schedule_periods=None,
            target_id=target_id,
        )

    def test_modify_task_reset_alerts(self, mock_gmp: GmpMockFactory):
        task_id = str(uuid4())
        target_id = str(uuid4())
        scanner_id = str(uuid4())
        scan_config_id = str(uuid4())
        schedule_id = str(uuid4())

        mock_gmp.mock_response(
            'modify_task',
            '''
            <modify_task_response status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyTask(input: {{
                    id: "{task_id}",
                    name: "bar"
                    comment: "Foo Bar",
                    targetId: "{target_id}",
                    scannerId: "{scanner_id}",
                    scanConfigId: "{scan_config_id}",
                    scheduleId: "{schedule_id}",
                    alterable: true,
                    preferences: {{
                        autoDeleteReports: 4
                        createAssets: true,
                        createAssetsApplyOverrides: false,
                        maxConcurrentNvts: 7,
                        maxConcurrentHosts: 13,
                    }}
                }}) {{
                    ok
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['modifyTask']['ok']

        self.assertEqual(ok, True)

        mock_gmp.gmp_protocol.modify_task.assert_called_with(
            task_id,
            alert_ids=[],
            alterable=True,
            comment="Foo Bar",
            config_id=scan_config_id,
            name="bar",
            observers=None,
            preferences={
                'auto_delete': 'keep',
                'auto_delete_data': 4,
                'max_checks': 7,
                'max_hosts': 13,
                'assets_apply_overrides': 'no',
                'in_assets': 'yes',
            },
            scanner_id=scanner_id,
            schedule_id=schedule_id,
            schedule_periods=None,
            target_id=target_id,
        )
