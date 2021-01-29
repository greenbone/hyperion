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
from selene.tests.entity import make_test_get_entity

CWD = Path(__file__).absolute().parent


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class AlertTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                alert(id: "08b69003-5fc2-4037-a479-93b440211c73") {
                    id
                    name
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_alert(self, mock_gmp: GmpMockFactory):
        alert_xml_path = CWD / 'example-alert.xml'
        alert_xml_str = alert_xml_path.read_text()

        mock_gmp.mock_response('get_alert', alert_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                alert(
                    id: "3a39bea5-fc9f-41f4-9107-7e0e69db9035",
                ) {
                    name
                    id
                    inUse
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
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.get_alert.assert_called_with(
            "3a39bea5-fc9f-41f4-9107-7e0e69db9035", tasks=True
        )

        alert = json['data']['alert']

        self.assertEqual(alert['id'], '3a39bea5-fc9f-41f4-9107-7e0e69db9035')
        self.assertEqual(alert['name'], 'bar')

        self.assertEqual(alert['inUse'], True)
        self.assertEqual(alert['writable'], True)
        self.assertEqual(alert['active'], True)

        self.assertEqual(alert['creationTime'], '2020-08-06T11:30:41+00:00')
        self.assertEqual(alert['modificationTime'], '2020-08-07T09:26:05+00:00')

        self.assertEqual(alert['permissions'][0]['name'], 'Everything')

        self.assertEqual(len(alert['tasks']), 1)
        self.assertEqual(alert['tasks'][0]['name'], 'scan_local')
        self.assertEqual(
            alert['tasks'][0]['id'], '173a38fe-1038-48a6-9c48-a623ffc04ba8'
        )

        event = alert['event']
        event_data = event['data']

        self.assertEqual(event['type'], 'Updated SecInfo arrived')
        self.assertEqual(event_data[0]['name'], 'secinfo_type')
        self.assertEqual(event_data[0]['value'], 'nvt')

        method = alert['method']
        method_data = method['data']

        self.assertEqual(len(method_data), 7)

        self.assertEqual(method['type'], 'Email')

        self.assertEqual(method_data[0]['name'], 'notice')
        self.assertEqual(method_data[0]['value'], '1')

        self.assertEqual(method_data[1]['name'], 'from_address')
        self.assertEqual(method_data[1]['value'], 'lorem@ipsum.com')

        self.assertEqual(method_data[2]['name'], 'delta_type')
        self.assertEqual(method_data[2]['value'], 'None')

        self.assertEqual(method_data[3]['name'], 'to_address')
        self.assertEqual(method_data[3]['value'], 'lorem@ipsum.com')

        self.assertEqual(method_data[4]['name'], 'delta_report_id')
        self.assertIsNone(method_data[4]['value'])

        self.assertEqual(method_data[5]['name'], 'subject')
        self.assertEqual(method_data[5]['value'], '[GVM] $T $q $S since $d')

        self.assertEqual(method_data[6]['name'], 'details_url')
        self.assertEqual(
            method_data[6]['value'], 'https://secinfo.greenbone.net/etc'
        )

        alert_filter = alert['filter']

        self.assertEqual(
            alert_filter['id'], '75c8145d-b00c-408f-8907-6664d5ce6108'
        )
        self.assertEqual(alert_filter['name'], 'resultFilter')
        self.assertEqual(alert_filter['trash'], 0)

    def test_get_alert_without_tasks(self, mock_gmp: GmpMockFactory):
        alert_xml_path = CWD / 'example-alert-2.xml'
        alert_xml_str = alert_xml_path.read_text()

        mock_gmp.mock_response('get_alert', alert_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                alert(
                    id: "5b149b44-ef86-4d5a-96f2-6ffbe4e7de00"
                    tasks:false
                ) {
                    tasks {
                        id
                        name
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        alert = json['data']['alert']

        self.assertIsNone(alert['tasks'])

    def test_get_alert_without_filters(self, mock_gmp: GmpMockFactory):
        alert_xml_path = CWD / 'example-alert-2.xml'
        alert_xml_str = alert_xml_path.read_text()

        mock_gmp.mock_response('get_alert', alert_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                alert(
                    id: "5b149b44-ef86-4d5a-96f2-6ffbe4e7de00"
                ) {
                    filter {
                        trash
                        name
                        id
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        alert = json['data']['alert']

        self.assertIsNone(alert['filter'])


class AlertGetEntityTestCase(SeleneTestCase):
    gmp_name = 'alert'
    test_get_entity = make_test_get_entity(gmp_name, tasks=True)
