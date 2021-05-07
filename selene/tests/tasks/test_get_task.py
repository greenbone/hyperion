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

from datetime import datetime, timezone
from pathlib import Path

from unittest.mock import patch

from gvm.protocols.next import ScannerType

from selene.schema.scan_configs.fields import ScanConfigType

from selene.schema.tasks.fields import TaskStatus

from selene.tests import SeleneTestCase, GmpMockFactory

from selene.tests.entity import make_test_get_entity

CWD = Path(__file__).absolute().parent


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class TaskTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                task(id: "05d1edfa-3df8-11ea-9651-7b09b3acce77") {
                    id
                    name
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_task(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_task',
            '''
            <get_tasks_response>
                <task id="75d23ba8-3d23-11ea-858e-b7c2cb43e815">
                    <name>a</name>
                </task>
            </get_tasks_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                task(id: "75d23ba8-3d23-11ea-858e-b7c2cb43e815") {
                    id
                    name
                    owner
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        task = json['data']['task']

        self.assertEqual(task['name'], 'a')
        self.assertEqual(task['id'], '75d23ba8-3d23-11ea-858e-b7c2cb43e815')
        self.assertIsNone(task['owner'])

    def test_complex_task(self, mock_gmp: GmpMockFactory):
        task_xml_path = CWD / 'example-task.xml'
        task_xml_str = task_xml_path.read_text()

        mock_gmp.mock_response('get_task', task_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                task(id: "291a7547-c817-4b46-88f2-32415d825335") {
                    id
                    name
                    alterable
                    averageDuration
                    reports {
                        counts {
                            total
                            finished
                        }
                        currentReport {
                            id
                            creationTime
                            scanStart
                            scanEnd
                        }
                        lastReport {
                            id
                            severity
                            creationTime
                            scanStart
                            scanEnd
                        }
                    }
                    status
                    trend
                    creationTime
                    modificationTime
                    progress
                    results {
                        counts {
                            current
                        }
                    }
                    observers {
                        users
                        groups {
                            name
                        }
                        roles {
                            name
                        }
                    }
                    scanConfig {
                        id
                    }
                    target {
                        id
                    }
                    scanner {
                        id
                    }
                    schedule {
                        id
                    }
                    alerts {
                        id
                    }
                    preferences {
                        autoDeleteReports
                        createAssets
                        createAssetsApplyOverrides
                        createAssetsMinQod
                        maxConcurrentHosts
                        maxConcurrentNvts
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        task = json['data']['task']

        self.assertEqual(task['name'], 'Task_for_Report')
        self.assertEqual(task['id'], '291a7547-c817-4b46-88f2-32415d825335')
        self.assertEqual(task['averageDuration'], 0)

        reports = task['reports']

        last_report = reports['lastReport']

        self.assertEqual(
            last_report['creationTime'], '2020-01-15T11:30:10+01:00'
        )
        self.assertEqual(last_report['severity'], 10.0)
        self.assertEqual(
            last_report['id'], 'd453374b-64cc-4c25-9959-7bc7c5287242'
        )
        self.assertEqual(last_report['scanStart'], '2020-01-15T11:30:28+01:00')
        self.assertEqual(last_report['scanEnd'], '2020-01-15T11:39:24+01:00')

        current_report = reports['currentReport']

        self.assertEqual(
            current_report['id'], '64213415-efe5-4441-9ee6-562cacf4e3ce'
        )
        self.assertEqual(
            current_report['creationTime'], '2020-02-04T09:42:14+01:00'
        )
        self.assertEqual(
            current_report['scanStart'], '2020-02-04T09:42:33+01:00'
        )
        self.assertIsNone(current_report['scanEnd'])

        reports_counts = reports['counts']

        self.assertEqual(reports_counts['total'], 1)
        self.assertEqual(reports_counts['finished'], 1)

        self.assertFalse(task['alterable'])

        self.assertEqual(
            task['status'],
            TaskStatus.DONE.name,  # pylint: disable=no-member
        )
        self.assertIsNone(task['trend'])

        dt = datetime(
            2020, 1, 8, hour=14, minute=36, second=21, tzinfo=timezone.utc
        )

        self.assertEqual(task['creationTime'], dt.isoformat())
        self.assertEqual(task['modificationTime'], dt.isoformat())
        self.assertEqual(task['progress'], -1)

        observers = task['observers']

        self.assertIsNotNone(observers)
        self.assertEqual(len(observers['groups']), 1)
        self.assertEqual(observers['groups'][0]['name'], 'plebeians')
        self.assertEqual(len(observers['roles']), 1)
        self.assertEqual(observers['roles'][0]['name'], 'Admin')
        self.assertEqual(len(observers['users']), 2)
        self.assertListEqual(observers['users'], ['admin', 'admin_Clone_4'])

        self.assertIsNone(task['scanConfig'])
        self.assertIsNone(task['target'])
        self.assertIsNone(task['scanner'])
        self.assertIsNone(task['schedule'])

        self.assertIsNone(task['alerts'])

        preferences = task['preferences']
        self.assertEqual(len(preferences), 6)

        self.assertEqual(preferences['autoDeleteReports'], 5)
        self.assertEqual(preferences['createAssets'], True)
        self.assertEqual(preferences['createAssetsApplyOverrides'], True)
        self.assertEqual(preferences['createAssetsMinQod'], 70)
        self.assertEqual(preferences['maxConcurrentNvts'], 4)
        self.assertEqual(preferences['maxConcurrentHosts'], 20)

        results_counts = task['results']['counts']
        self.assertEqual(results_counts['current'], 50000)

    def test_sub_objects(self, mock_gmp: GmpMockFactory):
        task_xml_path = CWD / 'example-task-2.xml'
        task_xml_str = task_xml_path.read_text()

        mock_gmp.mock_response('get_task', task_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                task(id: "7593ad78-6cbc-48aa-94a4-5e52bb6b3f80") {
                    id
                    name
                    scanConfig {
                        id
                        name
                        trash
                        type
                    }
                    target {
                        id
                        name
                        trash
                    }
                    scanner {
                        id
                        name
                        type
                        trash
                    }
                    schedule {
                        id
                        name
                        trash
                        icalendar
                        timezone
                    }
                    alerts {
                        id
                        name
                    }
                    schedulePeriods
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        task = json['data']['task']

        self.assertEqual(task['name'], 'Example')
        self.assertEqual(task['id'], '7593ad78-6cbc-48aa-94a4-5e52bb6b3f80')

        scan_config = task['scanConfig']
        self.assertEqual(scan_config['name'], 'Base')
        self.assertEqual(
            scan_config['id'], 'd21f6c81-2b88-4ac1-b7b4-a2a9f2ad4663'
        )
        self.assertFalse(scan_config['trash'])
        self.assertEqual(
            scan_config['type'],
            ScanConfigType.OPENVAS.name,  # pylint: disable=no-member
        )

        target = task['target']
        self.assertEqual(target['name'], 'Localhost')
        self.assertEqual(target['id'], 'e1db1b66-f86f-4a09-bb9e-c81d73d85a5d')
        self.assertFalse(target['trash'])

        scanner = task['scanner']
        self.assertEqual(scanner['name'], 'OpenVAS Default')
        self.assertEqual(scanner['id'], '08b69003-5fc2-4037-a479-93b440211c73')
        self.assertFalse(scanner['trash'])
        self.assertEqual(scanner['type'], ScannerType.OPENVAS_SCANNER_TYPE.name)

        schedule = task['schedule']
        self.assertEqual(schedule['name'], 'Every Week on Friday 16h UTC')
        self.assertEqual(schedule['id'], '25473f83-6086-40cb-bbf9-c52cb6c5b92e')
        self.assertFalse(schedule['trash'])
        self.assertEqual(schedule['timezone'], 'UTC')
        self.assertRegex(schedule['icalendar'], r'^BEGIN:VCALENDAR.*')
        self.assertEqual(schedule['timezone'], 'UTC')

        schedule_periods = task['schedulePeriods']

        self.assertEqual(schedule_periods, 0)

        alerts = task['alerts']
        self.assertEqual(len(alerts), 2)

        alert1 = alerts[0]
        self.assertEqual(alert1['name'], 'Http Alert')
        self.assertEqual(alert1['id'], '8c1e0414-95e4-4bd6-8823-fc507c1fe34b')

        alert2 = alerts[1]
        self.assertEqual(alert2['name'], 'Send to Host')
        self.assertEqual(alert2['id'], '8957b33c-ed0d-47c3-a955-4056498bfef2')


class TaskGetEntityTestCase(SeleneTestCase):
    gmp_name = 'task'
    test_get_entity = make_test_get_entity(gmp_name)
