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

from pathlib import Path

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory

CWD = Path(__file__).absolute().parent


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class ResultsTestCase(SeleneTestCase):
    def setUp(self):
        self.qu = '''
            query {
                result (
                    id: "1f3261c9-e47c-4a21-b677-826ea92d1d59"
                ) {
                    id
                    name
                }
            }
            '''

        self.resp = '''
            <get_results_response>
                <result id="1f3261c9-e47c-4a21-b677-826ea92d1d59">
                    <name>abc</name>
                </result>

            </get_results_response>
            '''

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(self.qu)

        self.assertResponseAuthenticationRequired(response)

    def test_get_minimal_result(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_result', self.resp)

        self.login('foo', 'bar')

        response = self.query(self.qu)

        json = response.json()

        self.assertResponseNoErrors(response)

        result = json['data']['result']

        self.assertEqual(result['name'], 'abc')
        self.assertEqual(result['id'], '1f3261c9-e47c-4a21-b677-826ea92d1d59')

    def test_get_full_result_nvt_type(self, mock_gmp: GmpMockFactory):
        result_xml_path = CWD / 'example-result.xml'
        result_xml_str = result_xml_path.read_text()

        mock_gmp.mock_response('get_result', result_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                result (
                    id: "9184608a-0b86-42e0-b733-4668feebc1c7"
                ) {
                    id
                    name
                    owner
                    type
                    overrides{
                        id
                        active
                        creationTime
                        modificationTime
                        text
                        endTime
                        severity
                        newSeverity
                    }
                    originResult{
                        id
                        details{
                            name
                            value
                        }
                    }
                    report {
                        id
                    }
                    task {
                        id
                        name
                    }
                    originalSeverity
                    creationTime
                    modificationTime
                    host {
                        ip
                        id
                        hostname
                    }
                    location
                    information {
                        __typename
                        ... on ResultNVT{
                            id
                            score
                            version
                            severities {
                                type
                                score
                                vector
                            }
                        }
                    }
                    severity
                    qod {
                        value
                        type
                    }
                    description
                    notes {
                        id
                        creationTime
                        modificationTime
                        active
                        text
                    }
                    tickets {
                        id
                    }
                    userTags {
                        count
                        tags {
                            id
                            name
                        }
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        result = json['data']['result']

        self.assertEqual(result['id'], '9184608a-0b86-42e0-b733-4668feebc1c7')
        self.assertEqual(
            result['name'],
            'Apache Tomcat RCE Vulnerability - April19 (Windows)',
        )
        self.assertEqual(result['owner'], 'jloechte')
        self.assertEqual(result['type'], 'NVT')
        self.assertEqual(result['creationTime'], '2020-06-19T09:31:15+00:00')
        self.assertEqual(
            result['modificationTime'], '2020-06-19T09:31:15+00:00'
        )

        self.assertIsNotNone(result['originResult'])
        origin_result = result['originResult']
        self.assertEqual(
            origin_result['id'], '9184608a-0b86-42e0-b733-4668feebc1c7'
        )
        self.assertIsNotNone(origin_result['details'])
        details = origin_result['details']
        self.assertEqual(len(details), 4)
        detail1 = details[0]
        self.assertEqual(detail1['name'], 'product')
        self.assertEqual(detail1['value'], 'cpe:/a:python:python:2.7.16')

        report = result['report']
        self.assertEqual(report['id'], 'f31d3b1a-4642-44bc-86ea-63ea029d4c63')
        self.assertEqual(
            result['task']['id'], 'dc9c6b7d-c81d-4e20-acd8-b187b018fa42'
        )
        self.assertEqual(
            result['task']['name'],
            'Offline Scan from 2019-06-27T08:10:13+01:00 38',
        )
        self.assertEqual(result['host']['ip'], '0.0.0.0')
        self.assertEqual(
            result['host']['id'], '2bcc682e-3c91-4f9c-80d6-59949159801f'
        )
        self.assertEqual(result['host']['hostname'], 'xyzxy')
        self.assertEqual(result['severity'], 9.3)
        self.assertEqual(result['qod']['value'], 75)
        self.assertIsNone(result['qod']['type'])
        self.assertEqual(result['originalSeverity'], 9.3)
        self.assertEqual(
            result['information']['id'], '1.3.6.1.4.1.25623.1.0.142265'
        )
        self.assertIsNone(result['information']['version'])
        self.assertEqual(result['information']['score'], 93)
        severities = result['information']['severities']
        self.assertEqual(severities[0]['type'], 'cvss_base_v2')
        self.assertEqual(severities[0]['score'], 93)
        self.assertEqual(severities[0]['vector'], 'AV:N/AC:M/Au:N/C:C/I:C/A:C')
        self.assertIsNone(result['description'])

        self.assertIsNotNone(result['notes'])
        notes = result['notes']
        self.assertEqual(len(notes), 1)

        note1 = notes[0]
        self.assertEqual(note1['id'], '330c8602-9a29-4683-8fd0-908ac3c66914')
        self.assertEqual(note1['creationTime'], '2021-03-12T13:00:32+00:00')
        self.assertEqual(note1['modificationTime'], '2021-03-12T13:00:32+00:00')
        self.assertTrue(note1['active'])
        self.assertEqual(note1['text'], 'test')

        self.assertIsNotNone(result['overrides'])
        overrides = result['overrides']
        self.assertEqual(len(overrides), 1)

        override1 = overrides[0]
        self.assertEqual(
            override1['id'], '6f1249cd-6c48-43e5-bf4f-2a11cb28fbbd'
        )
        self.assertEqual(override1['creationTime'], '2021-04-11T11:30:46+00:00')
        self.assertEqual(
            override1['modificationTime'], '2021-04-11T11:30:46+00:00'
        )
        self.assertTrue(override1['active'])
        self.assertEqual(override1['text'], 'hello world')
        self.assertEqual(override1['severity'], 6.4)
        self.assertEqual(override1['newSeverity'], 4.3)
        self.assertIsNone(override1['endTime'])

        self.assertIsNotNone(result['tickets'])
        tickets = result['tickets']
        self.assertEqual(len(tickets), 2)
        ticket1 = tickets[0]
        self.assertEqual(ticket1['id'], 'cc9170a3-b374-4675-be17-ba31c4953f88')
        ticket2 = tickets[1]
        self.assertEqual(ticket2['id'], '6e93d05c-26b7-42de-8d6e-40afccff831c')

        self.assertIsNotNone(result['userTags'])
        user_tags = result['userTags']
        self.assertEqual(user_tags['count'], 1)
        self.assertEqual(
            user_tags['tags'][0]['id'], '955e4b08-0a8e-4336-89a9-3c573824db2d'
        )
        self.assertEqual(user_tags['tags'][0]['name'], 'result:unnamed')

    def test_get_full_result_cve_type(self, mock_gmp: GmpMockFactory):
        result_xml_path = CWD / 'example-result-2.xml'
        result_xml_str = result_xml_path.read_text()

        mock_gmp.mock_response('get_result', result_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                result (
                    id: "2b555c60-e597-4b18-9d24-dac30f61cfa8"
                ) {
                    id
                    name
                    owner
                    originResult{
                        id
                        details{
                            name
                            value
                        }
                    }
                    report {
                        id
                    }
                    task {
                        id
                        name
                    }
                    originalSeverity
                    overrides{
                        id
                        active
                        creationTime
                        modificationTime
                        text
                        endTime
                        severity
                        newSeverity
                    }
                    creationTime
                    modificationTime
                    host {
                        ip
                        id
                        hostname
                    }
                    location
                    information {
                        __typename
                        ... on ResultCVE{
                            id
                            severity
                        }
                    }
                    severity
                    qod {
                        value
                        type
                    }
                    description
                    notes {
                        id
                        creationTime
                        modificationTime
                        active
                        text
                    }
                    tickets {
                        id
                    }
                    userTags {
                        count
                        tags {
                            id
                            name
                        }
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        result = json['data']['result']

        self.assertEqual(result['id'], '2b555c60-e597-4b18-9d24-dac30f61cfa8')
        self.assertIsNone(result['name'])
        self.assertEqual(result['owner'], 'admin')
        self.assertEqual(result['creationTime'], '2021-04-07T07:41:47+00:00')
        self.assertEqual(
            result['modificationTime'], '2021-04-07T07:41:47+00:00'
        )

        self.assertIsNotNone(result['originResult'])
        origin_result = result['originResult']
        self.assertEqual(
            origin_result['id'], '2b555c60-e597-4b18-9d24-dac30f61cfa8'
        )
        self.assertIsNotNone(origin_result['details'])
        details = origin_result['details']
        self.assertEqual(len(details), 4)
        detail1 = details[0]
        self.assertEqual(detail1['name'], 'product')
        self.assertEqual(detail1['value'], 'cpe:/a:nginx:nginx:1.14.2')

        report = result['report']
        self.assertEqual(report['id'], '9699a95d-e556-4af7-83ac-a7b70d90832a')
        self.assertEqual(
            result['task']['id'], 'ab9a1470-fc01-4547-9da0-33df6c1aa5d1'
        )
        self.assertEqual(result['task']['name'], 'Report Container')
        self.assertEqual(result['host']['ip'], '192.168.9.113')
        self.assertEqual(
            result['host']['id'], 'eb357684-6fcf-4d31-a5e0-02abe040caa4'
        )
        self.assertIsNone(result['host']['hostname'])
        self.assertEqual(result['severity'], 5.8)
        self.assertEqual(result['qod']['value'], 75)
        self.assertIsNone(result['qod']['type'])
        self.assertEqual(result['originalSeverity'], 5.8)
        self.assertEqual(result['information']['id'], 'CVE-2018-16845')
        self.assertEqual(result['information']['severity'], 6.1)
        self.assertEqual(
            result['description'],
            'The host carries the product: cpe:/a:nginx:nginx:1.14.2',
        )

        self.assertIsNone(result['notes'])
        self.assertIsNone(result['overrides'])
        self.assertIsNone(result['tickets'])
        self.assertIsNone(result['userTags'])

    def test_get_result_none_fields(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_result',
            '''
                <get_results_response>
                    <result id="1f3261c9-e47c-4a21-b677-826ea92d1d59">
                        <name>abc</name>
                </result>

                </get_results_response>
                ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                result (
                    id: "1f3261c9-e47c-4a21-b677-826ea92d1d59"
                ) {
                    id
                    name
                    owner
                    originResult{
                        id
                        details{
                            name
                            value
                        }
                    }
                    overrides{
                        id
                        active
                        creationTime
                        modificationTime
                        text
                        endTime
                        severity
                        newSeverity
                    }
                    report {
                        id
                    }
                    task {
                        id
                        name
                    }
                    originalSeverity
                    creationTime
                    modificationTime
                    host {
                        ip
                        id
                        hostname
                    }
                    location
                    information {
                        __typename
                        ... on ResultNVT{
                            id
                            version
                            score
                            severities {
                                type
                                score
                                vector
                            }
                        }
                    }
                    severity
                    qod {
                        value
                        type
                    }
                    description
                    notes {
                        id
                        creationTime
                        modificationTime
                        active
                        text
                    }
                    tickets {
                        id
                    }
                    userTags {
                        count
                        tags {
                            id
                            name
                        }
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        result = json['data']['result']

        self.assertEqual(result['id'], '1f3261c9-e47c-4a21-b677-826ea92d1d59')
        self.assertEqual(result['name'], 'abc')
        self.assertIsNone(result['owner'])
        self.assertIsNone(result['creationTime'])
        self.assertIsNone(result['modificationTime'])
        self.assertIsNone(result['originResult'])
        self.assertIsNone(result['report'])
        self.assertIsNone(result['task'])
        self.assertIsNone(result['host'])
        self.assertIsNone(result['location'])
        self.assertIsNone(result['severity'])
        self.assertIsNone(result['qod'])
        self.assertIsNone(result['originalSeverity'])
        self.assertIsNone(result['information'])
        self.assertIsNone(result['description'])
        self.assertIsNone(result['notes'])
        self.assertIsNone(result['overrides'])
        self.assertIsNone(result['tickets'])
        self.assertIsNone(result['userTags'])
