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

from selene.schema.parser import parse_filter_string, FilterString


class FilterStringTestCase(unittest.TestCase):
    def test_parse_filter_string(self):
        filter_string = parse_filter_string('foo=bar')

        self.assertIsInstance(filter_string, FilterString)
        self.assertEqual(str(filter_string), 'foo=bar')

    def test_parse_none(self):
        filter_string = parse_filter_string(None)

        self.assertIsInstance(filter_string, FilterString)
        self.assertEqual(str(filter_string), '')

    def test_remove_rows(self):
        filter_string1 = parse_filter_string('rows=1 foo=bar')
        filter_string2 = filter_string1.remove_rows()

        self.assertIsInstance(filter_string1, FilterString)
        self.assertIsInstance(filter_string2, FilterString)
        self.assertIsNot(filter_string1, filter_string2)

        self.assertEqual(str(filter_string2), "foo=bar")

    def test_remove_rows_should_leave_whitespace(self):
        filter_string = parse_filter_string("foo=bar rows=1 sort=last")
        filter_string = filter_string.remove_rows()

        self.assertEqual(str(filter_string), "foo=bar sort=last")

    def test_remove_rows_removes_whitespace(self):
        filter_string = parse_filter_string('  rows=1     foo=bar')
        filter_string = filter_string.remove_rows()

        self.assertEqual(str(filter_string), "foo=bar")

    def test_remove_rows_removes_non_integer(self):
        filter_string = parse_filter_string('rows=abcÜ$ foo=bar')
        filter_string = filter_string.remove_rows()

        self.assertEqual(str(filter_string), "foo=bar")

    def test_remove_rows_ignores_similar_terms(self):
        filter_string = parse_filter_string('irows=1 foo=bar')
        filter_string = filter_string.remove_rows()

        self.assertEqual(str(filter_string), "irows=1 foo=bar")

    def test_add_rows(self):
        filter_string = parse_filter_string('foo=bar')
        filter_string = filter_string.add_rows(123)

        self.assertEqual(str(filter_string), "foo=bar rows=123")

    def test_add_rows_should_return_new_instance(self):
        filter_string1 = parse_filter_string('foo=bar')
        filter_string2 = filter_string1.add_rows(123)

        self.assertIsNot(filter_string1, filter_string2)

    def test_add_rows_several_times(self):
        # currently add_rows is very stupid and will add the rows keyword
        # several times. a more elaborated version of the method should be
        # called set_rows
        filter_string = parse_filter_string('rows=1 foo=bar')
        filter_string = filter_string.add_rows(123)
        filter_string = filter_string.add_rows(321)

        self.assertEqual(str(filter_string), "rows=1 foo=bar rows=123 rows=321")

    def test_remove_first(self):
        filter_string1 = parse_filter_string('first=1 foo=bar')
        filter_string2 = filter_string1.remove_first()

        self.assertIsInstance(filter_string1, FilterString)
        self.assertIsInstance(filter_string2, FilterString)
        self.assertIsNot(filter_string1, filter_string2)

        self.assertEqual(str(filter_string2), "foo=bar")

    def test_remove_first_should_leave_whitespace(self):
        filter_string = parse_filter_string("foo=bar first=1 sort=last")
        filter_string = filter_string.remove_first()

        self.assertEqual(str(filter_string), "foo=bar sort=last")

    def test_remove_first_removes_whitespace(self):
        filter_string = parse_filter_string('  first=1     foo=bar')
        filter_string = filter_string.remove_first()

        self.assertEqual(str(filter_string), "foo=bar")

    def test_remove_first_removes_non_integer(self):
        filter_string = parse_filter_string('first=abcÜ$ foo=bar')
        filter_string = filter_string.remove_first()

        self.assertEqual(str(filter_string), "foo=bar")

    def test_remove_first_ignores_similar_terms(self):
        filter_string = parse_filter_string('ifirst=1 foo=bar')
        filter_string = filter_string.remove_first()

        self.assertEqual(str(filter_string), "ifirst=1 foo=bar")

    def test_add_first(self):
        filter_string = parse_filter_string('foo=bar')
        filter_string = filter_string.add_first(123)

        self.assertEqual(str(filter_string), "foo=bar first=123")

    def test_add_first_should_return_new_instance(self):
        filter_string1 = parse_filter_string('foo=bar')
        filter_string2 = filter_string1.add_first(123)

        self.assertIsNot(filter_string1, filter_string2)

    def test_add_first_several_times(self):
        # currently add_first is very stupid and will add the first keyword
        # several times. a more elaborated version of the method should be
        # called set_first
        filter_string = parse_filter_string('first=1 foo=bar')
        filter_string = filter_string.add_first(123)
        filter_string = filter_string.add_first(321)

        self.assertEqual(
            str(filter_string), "first=1 foo=bar first=123 first=321"
        )
