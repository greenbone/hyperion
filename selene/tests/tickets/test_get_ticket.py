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
class TicketTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                ticket(id: "cda26919-dbc2-439a-aa64-ce0ada728dd0") {
                    id
                    name
                    comment
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_ticket(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_ticket',
            '''
            <get_ticket_response>
                <ticket id="cda26919-dbc2-439a-aa64-ce0ada728dd0">
                    <owner>
                    <name>xyzxy</name>
                    </owner>
                    <name>what_ever</name>
                    <comment>weeee</comment>
                    <creation_time>2020-10-07T02:54:44Z</creation_time>
                    <modification_time>2020-10-07T02:54:44Z</modification_time>
                    <writable>1</writable>
                    <in_use>0</in_use>
                    <permissions>
                        <permission>
                            <name>Everything</name>
                        </permission>
                    </permissions>
                    <assigned_to>
                        <user id="3d74cfb5-a7bf-4c7e-b25d-0a719ec3f32a">
                            <name>glurp</name>
                        </user>
                    </assigned_to>
                    <severity>10.0</severity>
                    <host>172.16.20.120</host>
                    <location/>
                    <solution_type>VendorFix</solution_type>
                    <status>Open</status>
                    <open_time>2020-10-07T02:54:44Z</open_time>
                    <open_note>opened</open_note>
                    <fixed_time>2020-10-07T07:54:44Z</fixed_time>
                    <fixed_note>fixed</fixed_note>
                    <closed_time>2020-10-08T02:54:44Z</closed_time>
                    <closed_note>closed</closed_note>
                    <nvt oid="1.3.6.1.4.1.25623.1.0.100494"/>
                    <task id="dc9c6b7d-c81d-4e20-acd8-b187b018fa42">
                        <name>gwarp</name>
                        <trash>0</trash>
                    </task>
                    <report id="f31d3b1a-4642-44bc-86ea-63ea029d4c63">
                        <timestamp>2020-06-19T09:31:15Z</timestamp>
                    </report>
                    <result id="f5d7ce0b-4430-4467-bcf6-7908db17e2f5"/>
                    <orphan>0</orphan>
                </ticket>
            </get_ticket_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                ticket(id: "cda26919-dbc2-439a-aa64-ce0ada728dd0") {
                    id
                    name
                    comment
                    host
                    location
                    openNote
                    openTime
                    fixedNote
                    fixedTime
                    closedNote
                    closedTime
                    assignedTo {
                        id
                        name
                    }
                    nvtOid
                    task {
                        id
                        name
                    }
                    report {
                        id
                        timestamp
                    }
                    result
                    orphan
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ticket = json['data']['ticket']

        self.assertEqual(ticket['id'], 'cda26919-dbc2-439a-aa64-ce0ada728dd0')
        self.assertEqual(
            ticket['name'],
            "what_ever",
        )
        self.assertEqual(ticket['comment'], 'weeee')
        self.assertEqual(ticket['host'], '172.16.20.120')
        self.assertEqual(
            ticket['assignedTo']['id'], '3d74cfb5-a7bf-4c7e-b25d-0a719ec3f32a'
        )
        self.assertEqual(ticket['assignedTo']['name'], 'glurp')
        self.assertEqual(ticket['nvtOid'], '1.3.6.1.4.1.25623.1.0.100494')
        self.assertEqual(
            ticket['task']['id'],
            'dc9c6b7d-c81d-4e20-acd8-b187b018fa42',
        )
        self.assertEqual(ticket['openNote'], 'opened')
        self.assertEqual(ticket['openTime'], '2020-10-07T02:54:44+00:00')
        self.assertEqual(ticket['fixedNote'], 'fixed')
        self.assertEqual(ticket['fixedTime'], '2020-10-07T07:54:44+00:00')
        self.assertEqual(ticket['closedNote'], 'closed')
        self.assertEqual(ticket['closedTime'], '2020-10-08T02:54:44+00:00')

        self.assertEqual(ticket['task']['name'], 'gwarp')
        self.assertEqual(
            ticket['report']['id'], 'f31d3b1a-4642-44bc-86ea-63ea029d4c63'
        )
        self.assertEqual(
            ticket['report']['timestamp'], '2020-06-19T09:31:15+00:00'
        )
        self.assertEqual(
            ticket['result'], 'f5d7ce0b-4430-4467-bcf6-7908db17e2f5'
        )
        self.assertFalse(ticket['orphan'])


class TicketGetEntityTestCase(SeleneTestCase):
    gmp_name = 'ticket'
    test_get_entity = make_test_get_entity(gmp_name)
