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
class CreateTaskTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            f'''
            mutation {{
                createTask(input: {{
                    name: "foo",
                    scannerId: "{uuid4()}",
                    scanConfigId: "{uuid4()}",
                    targetId: "{uuid4()}"
                }}) {{
                    id
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_create_task(self, mock_gmp: GmpMockFactory):
        task_id = str(uuid4())
        config_id = str(uuid4())
        target_id = str(uuid4())
        scanner_id = str(uuid4())

        mock_gmp.mock_response(
            'create_task',
            f'''
            <create_task_response id="{task_id}" status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                createTask(input: {{
                    name: "bar",
                    scannerId: "{scanner_id}",
                    scanConfigId: "{config_id}",
                    targetId: "{target_id}",
                    preferences: {{
                        autoDeleteReports: 4,
                        createAssets: true,
                        createAssetsApplyOverrides: false
                        maxConcurrentNvts: 7,
                        maxConcurrentHosts: 13,
                    }}
                }}) {{
                    id
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        uuid = json['data']['createTask']['id']

        self.assertEqual(uuid, task_id)

        mock_gmp.gmp_protocol.create_task.assert_called_with(
            "bar",
            config_id,
            target_id,
            scanner_id,
            alert_ids=None,
            alterable=None,
            comment=None,
            observers=None,
            preferences={
                'auto_delete': 'keep',
                'auto_delete_data': 4,
                'max_checks': 7,
                'max_hosts': 13,
                'in_assets': 'yes',
                'assets_apply_overrides': 'no',
            },
            schedule_id=None,
            schedule_periods=None,
        )

    def test_create_task_auto_delete_reports_none(
        self, mock_gmp: GmpMockFactory
    ):
        task_id = str(uuid4())
        config_id = str(uuid4())
        target_id = str(uuid4())
        scanner_id = str(uuid4())

        mock_gmp.mock_response(
            'create_task',
            f'''
            <create_task_response id="{task_id}" status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                createTask(input: {{
                    name: "bar",
                    scannerId: "{scanner_id}",
                    scanConfigId: "{config_id}",
                    targetId: "{target_id}",
                    preferences: {{
                        createAssets: true,
                        createAssetsApplyOverrides: false
                        maxConcurrentNvts: 7,
                        maxConcurrentHosts: 13,
                    }}
                }}) {{
                    id
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        uuid = json['data']['createTask']['id']

        self.assertEqual(uuid, task_id)

        mock_gmp.gmp_protocol.create_task.assert_called_with(
            "bar",
            config_id,
            target_id,
            scanner_id,
            alert_ids=None,
            alterable=None,
            comment=None,
            observers=None,
            preferences={
                'auto_delete': 'no',
                'max_checks': 7,
                'max_hosts': 13,
                'in_assets': 'yes',
                'assets_apply_overrides': 'no',
            },
            schedule_id=None,
            schedule_periods=None,
        )
