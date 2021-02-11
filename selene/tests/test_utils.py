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

import datetime

from unittest import TestCase

from lxml import etree as et
from lxml.etree import Element

from selene.schema.utils import (
    has_id,
    get_owner,
    get_text,
    get_text_from_element,
    get_boolean_from_element,
    get_datetime_from_element,
    get_int_from_element,
    get_sub_element_if_id_available,
    get_subelement,
)


class HasIdTestCase(TestCase):
    def test_none(self):
        self.assertFalse(has_id(None))

    def test_no_id(self):
        element = Element("foo")
        self.assertFalse(has_id(element))

    def test_empty_id(self):
        element = Element("foo", attrib={'id': ''})
        self.assertFalse(has_id(element))

        element = Element("foo", attrib={'id': ' '})
        self.assertFalse(has_id(element))

    def test_has_id(self):
        element = Element("foo", attrib={'id': '1'})
        self.assertTrue(has_id(element))

        element = Element("foo", attrib={'id': 'bar'})
        self.assertTrue(has_id(element))


class GetOwnerTestCase(TestCase):
    def test_none(self):
        self.assertIsNone(get_owner(None))

    def test_no_owner(self):
        element = Element("foo")
        self.assertIsNone(get_owner(element))

    def test_no_name(self):
        element = Element("owner")
        self.assertIsNone(get_owner(element))

    def test_get_owner(self):
        element = et.fromstring('<foo><owner><name>foo</name></owner></foo>')
        owner = get_owner(element)

        self.assertIsNotNone(owner)
        self.assertEqual(owner, 'foo')

        element = et.fromstring(
            '<foo><owner><bar>bar</bar><name>foo</name></owner></foo>'
        )
        owner = get_owner(element)

        self.assertIsNotNone(owner)
        self.assertEqual(owner, 'foo')


class GetTextTestCase(TestCase):
    def test_none(self):
        self.assertIsNone(get_text(None))

    def test_simple_text(self):
        element = et.fromstring("<foo>bar</foo>")
        self.assertEqual(get_text(element), "bar")

    def test_text(self):
        element = et.fromstring("<foo>foo\nbar\n</foo>")
        self.assertEqual(get_text(element), "foo\nbar\n")

    def test_text_with_subelements(self):
        element = et.fromstring("<foo>bar\n<bar/><ipsum/></foo>")
        self.assertEqual(get_text(element), "bar\n")

    def test_text_with_subelements_and_tail(self):
        element = et.fromstring("<foo>bar<bar/><ipsum/>bar</foo>")
        self.assertEqual(get_text(element), "bar")


class GetTextFromElementTestCase(TestCase):
    def test_none(self):
        self.assertIsNone(get_text_from_element(None, 'foo'))

    def test_unkown_subelement(self):
        element = Element('foo')
        self.assertIsNone(get_text_from_element(element, 'bar'))

    def test_getting_text_from_subelement(self):
        element = et.fromstring("<foo><bar>ipsum</bar></foo>")
        self.assertEqual(get_text_from_element(element, 'bar'), 'ipsum')


class GetBooleanFromElementTestCase(TestCase):
    def test_none(self):
        self.assertIsNone(get_boolean_from_element(None, 'foo'))

    def test_unkown_subelement(self):
        element = Element('foo')
        self.assertIsNone(get_boolean_from_element(element, 'bar'))

    def test_empty_subelement(self):
        element = et.fromstring("<foo><bar></bar></foo>")
        self.assertFalse(get_boolean_from_element(element, 'bar'))

        element = et.fromstring("<foo><bar> </bar></foo>")
        self.assertFalse(get_boolean_from_element(element, 'bar'))

    def test_invalid_bool_string(self):
        element = et.fromstring("<foo><bar>ipsum</bar></foo>")
        self.assertFalse(get_boolean_from_element(element, 'bar'))

    def test_bool_strings(self):
        element = et.fromstring("<foo><bar>0</bar></foo>")
        self.assertFalse(get_boolean_from_element(element, 'bar'))

        element = et.fromstring("<foo><bar>1</bar></foo>")
        self.assertTrue(get_boolean_from_element(element, 'bar'))

    def test_additional_whitespace(self):
        element = et.fromstring("<foo><bar> 1 </bar></foo>")
        self.assertTrue(get_boolean_from_element(element, 'bar'))

        element = et.fromstring("<foo><bar>\n1\n</bar></foo>")
        self.assertTrue(get_boolean_from_element(element, 'bar'))


