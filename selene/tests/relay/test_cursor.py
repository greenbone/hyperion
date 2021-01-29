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

from base64 import b64encode
import unittest

from selene.schema.relay import get_cursor, get_offset_from_cursor


class GetCursorTestCase(unittest.TestCase):
    def test_create_cursor(self):
        # not sure if the implementation details should be tested here
        cursor = get_cursor('foo', 123)

        encoded_cursor = b64encode(b'foo:123').decode('utf-8')
        self.assertEqual(encoded_cursor, cursor)


class GetOffsetFromCursor(unittest.TestCase):
    def test_get_offset(self):
        cursor = get_cursor('foo', 123)
        offset = get_offset_from_cursor(cursor)

        self.assertEqual(offset, 123)
