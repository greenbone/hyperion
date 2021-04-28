# -*- coding: utf-8 -*-
# Copyright (C) 2019-2021 Greenbone Networks GmbH
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
class GetFeedTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                feed (feedType: SCAP) {
                    name,
                    version,
                    description
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_nvt_feed(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_feed',
            '''
            <get_feeds_response status="200" status_text="OK">
                <feed>
                    <type>NVT</type>
                    <name>Greenbone Security Feed</name>
                    <version>202010220502</version>
                    <description>This script synchronizes [...]</description>
                    <currently_syncing>
                        <timestamp>202011151700</timestamp>
                    </currently_syncing>
                </feed>
            </get_feeds_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                feed (feedType: NVT) {
                    type
                    name
                    version
                    description
                    currentlySyncing
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        feed = json['data']['feed']
        self.assertEqual(feed['type'], 'NVT')
        self.assertEqual(feed['name'], 'Greenbone Security Feed')
        self.assertEqual(feed['version'], '202010220502')
        self.assertEqual(feed['description'], 'This script synchronizes [...]')
        self.assertEqual(feed['currentlySyncing'], True)

    def test_get_cert_feed(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_feed',
            '''
            <get_feeds_response status="200" status_text="OK">
                <feed>
                    <type>CERT</type>
                    <name>Greenbone CERT Feed</name>
                    <version>202010220502</version>
                    <description>This script synchronizes [...]</description>
                    <currently_syncing>
                        <timestamp>202011151700</timestamp>
                    </currently_syncing>
                </feed>
            </get_feeds_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                feed (feedType: CERT) {
                    type
                    name
                    version
                    description
                    currentlySyncing
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        feed = json['data']['feed']
        self.assertEqual(feed['type'], 'CERT')
        self.assertEqual(feed['name'], 'Greenbone CERT Feed')
        self.assertEqual(feed['version'], '202010220502')
        self.assertEqual(
            feed['description'],
            'This script synchronizes [...]',
        )
        self.assertEqual(feed['currentlySyncing'], True)

    def test_get_scap_feed(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_feed',
            '''
            <get_feeds_response status="200" status_text="OK">
                <feed>
                    <type>SCAP</type>
                    <name>Greenbone SCAP Feed</name>
                    <version>202010220502</version>
                    <description>This script synchronizes [...]</description>
                    <currently_syncing>
                        <timestamp>202011151700</timestamp>
                    </currently_syncing>
                </feed>
            </get_feeds_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                feed (feedType: SCAP) {
                    type
                    name
                    version
                    description
                    currentlySyncing
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        feed = json['data']['feed']
        self.assertEqual(feed['type'], 'SCAP')
        self.assertEqual(feed['name'], 'Greenbone SCAP Feed')
        self.assertEqual(feed['version'], '202010220502')
        self.assertEqual(
            feed['description'],
            'This script synchronizes [...]',
        )
        self.assertEqual(feed['currentlySyncing'], True)

    def test_get_gvmd_data_feed(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_feed',
            '''
            <get_feeds_response status="200" status_text="OK">
                <feed>
                    <type>GVMD_DATA</type>
                    <name>Greenbone gvmd Data Feed</name>
                    <version>202010220502</version>
                    <description>This script synchronizes [...]</description>
                    <currently_syncing>
                        <timestamp>202011151700</timestamp>
                    </currently_syncing>
                </feed>
            </get_feeds_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                feed (feedType: GVMD_DATA) {
                    type
                    name
                    version
                    description
                    currentlySyncing
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        feed = json['data']['feed']
        self.assertEqual(feed['type'], 'GVMD_DATA')
        self.assertEqual(feed['name'], 'Greenbone gvmd Data Feed')
        self.assertEqual(feed['version'], '202010220502')
        self.assertEqual(
            feed['description'],
            'This script synchronizes [...]',
        )
        self.assertEqual(feed['currentlySyncing'], True)
