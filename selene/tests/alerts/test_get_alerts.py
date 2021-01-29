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

from selene.schema.alerts.queries import GetAlerts

from selene.tests.entity import make_test_get_entities

from selene.tests.pagination import (
    make_test_counts,
    make_test_after_first,
    make_test_page_info,
    make_test_edges,
    make_test_before_last,
    make_test_after_first_before_last,
)

CWD = Path(__file__).absolute().parent


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class AlertsTestCase(SeleneTestCase):
    def setUp(self):
        self.xml = '''
            <get_alerts_response status="200" status_text="OK">
                <alert id="63431604-1cd5-402c-bb05-748e130edb03">
                    <name>foo</name>
                    <comment/>
                    <tasks />
                </alert>
                <alert id="3a39bea5-fc9f-41f4-9107-7e0e69db9035">
                    <name>bar</name>
                    <comment>baz</comment>
                    <tasks>
                        <task id="173a38fe-1038-48a6-9c48-a623ffc04ba8">
                            <name>scan_local</name>
                        </task>
                    </tasks>
                    <active>1</active>
                </alert>
            </get_alerts_response>
            '''

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                alerts {
                    nodes {
                        id
                        name
                        comment
                        tasks {
                            id
                            name
                        }
                    }
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_alerts(self, mock_gmp: GmpMockFactory):
        alerts_xml_path = CWD / 'example-alert-list.xml'
        alerts_xml_str = alerts_xml_path.read_text()

        mock_gmp.mock_response('get_alerts', alerts_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                alerts {
                    nodes {
                        name
                        id
                        inUse
                        comment
                        writable
                        owner
                        creationTime
                        modificationTime
                        filter {
                            trash
                            name
                            id
                        }
                        tasks {
                            id
                            name
                        }
                        event {
                            type
                            data {
                                name
                                value
                            }
                        }
                        condition {
                            type
                            data {
                                name
                                value
                            }
                        }
                        method {
                            type
                            data {
                                name
                                value
                            }
                        }
                        permissions {
                            name
                        }
                        active
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        alerts = json['data']['alerts']['nodes']

        self.assertEqual(len(alerts), 2)

        alert1 = alerts[0]
        alert2 = alerts[1]

        # Alert 1

        self.assertEqual(alert1['id'], '63431604-1cd5-402c-bb05-748e130edb03')
        self.assertEqual(alert1['name'], 'foo')

        self.assertIsNone(alert1['tasks'])

        self.assertIsNone(alert1['comment'])

        self.assertEqual(alert1['inUse'], False)
        self.assertEqual(alert1['writable'], True)
        self.assertEqual(alert1['active'], True)

        self.assertEqual(alert1['creationTime'], '2020-08-06T11:34:15+00:00')
        self.assertEqual(
            alert1['modificationTime'], '2020-08-06T11:34:15+00:00'
        )

        self.assertEqual(alert1['permissions'][0]['name'], 'Everything')
        self.assertIsNone(alert1['filter'])

        event1 = alert1['event']
        event_data1 = event1['data']

        self.assertEqual(event1['type'], 'Task run status changed')
        self.assertEqual(event_data1[0]['name'], 'status')
        self.assertEqual(event_data1[0]['value'], 'Done')

        method1 = alert1['method']
        method_data1 = method1['data']

        self.assertEqual(len(method_data1), 11)

        self.assertEqual(method1['type'], 'Alemba vFire')

        self.assertEqual(method_data1[0]['name'], 'report_formats')
        self.assertEqual(
            method_data1[0]['value'], 'c1645568-627a-11e3-a660-406186ea4fc5'
        )

        self.assertEqual(method_data1[1]['name'], 'vfire_base_url')
        self.assertEqual(method_data1[1]['value'], '127.0.0.1')

        # Alert 2

        self.assertEqual(alert2['id'], '3a39bea5-fc9f-41f4-9107-7e0e69db9035')
        self.assertEqual(alert2['name'], 'bar')

        self.assertEqual(alert2['comment'], 'baz')

        self.assertEqual(alert2['inUse'], True)
        self.assertEqual(alert2['writable'], True)
        self.assertEqual(alert2['active'], True)

        self.assertEqual(alert2['creationTime'], '2020-08-06T11:30:41+00:00')
        self.assertEqual(
            alert2['modificationTime'], '2020-08-07T09:26:05+00:00'
        )

        self.assertEqual(alert2['permissions'][0]['name'], 'Everything')

        self.assertEqual(len(alert2['tasks']), 1)
        self.assertEqual(alert2['tasks'][0]['name'], 'scan_local')
        self.assertEqual(
            alert2['tasks'][0]['id'], '173a38fe-1038-48a6-9c48-a623ffc04ba8'
        )

        filter2 = alert2['filter']

        self.assertEqual(filter2['id'], '75c8145d-b00c-408f-8907-6664d5ce6108')
        self.assertEqual(filter2['name'], 'resultFilter')
        self.assertEqual(filter2['trash'], 0)

        event2 = alert2['event']
        event_data2 = event2['data']

        self.assertEqual(event2['type'], 'Updated SecInfo arrived')
        self.assertEqual(event_data2[0]['name'], 'secinfo_type')
        self.assertEqual(event_data2[0]['value'], 'nvt')

        method2 = alert2['method']
        method_data2 = method2['data']

        self.assertEqual(len(method_data2), 7)

        self.assertEqual(method2['type'], 'Email')

        self.assertEqual(method_data2[0]['name'], 'notice')
        self.assertEqual(method_data2[0]['value'], '1')

        self.assertEqual(method_data2[1]['name'], 'from_address')
        self.assertEqual(method_data2[1]['value'], 'lorem@ipsum.com')

    def test_get_filtered_alerts(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_alerts', self.xml)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                alerts (filterString: "lorem") {
                    nodes {
                        id
                        name
                        comment
                        tasks {
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

        alerts = json['data']['alerts']['nodes']

        self.assertEqual(len(alerts), 2)

        alert1 = alerts[0]
        alert2 = alerts[1]

        # Alert 1

        self.assertEqual(alert1['id'], '63431604-1cd5-402c-bb05-748e130edb03')
        self.assertEqual(alert1['name'], 'foo')

        self.assertIsNone(alert1['tasks'])
        self.assertIsNone(alert1['comment'])

        # Alert 2

        self.assertEqual(alert2['id'], '3a39bea5-fc9f-41f4-9107-7e0e69db9035')
        self.assertEqual(alert2['name'], 'bar')

        self.assertEqual(alert2['tasks'][0]['name'], 'scan_local')
        self.assertEqual(
            alert2['tasks'][0]['id'], '173a38fe-1038-48a6-9c48-a623ffc04ba8'
        )

        self.assertEqual(alert2['comment'], 'baz')


class AlertsPaginationTestCase(SeleneTestCase):
    gmp_name = 'alert'
    test_pagination_with_after_and_first = make_test_after_first(
        gmp_name, tasks=True
    )
    test_counts = make_test_counts(gmp_name)
    test_page_info = make_test_page_info(gmp_name, query=GetAlerts)
    test_pagination_with_before_and_last = make_test_before_last(
        gmp_name, tasks=True
    )
    test_edges = make_test_edges(gmp_name)
    test_after_first_before_last = make_test_after_first_before_last(
        gmp_name, tasks=True
    )


class AlertsGetEntitiesTestCase(SeleneTestCase):
    gmp_name = 'alert'
    test_get_entities = make_test_get_entities(gmp_name, tasks=True)
