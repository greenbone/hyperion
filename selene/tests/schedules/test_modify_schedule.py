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

from uuid import uuid4

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class ModifyScheduleTestCase(SeleneTestCase):
    def setUp(self):
        self.schedule_id = uuid4()
        self.ical = (
            "BEGIN:VCALENDAR"
            "VERSION:2.0"
            "PRODID:-//Greenbone.net//NONSGML Greenbone \
            Security Manager 8.0.0//EN"
            "BEGIN:VEVENT"
            "UID:c35f82f1-7798-4b84-b2c4-761a33068956"
            "DTSTAMP:20190715T124352Z"
            "DTSTART:20190716T040000Z"
            "END:VEVENT"
            "END:VCALENDAR"
        )

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            f'''
            mutation {{
                modifySchedule(input: {{
                    id: "{self.schedule_id}"
                }}) {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_modify_schedule(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'modify_schedule',
            '''
            <modify_schedule_response status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifySchedule(input: {{
                    id: "{self.schedule_id}",
                    icalendar: "{self.ical}"
                }}) {{
                    ok
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['modifySchedule']['ok']

        self.assertEqual(ok, True)

        mock_gmp.gmp_protocol.modify_schedule.assert_called_with(
            str(self.schedule_id),
            name=None,
            icalendar=self.ical,
            timezone=None,
            comment=None,
        )
