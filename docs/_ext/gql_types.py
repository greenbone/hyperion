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
from docutils import nodes
from docutils.statemachine import ViewList
from docutils.parsers.rst.directives.body import Container
from sphinx.util.nodes import nested_parse_with_titles
from graphene.types.schema import Schema

# https://spec.graphql.org/June2018/#sec-Schema-Introspection

TABLE_HEADERS = ['Argument', 'Type', 'Description']


class LoadModule(Container):
    """Loads the module passed by sphinx and runs the table creation
    commands"""

    required_arguments = 1

    def run(self):
        schema_module = importlib.import_module(self.arguments[0])
        if not isinstance(schema_module.schema, Schema):
            raise TypeError(
                f"To run this documentation extension, you "
                f"need to pass a {type(Schema()).__name__}"
            )

        type_map = schema_module.schema.get_type_map()
        node = build_types(type_map, self.state)
        return node


def build_types(type_map, state):
    """Iteration over the different module fields and create
    a table for each class"""
    tables = []
    for item in type_map.items():
        node = table_container(item, state)
        tables += node
    return tables


def table_container(item, state):
    """Parse a table"""
    nsection = nodes.section()
    nsubtitle, ndescription = header(item)
    nsection.append(nsubtitle)
    nsection.append(ndescription)
    # If there are fields, we parse a table ...
    if hasattr(item[1], 'fields'):
        # TO DO Exclude queries from types as they are already in Queries ...
        # if item[0] == 'Query':
        #    queries = [field[0] for field in item[1].fields]
        table_node = table(item, state)
        nsection.append(table_node)
    return nsection


def table(item, state):
    """Build the arguments table"""
    # Set up the column specifications
    # based on the widths.
    col_widths = [300, 300, 300]
    ntable = nodes.table(align='left')
    ngroup = nodes.tgroup(cols=len(TABLE_HEADERS))
    ntable += ngroup
    ngroup.extend(nodes.colspec(colwidth=col_width) for col_width in col_widths)

    # Set the table headers
    nhead = nodes.thead()
    ngroup += nhead
    head_row = nodes.row()
    nhead += head_row
    head_row.extend(
        nodes.entry(header, nodes.paragraph(text=header))
        for header in TABLE_HEADERS
    )

    tbody = nodes.tbody()
    ngroup += tbody
    rows = []

    for key, value in item[1].fields.items():
        trow = nodes.row()
        row = [str(key), str(value.type), str(value.description)]
        for cell in row:
            rst = ViewList()
            entry = nodes.entry(cell)

            rst.append(cell, 'schema.rst', 0)

            nested_parse_with_titles(state, rst, entry)  # parse rst markup
            trow += entry

        rows.append(trow)

    tbody.extend(rows)

    return ntable


def header(item):
    """Creates an Table Header with the Type Name and Documentation"""
    nsubtitle = nodes.rubric(text='')
    subt = f'{str(item[0])}'
    nstrong = nodes.strong(text=subt)
    nsubtitle.append(nstrong)
    desc = str(item[1].description).split('\n')
    ndescription = nodes.paragraph(text='')
    for line in desc:
        if 'Args' in line:
            break
        ndescription.append(nodes.Text(f'{line}'))

    return nsubtitle, ndescription


def setup(app):
    app.add_directive('gql-types', LoadModule)
