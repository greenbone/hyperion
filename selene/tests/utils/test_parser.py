# -*- coding: utf-8 -*-
# Copyright (C) 2019-2021 Greenbone Networks GmbH
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

from uuid import UUID

from selene.schema.parser import (
    parse_bool,
    parse_datetime,
    parse_uuid,
    parse_int,
)


class ParseBoolTestCase(TestCase):
    def test_none(self):
        self.assertIsNone(parse_bool(None))

    def test_str(self):
        self.assertTrue(parse_bool('1'))
        self.assertFalse(parse_bool('0'))
        self.assertFalse(parse_bool(''))
        self.assertFalse(parse_bool('foo'))

    def test_int(self):
        self.assertTrue(parse_bool(1))
        self.assertFalse(parse_bool(0))
        self.assertFalse(parse_bool(12))
        self.assertFalse(parse_bool(-1))


class ParseDateTimeTestCase(TestCase):
    def test_none(self):
        self.assertIsNone(parse_datetime(None))
        self.assertIsNone(parse_datetime(''))

    def test_iso_like_format(self):
        dt = parse_datetime('2020-01-08T14:36:21Z')
        self.assertEqual(dt.day, 8)
        self.assertEqual(dt.month, 1)
        self.assertEqual(dt.year, 2020)
        self.assertEqual(dt.hour, 14)
        self.assertEqual(dt.minute, 36)
        self.assertEqual(dt.second, 21)
        self.assertEqual(dt.tzinfo.tzname(dt), 'UTC')


class ParseUuidTestCase(TestCase):
    def test_none(self):
        self.assertIsNone(parse_uuid(None))
        self.assertIsNone(parse_uuid(''))

    def test_valid_uuid(self):
        uuid = parse_uuid('75d23ba8-3d23-11ea-858e-b7c2cb43e815')
        self.assertIsInstance(uuid, UUID)
        self.assertEqual(str(uuid), '75d23ba8-3d23-11ea-858e-b7c2cb43e815')

    def test_invalid_uuid(self):
        with self.assertRaises(ValueError):
            parse_uuid('foo')


class ParseIntTestCase(TestCase):
    def test_none(self):
        self.assertIsNone(parse_int(None))
        self.assertIsNone(parse_int(''))
        self.assertIsNone(parse_int('a'))
        self.assertIsNone(parse_int('1.2'))

    def test_valid_int(self):
        self.assertEqual(parse_int('1'), 1)
        self.assertEqual(parse_int('666'), 666)
        self.assertEqual(parse_int('01'), 1)
        self.assertEqual(parse_int(' 1'), 1)
        self.assertEqual(parse_int('                666             '), 666)

    def test_raise_exception(self):
        with self.assertRaises(ValueError):
            parse_int(' ', safe=False)

        with self.assertRaises(ValueError):
            parse_int('a', safe=False)

        with self.assertRaises(ValueError):
            parse_int('1.2', safe=False)
