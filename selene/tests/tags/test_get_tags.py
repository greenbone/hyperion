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

from selene.schema.tags.queries import GetTags


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class TagsTestCase(SeleneTestCase):
    def setUp(self):
        self.xml = '''
            <get_tags_response status="200" status_text="OK">
                <tag id="e9b98e26-9fff-4ee8-9378-bc44fe3d6f2b">
                    <name>cat</name>
                    <comment>dog</comment>
                    <value>goat</value>
                </tag>
                <tag id="85787cbb-a737-463d-94b8-fcc348225f3b">
                    <name>fooTag</name>
                    <comment/>
                    <value>bar</value>
                </tag>
                  <tags start="1" max="10"/>
                  <tag_count>2<filtered>2</filtered>
                    <page>2</page>
                  </tag_count>
            </get_tags_response>
            '''

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                tags {
                    nodes {
                        id
                        name
                        comment
                        value
                    }
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_tags(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_tags', self.xml)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                tags {
                    nodes {
                        id
                        name
                        comment
                        value
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        tags = json['data']['tags']['nodes']

        self.assertEqual(len(tags), 2)

        tag1 = tags[0]
        tag2 = tags[1]

        self.assertEqual(tag1['name'], 'cat')
        self.assertEqual(tag1['comment'], "dog")
        self.assertEqual(tag1['id'], 'e9b98e26-9fff-4ee8-9378-bc44fe3d6f2b')
        self.assertEqual(tag1['value'], "goat")
        self.assertEqual(tag2['name'], 'fooTag')
        self.assertEqual(tag2['comment'], None)
        self.assertEqual(tag2['id'], '85787cbb-a737-463d-94b8-fcc348225f3b')
        self.assertEqual(tag2['value'], "bar")

    def test_get_filtered_tags(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_tags', self.xml)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                tags (
                    filterString: "lorem",
                ) {
                    nodes {
                        id
                        name
                        comment
                        value
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        tags = json['data']['tags']['nodes']

        self.assertEqual(len(tags), 2)

        tag1 = tags[0]
        tag2 = tags[1]

        self.assertEqual(tag1['name'], 'cat')
        self.assertEqual(tag1['comment'], "dog")
        self.assertEqual(tag1['id'], 'e9b98e26-9fff-4ee8-9378-bc44fe3d6f2b')
        self.assertEqual(tag1['value'], "goat")
        self.assertEqual(tag2['name'], 'fooTag')
        self.assertEqual(tag2['comment'], None)
        self.assertEqual(tag2['id'], '85787cbb-a737-463d-94b8-fcc348225f3b')
        self.assertEqual(tag2['value'], "bar")


class TagsPaginationTestCase(SeleneTestCase):
    entity_name = 'tag'
    test_pagination_with_after_and_first = make_test_after_first(entity_name)
    test_counts = make_test_counts(entity_name)
    test_page_info = make_test_page_info(entity_name, query=GetTags)
    test_pagination_with_before_and_last = make_test_before_last(entity_name)
    test_edges = make_test_edges(entity_name)
    test_after_first_before_last = make_test_after_first_before_last(
        entity_name
    )
