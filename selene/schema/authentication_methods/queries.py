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

import graphene

from selene.schema.authentication_methods.fields import (
    LDAPAuthenticationSettings,
    RADIUSAuthenticationSettings,
)

from selene.schema.utils import get_gmp, require_authentication, XmlElement


class GetLDAPAuthenticationSettings(graphene.Field):
    """Get the current settings for LDAP based authentication"""

    def __init__(self):
        super().__init__(LDAPAuthenticationSettings, resolver=self.resolve)

    @staticmethod
    @require_authentication
    def resolve(_root, info):
        gmp = get_gmp(info)

        xml: XmlElement = gmp.describe_auth()
        ldap_group = xml.xpath("group[@name='method:ldap_connect']")

        if ldap_group:  # xml.xpath returns an array
            return ldap_group[0]
        return None


class GetRADIUSAuthenticationSettings(graphene.Field):
    """Get the current settings for RADIUS based authentication"""

    def __init__(self):
        super().__init__(RADIUSAuthenticationSettings, resolver=self.resolve)

    @staticmethod
    @require_authentication
    def resolve(_root, info):
        gmp = get_gmp(info)

        xml: XmlElement = gmp.describe_auth()
        radius_group = xml.xpath("group[@name='method:radius_connect']")

        if radius_group:  # xml.xpath returns an array
            return radius_group[0]
        return None
