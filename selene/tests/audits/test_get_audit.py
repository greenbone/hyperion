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

from pathlib import Path

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory

from selene.tests.entity import make_test_get_entity

CWD = Path(__file__).absolute().parent


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class AuditTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                audit(id: "05d1edfa-3df8-11ea-9651-7b09b3acce77") {
                    id
                    name
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_audit(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_audit',
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
                audit(id: "75d23ba8-3d23-11ea-858e-b7c2cb43e815") {
                    id
                    name
                    owner
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        audit = json['data']['audit']

        self.assertEqual(audit['name'], 'a')
        self.assertEqual(audit['id'], '75d23ba8-3d23-11ea-858e-b7c2cb43e815')
        self.assertIsNone(audit['owner'])

    def test_complex_audit(self, mock_gmp: GmpMockFactory):
        audit_xml_path = CWD / 'example-audit.xml'
        audit_xml_str = audit_xml_path.read_text()

        mock_gmp.mock_response('get_audit', audit_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                audit(id: "c4335bf9-de7d-4d45-984a-a4a19709a098") {
                    id
                    name
                    comment
                    alterable
                    reports {
                        counts {
                            total
                            finished
                        }
                        currentReport {
                            id
                            timestamp
                            scanStart
                            scanEnd
                        }
                        lastReport {
                            id
                            severity
                            timestamp
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
                    policy {
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
                    preferences {
                        name
                        description
                        value
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        audit = json['data']['audit']

        self.assertEqual(audit['name'], 'Audit_for_Report')
        self.assertEqual(audit['id'], 'c4335bf9-de7d-4d45-984a-a4a19709a098')
        self.assertEqual(audit['comment'], 'foo')
        self.assertEqual(audit['status'], 'New')
        self.assertEqual(audit['progress'], -1)
        self.assertIsNone(audit['trend'])

        reports = audit['reports']

        self.assertIsNone(reports['lastReport'])
        self.assertIsNone(reports['currentReport'])
        self.assertEqual(reports['counts']['total'], 0)

        target = audit['target']
        self.assertEqual(target['id'], '2d161fb3-1867-4683-a5dc-f2e375194552')
        self.assertEqual(target['name'], '234234Unnamed')

        scanner = audit['scanner']
        self.assertEqual(scanner['id'], '08b69003-5fc2-4037-a479-93b440211c73')
        self.assertEqual(scanner['name'], 'OpenVAS Default')
        self.assertEqual(scanner['type'], 'OPENVAS_SCANNER_TYPE')

        schedule = audit['schedule']
        self.assertEqual(schedule['id'], 'fef95cd5-3a0a-4df5-bb73-161f75aa3eda')
        self.assertEqual(
            schedule['name'], 'Schedule for alertask - 2020-10-21T08:56:08.850Z'
        )
        self.assertEqual(schedule['timezone'], 'UTC')
        self.assertEqual(
            schedule['icalendar'],
            """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Greenbone.net//NONSGML Greenbone Security Manager
 21.4.0~dev1~git-a98bd26-master//EN
BEGIN:VEVENT
DTSTART:20201021T085600Z
DURATION:PT0S
UID:339d3438-ae77-49cd-a680-505bc0bb026a
DTSTAMP:20201021T085608Z
END:VEVENT
END:VCALENDAR
            """,
        )

        self.assertIsNone(audit['alerts'])
        observers = audit['observers']
        self.assertEqual(observers['users'], ['admin'])

        policy = audit['policy']
        self.assertEqual(policy['id'], '9f822ad3-9208-4e02-ac03-78dce3ca9a23')
        self.assertEqual(policy['name'], 'EulerOS Linux Security Configuration')
        self.assertEqual(policy['type'], 0)
        self.assertEqual(policy['trash'], 0)


class AuditGetEntityTestCase(SeleneTestCase):
    gmp_name = 'task'
    selene_name = 'audit'
    gmp_cmd = 'get_audit'
    test_get_entity = make_test_get_entity(
        gmp_name=gmp_name, selene_name=selene_name, gmp_cmd=gmp_cmd
    )
