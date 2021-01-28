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

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory
from selene.tests.pagination import (
    make_test_counts,
    make_test_after_first,
    make_test_page_info,
    make_test_edges,
    make_test_before_last,
    make_test_after_first_before_last,
)
from selene.tests.entity import make_test_get_entities

from selene.schema.schedules.queries import GetSchedules


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class SchedulesTestCase(SeleneTestCase):
    def setUp(self):
        # pylint: disable=line-too-long
        self.xml = '''
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
                <schedule id="2bc16940-bde7-459e-84ff-c1067157c511">
                    <name>Order 66</name>
                    <comment>Only once</comment>
                    <owner><name>Palpatine</name></owner>
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
                <schedule_count>
                    20
                    <filtered>2</filtered>
                </schedule_count>
                <schedules max="10" start="1"/>
            </get_schedules_response>
            '''

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                schedules {
                    nodes {
                        id
                    }
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_schedules(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_schedules', self.xml)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                schedules {
                    nodes {
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
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        schedules = json['data']['schedules']['nodes']

        self.assertEqual(len(schedules), 2)

        schedule1 = schedules[0]
        schedule2 = schedules[1]

        self.assertEqual(
            schedule1['id'], '2bc16940-bde7-459e-84ff-c1067157c510'
        )
        self.assertEqual(schedule1['owner'], 'Fives')
        self.assertEqual(schedule1['creationTime'], '2020-06-30T09:16:25+00:00')
        self.assertEqual(
            schedule1['modificationTime'], '2020-07-30T09:16:25+00:00'
        )
        self.assertEqual(schedule1['writable'], True)
        self.assertEqual(schedule1['inUse'], True)
        self.assertEqual(schedule1['name'], 'Weekly schedule')
        self.assertEqual(schedule1['comment'], 'Heavy')
        self.assertEqual(schedule1['timezone'], 'UTC')
        # pylint: disable=line-too-long
        self.assertEqual(
            schedule1['icalendar'],
            'BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Greenbone.net//NONSGML Greenbone Security Manager \n 21.04+alpha~git-bb97c86-master//EN\nBEGIN:VEVENT\nDTSTART:20200812T100600Z\nDURATION:PT0S\nUID:3dfd6e6f-4e79-4f18-a5c2-adb3fca56bd3\nDTSTAMP:20200812T091145Z\nEND:VEVENT\nEND:VCALENDAR\n',
        )
        self.assertEqual(schedule1['permissions'][0]['name'], 'Everything')
        self.assertEqual(schedule1['userTags']['count'], 1)
        self.assertEqual(
            schedule1['tasks'][0]['id'], '2bc16940-bde7-459e-84ff-c1067157c512'
        )
        self.assertEqual(schedule1['tasks'][0]['name'], 'scheduled task')
        self.assertEqual(
            schedule2['id'], '2bc16940-bde7-459e-84ff-c1067157c511'
        )
        self.assertEqual(schedule2['owner'], 'Palpatine')
        self.assertEqual(schedule2['creationTime'], '2020-06-30T09:16:25+00:00')
        self.assertEqual(
            schedule2['modificationTime'], '2020-07-30T09:16:25+00:00'
        )
        self.assertEqual(schedule2['writable'], True)
        self.assertEqual(schedule2['inUse'], True)
        self.assertEqual(schedule2['name'], 'Order 66')
        self.assertEqual(schedule2['comment'], 'Only once')
        self.assertEqual(schedule2['timezone'], 'UTC')
        # pylint: disable=line-too-long
        self.assertEqual(
            schedule2['icalendar'],
            'BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Greenbone.net//NONSGML Greenbone Security Manager \n 21.04+alpha~git-bb97c86-master//EN\nBEGIN:VEVENT\nDTSTART:20200812T100600Z\nDURATION:PT0S\nUID:3dfd6e6f-4e79-4f18-a5c2-adb3fca56bd3\nDTSTAMP:20200812T091145Z\nEND:VEVENT\nEND:VCALENDAR\n',
        )
        self.assertEqual(schedule2['permissions'][0]['name'], 'Everything')
        self.assertEqual(schedule2['userTags']['count'], 1)
        self.assertEqual(
            schedule2['tasks'][0]['id'], '2bc16940-bde7-459e-84ff-c1067157c512'
        )
        self.assertEqual(schedule2['tasks'][0]['name'], 'scheduled task')

    def test_get_filtered_schedules(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_schedules', self.xml)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                schedules (
                    filterString: "order",
                ) {
                    nodes {
                        id
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        schedules = json['data']['schedules']['nodes']

        self.assertEqual(len(schedules), 2)

        schedule1 = schedules[0]
        schedule2 = schedules[1]

        self.assertEqual(
            schedule1['id'], '2bc16940-bde7-459e-84ff-c1067157c510'
        )

        self.assertEqual(
            schedule2['id'], '2bc16940-bde7-459e-84ff-c1067157c511'
        )


class SchedulesGetEntitiesTestCase(SeleneTestCase):
    gmp_name = 'schedule'
    test_get_entities = make_test_get_entities(gmp_name)


class SchedulesPaginationTestCase(SeleneTestCase):
    gmp_name = 'schedule'
    test_pagination_with_after_and_first = make_test_after_first(gmp_name)
    test_counts = make_test_counts(gmp_name)
    test_page_info = make_test_page_info(gmp_name, query=GetSchedules)
    test_pagination_with_before_and_last = make_test_before_last(gmp_name)
    test_edges = make_test_edges(gmp_name)
    test_after_first_before_last = make_test_after_first_before_last(gmp_name)
