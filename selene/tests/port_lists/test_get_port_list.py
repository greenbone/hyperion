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


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class PortListTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                portList(id: "4a4717fe-57d2-11e1-9a26-406186ea4fc5") {
                    id
                    name
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_port_list(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_port_list',
            '''
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
            </get_port_lists_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                portList(id: "4a4717fe-57d2-11e1-9a26-406186ea4fc5") {
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
                        protocolType
                    }
                    targets {
                        id
                        name
                    }
                }
            }
            '''
        )
        json = response.json()

        self.assertResponseNoErrors(response)

        port_list = json['data']['portList']

        self.assertEqual(
            port_list['id'], '4a4717fe-57d2-11e1-9a26-406186ea4fc5'
        )
        self.assertEqual(port_list['owner'], 'Palpatine')
        self.assertEqual(port_list['creationTime'], '2020-06-30T09:16:25+00:00')
        self.assertEqual(
            port_list['modificationTime'], '2020-07-30T09:16:25+00:00'
        )
        self.assertEqual(port_list['writable'], True)
        self.assertEqual(port_list['inUse'], True)
        self.assertEqual(port_list['name'], 'All IANA assigned TCP and UDP')

        targets = port_list['targets']
        self.assertEqual(
            targets[0]['id'], '66dcb401-2621-4d8e-9a1a-7044f1456f18'
        )
        self.assertEqual(targets[0]['name'], 'Sidious')

        port_ranges = port_list['portRanges']
        self.assertEqual(
            port_ranges[0]['id'], '2864fa44-594a-45d5-88ee-6c9742481b8e'
        )
        self.assertEqual(port_ranges[0]['start'], 1)
        self.assertEqual(port_ranges[0]['end'], 3)
        self.assertEqual(port_ranges[0]['protocolType'], 'tcp')
        self.assertEqual(
            port_ranges[1]['id'], '6390a473-86b3-4583-b4b9-e7e3b2a55355'
        )
        self.assertEqual(port_ranges[1]['start'], 5)
        self.assertEqual(port_ranges[1]['end'], 5)
        self.assertEqual(port_ranges[1]['protocolType'], 'udp')

        port_list_counts = port_list['portCount']
        self.assertEqual(port_list_counts['all'], 42)
        self.assertEqual(port_list_counts['tcp'], 21)
        self.assertEqual(port_list_counts['udp'], 21)
