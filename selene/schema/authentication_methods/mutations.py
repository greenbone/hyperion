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

from selene.schema.utils import get_gmp, require_authentication


def _to_bool(value: bool) -> str:
    return "true" if value else "false"


class ModifyLDAPAuthenticationSettings(graphene.Mutation):
    class Arguments:
        auth_dn = graphene.String(
            description='DN used for authentication', required=True
        )
        certificate = graphene.String(description='Content of a .cert file')
        enable = graphene.Boolean(
            description='True to enable the LDAP authentication', required=True
        )
        host = graphene.String(
            description='Hostname or IP of the LDAP server', required=True
        )

    ok = graphene.Boolean()

    @staticmethod
    @require_authentication
    def mutate(
        _root, info, auth_dn: str, certificate: str, enable: bool, host: str
    ):
        gmp = get_gmp(info)

        settings = {
            'enable': _to_bool(enable),
            'authdn': auth_dn,
            'ldaphost': host,
        }

        if certificate:
            settings['cacert'] = certificate

        gmp.modify_auth("method:ldap_connect", settings)

        return ModifyLDAPAuthenticationSettings(ok=True)


class ModifyRADIUSAuthenticationSettings(graphene.Mutation):
    class Arguments:
        enable = graphene.Boolean(
            description='True to enable the RADIUS authentication',
            required=True,
        )
        host = graphene.String(
            description='Hostname or IP of the RADIUS server', required=True
        )
        secret_key = graphene.String(
            required=True,
            description="Secret key used for connecting to the RADIUS server",
        )

    ok = graphene.Boolean()

    @staticmethod
    @require_authentication
    def mutate(_root, info, enable: bool, host: str, secret_key: str):
        gmp = get_gmp(info)

        settings = {
            'enable': _to_bool(enable),
            'radiushost': host,
            'radiuskey': secret_key,
        }

        gmp.modify_auth("method:radius_connect", settings)

        return ModifyLDAPAuthenticationSettings(ok=True)
