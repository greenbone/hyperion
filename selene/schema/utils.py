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

from datetime import datetime
from typing import Optional, Callable, List
from xml.etree import ElementTree

from django.http import HttpRequest

from graphql import ResolveInfo

from gvm.protocols.gmpv214 import Gmp

from selene.errors import AuthenticationRequired

from selene.schema.parser import parse_bool, parse_datetime, parse_int

XmlElement = ElementTree.Element  # pylint: disable=invalid-name


def has_id(element: XmlElement) -> bool:
    if element is None:
        return False

    id_attr = element.get('id')

    if not id_attr:
        return False

    return bool(id_attr.strip())


def get_subelement(element: XmlElement, name: str) -> Optional[str]:
    """ Return a sub-element of element if available or None """
    if element is None:
        return None

    return element.find(name)


def get_owner(element: XmlElement) -> Optional[str]:
    owner = get_subelement(element, 'owner')

    if owner is None:
        return None

    return get_text_from_element(owner, 'name')


def get_text(element: XmlElement) -> Optional[str]:
    if element is not None:
        return element.text
    return None


def get_text_from_element(element: XmlElement, name: str) -> Optional[str]:
    return get_text(get_subelement(element, name))


def get_boolean_from_element(element: XmlElement, name: str) -> Optional[bool]:
    text = get_text_from_element(element, name)

    if text is None:
        return None

    return parse_bool(text.strip())


def get_datetime_from_element(element: XmlElement, name) -> Optional[datetime]:
    return parse_datetime(get_text_from_element(element, name))


def get_int_from_element(element: XmlElement, name: str) -> Optional[int]:
    return parse_int(get_text_from_element(element, name))


def get_sub_element_if_id_available(
    element: XmlElement, name: str
) -> Optional[XmlElement]:
    sub_element = get_subelement(element, name)

    if not has_id(sub_element):
        return None

    return sub_element


def get_gmp(info: ResolveInfo) -> Gmp:
    return info.context.gmp


def get_request(info: ResolveInfo) -> HttpRequest:
    return info.context


def check_authentication(info: ResolveInfo):
    request = get_request(info)
    if not request.session.get('username'):
        raise AuthenticationRequired('Not Authorized')


def require_authentication(resolver) -> Callable:
    def resolve(self, info: ResolveInfo, *args, **kwargs) -> Callable:
        check_authentication(info)
        return resolver(self, info, *args, **kwargs)

    return resolve


def csv_to_list(csv_list: str) -> List[str]:
    if not csv_list:
        return []

    return [value.strip() for value in csv_list.split(',')]
