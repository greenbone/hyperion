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

from selene.schema.entity import EntityObjectType
from selene.schema.severity import SeverityType
from selene.schema.utils import get_datetime_from_element, get_text_from_element


class CVSSv2Vector(graphene.ObjectType):
    access_vector = graphene.String()
    access_complexity = graphene.String()
    authentication = graphene.String()
    confidentiality = graphene.String()
    integrity = graphene.String()
    availability = graphene.String()
    base_score = graphene.Field(SeverityType)
    vector = graphene.String()

    @staticmethod
    def resolve_access_vector(root, _info):
        return get_text_from_element(root, '{*}access-vector')

    @staticmethod
    def resolve_access_complexity(root, _info):
        return get_text_from_element(root, '{*}access-complexity')

    @staticmethod
    def resolve_authentication(root, _info):
        return get_text_from_element(root, '{*}authentication')

    @staticmethod
    def resolve_confidentiality(root, _info):
        return get_text_from_element(root, '{*}confidentiality-impact')

    @staticmethod
    def resolve_integrity(root, _info):
        return get_text_from_element(root, '{*}integrity-impact')

    @staticmethod
    def resolve_availability(root, _info):
        return get_text_from_element(root, '{*}availability-impact')

    @staticmethod
    def resolve_base_score(root, _info):
        return get_text_from_element(root, '{*}score')

    @staticmethod
    def resolve_vector(root, _info):
        return get_text_from_element(root, '{*}vector-string')


class CVSSv3Vector(graphene.ObjectType):
    attack_vector = graphene.String()
    attack_complexity = graphene.String()
    privileges_required = graphene.String()
    user_interaction = graphene.String()
    scope = graphene.String()
    confidentiality = graphene.String()
    integrity = graphene.String()
    availability = graphene.String()
    base_score = graphene.Field(SeverityType)
    vector = graphene.String()

    @staticmethod
    def resolve_attack_vector(root, _info):
        return get_text_from_element(root, '{*}attack-vector')

    @staticmethod
    def resolve_attack_complexity(root, _info):
        return get_text_from_element(root, '{*}attack-complexity')

    @staticmethod
    def resolve_privileges_required(root, _info):
        return get_text_from_element(root, '{*}privileges-required')

    @staticmethod
    def resolve_user_interaction(root, _info):
        return get_text_from_element(root, '{*}user-interaction')

    @staticmethod
    def resolve_scope(root, _info):
        return get_text_from_element(root, '{*}scope')

    @staticmethod
    def resolve_confidentiality(root, _info):
        return get_text_from_element(root, '{*}confidentiality-impact')

    @staticmethod
    def resolve_integrity(root, _info):
        return get_text_from_element(root, '{*}integrity-impact')

    @staticmethod
    def resolve_availability(root, _info):
        return get_text_from_element(root, '{*}availability-impact')

    @staticmethod
    def resolve_base_score(root, _info):
        return get_text_from_element(root, '{*}base-score')

    @staticmethod
    def resolve_vector(root, _info):
        return get_text_from_element(root, '{*}vector-string')


class NvtRef(graphene.ObjectType):
    oid = graphene.String(name='id', description='NVT reference oid')
    name = graphene.String(description='NVT reference oid')

    @staticmethod
    def resolve_oid(root, _info):
        return root.get('oid')

    @staticmethod
    def resolve_name(root, _info):
        return get_text_from_element(root, 'name')


class CertRef(graphene.ObjectType):
    name = graphene.String(description='Cert reference Name')
    title = graphene.String(description='Cert reference title')
    cert_type = graphene.String(name='type', description='Cert reference type')

    @staticmethod
    def resolve_name(root, _info):
        return get_text_from_element(root, 'name')

    @staticmethod
    def resolve_title(root, _info):
        return get_text_from_element(root, 'title')

    @staticmethod
    def resolve_cert_type(root, _info):
        return root.get('type')


class Refs(graphene.ObjectType):
    source = graphene.String()
    link = graphene.String()
    reference = graphene.String()

    @staticmethod
    def resolve_source(root, _info):
        return get_text_from_element(root, '{*}source')

    @staticmethod
    def resolve_link(root, _info):
        ref = root.find('{*}reference')
        if ref is not None:
            return ref.get('href')
        return None

    @staticmethod
    def resolve_reference(root, _info):
        return get_text_from_element(root, '{*}reference')


class CVE(EntityObjectType):
    uuid = graphene.String(name='id')
    update_time = graphene.DateTime()
    score = graphene.Field(SeverityType)
    cvss_vector = graphene.String()
    cvss_v2_vector = graphene.Field(CVSSv2Vector)
    cvss_v3_vector = graphene.Field(CVSSv3Vector)
    description = graphene.String()
    products = graphene.List(graphene.String)
    refs = graphene.List(Refs)
    nvt_refs = graphene.List(NvtRef)
    cert_refs = graphene.List(CertRef)

    @staticmethod
    def resolve_uuid(root, _info):
        return root.get('id')

    @staticmethod
    def resolve_update_time(root, _info):
        return get_datetime_from_element(root, 'update_time')

    @staticmethod
    def resolve_cvss_vector(root, _info):
        cve = root.find('cve')
        if cve is not None:
            return get_text_from_element(cve, 'cvss_vector')
        return None

    @staticmethod
    def resolve_cvss_v2_vector(root, _info):
        entry = root.find('cve/raw_data/{*}entry')
        if entry is not None:
            return entry.find('{*}cvss/{*}base_metrics')
        return None

    @staticmethod
    def resolve_cvss_v3_vector(root, _info):
        entry = root.find('cve/raw_data/{*}entry')
        if entry is not None:
            return entry.find('{*}cvss3/{*}base_metrics')
        return None

    @staticmethod
    def resolve_score(root, _info):
        cve = root.find('cve')
        if cve is not None:
            return get_text_from_element(cve, 'score')
        return None

    @staticmethod
    def resolve_description(root, _info):
        return get_text_from_element(root.find('cve'), 'description')

    @staticmethod
    def resolve_products(root, _info):
        cve = root.find('cve')
        if cve is not None:
            products = get_text_from_element(cve, 'products')
            if products is not None:
                return products.rstrip().split(' ')
        return None

    @staticmethod
    def resolve_nvt_refs(root, _info):
        nvts = root.find('cve/nvts')
        if nvts is not None:
            return nvts.findall('nvt')
        return None

    @staticmethod
    def resolve_cert_refs(root, _info):
        cert = root.find('cve/cert')
        if cert is not None:
            return cert.findall('cert_ref')
        return None

    @staticmethod
    def resolve_refs(root, _info):
        entry = root.find('cve/raw_data/{*}entry')
        if entry is not None:
            refs = entry.findall('{*}references')
            if len(refs) > 0:
                return refs
        return None
