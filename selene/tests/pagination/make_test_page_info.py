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

import unittest

from selene.tests import GmpMockFactory

from selene.tests.utils.utils import pluralize_name, compose_mock_command


def compose_mock_response(entity_name, no_plural):
    entities_name = pluralize_name(entity_name)
    xml_response = f'''
        <get_{entities_name}_response>
                <{entity_name} id="f650a1c0-3d23-11ea-8540-e790e17c1b00">
                    <name>a</name>
                </{entity_name}>
                <{entity_name} id="0778ac90-3d24-11ea-b722-fff755412c48">
                    <name>b</name>
                </{entity_name}>
                <{entity_name}_count>
                    20
                    <filtered>11</filtered>
                </{entity_name}_count>
                <{entity_name if no_plural else entities_name} max="10" start="3"/>
        </get_{entities_name}_response>
    '''
    return xml_response


def compose_mock_query(plural_name):
    query = f'''
            query {{
                {plural_name} {{
                    pageInfo {{
                        hasNextPage
                        hasPreviousPage
                        startCursor
                        endCursor
                    }}
                }}
            }}
            '''
    return query


def make_test_page_info(
    gmp_name: str,
    *,
    selene_name: str = None,
    query=None,
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

        json = response.json()

        self.assertResponseNoErrors(response)

        page_info = json['data'][plural_selene_name]['pageInfo']

        self.assertTrue(page_info['hasNextPage'])
        self.assertTrue(page_info['hasPreviousPage'])

        edge_class = query().type._meta.edge

        self.assertEqual(page_info['startCursor'], edge_class.get_cursor(2))
        self.assertEqual(page_info['endCursor'], edge_class.get_cursor(3))

    return test
