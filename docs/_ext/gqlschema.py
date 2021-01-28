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

import importlib

from typing import List, Tuple

from docutils import nodes
from docutils.statemachine import ViewList
from docutils.parsers.rst.directives.tables import Table

from sphinx.util.nodes import nested_parse_with_titles

TABLEHEAD = ['Name', 'Field']


def get_rows(
    arr: List[str],
) -> List[Tuple[int, int]]:  # Get start/end positions of rows
    pairs = []
    i = 0

    while i < len(arr):
        if '{' in arr[i]:  # row start
            start = i

            k = 1

            while '}' not in arr[i + k]:
                k += 1

            # Should not have index error
            # Because we're grabbing schema
            # directly from code
            pairs.append((start, i + k))  # add (start, end)

            i += k
        else:
            i += 1

    return pairs


def parse_line(line: str) -> str:
    stripped_line = line.strip()
    if ':' in stripped_line and not '(' in stripped_line:
        index = stripped_line.find(':')
    elif '(' in stripped_line:
        index = stripped_line.find('(')
    else:
        index = -1

    if index < 0:
        field = stripped_line
    else:
        field = stripped_line[0:index]

    parsed_line = stripped_line.replace(
        # make field names bold
        field,
        '**' + field + '** ',
        1,
    ).replace('!', ' (*required*)')

    return '* ' + parsed_line


def parse_header(index: int, lines: List[str]) -> List[str]:
    words = lines[index].split()
    if words[0] == 'schema':
        return [words[0]]

    return [words[0].upper() + ' ' + words[1]]


def parse_block(
    start: int, end: int, lines: List[str]
) -> List[str]:  # parses block of fields
    to_print = []
    for i in range(start + 1, end):
        to_print.append(parse_line(lines[i]))

    return to_print


def parse_row(
    start: int, end: int, lines: List[str]
) -> Tuple[List[str], List[str]]:
    # each row consists of name,
    # and all of the fields in an array
    return (parse_header(start, lines), parse_block(start, end, lines))


def parse_table(schema: str) -> List[str]:
    lines = schema.split('\n')
    pairs = get_rows(lines)
    parsed_table = []

    # parse whole document into an arr of rows
    for index_pair in pairs:
        start = index_pair[0]
        end = index_pair[1]
        parsed_table.append(parse_row(start, end, lines))

    return parsed_table


class SchemaTable(Table):
    required_arguments = 1

    def run(self):
        schema_module = importlib.import_module(self.arguments[0])
        table_body = parse_table(str(schema_module.schema))

        # Extract some values we need for building the table.
        table_headers = TABLEHEAD

        max_cols = len(table_headers)
        col_widths = self.get_column_widths(max_cols)
        title, messages = self.make_title()

        # Build the node containing the table content
        table_node = self.build_table(table_body, col_widths, table_headers)
        self.add_name(table_node)
        if title:
            table_node.insert(0, title)
        return [table_node] + messages

    def build_table(self, table_data, col_widths, headers):
        table = nodes.table()

        # Set up the column specifications
        # based on the widths.
        tgroup = nodes.tgroup(cols=len(col_widths))
        table += tgroup
        tgroup.extend(
            nodes.colspec(colwidth=col_width) for col_width in col_widths
        )

        # Set the headers
        thead = nodes.thead()
        tgroup += thead
        row_node = nodes.row()
        thead += row_node
        row_node.extend(
            nodes.entry(h, nodes.paragraph(text=h)) for h in headers
        )

        # The body of the table is made up of rows.
        # Each row contains a series of entries,
        # and each entry contains a paragraph of text.
        tbody = nodes.tbody()
        tgroup += tbody
        rows = []

        for row in table_data:
            trow = nodes.row()

            for cell in row:
                rst = ViewList()
                entry = nodes.entry()
                para = nodes.paragraph()

                for elm in cell:
                    rst.append(elm, 'schema.rst', 0)

                nested_parse_with_titles(
                    self.state, rst, para
                )  # parse rst markup
                entry += para
                trow += entry

            rows.append(trow)

        tbody.extend(rows)

        # print table
        return table


def setup(app):
    app.add_directive('gql-schema', SchemaTable)
