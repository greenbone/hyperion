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
class DeleteSchedulesByIdsTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            mutation {
                deleteSchedulesByIds(
                    ids: ["a1438fb2-ab2c-4f4a-ad6b-de97005256e8",
                          "b1438fb2-ab2c-4f4a-ad6b-de97005256e8"],
                    ultimate: false)
                {
                   ok
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_delete_schedules_by_ids(self, mock_gmp: GmpMockFactory):
        self.login('foo', 'bar')

        id1 = uuid4()
        id2 = uuid4()

        mock_gmp.mock_response(
            'get_schedules',
            f'''
            <get_schedule_response status="200" status_text="OK">
                <schedule id="{id1}">
                </schedule>
                <schedule id="{id2}">
                </schedule>
            </get_schedule_response>
            ''',
        )

        response = self.query(
            f'''
            mutation {{
                deleteSchedulesByIds(ids: ["{id1}", "{id2}"],
                    ultimate:true)
                {{
                    ok
                }}
            }}
            '''
        )
        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['deleteSchedulesByIds']['ok']
        self.assertTrue(ok)

        mock_gmp.gmp_protocol.get_schedules.assert_called_with(
            filter=f'uuid={id1} uuid={id2} '
        )

        mock_gmp.gmp_protocol.delete_schedule.assert_any_call(
            schedule_id=str(id1), ultimate=True
        )

        mock_gmp.gmp_protocol.delete_schedule.assert_any_call(
            schedule_id=str(id2), ultimate=True
        )

    def test_delete_by_ids_invalid(self, mock_gmp: GmpMockFactory):
        self.login('foo', 'bar')

        id1 = uuid4()
        id2 = uuid4()

        # Return only one schedule instead of the queried two.
        mock_gmp.mock_response(
            'get_schedules',
            f'''
            <get_schedule_response status="200" status_text="OK">
                <schedule id="{id1}">
                </schedule>
            </get_schedule_response>
            ''',
        )

        response = self.query(
            f'''
            mutation {{
                deleteSchedulesByIds(ids: ["{id1}", "{id2}"],
                    ultimate:true)
                {{
                    ok
                }}
            }}
            '''
        )
        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['deleteSchedulesByIds']['ok']
        self.assertFalse(ok)

        mock_gmp.gmp_protocol.get_schedules.assert_called_with(
            filter=f'uuid={id1} uuid={id2} '
        )
