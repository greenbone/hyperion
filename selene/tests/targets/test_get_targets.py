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
from selene.tests.entity import make_test_get_entities

from selene.schema.targets.queries import GetTargets


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class TargetsTestCase(SeleneTestCase):
    def setUp(self):
        self.xml = '''
            <get_targets_response>
                <target id="08b69003-5fc2-4037-a479-93b440211c73">
                    <name>foo</name>
                    <comment>bar</comment>
                </target>
                <target id="6b2db524-9fb0-45b8-9b56-d958f84cb546">
                    <name>lorem</name>
                    <comment>ipsum</comment>
                </target>
                <targets start="1" max="10"/>
                <target_count>2<filtered>2</filtered>
                    <page>2</page>
                </target_count>
            </get_targets_response>
            '''

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                targets {
                    nodes {
                        id
                        name
                        comment
                    }
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_targets(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_targets', self.xml)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                targets {
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

        targets = json['data']['targets']['nodes']

        self.assertEqual(len(targets), 2)

        target1 = targets[0]
        target2 = targets[1]

        # Target 1

        self.assertEqual(target1['id'], '08b69003-5fc2-4037-a479-93b440211c73')
        self.assertEqual(target1['name'], 'foo')

        # Target 2

        self.assertEqual(target2['id'], '6b2db524-9fb0-45b8-9b56-d958f84cb546')
        self.assertEqual(target2['name'], 'lorem')

    def test_get_filtered_targets(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_targets', self.xml)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                targets (
                    filterString: "lorem",
                ) {
                    nodes {
                        id
                        name
                        comment
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        targets = json['data']['targets']['nodes']

        self.assertEqual(len(targets), 2)

        target1 = targets[0]
        target2 = targets[1]

        self.assertEqual(target1['id'], '08b69003-5fc2-4037-a479-93b440211c73')
        self.assertEqual(target1['name'], 'foo')
        self.assertEqual(target1['comment'], 'bar')

        self.assertEqual(target2['id'], '6b2db524-9fb0-45b8-9b56-d958f84cb546')
        self.assertEqual(target2['name'], 'lorem')
        self.assertEqual(target2['comment'], 'ipsum')


class TargetsPaginationTestCase(SeleneTestCase):
    entity_name = 'target'
    test_pagination_with_after_and_first = make_test_after_first(entity_name)
    test_counts = make_test_counts(entity_name)
    test_get_page_info = make_test_page_info(entity_name, query=GetTargets)
    test_edges = make_test_edges(entity_name)
    test_pagination_with_before_and_last = make_test_before_last(entity_name)
    test_after_first_before_last = make_test_after_first_before_last(
        entity_name
    )


class TargetsGetEntitiesTestCase(SeleneTestCase):
    gmp_name = "target"
    test_get_entities = make_test_get_entities(gmp_name)
