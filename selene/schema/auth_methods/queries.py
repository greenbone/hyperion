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

import graphene

from selene.schema.utils import (
    get_gmp,
    require_authentication,
    XmlElement,
)

from selene.schema.auth_methods.fields import AuthMethodGroup


class DescribeAuth(graphene.List):
    """Describes authentication methods.

    Example:

        .. code-block::

            query {
                auth {
                    name
                    authConfSettings {
                        key
                        value
                    }
                }
            }

        Response:

        .. code-block::

            {
                "data": {

                }
            }
    """

    def __init__(self):
        super().__init__(
            AuthMethodGroup,
            resolver=self.resolve,
        )

    @staticmethod
    @require_authentication
    def resolve(_root, info):
        gmp = get_gmp(info)

        xml: XmlElement = gmp.describe_auth()
        return xml.findall('group')
