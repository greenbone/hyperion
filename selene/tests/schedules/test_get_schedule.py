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
class ScheduleTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                schedule(id: "2bc16940-bde7-459e-84ff-c1067157c510") {
                    id
                    name
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_schedule(self, mock_gmp: GmpMockFactory):
        # pylint: disable=line-too-long
        mock_gmp.mock_response(
            'get_schedule',
            '''
            <get_schedules_response>
                <schedule id="2bc16940-bde7-459e-84ff-c1067157c510">
                    <name>Weekly schedule</name>
                    <comment>Heavy</comment>
                    <owner><name>Fives</name></owner>
                    <creation_time>2020-06-30T09:16:25Z</creation_time>
                    <modification_time>2020-07-30T09:16:25Z</modification_time>
                    <writable>1</writable>
                    <in_use>1</in_use>
                    <icalendar>BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Greenbone.net//NONSGML Greenbone Security Manager \n 21.04+alpha~git-bb97c86-master//EN\nBEGIN:VEVENT\nDTSTART:20200812T100600Z\nDURATION:PT0S\nUID:3dfd6e6f-4e79-4f18-a5c2-adb3fca56bd3\nDTSTAMP:20200812T091145Z\nEND:VEVENT\nEND:VCALENDAR\n</icalendar>
                    <timezone>UTC</timezone>
                    <permissions>
                        <permission><name>Everything</name></permission>
                    </permissions>
                    <user_tags>
                        <count>1</count>
                    </user_tags>
                    <tasks>
                        <task id="2bc16940-bde7-459e-84ff-c1067157c512">
                            <name>scheduled task</name>
                        </task>
                    </tasks>
                </schedule>
            </get_schedules_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                schedule(
                    id: "2bc16940-bde7-459e-84ff-c1067157c510"
                ) {
                    name
                    comment
                    id
                    owner
                    creationTime
                    modificationTime
                    writable
                    inUse
                    icalendar
                    timezone
                    permissions {
                        name
                    }
                    userTags {
                        count
                    }
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

        schedule = json['data']['schedule']

        self.assertEqual(schedule['id'], '2bc16940-bde7-459e-84ff-c1067157c510')
        self.assertEqual(schedule['owner'], 'Fives')
        self.assertEqual(schedule['creationTime'], '2020-06-30T09:16:25+00:00')
        self.assertEqual(
            schedule['modificationTime'], '2020-07-30T09:16:25+00:00'
        )
        self.assertEqual(schedule['writable'], True)
        self.assertEqual(schedule['inUse'], True)
        self.assertEqual(schedule['name'], 'Weekly schedule')
        self.assertEqual(schedule['comment'], 'Heavy')
        self.assertEqual(schedule['timezone'], 'UTC')
        # pylint: disable=line-too-long
        self.assertEqual(
            schedule['icalendar'],
            'BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Greenbone.net//NONSGML Greenbone Security Manager \n 21.04+alpha~git-bb97c86-master//EN\nBEGIN:VEVENT\nDTSTART:20200812T100600Z\nDURATION:PT0S\nUID:3dfd6e6f-4e79-4f18-a5c2-adb3fca56bd3\nDTSTAMP:20200812T091145Z\nEND:VEVENT\nEND:VCALENDAR\n',
        )
        self.assertEqual(schedule['permissions'][0]['name'], 'Everything')
        self.assertEqual(schedule['userTags']['count'], 1)
        self.assertEqual(
            schedule['tasks'][0]['id'], '2bc16940-bde7-459e-84ff-c1067157c512'
        )


class ScheduleGetEntityTestCase(SeleneTestCase):
    gmp_name = 'schedule'
    test_get_entity = make_test_get_entity(gmp_name, tasks=True)