class GetDatetimeFromElementTestCase(TestCase):
    def test_none(self):
        self.assertIsNone(get_datetime_from_element(None, 'foo'))

    def test_unkown_subelement(self):
        element = Element('foo')
        self.assertIsNone(get_datetime_from_element(element, 'bar'))

    def test_invalid_datetime(self):
        element = et.fromstring("<foo><bar>ipsum</bar></foo>")
        self.assertIsNone(get_datetime_from_element(element, 'bar'))

    def test_empty_subelement(self):
        element = et.fromstring("<foo><bar></bar></foo>")
        self.assertFalse(get_datetime_from_element(element, 'bar'))

        element = et.fromstring("<foo><bar> </bar></foo>")
        self.assertFalse(get_datetime_from_element(element, 'bar'))

    def test_iso_time(self):
        element = et.fromstring("<foo><bar>2020-01-10T13:13:33Z</bar></foo>")
        dt = get_datetime_from_element(element, 'bar')

        self.assertIsNotNone(dt)
        self.assertIsInstance(dt, datetime.datetime)

        self.assertEqual(dt.year, 2020)
        self.assertEqual(dt.month, 1)
        self.assertEqual(dt.day, 10)

        self.assertEqual(dt.hour, 13)
        self.assertEqual(dt.minute, 13)
        self.assertEqual(dt.second, 33)
        self.assertEqual(str(dt.tzinfo), 'UTC')


class GetIntFromElementTestCase(TestCase):
    def test_none(self):
        self.assertIsNone(get_int_from_element(None, 'foo'))

    def test_unkown_subelement(self):
        element = Element('foo')
        self.assertIsNone(get_int_from_element(element, 'bar'))

    def test_invalid_int(self):
        element = et.fromstring("<foo><bar>ipsum</bar></foo>")
        self.assertIsNone(get_int_from_element(element, 'bar'))

    def test_empty_subelement(self):
        element = et.fromstring("<foo><bar></bar></foo>")
        self.assertIsNone(get_int_from_element(element, 'bar'))

        element = et.fromstring("<foo><bar> </bar></foo>")
        self.assertIsNone(get_int_from_element(element, 'bar'))

    def test_int(self):
        element = et.fromstring("<foo><bar>123</bar></foo>")
        self.assertEqual(get_int_from_element(element, 'bar'), 123)

        element = et.fromstring("<foo><bar>666</bar></foo>")
        self.assertEqual(get_int_from_element(element, 'bar'), 666)

    def test_additional_whitespace(self):
        element = et.fromstring("<foo><bar> 666 </bar></foo>")
        self.assertEqual(get_int_from_element(element, 'bar'), 666)

        element = et.fromstring("<foo><bar>\n666\n</bar></foo>")
        self.assertEqual(get_int_from_element(element, 'bar'), 666)


class GetSubElementIfIdAvailableTestCase(TestCase):
    def test_none(self):
        self.assertIsNone(get_sub_element_if_id_available(None, 'foo'))

    def test_unkown_subelement(self):
        element = Element('foo')
        self.assertIsNone(get_sub_element_if_id_available(element, 'bar'))

    def test_subelement_no_id(self):
        element = et.fromstring("<foo><bar></bar></foo>")
        self.assertIsNone(get_sub_element_if_id_available(element, 'bar'))

    def test_subelement_empty_id(self):
        element = et.fromstring("<foo><bar id=''></bar></foo>")
        self.assertIsNone(get_sub_element_if_id_available(element, 'bar'))

        element = et.fromstring("<foo><bar id=' '></bar></foo>")
        self.assertIsNone(get_sub_element_if_id_available(element, 'bar'))

    def test_get_subelement(self):
        element = et.fromstring("<foo><bar id='foo'></bar></foo>")
        subelement = get_sub_element_if_id_available(element, 'bar')

        self.assertIsNotNone(subelement)
        self.assertEqual(subelement.tag, 'bar')

        element = et.fromstring("<foo><bar id='1'></bar></foo>")
        subelement = get_sub_element_if_id_available(element, 'bar')

        self.assertIsNotNone(subelement)
        self.assertEqual(subelement.tag, 'bar')


class GetSubelementTestCase(TestCase):
    def test_none(self):
        self.assertIsNone(get_subelement(None, 'foo'))

    def test_unknown_subelement(self):
        element = et.fromstring("<foo></foo>")
        self.assertIsNone(get_subelement(element, 'bar'))

    def test_valid_subelement(self):
        element = et.fromstring("<foo><bar></bar></foo>")
        subelement = get_subelement(element, 'bar')

        self.assertIsNotNone(subelement)
        self.assertEqual(subelement.tag, 'bar')
