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

# from datetime import datetime, timezone
from pathlib import Path

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory

from selene.tests.entity import make_test_get_entity

CWD = Path(__file__).absolute().parent


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class HostTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                filter(
                        id: "05d1edfa-3df8-11ea-9651-7b09b3acce77"
                        alerts: false
                    ) {
                    id
                    name
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_filter(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_filter',
            '''
            <get_filters_response>
                <filter id="75d23ba8-3d23-11ea-858e-b7c2cb43e815">
                    <name>a</name>
                </filter>
            </get_filters_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                filter(id: "75d23ba8-3d23-11ea-858e-b7c2cb43e815") {
                    id
                    name
                    owner
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        filter_ = json['data']['filter']

        self.assertEqual(filter_['name'], 'a')
        self.assertEqual(filter_['id'], '75d23ba8-3d23-11ea-858e-b7c2cb43e815')
        self.assertIsNone(filter_['owner'])

    def test_complex_filter(self, mock_gmp: GmpMockFactory):
        filter_xml_path = CWD / 'example-filter.xml'
        filter_xml_str = filter_xml_path.read_text()

        mock_gmp.mock_response('get_filter', filter_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                filter(
                    id: "69635c70-8447-4873-946e-8e204f2f28a4"
                    alerts: true
                ) {
                    id
                    name
                    type
                    term
                    alerts {
                        id
                        name
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        filter_ = json['data']['filter']

        self.assertEqual(filter_['name'], 'yyy Clone 5 Clone 4 Clone 4 Clone 2')
        self.assertEqual(filter_['id'], '69635c70-8447-4873-946e-8e204f2f28a4')
        self.assertEqual(filter_['type'], 'result')
        self.assertEqual(filter_['term'], 'alert first=1 rows=100 sort=name')

        self.assertIsNotNone(filter_['alerts'])
        alerts = filter_['alerts']
        self.assertEqual(alerts[0]['name'], 'xdfxdf')


class HostGetEntityTestCase(SeleneTestCase):
    gmp_name = 'filter'
    selene_name = 'filter'
    test_get_entity = make_test_get_entity(
        gmp_name, selene_name=selene_name, alerts=False
    )
