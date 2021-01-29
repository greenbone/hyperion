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

from selene.schema.parser import parse_datetime

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class SystemReportTestCase(SeleneTestCase):
    """
    Tests for the systemReport query.
    """

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        """
        Test the authentication requirement.
        """
        response = self.query(
            '''
            query {
                systemReport(name: "load") {
                    name
                    title
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def make_mock_response(self, duration, start_time, end_time):
        """
        Helper function for building a mock system report.
        """
        content = 'iVBORw0KGgoAAAA...'
        return f'''
                <get_system_reports_response>
                    <system_report>
                        <name>proc</name>
                        <title>Processes</title>
                        <report format="png"
                                duration="{duration}"
                                start_time="{start_time}"
                                end_time="{end_time}">{content}</report>
                    </system_report>
                </get_system_reports_response>
                '''

    def test_get_system_report_default(self, mock_gmp: GmpMockFactory):
        """
        Test getting a system report with default values.
        """
        mock_gmp.mock_response(
            'get_system_reports',
            self.make_mock_response('86400', '', ''),
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                systemReport(name: "load") {
                    name
                    title
                    report {
                        format
                        startTime
                        endTime
                        duration
                        content
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        system_report = json['data']['systemReport']
        self.assertEqual(system_report['name'], 'proc')
        self.assertEqual(system_report['title'], 'Processes')
        inner_report = system_report['report']
        self.assertEqual(inner_report['format'], 'png')
        self.assertEqual(inner_report['duration'], 86400)
        self.assertEqual(inner_report['startTime'], None)
        self.assertEqual(inner_report['endTime'], None)
        self.assertEqual(inner_report['content'], 'iVBORw0KGgoAAAA...')

        mock_gmp.gmp_protocol.get_system_reports.assert_called_with(
            name='load',
            slave_id=None,
            duration=None,
            start_time=None,
            end_time=None,
        )

    def test_get_system_report_time_range(self, mock_gmp: GmpMockFactory):
        """
        Test getting a system report with a start and end time as well
        as a sensorId.
        """
        mock_gmp.mock_response(
            'get_system_reports',
            self.make_mock_response(
                '',
                '2020-11-18T12:30:00Z',
                '2020-11-18T18:30:00Z',
            ),
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                systemReport(
                    name: "load"
                    sensorId: "08b69003-5fc2-4037-a479-93b440211c73"
                    startTime: "2020-11-18T12:30:00Z"
                    endTime: "2020-11-18T18:30:00Z"
                ) {
                    name
                    title
                    report {
                        format
                        startTime
                        endTime
                        duration
                        content
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        system_report = json['data']['systemReport']
        self.assertEqual(system_report['name'], 'proc')
        self.assertEqual(system_report['title'], 'Processes')
        inner_report = system_report['report']
        self.assertEqual(inner_report['format'], 'png')
        self.assertEqual(inner_report['duration'], None)
        self.assertEqual(inner_report['startTime'], "2020-11-18T12:30:00+00:00")
        self.assertEqual(inner_report['endTime'], "2020-11-18T18:30:00+00:00")
        self.assertEqual(inner_report['content'], 'iVBORw0KGgoAAAA...')

        mock_gmp.gmp_protocol.get_system_reports.assert_called_with(
            name='load',
            slave_id='08b69003-5fc2-4037-a479-93b440211c73',
            duration=None,
            start_time=parse_datetime('2020-11-18T12:30:00Z'),
            end_time=parse_datetime('2020-11-18T18:30:00Z'),
        )

    def test_get_system_report_duration(self, mock_gmp: GmpMockFactory):
        """
        Test getting a system report with a duration.
        """
        mock_gmp.mock_response(
            'get_system_reports',
            self.make_mock_response(
                '3600',
                '',
                '',
            ),
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                systemReport(
                    name: "load"
                    duration: 3600
                ) {
                    name
                    title
                    report {
                        format
                        startTime
                        endTime
                        duration
                        content
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        system_report = json['data']['systemReport']
        self.assertEqual(system_report['name'], 'proc')
        self.assertEqual(system_report['title'], 'Processes')
        inner_report = system_report['report']
        self.assertEqual(inner_report['format'], 'png')
        self.assertEqual(inner_report['duration'], 3600)
        self.assertEqual(inner_report['startTime'], None)
        self.assertEqual(inner_report['endTime'], None)
        self.assertEqual(inner_report['content'], 'iVBORw0KGgoAAAA...')

        mock_gmp.gmp_protocol.get_system_reports.assert_called_with(
            name='load',
            slave_id=None,
            duration=3600,
            start_time=None,
            end_time=None,
        )
