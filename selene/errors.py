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

from enum import Enum, auto


class AutoName(Enum):
    """Enum class to use the enum name as value automatically

    https://docs.python.org/3/library/enum.html#using-automatic-values
    """

    @staticmethod
    def _generate_next_value_(name, _start, _count, _last_values):
        return name


class ErrorCode(AutoName):
    UNKNOWN = auto()
    AUTHENTICATION_REQUIRED = auto()
    AUTHENTICATION_FAILED = auto()
    INVALID_REQUEST = auto()

    def __str__(self):
        if isinstance(self.value, str):
            return self.value
        return str(self.value)


class SeleneError(Exception):
    errorCode = ErrorCode.UNKNOWN
    httpStatusCode = 200


class AuthenticationRequired(SeleneError):
    errorCode = ErrorCode.AUTHENTICATION_REQUIRED
    httpStatusCode = 401


class AuthenticationFailed(SeleneError):
    errorCode = ErrorCode.AUTHENTICATION_FAILED


class InvalidRequest(SeleneError):
    errorCode = ErrorCode.INVALID_REQUEST
