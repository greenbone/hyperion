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

# pylint: disable=no-self-argument, no-member

import graphene

from selene.schema.base import CACertificateMixin

from selene.schema.utils import (
    get_datetime_from_element,
    get_gmp,
    get_text_from_element,
    require_authentication,
    XmlElement,
)


class CaCertificate(CACertificateMixin, graphene.ObjectType):
    certificate = graphene.String(
        description='Base64 encoded data of the CA certificate'
    )
    time_status = graphene.String(
        description=(
            'Whether the certificate is valid, ' 'expired or not active yet.'
        ),
    )

    def resolve_certificate(root: XmlElement, _info):
        return get_text_from_element(root, "value")

    def resolve_time_status(root: XmlElement, _info):
        cert_info = root.find('certificate_info')
        return get_text_from_element(cert_info, 'time_status')

    def resolve_md5_fingerprint(root: XmlElement, _info):
        cert_info = root.find('certificate_info')
        return get_text_from_element(cert_info, 'md5_fingerprint')

    def resolve_issuer(root: XmlElement, _info):
        cert_info = root.find('certificate_info')
        return get_text_from_element(cert_info, 'issuer')

    def resolve_activation_time(root: XmlElement, _info):
        cert_info = root.find('certificate_info')
        return get_datetime_from_element(cert_info, 'activation_time')

    def resolve_expiration_time(root: XmlElement, _info):
        cert_info = root.find('certificate_info')
        return get_datetime_from_element(cert_info, 'expiration_time')


class LDAPAuthenticationSettings(graphene.ObjectType):
    # pylint: disable=not-an-iterable

    auth_dn = graphene.String()
    ca_certificate = graphene.Field(
        CaCertificate,
        description="CA certificate used to connect to the LDAP server",
    )
    host = graphene.String(
        description="Hostname or IP address of the LDAP server"
    )
    enable = graphene.Boolean(
        description="True if the LDAP authentication is in use"
    )

    def resolve_auth_dn(group: XmlElement, _info):
        for setting in group:
            key = setting.find('key').text
            if key == 'authdn':
                return setting.find('value').text
        return None

    def resolve_enable(group: XmlElement, _info):
        for setting in group:
            key = setting.find('key').text
            if key == 'enable':
                return setting.find('value').text == 'true'
        return None

    def resolve_host(group: XmlElement, _info):
        for setting in group:
            key = setting.find('key').text
            if key == 'ldaphost':
                return setting.find('value').text
        return None

    def resolve_ca_certificate(group: XmlElement, _info):
        for setting in group:
            key = setting.find('key').text
            if key == 'cacert':
                return setting
        return None


class GetLDAPAuthenticationSettings(graphene.Field):
    def __init__(self):
        super().__init__(
            LDAPAuthenticationSettings,
            resolver=self.resolve,
        )

    @staticmethod
    @require_authentication
    def resolve(_root, info):
        gmp = get_gmp(info)

        xml: XmlElement = gmp.describe_auth()
        ldap_group = xml.xpath("group[@name='method:ldap_connect']")

        if ldap_group:  # xml.xpath returns an array
            return ldap_group[0]
        return None


class RADIUSAuthenticationSettings(graphene.ObjectType):
    # pylint: disable=not-an-iterable

    enable = graphene.Boolean(
        description="True if the RADIUS authentication is in use"
    )
    host = graphene.String(
        description="Hostname or IP address for the RADIUS server"
    )
    secret_key = graphene.String(
        description="Secret key used for connecting to the RADIUS server"
    )

    def resolve_enable(group: XmlElement, _info):
        for setting in group:
            key = setting.find('key').text
            if key == 'enable':
                return setting.find('value').text == 'true'
        return None

    def resolve_host(group: XmlElement, _info):
        for setting in group:
            key = setting.find('key').text
            if key == 'radiushost':
                return setting.find('value').text
        return None

    def resolve_secret_key(group: XmlElement, _info):
        for setting in group:
            key = setting.find('key').text
            if key == 'radiuskey':
                return setting.find('value').text
        return None


class GetRADIUSAuthenticationSettings(graphene.Field):
    def __init__(self):
        super().__init__(
            RADIUSAuthenticationSettings,
            resolver=self.resolve,
        )

    @staticmethod
    @require_authentication
    def resolve(_root, info):
        gmp = get_gmp(info)

        xml: XmlElement = gmp.describe_auth()
        radius_group = xml.xpath("group[@name='method:radius_connect']")

        if radius_group:  # xml.xpath returns an array
            return radius_group[0]
        return None
