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

# pylint: disable=no-self-argument, no-member

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

    def resolve_uuid(root, _info):
        return parse_uuid(root.get('id'))

    def resolve_host_ip(root, _info):
        host = root.find('host')
        return get_text_from_element(host, 'ip')

    def resolve_host_id(root, _info):
        host = root.find('host')
        return parse_uuid(host.find('asset').get('id'))

    def resolve_port(root, _info):
        return get_int_from_element(root, 'port')


class TLSSourceOrigin(graphene.ObjectType):
    uuid = graphene.UUID(name='id')
    origin_type = graphene.String()
    origin_id = graphene.UUID()
    origin_data = graphene.String()

    def resolve_uuid(root, _info):
        return parse_uuid(root.get('id'))

    def resolve_origin_type(root, _info):
        return get_text_from_element(root, 'origin_type')

    def resolve_origin_id(root, _info):
        return get_text_from_element(root, 'origin_id')

    def resolve_origin_data(root, _info):
        return get_text_from_element(root, 'origin_data')


class TLSSource(graphene.ObjectType):
    uuid = graphene.UUID(name='id')
    timestamp = graphene.DateTime()
    tls_versions = graphene.List(graphene.String)
    location = graphene.Field(TLSSourceLocation)
    origin = graphene.Field(TLSSourceOrigin)

    def resolve_uuid(root, _info):
        return parse_uuid(root.get('id'))

    def resolve_timestamp(root, _info):
        return get_datetime_from_element(root, 'timestamp')

    def resolve_tls_versions(root, _info):
        return get_text_from_element(root, 'tls_versions').split(', ')

    def resolve_location(root, _info):
        return root.find('location')

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

    def resolve_certificate_format(root, _info):
        return root.find('certificate').get('format')

    def resolve_certificate(root, _info):
        return get_text_from_element(root, 'certificate')

    def resolve_sha256_fingerprint(root, _info):
        return get_text_from_element(root, 'sha256_fingerprint')

    def resolve_md5_fingerprint(root, _info):
        return get_text_from_element(root, 'md5_fingerprint')

    def resolve_trust(root, _info):
        return get_boolean_from_element(root, 'trust')

    def resolve_valid(root, _info):
        return get_boolean_from_element(root, 'valid')

    def resolve_time_status(root, _info):
        return get_text_from_element(root, 'time_status')

    def resolve_activation_time(root, _info):
        return get_datetime_from_element(root, 'activation_time')

    def resolve_expiration_time(root, _info):
        return get_datetime_from_element(root, 'expiration_time')

    def resolve_subject_dn(root, _info):
        return get_text_from_element(root, 'subject_dn')

    def resolve_issuer_dn(root, _info):
        return get_text_from_element(root, 'issuer_dn')

    def resolve_serial(root, _info):
        return get_text_from_element(root, 'serial')

    def resolve_last_seen(root, _info):
        return get_datetime_from_element(root, 'last_seen')

    def resolve_sources(root, _info):
        sources = root.find('sources')
        if sources is not None:
            return sources.findall('source')
        return None
