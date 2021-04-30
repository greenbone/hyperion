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

import graphene

from selene.schema.utils import (
    get_boolean_from_element,
    get_datetime_from_element,
    get_int_from_element,
    get_text_from_element,
)
from selene.schema.parser import parse_uuid
from selene.schema.entity import EntityObjectType


class TLSSourceLocation(graphene.ObjectType):
    uuid = graphene.UUID(name='id')
    host_ip = graphene.String()
    host_id = graphene.UUID()
    port = graphene.Int()

    @staticmethod
    def resolve_uuid(root, _info):
        return parse_uuid(root.get('id'))

    @staticmethod
    def resolve_host_ip(root, _info):
        host = root.find('host')
        return get_text_from_element(host, 'ip')

    @staticmethod
    def resolve_host_id(root, _info):
        host = root.find('host')
        return parse_uuid(host.find('asset').get('id'))

    @staticmethod
    def resolve_port(root, _info):
        return get_int_from_element(root, 'port')


class TLSSourceOrigin(graphene.ObjectType):
    uuid = graphene.UUID(name='id')
    origin_type = graphene.String()
    origin_id = graphene.UUID()
    origin_data = graphene.String()

    @staticmethod
    def resolve_uuid(root, _info):
        return parse_uuid(root.get('id'))

    @staticmethod
    def resolve_origin_type(root, _info):
        return get_text_from_element(root, 'origin_type')

    @staticmethod
    def resolve_origin_id(root, _info):
        return get_text_from_element(root, 'origin_id')

    @staticmethod
    def resolve_origin_data(root, _info):
        return get_text_from_element(root, 'origin_data')


class TLSSource(graphene.ObjectType):
    uuid = graphene.UUID(name='id')
    timestamp = graphene.DateTime()
    tls_versions = graphene.List(graphene.String)
    location = graphene.Field(TLSSourceLocation)
    origin = graphene.Field(TLSSourceOrigin)

    @staticmethod
    def resolve_uuid(root, _info):
        return parse_uuid(root.get('id'))

    @staticmethod
    def resolve_timestamp(root, _info):
        return get_datetime_from_element(root, 'timestamp')

    @staticmethod
    def resolve_tls_versions(root, _info):
        return get_text_from_element(root, 'tls_versions').split(', ')

    @staticmethod
    def resolve_location(root, _info):
        return root.find('location')

    @staticmethod
    def resolve_origin(root, _info):
        return root.find('origin')


class TLSCertificate(EntityObjectType):
    """TLSCertificate object type."""

    certificate_format = graphene.String()
    certificate = graphene.String()
    sha256_fingerprint = graphene.String()
    md5_fingerprint = graphene.String()
    trust = graphene.Boolean()
    valid = graphene.Boolean()
    time_status = graphene.String()
    activation_time = graphene.DateTime()
    expiration_time = graphene.DateTime()
    subject_dn = graphene.String()
    issuer_dn = graphene.String()
    serial = graphene.String()
    last_seen = graphene.DateTime()
    sources = graphene.List(TLSSource)

    @staticmethod
    def resolve_certificate_format(root, _info):
        return root.find('certificate').get('format')

    @staticmethod
    def resolve_certificate(root, _info):
        return get_text_from_element(root, 'certificate')

    @staticmethod
    def resolve_sha256_fingerprint(root, _info):
        return get_text_from_element(root, 'sha256_fingerprint')

    @staticmethod
    def resolve_md5_fingerprint(root, _info):
        return get_text_from_element(root, 'md5_fingerprint')

    @staticmethod
    def resolve_trust(root, _info):
        return get_boolean_from_element(root, 'trust')

    @staticmethod
    def resolve_valid(root, _info):
        return get_boolean_from_element(root, 'valid')

    @staticmethod
    def resolve_time_status(root, _info):
        return get_text_from_element(root, 'time_status')

    @staticmethod
    def resolve_activation_time(root, _info):
        return get_datetime_from_element(root, 'activation_time')

    @staticmethod
    def resolve_expiration_time(root, _info):
        return get_datetime_from_element(root, 'expiration_time')

    @staticmethod
    def resolve_subject_dn(root, _info):
        return get_text_from_element(root, 'subject_dn')

    @staticmethod
    def resolve_issuer_dn(root, _info):
        return get_text_from_element(root, 'issuer_dn')

    @staticmethod
    def resolve_serial(root, _info):
        return get_text_from_element(root, 'serial')

    @staticmethod
    def resolve_last_seen(root, _info):
        return get_datetime_from_element(root, 'last_seen')

    @staticmethod
    def resolve_sources(root, _info):
        sources = root.find('sources')
        if sources is not None:
            return sources.findall('source')
        return None
