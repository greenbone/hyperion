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
from pathlib import Path

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory
from selene.tests.entity import make_test_get_entity

CWD = Path(__file__).absolute().parent


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class GetReportFormatTestCase(SeleneTestCase):
    def setUp(self):
        self.report_format_id = str(uuid4())

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            f'''
            query {{
                reportFormat(id: "{self.report_format_id}") {{
                    id
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_report_format(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_report_format',
            f'''
            <get_report_formats_response status="200" status_text="OK">
                <report_format id="{self.report_format_id}">
                    <name>XML</name>
                </report_format>
                <filters id="">
                    <term>first=1 rows=10 sort=name</term>
                    <keywords>
                        <keyword>
                            <column>first</column>
                            <relation>=</relation>
                            <value>1</value>
                        </keyword>
                        <keyword>
                            <column>rows</column>
                            <relation>=</relation>
                            <value>10</value>
                        </keyword>
                        <keyword>
                            <column>sort</column>
                            <relation>=</relation>
                            <value>name</value>
                        </keyword>
                    </keywords>
                </filters>
                <sort>
                    <field>name<order>ascending</order>
                    </field>
                </sort>
                <report_formats start="1" max="2"/>
                <report_format_count>19<filtered>1</filtered>
                    <page>1</page>
                </report_format_count>
            </get_report_formats_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            query {{
                reportFormat(id: "{self.report_format_id}") {{
                    id
                    name
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        report_format = json['data']['reportFormat']

        self.assertEqual(report_format['name'], 'XML')
        self.assertEqual(report_format['id'], self.report_format_id)

    def test_full_report_format(self, mock_gmp: GmpMockFactory):
        report_format_xml_path = CWD / 'get_report_format.xml'
        report_format_xml_str = report_format_xml_path.read_text()

        mock_gmp.mock_response('get_report_format', report_format_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
        query {
            reportFormat(id: "5057e5cc-b825-11e4-9d0e-28d24461215b") {
                id
                name
                creationTime
                trustTime
                active
                comment
                trust
                modificationTime
                predefined
                extension
                inUse
                writable
                summary
                description
            }
        }
            '''
        )
        json = response.json()
        self.assertResponseNoErrors(response)

        report_format = json['data']['reportFormat']
        self.assertEqual(report_format['name'], 'Anonymous XML')
        self.assertEqual(
            report_format['id'], '5057e5cc-b825-11e4-9d0e-28d24461215b'
        )
        self.assertIsNone(report_format['comment'])
        self.assertEqual(
            report_format['creationTime'], '2019-09-05T12:25:40+00:00'
        )
        self.assertEqual(
            report_format['modificationTime'], '2020-08-18T18:42:31+00:00'
        )
        self.assertEqual(
            report_format['trustTime'], '2020-09-04T10:13:50+00:00'
        )
        self.assertEqual(report_format['active'], True)
        self.assertEqual(report_format['predefined'], True)
        self.assertEqual(report_format['inUse'], False)
        self.assertEqual(report_format['writable'], False)
        self.assertEqual(report_format['extension'], 'xml')
        self.assertEqual(
            report_format['summary'], 'Anonymous version of the raw XML report'
        )
        self.assertEqual(
            report_format['description'],
            'Anonymized scan report in GMP XML format.',
        )


class ReportFormatGetEntityTestCase(SeleneTestCase):
    gmp_name = 'report_format'
    selene_name = 'reportFormat'
    test_get_entity = make_test_get_entity(gmp_name, selene_name=selene_name)
