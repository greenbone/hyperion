# -*- coding: utf-8 -*-
# Copyright (C) 2019 Greenbone Networks GmbH
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
class GetFeedTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                feeds {
                    name,
                    version,
                    description
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_feeds(self, mock_gmp: GmpMockFactory):
        feeds_xml_path = CWD / 'example-get_feeds-response.xml'
        feeds_xml_str = feeds_xml_path.read_text()

        mock_gmp.mock_response('get_feeds', feeds_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                feeds {
                    type
                    name
                    version
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        feeds = json['data']['feeds']
        self.assertEqual(len(feeds), 4)

        self.assertEqual(feeds[0]['type'], 'NVT')
        self.assertEqual(feeds[0]['name'], 'Greenbone Security Feed')
        self.assertEqual(feeds[0]['version'], '202010220502')

        self.assertEqual(feeds[1]['type'], 'SCAP')
        self.assertEqual(feeds[1]['name'], 'Greenbone SCAP Feed')
        self.assertEqual(feeds[1]['version'], '202011130230')

        self.assertEqual(feeds[2]['type'], 'CERT')
        self.assertEqual(feeds[2]['name'], 'Greenbone CERT Feed')
        self.assertEqual(feeds[2]['version'], '202010220030')

        self.assertEqual(feeds[3]['type'], 'GVMD_DATA')
        self.assertEqual(feeds[3]['name'], 'Greenbone gvmd Data Feed')
        self.assertEqual(feeds[3]['version'], '202010160853')
