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

from gvm.protocols.next import get_ticket_status_from_string

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class ModifyTicketTestCase(SeleneTestCase):
    def setUp(self):
        self.ticket_id = uuid4()
        self.result_id = uuid4()
        self.assignee_id = uuid4()

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            f'''
            mutation {{
                modifyTicket(input: {{
                    id: "{self.ticket_id}",
                }}) {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_modify_ticket(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'modify_ticket',
            '''
            <modify_ticket_response status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyTicket(input: {{
                    id: "{self.ticket_id}"
                    ticketStatus: CLOSED
                    comment: "glurp"
                    note: "bar"
                    assignedToUserId: "{self.assignee_id}"
                }}) {{
                    ok
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['modifyTicket']['ok']

        self.assertEqual(ok, True)

        mock_gmp.gmp_protocol.modify_ticket.assert_called_with(
            str(self.ticket_id),
            note="bar",
            comment="glurp",
            assigned_to_user_id=str(self.assignee_id),
            status=get_ticket_status_from_string('closed'),
        )
