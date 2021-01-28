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
from pathlib import Path

from selene.tests import SeleneTestCase, GmpMockFactory
from selene.tests.entity import make_test_get_entities

from selene.tests.pagination import (
    make_test_counts,
    make_test_after_first,
    make_test_page_info,
    make_test_before_last,
    make_test_after_first_before_last,
)
from selene.schema.report_formats.queries import GetReportFormats

CWD = Path(__file__).absolute().parent


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class GetReportFormatsTestCase(SeleneTestCase):
    def setUp(self):
        self.qu = '''
                    query {
                        reportFormats {
                            nodes {
                                id
                                name
                            }
                        }
                    }
                    '''

        self.resp = '''
                    <get_report_formats_response>
                        <report_format id="1f3261c9-e47c-4a21-b677-826ea92d1d59">
                            <name>a</name>
                        </report_format>
                        <report_format id="83c907a4-b2e4-403e-a5ba-9f831092b106">
                            <name>b</name>
                        </report_format>
                    </get_report_formats_response>
                    '''

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(self.qu)

        self.assertResponseAuthenticationRequired(response)

    def test_get_reports(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_report_formats', self.resp)

        self.login('foo', 'bar')

        response = self.query(self.qu)

        json = response.json()

        self.assertResponseNoErrors(response)

        reports = json['data']['reportFormats']['nodes']

        self.assertEqual(len(reports), 2)

        report1 = reports[0]
        report2 = reports[1]

        self.assertEqual(report1['name'], 'a')
        self.assertEqual(report1['id'], '1f3261c9-e47c-4a21-b677-826ea92d1d59')
        self.assertEqual(report2['name'], 'b')
        self.assertEqual(report2['id'], '83c907a4-b2e4-403e-a5ba-9f831092b106')

    def test_get_filtered_reports(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_report_formats', self.resp)

        self.login('foo', 'bar')

        response = self.query(self.qu)

        json = response.json()

        self.assertResponseNoErrors(response)

        report_formats = json['data']['reportFormats']['nodes']

        self.assertEqual(len(report_formats), 2)

        report_format1 = report_formats[0]
        report_format2 = report_formats[1]

        self.assertEqual(report_format1['name'], 'a')
        self.assertEqual(
            report_format1['id'], '1f3261c9-e47c-4a21-b677-826ea92d1d59'
        )
        self.assertEqual(report_format2['name'], 'b')
        self.assertEqual(
            report_format2['id'], '83c907a4-b2e4-403e-a5ba-9f831092b106'
        )

    def test_edges(self, mock_gmp: GmpMockFactory):
        report_format_xml_path = CWD / 'get_report_formats.xml'
        report_format_xml_str = report_format_xml_path.read_text()

        mock_gmp.mock_response('get_report_formats', report_format_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                reportFormats {
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

        edges = json['data']['reportFormats']['edges']

        self.assertEqual(len(edges), 10)

        edge_class = GetReportFormats().type._meta.edge

        edge1 = edges[0]
        edge2 = edges[1]

        self.assertEqual(edge1['cursor'], edge_class.get_cursor(0))
        self.assertEqual(
            edge1['node']['id'], "5057e5cc-b825-11e4-9d0e-28d24461215b"
        )
        self.assertEqual(edge1['node']['name'], "Anonymous XML")
        self.assertEqual(edge2['cursor'], edge_class.get_cursor(1))
        self.assertEqual(
            edge2['node']['id'], "910200ca-dc05-11e1-954f-406186ea4fc5"
        )
        self.assertEqual(edge2['node']['name'], "ARF")


class ReportFormatsPaginationTestCase(SeleneTestCase):
    gmp_name = 'report_format'
    selene_name = 'reportFormat'
    test_pagination_with_after_and_first = make_test_after_first(
        gmp_name, selene_name=selene_name
    )
    test_counts = make_test_counts(gmp_name, selene_name=selene_name)
    test_page_info = make_test_page_info(
        gmp_name, selene_name=selene_name, query=GetReportFormats
    )
    test_pagination_with_before_and_last = make_test_before_last(
        gmp_name, selene_name=selene_name
    )
    test_after_first_before_last = make_test_after_first_before_last(
        gmp_name, selene_name=selene_name
    )


class ReportFormatsGetEntityTestCase(SeleneTestCase):
    gmp_name = 'report_format'
    selene_name = 'reportFormat'
    test_get_entity = make_test_get_entities(gmp_name, selene_name=selene_name)
