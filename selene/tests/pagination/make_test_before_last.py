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

from selene.schema.relay import get_cursor

from selene.tests import GmpMockFactory

from selene.tests.utils.utils import (
    pluralize_name,
    compose_mock_command,
    return_gmp_methods,
)

from selene.tests.pagination.make_test_after_first import compose_mock_response


def compose_mock_query(plural_name):
    query = f'''
            query {{
                {plural_name} (
                    filterString: "lorem rows=5 first=1",
                    before: "{get_cursor('abc', 123)}",
                    last: 10,
                ) {{
                    nodes {{
                        id
                    }}
                }}
            }}
            '''
    return query


def make_test_before_last(
    gmp_name: str,
    *,
    selene_name: str = None,
    gmp_cmd: str = None,
    plural_selene_name: str = None,
    **kwargs,
):

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

        gmp_commands = return_gmp_methods(mock_gmp.gmp_protocol)

        mock_gmp.mock_response(gmp_cmd, compose_mock_response(gmp_name))

        self.login('foo', 'bar')

        response = self.query(compose_mock_query(plural_selene_name))

        json = response.json()

        self.assertResponseNoErrors(response)

        get_entities = gmp_commands[gmp_cmd]

        get_entities.assert_called_with(
            filter='lorem rows=10 first=114', **kwargs
        )

        entities = json['data'][plural_selene_name]['nodes']

        self.assertEqual(len(entities), 2)

    return test
