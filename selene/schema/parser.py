# -*- coding: utf-8 -*-
# Copyright (C) 2019 Greenbone Networks GmbH
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
import re

from uuid import UUID

from typing import Union, Optional

from django.utils.dateparse import parse_datetime as django_parse_datatime

ROWS_RE = re.compile(r'(^|\s+)rows=\S+\s*')
FIRST_RE = re.compile(r'(^|\s+)first=\S+\s*')


class FilterString:
    """Very simplified representation of a gvmd filter"""

    def __init__(self, filter_string: str = None):
        self.filter_string = filter_string

    def remove_rows(self) -> "FilterString":
        """Remove rows term from filter string"""
        filter_string = ROWS_RE.sub(' ', self.filter_string)
        return FilterString(filter_string.strip())

    def remove_first(self) -> "FilterString":
        """Remove first term from filter string"""
        filter_string = FIRST_RE.sub(' ', self.filter_string)
        return FilterString(filter_string.strip())

    def add_rows(self, rows: int) -> "FilterString":
        """Add rows filter term"""
        filter_string = self.filter_string + f' rows={rows}'
        return FilterString(filter_string)

    def add_first(self, first: int) -> "FilterString":
        """Add first filter term"""
        filter_string = self.filter_string + f' first={first}'
        return FilterString(filter_string)

    def __str__(self) -> str:
        return self.filter_string or ''


def check_severity(value):
    test_val = int(float(value) * 10)
    # From gvmd ...
    #  -1.0: False positive severity constant
    #  -2.0: Debug message severity constant
    #  -3.0: Error message severity constant
    # -98.0: Constant for undefined severity (for ranges)
    # -99.0: Constant for missing or invalid severity
    if 0 <= test_val <= 100 or -10 or -20 or -30 or -980 or -990:
        return float(test_val / 10)
    return None


def parse_bool(value: Union[str, int]) -> Optional[bool]:
    """Parse a string or int as boolean"""
    if value is None:
        return None

    if value == '1' or value == 1:
        return True
    return False


def parse_datetime(value: str) -> Optional[datetime.datetime]:
    """Parse a string as datetime"""
    if not value:
        return None

    return django_parse_datatime(value)


def parse_filter_string(value: str) -> FilterString:
    return FilterString(value)


def parse_int(value: str, *, safe: bool = True) -> Optional[int]:
    """Parse a string as integer"""
    if not value:
        return None

    try:
        return int(value.strip())
    except ValueError as e:
        if safe:
            return None
        raise e from None


def parse_uuid(value: str) -> Optional[UUID]:
    """Parse a string as UUID"""
    if not value:
        return None

    return UUID(value)
