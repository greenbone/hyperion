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

from selene.schema.policies.queries import GetPolicies


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class PoliciesTestCase(SeleneTestCase):
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
                policies{
                    nodes {
                        id
                        name
                    }
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_policies(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_policies', self.xml)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                policies {
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

        policies = json['data']['policies']['nodes']

        self.assertEqual(len(policies), 2)

        policy1 = policies[0]
        policy2 = policies[1]

        # Policy 1

        self.assertEqual(policy1['id'], '08b69003-5fc2-4037-a479-93b440211c73')
        self.assertEqual(policy1['name'], 'foo')

        # Policy 2

        self.assertEqual(policy2['id'], '6b2db524-9fb0-45b8-9b56-d958f84cb546')
        self.assertEqual(policy2['name'], 'lorem')

    def test_get_filtered_policies(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_policies', self.xml)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                policies (
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

        policies = json['data']['policies']['nodes']

        self.assertEqual(len(policies), 2)

        policy1 = policies[0]
        policy2 = policies[1]

        self.assertEqual(policy1['id'], '08b69003-5fc2-4037-a479-93b440211c73')
        self.assertEqual(policy1['name'], 'foo')

        self.assertEqual(policy2['id'], '6b2db524-9fb0-45b8-9b56-d958f84cb546')
        self.assertEqual(policy2['name'], 'lorem')


class PoliciesPaginationTestCase(SeleneTestCase):
    gmp_name = 'config'
    gmp_cmd = 'get_policies'
    selene_name = 'policy'
    plural_name = 'policies'
    test_pagination_with_after_and_first = make_test_after_first(
        gmp_name,
        selene_name=selene_name,
        gmp_cmd=gmp_cmd,
        plural_selene_name=plural_name,
        details=False,
    )
    test_counts = make_test_counts(
        gmp_name,
        gmp_cmd=gmp_cmd,
        selene_name=selene_name,
        plural_selene_name=plural_name,
    )
    test_page_info = make_test_page_info(
        gmp_name,
        selene_name=selene_name,
        gmp_cmd=gmp_cmd,
        plural_selene_name=plural_name,
        query=GetPolicies,
    )
    test_pagination_with_before_and_last = make_test_before_last(
        gmp_name,
        selene_name=selene_name,
        gmp_cmd=gmp_cmd,
        plural_selene_name=plural_name,
        details=False,
    )
    test_edges = make_test_edges(
        gmp_name,
        gmp_cmd=gmp_cmd,
        selene_name=selene_name,
        plural_selene_name=plural_name,
    )
    test_after_first_before_last = make_test_after_first_before_last(
        gmp_name,
        selene_name=selene_name,
        gmp_cmd=gmp_cmd,
        plural_selene_name=plural_name,
        details=False,
    )


class PoliciesGetEntitiesTestCase(SeleneTestCase):
    # it gets weirder and weirder ....
    gmp_name = 'config'
    gmp_cmd = 'get_policies'
    selene_name = 'policy'
    plural_name = 'policies'
    test_get_entities = make_test_get_entities(
        gmp_name,
        selene_name=selene_name,
        gmp_cmd=gmp_cmd,
        plural_selene_name=plural_name,
        details=False,
    )
