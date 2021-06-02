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

from selene.schema.nvts.queries import GetNVTs


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class NVTsTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                nvts {
                    nodes {
                        id
                        name
                    }
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_nvts(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_nvt_list',
            '''
            <get_info_response>
                <info id="NVT-2020-12345">
                    <name>a</name>
                </info>
                <info id="NVT-2020-12346">
                    <name>b</name>
                </info>
            </get_info_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                nvts {
                    nodes {
                        id
                        name
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        nvts = json['data']['nvts']['nodes']

        self.assertEqual(len(nvts), 2)

        nvt1 = nvts[0]
        nvt2 = nvts[1]

        self.assertEqual(nvt1['name'], 'a')
        self.assertEqual(nvt1['id'], 'NVT-2020-12345')
        self.assertEqual(nvt2['name'], 'b')
        self.assertEqual(nvt2['id'], 'NVT-2020-12346')

    def test_get_filtered_nvts(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_nvt_list',
            '''
            <get_info_response>
                <info id="NVT-2020-12345">
                    <name>a</name>
                </info>
                <info id="NVT-2020-12346">
                    <name>b</name>
                </info>
            </get_info_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                nvts (
                    filterString: "lorem",
                ) {
                    nodes {
                        id
                        name
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        nvts = json['data']['nvts']['nodes']

        self.assertEqual(len(nvts), 2)

        nvt1 = nvts[0]
        nvt2 = nvts[1]

        self.assertEqual(nvt1['name'], 'a')
        self.assertEqual(nvt1['id'], 'NVT-2020-12345')
        self.assertEqual(nvt2['name'], 'b')
        self.assertEqual(nvt2['id'], 'NVT-2020-12346')


class NVTsPaginationTestCase(SeleneTestCase):
    gmp_name = 'info'
    gmp_cmd = 'get_nvt_list'
    selene_name = 'nvt'
    test_pagination_with_after_and_first = make_test_after_first(
        gmp_name=gmp_name,
        selene_name=selene_name,
        gmp_cmd=gmp_cmd,
    )
    test_counts = make_test_counts(
        gmp_name=gmp_name,
        selene_name=selene_name,
        gmp_cmd=gmp_cmd,
        no_plural=True,
    )
    test_page_info = make_test_page_info(
        gmp_name=gmp_name,
        selene_name=selene_name,
        gmp_cmd=gmp_cmd,
        query=GetNVTs,
        no_plural=True,
    )
    test_edges = make_test_edges(
        gmp_name=gmp_name,
        gmp_cmd=gmp_cmd,
        selene_name=selene_name,
        no_plural=True,
    )
    test_pagination_with_before_and_last = make_test_before_last(
        gmp_name=gmp_name,
        selene_name=selene_name,
        gmp_cmd=gmp_cmd,
    )
    test_after_first_before_last = make_test_after_first_before_last(
        gmp_name=gmp_name,
        selene_name=selene_name,
        gmp_cmd=gmp_cmd,
    )


class NVTsGetEntitiesTestCase(SeleneTestCase):
    gmp_name = 'info'
    gmp_cmd = 'get_nvt_list'
    selene_name = 'nvt'
    test_get_entities = make_test_get_entities(
        gmp_name=gmp_name,
        selene_name=selene_name,
        gmp_cmd=gmp_cmd,
    )
