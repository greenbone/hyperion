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
from selene.tests.entity import make_test_get_entities

from selene.schema.scan_configs.queries import GetScanConfigs


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class ScanConfigsTestCase(SeleneTestCase):
    def setUp(self):
        self.xml = '''
            <get_config_response>
                <config id="08b69003-5fc2-4037-a479-93b440211c73">
                    <name>foo</name>
                    <type>0</type>
                </config>
                <config id="6b2db524-9fb0-45b8-9b56-d958f84cb546">
                    <name>lorem</name>
                    <type>1</type>
                </config>
            </get_config_response>
            '''

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                scanConfigs{
                    nodes {
                        id
                        name
                        type
                    }
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_scan_configs(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_configs', self.xml)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                scanConfigs {
                    nodes {
                        id
                        name
                        type
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        configs = json['data']['scanConfigs']['nodes']

        self.assertEqual(len(configs), 2)

        scan_config1 = configs[0]
        scan_config2 = configs[1]

        # Config 1

        self.assertEqual(
            scan_config1['id'], '08b69003-5fc2-4037-a479-93b440211c73'
        )
        self.assertEqual(scan_config1['name'], 'foo')

        self.assertEqual(scan_config1['type'], 0)

        # Config 2

        self.assertEqual(
            scan_config2['id'], '6b2db524-9fb0-45b8-9b56-d958f84cb546'
        )
        self.assertEqual(scan_config2['name'], 'lorem')

        self.assertEqual(scan_config2['type'], 1)

    def test_get_filtered_scan_configs(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_configs', self.xml)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                scanConfigs (
                    filterString: "lorem",
                ) {
                    nodes {
                        id
                        name
                        type
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        configs = json['data']['scanConfigs']['nodes']

        self.assertEqual(len(configs), 2)

        config1 = configs[0]
        config2 = configs[1]

        self.assertEqual(config1['id'], '08b69003-5fc2-4037-a479-93b440211c73')
        self.assertEqual(config1['name'], 'foo')
        self.assertEqual(config1['type'], 0)

        self.assertEqual(config2['id'], '6b2db524-9fb0-45b8-9b56-d958f84cb546')
        self.assertEqual(config2['name'], 'lorem')
        self.assertEqual(config2['type'], 1)


class ScanConfigsPaginationTestCase(SeleneTestCase):
    gmp_name = 'config'
    selene_name = 'scanConfig'
    test_pagination_with_after_and_first = make_test_after_first(
        gmp_name, selene_name=selene_name, details=False
    )
    test_counts = make_test_counts(gmp_name, selene_name=selene_name)
    test_page_info = make_test_page_info(
        gmp_name, selene_name=selene_name, query=GetScanConfigs
    )
    test_pagination_with_before_and_last = make_test_before_last(
        gmp_name, selene_name=selene_name, details=False
    )
    test_edges = make_test_edges(gmp_name, selene_name=selene_name)
    test_after_first_before_last = make_test_after_first_before_last(
        gmp_name, selene_name=selene_name, details=False
    )


class ScanConfigsGetEntitiesTestCase(SeleneTestCase):
    gmp_name = 'config'
    selene_name = 'scanConfig'
    test_get_entities = make_test_get_entities(
        gmp_name, selene_name=selene_name, details=False
    )
