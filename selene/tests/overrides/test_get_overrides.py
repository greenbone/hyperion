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

from selene.schema.overrides.queries import GetOverrides


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class OverrideTestCase(SeleneTestCase):
    def setUp(self):
        self.xml = '''
            <get_override_response>
                <override id="08b69003-5fc2-4037-a479-93b440211c73">
                    <text>foo</text>
                    <owner><name>Han</name></owner>
                    <creation_time>2020-06-30T09:16:25Z</creation_time>
                    <modification_time>2020-07-30T09:16:25Z</modification_time>
                    <writable>1</writable>
                    <in_use>1</in_use>
                    <active>1</active>
                    <orphan>0</orphan>
                    <nvt><name>Greedo</name></nvt>
                    <hosts>123.456.789.1,123.456.789.2</hosts>
                    <severity>5.5</severity>
                    <new_severity>10</new_severity>
                </override>
                <override id="6b2db524-9fb0-45b8-9b56-d958f84cb546">
                    <text>bar</text>
                    <owner><name>Lorem</name></owner>
                    <creation_time>2020-06-30T09:16:25Z</creation_time>
                    <modification_time>2020-07-30T09:16:25Z</modification_time>
                    <writable>1</writable>
                    <in_use>1</in_use>
                    <active>1</active>
                    <orphan>0</orphan>
                    <nvt><name>Ipsum</name></nvt>
                    <hosts>123.456.789.3,123.456.789.4</hosts>
                    <severity>5.5</severity>
                    <new_severity>10</new_severity>
                </override>
                <override_count>
                    20
                    <filtered>2</filtered>
                </override_count>
                <overrides max="10" start="1"/>
            </get_override_response>
            '''

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                overrides {
                    nodes {
                        id
                        text
                    }
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_overrides(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_overrides', self.xml)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                overrides {
                    nodes {
                        id
                        text
                        creationTime
                        modificationTime
                        active
                        inUse
                        orphan
                        writable
                        hosts
                        name
                        owner
                        severity
                        newSeverity
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        overrides = json['data']['overrides']['nodes']

        self.assertEqual(len(overrides), 2)

        override1 = overrides[0]
        override2 = overrides[1]

        self.assertEqual(
            override1['id'], '08b69003-5fc2-4037-a479-93b440211c73'
        )
        self.assertEqual(override1['text'], 'foo')
        self.assertEqual(override1['creationTime'], '2020-06-30T09:16:25+00:00')
        self.assertEqual(
            override1['modificationTime'], '2020-07-30T09:16:25+00:00'
        )
        self.assertEqual(override1['active'], True)
        self.assertEqual(override1['owner'], 'Han')
        self.assertEqual(override1['inUse'], True)
        self.assertEqual(override1['orphan'], False)
        self.assertEqual(override1['writable'], True)
        self.assertEqual(override1['name'], 'Greedo')
        self.assertListEqual(
            override1['hosts'], ['123.456.789.1', '123.456.789.2']
        )
        self.assertEqual(override1['severity'], 5.5)
        self.assertEqual(override1['newSeverity'], 10)

        self.assertEqual(
            override2['id'], '6b2db524-9fb0-45b8-9b56-d958f84cb546'
        )
        self.assertEqual(override2['text'], 'bar')
        self.assertEqual(override2['creationTime'], '2020-06-30T09:16:25+00:00')
        self.assertEqual(
            override2['modificationTime'], '2020-07-30T09:16:25+00:00'
        )
        self.assertEqual(override2['active'], True)
        self.assertEqual(override2['owner'], 'Lorem')
        self.assertEqual(override2['inUse'], True)
        self.assertEqual(override2['orphan'], False)
        self.assertEqual(override2['writable'], True)
        self.assertEqual(override2['name'], 'Ipsum')
        self.assertEqual(override2['hosts'], ['123.456.789.3', '123.456.789.4'])
        self.assertEqual(override2['severity'], 5.5)
        self.assertEqual(override2['newSeverity'], 10)

    def test_get_filtered_overrides(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_overrides', self.xml)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                overrides (
                    filterString: "lorem",
                ) {
                    nodes {
                        id
                        text
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        overrides = json['data']['overrides']['nodes']

        self.assertEqual(len(overrides), 2)

        override1 = overrides[0]
        override2 = overrides[1]

        self.assertEqual(
            override1['id'], '08b69003-5fc2-4037-a479-93b440211c73'
        )
        self.assertEqual(override1['text'], 'foo')

        self.assertEqual(
            override2['id'], '6b2db524-9fb0-45b8-9b56-d958f84cb546'
        )
        self.assertEqual(override2['text'], 'bar')


class OverridesPaginationTestCase(SeleneTestCase):
    entity_name = 'override'
    test_pagination_with_after_and_first = make_test_after_first(
        entity_name, details=True
    )
    test_counts = make_test_counts(entity_name)
    test_page_info = make_test_page_info(entity_name, query=GetOverrides)
    test_pagination_with_before_and_last = make_test_before_last(
        entity_name, details=True
    )
    test_edges = make_test_edges(entity_name)
    test_after_first_before_last = make_test_after_first_before_last(
        entity_name, details=True
    )
