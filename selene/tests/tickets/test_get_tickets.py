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
    make_test_edges,
    make_test_page_info,
    make_test_before_last,
    make_test_after_first_before_last,
)
from selene.tests.entity import make_test_get_entities

from selene.schema.tickets.queries import GetTickets


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class TicketTestCase(SeleneTestCase):
    def setUp(self):
        self.xml = '''
            <get_tickets_response>
                <ticket id="08b69003-5fc2-4037-a479-93b440211c73">
                    <name>foo</name>
                    <comment>bar</comment>
                </ticket>
                <ticket id="6b2db524-9fb0-45b8-9b56-d958f84cb546">
                    <name>lorem</name>
                    <comment>ipsum</comment>
                </ticket>
                <tickets start="1" max="10"/>
                <ticket_count>2<filtered>2</filtered>
                    <page>2</page>
                </ticket_count>
            </get_tickets_response>
            '''

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                tickets {
                    nodes {
                        id
                        name
                        comment
                    }
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_tickets(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_tickets', self.xml)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                tickets {
                    nodes {
                        id
                        name
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        tickets = json['data']['tickets']['nodes']

        self.assertEqual(len(tickets), 2)

        ticket1 = tickets[0]
        ticket2 = tickets[1]

        # Ticket 1

        self.assertEqual(ticket1['id'], '08b69003-5fc2-4037-a479-93b440211c73')
        self.assertEqual(ticket1['name'], 'foo')

        # Ticket 2

        self.assertEqual(ticket2['id'], '6b2db524-9fb0-45b8-9b56-d958f84cb546')
        self.assertEqual(ticket2['name'], 'lorem')

    def test_get_filtered_tickets(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_tickets', self.xml)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                tickets (
                    filterString: "lorem",
                ) {
                    nodes {
                        id
                        name
                        comment
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        tickets = json['data']['tickets']['nodes']

        self.assertEqual(len(tickets), 2)

        ticket1 = tickets[0]
        ticket2 = tickets[1]

        self.assertEqual(ticket1['id'], '08b69003-5fc2-4037-a479-93b440211c73')
        self.assertEqual(ticket1['name'], 'foo')
        self.assertEqual(ticket1['comment'], 'bar')

        self.assertEqual(ticket2['id'], '6b2db524-9fb0-45b8-9b56-d958f84cb546')
        self.assertEqual(ticket2['name'], 'lorem')
        self.assertEqual(ticket2['comment'], 'ipsum')


class TicketsPaginationTestCase(SeleneTestCase):
    entity_name = 'ticket'
    edge_name = 'remediationticket'
    test_pagination_with_after_and_first = make_test_after_first(entity_name)
    test_counts = make_test_counts(entity_name)
    test_get_page_info = make_test_page_info(entity_name, query=GetTickets)
    test_edges = make_test_edges(entity_name, edge_name=edge_name)
    test_pagination_with_before_and_last = make_test_before_last(entity_name)
    test_after_first_before_last = make_test_after_first_before_last(
        entity_name
    )


class TicketsGetEntitiesTestCase(SeleneTestCase):
    gmp_name = "ticket"
    test_get_entities = make_test_get_entities(gmp_name)
