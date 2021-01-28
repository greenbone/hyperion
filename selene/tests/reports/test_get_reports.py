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

from selene.schema.reports.queries import GetReports


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class ReportsTestCase(SeleneTestCase):
    def setUp(self):
        self.qu = '''
                    query {
                        reports {
                            nodes {
                                id
                                name
                            }
                        }
                    }
                    '''

        self.resp = '''
                    <get_reports_response>
                        <report id="1f3261c9-e47c-4a21-b677-826ea92d1d59">
                            <name>a</name>
                        </report>
                        <report id="83c907a4-b2e4-403e-a5ba-9f831092b106">
                            <name>b</name>
                        </report>
                    </get_reports_response>
                    '''

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(self.qu)

        self.assertResponseAuthenticationRequired(response)

    def test_get_reports(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_reports', self.resp)

        self.login('foo', 'bar')

        response = self.query(self.qu)

        json = response.json()

        self.assertResponseNoErrors(response)

        reports = json['data']['reports']['nodes']

        self.assertEqual(len(reports), 2)

        report1 = reports[0]
        report2 = reports[1]

        self.assertEqual(report1['name'], 'a')
        self.assertEqual(report1['id'], '1f3261c9-e47c-4a21-b677-826ea92d1d59')
        self.assertEqual(report2['name'], 'b')
        self.assertEqual(report2['id'], '83c907a4-b2e4-403e-a5ba-9f831092b106')

    def test_get_filtered_reports(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_reports', self.resp)

        self.login('foo', 'bar')

        response = self.query(self.qu)

        json = response.json()

        self.assertResponseNoErrors(response)

        reports = json['data']['reports']['nodes']

        self.assertEqual(len(reports), 2)

        report1 = reports[0]
        report2 = reports[1]

        self.assertEqual(report1['name'], 'a')
        self.assertEqual(report1['id'], '1f3261c9-e47c-4a21-b677-826ea92d1d59')
        self.assertEqual(report2['name'], 'b')
        self.assertEqual(report2['id'], '83c907a4-b2e4-403e-a5ba-9f831092b106')

    def test_edges(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_reports',
            '''
            <get_reports_response>
                <report id="f650a1c0-3d23-11ea-8540-e790e17c1b00">
                    <name>a</name>
                </report>
                <report id="0778ac90-3d24-11ea-b722-fff755412c48">
                    <name>b</name>
                </report>
                <report_count>
                    20
                    <filtered>11</filtered>
                </report_count>
                <reports max="10" start="3"/>
            </get_reports_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                reports {
                    edges {
                        node {
                            id
                            name
                        }
                        cursor
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        edges = json['data']['reports']['edges']

        self.assertEqual(len(edges), 2)

        edge_class = GetReports().type._meta.edge

        edge1 = edges[0]
        edge2 = edges[1]

        self.assertEqual(edge1['cursor'], edge_class.get_cursor(2))
        self.assertEqual(
            edge1['node']['id'], "f650a1c0-3d23-11ea-8540-e790e17c1b00"
        )
        self.assertEqual(edge1['node']['name'], "a")
        self.assertEqual(edge2['cursor'], edge_class.get_cursor(3))
        self.assertEqual(
            edge2['node']['id'], "0778ac90-3d24-11ea-b722-fff755412c48"
        )
        self.assertEqual(edge2['node']['name'], "b")


class ReportsPaginationTestCase(SeleneTestCase):
    entity_name = 'report'
    test_pagination_with_after_and_first = make_test_after_first(entity_name)
    test_counts = make_test_counts(entity_name)
    test_page_info = make_test_page_info(entity_name, query=GetReports)
    test_pagination_with_before_and_last = make_test_before_last(entity_name)
    test_edges = make_test_edges(entity_name)
    test_after_first_before_last = make_test_after_first_before_last(
        entity_name
    )
