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

# pylint: disable=no-self-argument, no-member

from selene.schema.utils import (
    get_text,
    get_text_from_element,
    get_boolean_from_element,
    get_int_from_element,
)


def text_resolver(attname, default_value, root, info, **args):
    # pylint: disable=unused-argument
    return get_text_from_element(root, attname)


def boolean_resolver(attname, default_value, root, info, **args):
    ##pylint: disable=unused-argument
    return get_boolean_from_element(root, attname)


def int_resolver(attname, default_value, root, info, **args):
    ##pylint: disable=unused-argument
    return get_int_from_element(root, attname)


def find_resolver(attname, default_value, root, info, **args):
    # pylint: disable=unused-argument
    return root.find(attname)


def nvt_tags_resolver(attname, default_value, root, info, **args):
    # pylint: disable=unused-argument
    tags = get_text(root)
    if tags:
        tags = tags.split('|')
        for tag in tags:
            key, value = tag.strip().split('=', 1)
            if key == attname:
                return value
    return None
