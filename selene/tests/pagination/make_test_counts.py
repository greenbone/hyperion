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

from selene.tests import GmpMockFactory

from selene.tests.utils.utils import pluralize_name, compose_mock_command


def compose_mock_query(plural_name):
    query = f'''
            query {{
                {plural_name} {{
                    nodes {{
                        id
                    }}
                    counts {{
                        filtered
                        total
                        offset
                        limit
                        length
                    }}
                }}
            }}
            '''
    return query


def compose_mock_response(entity_name, no_plural):
    entities_name = pluralize_name(entity_name)
    xml_response = f'''
        <get_{entities_name}_response status="200" status_text="OK">
            <{entity_name} id="e9b98e26-9fff-4ee8-9378-bc44fe3d6f2b">
                <name>foo</name>
            </{entity_name}>
            <{entity_name} id="85787cbb-a737-463d-94b8-fcc348225f3b">
                <name>bar</name>
            </{entity_name}>
            <{entity_name if no_plural else entities_name} start="1" max="10"/>
            <{entity_name}_count>2<filtered>2</filtered>
                <page>2</page>
            </{entity_name}_count>
        </get_{entities_name}_response>
    '''
    return xml_response


def make_test_counts(
    gmp_name: str,
    *,
    selene_name: str = None,
    gmp_cmd: str = None,
    plural_selene_name: str = None,
    no_plural: bool = False,
):
    # no_plural for e.g. info where there is no plural - I wanted
    # to use this tests for that entity too
    # was a little hacky ... but this way no old tests need to be adjusted ...
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

        self.assertResponseNoErrors(response)

        json = response.json()
        entities = json['data'][plural_selene_name]['nodes']
        self.assertEqual(len(entities), 2)

        counts = json['data'][plural_selene_name]['counts']

        self.assertEqual(counts['filtered'], 2)
        self.assertEqual(counts['total'], 2)
        self.assertEqual(counts['offset'], 0)
        self.assertEqual(counts['limit'], 10)
        self.assertEqual(counts['length'], 2)

    return test
