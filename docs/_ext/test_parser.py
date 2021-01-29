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

from unittest import TestCase
from gqlschema import (
    parse_line,
    parse_block,
    parse_row,
    parse_table,
    parse_header,
    get_rows,
)


class ParserTestCase(TestCase):
    def setUp(self):
        self.schema = (
            'schema {\n'
            '  query: Query\n'
            '  mutation: Mutations\n'
            '}\n'
            '\n'
            'type LOREM {\n'
            '  value: Ipsum\n'
            '  dolor: Fecit\n'
            '}'
        )
        self.block = [
            'type LOREM {',
            '  value: Ipsum',
            '  dolor: Fecit',
            '}',
        ]

        self.block2 = [
            'schema {',
            '  value: Foo',
            '}',
        ]

        self.lines = self.block + [''] + self.block2

    def test_parse_line(self):
        line1 = '  foo: BAR'
        line2 = '  myMutation(arg1: Lies, arg2: String!): MyMutation'
        line3 = '  HELLO_WORLD'
        line4 = '  listOf: [Apples]'

        self.assertEqual(parse_line(line1), '* **foo** : BAR')
        self.assertEqual(
            parse_line(line2),
            '* **myMutation** (arg1: Lies, '
            + 'arg2: String (*required*)): MyMutation',
        )
        self.assertEqual(parse_line(line3), '* **HELLO_WORLD** ')
        self.assertEqual(parse_line(line4), '* **listOf** : [Apples]')

    def test_parse_block(self):

        parsed_block = [
            '* **value** : Ipsum',
            '* **dolor** : Fecit',
        ]

        self.assertEqual(parse_block(0, 3, self.block), parsed_block)

    def test_parse_header(self):

        header1 = ['TYPE LOREM']
        header2 = ['schema']

        self.assertEqual(parse_header(0, self.block), header1)
        self.assertEqual(parse_header(0, self.block2), header2)

    def test_parse_row(self):

        row = (['TYPE LOREM'], ['* **value** : Ipsum', '* **dolor** : Fecit'])

        row2 = (['schema'], ['* **value** : Foo'])

        self.assertEqual(parse_row(0, 3, self.block), row)
        self.assertEqual(parse_row(0, 2, self.block2), row2)

    def test_get_rows(self):
        test_pairs = [(0, 3), (5, 7)]

        self.assertEqual(get_rows(self.lines), test_pairs)

    def test_parse_table(self):

        table = [
            (['schema'], ['* **query** : Query', '* **mutation** : Mutations']),
            (['TYPE LOREM'], ['* **value** : Ipsum', '* **dolor** : Fecit']),
        ]
        self.assertEqual(parse_table(self.schema), table)
