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
from selene.tests.pagination import (
    make_test_counts,
    make_test_after_first,
    make_test_page_info,
    make_test_edges,
    make_test_before_last,
    make_test_after_first_before_last,
)

from selene.schema.port_list.queries import GetPortLists


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class PortListTestCase(SeleneTestCase):
    def setUp(self):
        self.xml = '''
            <get_port_lists_response>
                <port_list id="4a4717fe-57d2-11e1-9a26-406186ea4fc5">
                    <name>All IANA assigned TCP and UDP</name>
                    <owner><name>Palpatine</name></owner>
                    <creation_time>2020-06-30T09:16:25Z</creation_time>
                    <modification_time>2020-07-30T09:16:25Z</modification_time>
                    <writable>1</writable>
                    <in_use>1</in_use>
                    <port_count>
                        <all>42</all>
                        <tcp>21</tcp>
                        <udp>21</udp>
                    </port_count>
                    <port_ranges>
                        <port_range id="2864fa44-594a-45d5-88ee-6c9742481b8e">
                            <start>1</start>
                            <end>3</end>
                            <type>tcp</type>
                        </port_range>
                        <port_range id="6390a473-86b3-4583-b4b9-e7e3b2a55355">
                            <start>5</start>
                            <end>5</end>
                            <type>udp</type>
                        </port_range>
                    </port_ranges>
                    <targets>
                        <target id="66dcb401-2621-4d8e-9a1a-7044f1456f18">
                            <name>Sidious</name>
                        </target>
                    </targets>
                </port_list>
                <port_list id="33d0cd82-57c6-11e1-8ed1-406186ea4fc5">
                    <name>All IANA assigned TCP</name>
                    <owner><name>Sen. Organa</name></owner>
                    <creation_time>2020-07-30T09:16:25Z</creation_time>
                    <modification_time>2020-08-30T09:16:25Z</modification_time>
                    <writable>0</writable>
                    <in_use>0</in_use>
                    <port_count>
                        <all>42</all>
                        <tcp>21</tcp>
                        <udp>21</udp>
                    </port_count>
                    <port_ranges>
                        <port_range id="2864fa44-594a-45d5-88ee-6c9742481b81">
                            <start>1</start>
                            <end>3</end>
                            <type>tcp</type>
                        </port_range>
                        <port_range id="6390a473-86b3-4583-b4b9-e7e3b2a55351">
                            <start>5</start>
                            <end>5</end>
                            <type>udp</type>
                        </port_range>
                    </port_ranges>
                    <targets>
                        <target id="66dcb401-2621-4d8e-9a1a-7044f1456f11">
                            <name>Bail</name>
                        </target>
                    </targets>
                </port_list>
                <port_list_count>
                    20
                    <filtered>2</filtered>
                </port_list_count>
                <port_lists max="10" start="1"/>
            </get_port_lists_response>
            '''

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                portLists {
                    nodes {
                        id
                    }
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_port_lists(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_port_lists', self.xml)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                portLists {
                    nodes {
                        name
                        id
                        owner
                        creationTime
                        modificationTime
                        writable
                        inUse
                        portCount {
                            all
                            tcp
                            udp
                        }
                        portRanges {
                            id
                            start
                            end
                            type
                        }
                        targets {
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

        port_lists = json['data']['portLists']['nodes']

        self.assertEqual(len(port_lists), 2)

        port_list1 = port_lists[0]
        port_list2 = port_lists[1]

        self.assertEqual(
            port_list1['id'], '4a4717fe-57d2-11e1-9a26-406186ea4fc5'
        )
        self.assertEqual(port_list1['owner'], 'Palpatine')
        self.assertEqual(
            port_list1['creationTime'], '2020-06-30T09:16:25+00:00'
        )
        self.assertEqual(
            port_list1['modificationTime'], '2020-07-30T09:16:25+00:00'
        )
        self.assertEqual(port_list1['writable'], True)
        self.assertEqual(port_list1['inUse'], True)
        self.assertEqual(port_list1['name'], 'All IANA assigned TCP and UDP')

        targets1 = port_list1['targets']
        self.assertEqual(
            targets1[0]['id'], '66dcb401-2621-4d8e-9a1a-7044f1456f18'
        )
        self.assertEqual(targets1[0]['name'], 'Sidious')

        port_ranges1 = port_list1['portRanges']
        self.assertEqual(
            port_ranges1[0]['id'], '2864fa44-594a-45d5-88ee-6c9742481b8e'
        )
        self.assertEqual(port_ranges1[0]['start'], 1)
        self.assertEqual(port_ranges1[0]['end'], 3)
        self.assertEqual(port_ranges1[0]['type'], 'TCP')
        self.assertEqual(
            port_ranges1[1]['id'], '6390a473-86b3-4583-b4b9-e7e3b2a55355'
        )
        self.assertEqual(port_ranges1[1]['start'], 5)
        self.assertEqual(port_ranges1[1]['end'], 5)
        self.assertEqual(port_ranges1[1]['type'], 'UDP')

        port_list_counts1 = port_list1['portCount']
        self.assertEqual(port_list_counts1['all'], 42)
        self.assertEqual(port_list_counts1['tcp'], 21)
        self.assertEqual(port_list_counts1['udp'], 21)

        self.assertEqual(
            port_list2['id'], '33d0cd82-57c6-11e1-8ed1-406186ea4fc5'
        )
        self.assertEqual(port_list2['owner'], 'Sen. Organa')
        self.assertEqual(
            port_list2['creationTime'], '2020-07-30T09:16:25+00:00'
        )
        self.assertEqual(
            port_list2['modificationTime'], '2020-08-30T09:16:25+00:00'
        )
        self.assertEqual(port_list2['writable'], False)
        self.assertEqual(port_list2['inUse'], False)
        self.assertEqual(port_list2['name'], 'All IANA assigned TCP')

        targets2 = port_list2['targets']
        self.assertEqual(
            targets2[0]['id'], '66dcb401-2621-4d8e-9a1a-7044f1456f11'
        )
        self.assertEqual(targets2[0]['name'], 'Bail')

        port_ranges2 = port_list2['portRanges']
        self.assertEqual(
            port_ranges2[0]['id'], '2864fa44-594a-45d5-88ee-6c9742481b81'
        )
        self.assertEqual(port_ranges2[0]['start'], 1)
        self.assertEqual(port_ranges2[0]['end'], 3)
        self.assertEqual(port_ranges2[0]['type'], 'TCP')
        self.assertEqual(
            port_ranges2[1]['id'], '6390a473-86b3-4583-b4b9-e7e3b2a55351'
        )
        self.assertEqual(port_ranges2[1]['start'], 5)
        self.assertEqual(port_ranges2[1]['end'], 5)
        self.assertEqual(port_ranges2[1]['type'], 'UDP')

        port_list_counts2 = port_list2['portCount']
        self.assertEqual(port_list_counts2['all'], 42)
        self.assertEqual(port_list_counts2['tcp'], 21)
        self.assertEqual(port_list_counts2['udp'], 21)

    def test_get_filtered_port_lists(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_port_lists', self.xml)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                portLists (
                    filterString: "All IANA",
                ) {
                    nodes {
                        id
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        port_lists = json['data']['portLists']['nodes']

        self.assertEqual(len(port_lists), 2)

        port_list1 = port_lists[0]
        port_list2 = port_lists[1]

        self.assertEqual(
            port_list1['id'], '4a4717fe-57d2-11e1-9a26-406186ea4fc5'
        )

        self.assertEqual(
            port_list2['id'], '33d0cd82-57c6-11e1-8ed1-406186ea4fc5'
        )


class PortListsPaginationTestCase(SeleneTestCase):
    gmp_name = 'port_list'
    selene_name = 'portList'
    test_pagination_with_after_and_first = make_test_after_first(
        gmp_name, selene_name=selene_name, details=True
    )
    test_counts = make_test_counts(gmp_name, selene_name=selene_name)
    test_page_info = make_test_page_info(
        gmp_name, selene_name=selene_name, query=GetPortLists
    )
    test_pagination_with_before_and_last = make_test_before_last(
        gmp_name, selene_name=selene_name, details=True
    )
    test_edges = make_test_edges(gmp_name, selene_name=selene_name)
    test_after_first_before_last = make_test_after_first_before_last(
        gmp_name, selene_name=selene_name, details=True
    )
