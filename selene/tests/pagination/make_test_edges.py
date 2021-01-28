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

import unittest

from selene.schema.relay import get_cursor

from selene.tests import GmpMockFactory

from selene.tests.pagination.make_test_counts import compose_mock_response

from selene.tests.utils.utils import pluralize_name, compose_mock_command


def compose_mock_query(plural_name):
    query = f'''
            query {{
                {plural_name} {{
                    edges {{
                        node {{
                            id
                        }}
                        cursor
                    }}
                }}
            }}
            '''
    return query


def make_test_edges(
    gmp_name: str,
    *,
    selene_name: str = None,
    edge_name: str = None,
    gmp_cmd: str = None,
    plural_selene_name: str = None,
    no_plural: bool = False,
):
    # no_plural for e.g. info where there is no plural - I wanted
    # to use this tests for that entity too
    # was a little hacky ...
    if not selene_name:
        selene_name = gmp_name

    # for special gmp commands like "get_info_list"
    if not gmp_cmd:
        gmp_cmd = compose_mock_command(gmp_name)

    if edge_name is None:
        edge_name = selene_name.lower()

    # for special plurals of irregulars like policy
    if not plural_selene_name:
        plural_selene_name = pluralize_name(selene_name)

    @unittest.mock.patch('selene.views.Gmp', new_callable=GmpMockFactory)
    def test(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            gmp_cmd, compose_mock_response(gmp_name, no_plural)
        )

        self.login('foo', 'bar')

        response = self.query(compose_mock_query(plural_selene_name))
        self.assertResponseNoErrors(response)

        json = response.json()

        edges = json['data'][plural_selene_name]['edges']

        edge1 = edges[0]
        edge2 = edges[1]

        self.assertEqual(edge1['cursor'], get_cursor(edge_name, 0))
        self.assertEqual(edge2['cursor'], get_cursor(edge_name, 1))

        entity1 = edge1['node']
        entity2 = edge2['node']

        self.assertEqual(entity1['id'], 'e9b98e26-9fff-4ee8-9378-bc44fe3d6f2b')

        self.assertEqual(entity2['id'], '85787cbb-a737-463d-94b8-fcc348225f3b')

    return test
