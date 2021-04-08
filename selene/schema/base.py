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

from selene.schema.parser import parse_uuid
from selene.schema.utils import get_datetime_from_element, get_text_from_element


class NameObjectTypeMixin:
    name = graphene.String(description='Name of the object')

    def resolve_name(root, _info):
        return get_text_from_element(root, 'name')


class UUIDObjectTypeMixin:
    uuid = graphene.UUID(
        name='id', description='Unique identifier of the object'
    )

    def resolve_uuid(root, _info):
        return parse_uuid(root.get('id'))


class BaseObjectType(
    NameObjectTypeMixin, UUIDObjectTypeMixin, graphene.ObjectType
):
    """ A base object type resolving an ID and name """


class CACertificateMixin:

    md5_fingerprint = graphene.String(
        name="md5 fingerprint of the CA certificate"
    )

    issuer = graphene.String(name="Issuer identification of the CA certificate")

    activation_time = graphene.DateTime(
        name="Datetime when the CA certificate is active and considered valid"
    )
    expiration_time = graphene.DateTime(
        name="Datetime when the CA certificate will expire"
    )

    def resolve_md5_fingerprint(root, _into):
        return get_text_from_element(root, 'md5_fingerprint')

    def resolve_issuer(root, _into):
        return get_text_from_element(root, 'issuer')

    def resolve_activation_time(root, _info):
        return get_datetime_from_element(root, 'activation_time')

    def resolve_expiration_time(root, _info):
        return get_datetime_from_element(root, 'expiration_time')
