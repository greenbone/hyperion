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
from selene.tests.pagination import (
    make_test_counts,
    make_test_after_first,
    make_test_page_info,
    make_test_edges,
    make_test_before_last,
    make_test_after_first_before_last,
)

from selene.schema.results.queries import GetResults


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class ResultsTestCase(SeleneTestCase):
    def setUp(self):
        self.qu = '''
                    query {
                        results {
                            nodes {
                                id
                                name
                            }
                        }
                    }
                    '''

        self.resp = '''
                    <get_results_response>
                        <result id="1f3261c9-e47c-4a21-b677-826ea92d1d59">
                            <name>abc</name>
                        </result>
                        <result id="83c907a4-b2e4-403e-a5ba-9f831092b106">
                            <name>def</name>
                        </result>
                    </get_results_response>
                    '''

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(self.qu)

        self.assertResponseAuthenticationRequired(response)

    def test_get_results(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_results', self.resp)

        self.login('foo', 'bar')

        response = self.query(self.qu)

        json = response.json()

        self.assertResponseNoErrors(response)

        results = json['data']['results']['nodes']

        self.assertEqual(len(results), 2)

        result1 = results[0]
        result2 = results[1]

        self.assertEqual(result1['name'], 'abc')
        self.assertEqual(result1['id'], '1f3261c9-e47c-4a21-b677-826ea92d1d59')
        self.assertEqual(result2['name'], 'def')
        self.assertEqual(result2['id'], '83c907a4-b2e4-403e-a5ba-9f831092b106')

    def test_get_filtered_results(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_results', self.resp)

        self.login('foo', 'bar')

        response = self.query(self.qu)

        json = response.json()

        self.assertResponseNoErrors(response)

        results = json['data']['results']['nodes']

        self.assertEqual(len(results), 2)

        result1 = results[0]
        result2 = results[1]

        self.assertEqual(result1['name'], 'abc')
        self.assertEqual(result1['id'], '1f3261c9-e47c-4a21-b677-826ea92d1d59')
        self.assertEqual(result2['name'], 'def')
        self.assertEqual(result2['id'], '83c907a4-b2e4-403e-a5ba-9f831092b106')


class ResultsPaginationTestCase(SeleneTestCase):
    entity_name = 'result'
    test_pagination_with_after_and_first = make_test_after_first(entity_name)
    test_counts = make_test_counts(entity_name)
    test_page_info = make_test_page_info(entity_name, query=GetResults)
    test_pagination_with_before_and_last = make_test_before_last(entity_name)
    test_edges = make_test_edges(entity_name)
    test_after_first_before_last = make_test_after_first_before_last(
        entity_name
    )
