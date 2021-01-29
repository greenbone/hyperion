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


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class SystemReportTestCase(SeleneTestCase):
    """
    Tests for the systemReports query.
    """

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        """
        Test the authentication requirement.
        """
        response = self.query(
            '''
            query {
                systemReports {
                    name
                    title
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_system_reports(self, mock_gmp: GmpMockFactory):
        """
        Test getting a list of system report names and titles.
        """
        mock_gmp.mock_response(
            'get_system_reports',
            '''
            <get_system_reports_response>
                <system_report>
                    <name>proc</name>
                    <title>Processes</title>
                </system_report>
                <system_report>
                    <name>load</name>
                    <title>System Load</title>
                </system_report>
                <system_report>
                    <name>cpu-0</name>
                    <title>CPU Usage: cpu-0</title>
                </system_report>
            </get_system_reports_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                systemReports (
                    sensorId: "08b69003-5fc2-4037-a479-93b440211c73"
                ) {
                    name
                    title
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        system_reports = json['data']['systemReports']

        self.assertEqual(len(system_reports), 3)

        self.assertEqual(system_reports[0]['name'], 'proc')
        self.assertEqual(system_reports[0]['title'], 'Processes')
        self.assertEqual(system_reports[1]['name'], 'load')
        self.assertEqual(system_reports[1]['title'], 'System Load')
        self.assertEqual(system_reports[2]['name'], 'cpu-0')
        self.assertEqual(system_reports[2]['title'], 'CPU Usage: cpu-0')

        mock_gmp.gmp_protocol.get_system_reports.assert_called_with(
            brief=True, slave_id='08b69003-5fc2-4037-a479-93b440211c73'
        )
