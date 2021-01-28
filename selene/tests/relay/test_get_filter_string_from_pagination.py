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

from selene.schema.parser import FilterString
from selene.schema.relay import get_filter_string_for_pagination, get_cursor


class GetFilterStringFromPagination(unittest.TestCase):
    def test_should_parse_none(self):
        filter_string = get_filter_string_for_pagination(None)

        self.assertIsInstance(filter_string, FilterString)
        self.assertIsNone(filter_string.filter_string)

    def test_should_return_filter_string(self):
        filter_string1 = FilterString('foo=1 bar=2')
        filter_string2 = get_filter_string_for_pagination(filter_string1)

        self.assertEqual(str(filter_string2), 'foo=1 bar=2')
        self.assertIs(filter_string1, filter_string2)

    def test_should_update_rows_for_first(self):
        filter_string1 = FilterString('foo=1 rows=2')
        filter_string2 = get_filter_string_for_pagination(
            filter_string1, first=10
        )

        self.assertEqual(str(filter_string2), 'foo=1 rows=10')

    def test_should_update_rows_for_last(self):
        filter_string1 = FilterString('foo=1 rows=2')
        filter_string2 = get_filter_string_for_pagination(
            filter_string1, last=10
        )

        self.assertEqual(str(filter_string2), 'foo=1 rows=10')

    def test_should_update_first_for_after(self):
        cursor = get_cursor('foo', 123)
        filter_string1 = FilterString('first=1 rows=10')
        filter_string2 = get_filter_string_for_pagination(
            filter_string1, after=cursor
        )

        self.assertEqual(str(filter_string2), 'rows=10 first=125')

    def test_should_update_first_for_before(self):
        cursor = get_cursor('foo', 123)
        filter_string1 = FilterString('first=1 rows=10')
        filter_string2 = get_filter_string_for_pagination(
            filter_string1, before=cursor, last=10
        )

        self.assertEqual(str(filter_string2), 'rows=10 first=114')

    def test_should_update_first_and_rows_for_after_and_first(self):
        cursor = get_cursor('foo', 123)
        filter_string1 = FilterString('first=1 rows=10')
        filter_string2 = get_filter_string_for_pagination(
            filter_string1, after=cursor, first=5
        )

        self.assertEqual(str(filter_string2), 'rows=5 first=125')

    def test_should_prefer_after_for_before(self):
        after = get_cursor('foo', 100)
        before = get_cursor('foo', 200)
        filter_string1 = FilterString('first=1 rows=10')
        filter_string2 = get_filter_string_for_pagination(
            filter_string1, after=after, first=5, last=15, before=before
        )

        self.assertEqual(str(filter_string2), 'rows=5 first=102')
