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
class DeleteTicketByFilterTestCase(SeleneTestCase):
    def setUp(self):
        self.id1 = uuid4()
        self.id2 = uuid4()
        self.xml = f'''
            <get_ticket_response status="200" status_text="OK">
                <ticket id="{self.id1}">
                    <name>Foo Clone 1</name>
                    <type>0</type>
                </ticket>
                <ticket id="{self.id2}">
                    <name>Foo Clone 2</name>
                    <type>1</type>
                </ticket>
            </get_ticket_response>
            '''

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            mutation {
                deleteTicketsByFilter(
                    filterString:"name~Clone",
                    ultimate: false)
                {
                   ok
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_delte_tickets_by_filter(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_tickets', self.xml)

        self.login('foo', 'bar')

        response = self.query(
            '''
            mutation {
                deleteTicketsByFilter(
                    filterString:"name~Clone",
                    ultimate: false)
                {
                   ok
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['deleteTicketsByFilter']['ok']
        self.assertTrue(ok)

        mock_gmp.gmp_protocol.get_tickets.assert_called_with(
            filter_string="name~Clone"
        )

        mock_gmp.gmp_protocol.delete_ticket.assert_any_call(
            ticket_id=str(self.id1)
        )
        mock_gmp.gmp_protocol.delete_ticket.assert_any_call(
            ticket_id=str(self.id2)
        )
