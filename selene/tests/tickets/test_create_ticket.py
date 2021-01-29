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
class CreateTicketTestCase(SeleneTestCase):
    def setUp(self):
        self.ticket_id = uuid4()
        self.result_id = uuid4()
        self.assignee_id = uuid4()

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            f'''
            mutation {{
                createTicket(input: {{
                    note: "bar"
                    resultId: "{self.result_id}"
                    assignedToUserId: "{self.assignee_id}"
                }}) {{
                    id
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_create_ticket(self, mock_gmp: GmpMockFactory):

        mock_gmp.mock_response(
            'create_ticket',
            f'''
            <create_ticket_response
                id="{self.ticket_id}"
                status="200"
                status_text="OK"
            />
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                createTicket(input: {{
                    note: "bar"
                    resultId: "{self.result_id}"
                    assignedToUserId: "{self.assignee_id}"
                    comment: "glurp"
                }}) {{
                    id
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        uuid = json['data']['createTicket']['id']

        self.assertEqual(uuid, str(self.ticket_id))

        mock_gmp.gmp_protocol.create_ticket.assert_called_with(
            note="bar",
            comment="glurp",
            result_id=str(self.result_id),
            assigned_to_user_id=str(self.assignee_id),
        )
