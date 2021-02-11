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

from selene.schema.entity import EntityObjectType
from selene.schema.severity import SeverityType
from selene.schema.utils import (
    get_datetime_from_element,
    get_int_from_element,
    get_text_from_element,
)


class CertBundAdvisoryRevision(graphene.ObjectType):
    date = graphene.DateTime()
    description = graphene.String()
    number = graphene.Int()

    def resolve_date(root, _info):
        return get_datetime_from_element(root, 'Date')

    def resolve_description(root, _info):
        return get_text_from_element(root, 'Description')

    def resolve_number(root, _info):
        return get_int_from_element(root, 'Number')


class CertBundAdvisoryInfo(graphene.ObjectType):
    info_issuer = graphene.String()
    info_url = graphene.String()

    def resolve_info_issuer(root, _info):
        return root.get('Info_Issuer')

    def resolve_info_url(root, _info):
        return root.get('Info_URL')


class CertBundAdvisory(EntityObjectType):
    uuid = graphene.String(name='id')
    update_time = graphene.DateTime()
    max_cvss = SeverityType
    score = SeverityType
    cve_refs = graphene.Int()
    cves = graphene.List(graphene.String)
    categories = graphene.List(graphene.String)
    title = graphene.String()
    description = graphene.String()
    infos = graphene.List(CertBundAdvisoryInfo)
    revisions = graphene.List(CertBundAdvisoryRevision)
    effect = graphene.String()
    remote_attack = graphene.Boolean()
    platform = graphene.String()
    reference_source = graphene.String()
    reference_url = graphene.String()
    reference_id = graphene.String()
    reference_number = graphene.Int()
    risk = graphene.String()
    software = graphene.String()

    def resolve_uuid(root, _info):
        return root.get('id')

    def resolve_update_time(root, _info):
        return get_datetime_from_element(root, 'update_time')

    def resolve_max_cvss(root, _info):
        cert_bund = root.find('cert_bund_adv')
        return get_text_from_element(cert_bund, 'max_cvss')

    def resolve_score(root, _info):
        cert_bund = root.find('cert_bund_adv')
        return get_text_from_element(cert_bund, 'score')

    def resolve_cve_refs(root, _info):
        cert_bund = root.find('cert_bund_adv')
        return get_int_from_element(cert_bund, 'cve_refs')

    def resolve_cves(root, _info):
        adv = root.find('cert_bund_adv').find('raw_data').find('Advisory')
        if adv is not None:
            cves_tag = adv.find('CVEList').findall('CVE')
            cves = []
            for cve in cves_tag:
                cves.append(cve.text)
            return cves
        return None

    def resolve_categories(root, _info):
        adv = root.find('cert_bund_adv').find('raw_data').find('Advisory')
        if adv is not None:
            category_tags = adv.findall('CategoryTree')
            categories = []
            for category in category_tags:
                categories.append(category.text)
            return categories
        return None

    def resolve_description(root, _info):
        return get_text_from_element(root.find('cert_bund_adv'), 'summary')

    def resolve_title(root, _info):
        return get_text_from_element(root.find('cert_bund_adv'), 'title')

    def resolve_infos(root, _info):
        adv = root.find('cert_bund_adv').find('raw_data').find('Advisory')
        if adv is not None:
            elements = adv.find('Description').findall('Element')
            for element in elements:
                infos = element.find('Infos')
                if infos is not None:
                    return infos.findall('Info')
        return None

    def resolve_effect(root, _info):
        adv = root.find('cert_bund_adv').find('raw_data').find('Advisory')
        if adv is not None:
            return get_text_from_element(adv, 'Effect')

    def resolve_remote_attack(root, _info):
        adv = root.find('cert_bund_adv').find('raw_data').find('Advisory')
        if adv is not None:
            if get_text_from_element(adv, 'RemoteAttack') == 'yes':
                return True
        return False

    def resolve_platform(root, _info):
        adv = root.find('cert_bund_adv').find('raw_data').find('Advisory')
        if adv is not None:
            return get_text_from_element(adv, 'Platform')

    def resolve_reference_id(root, _info):
        adv = root.find('cert_bund_adv').find('raw_data').find('Advisory')
        if adv is not None:
            return get_text_from_element(adv, 'Ref_Num')

    def resolve_reference_number(root, _info):
        adv = root.find('cert_bund_adv').find('raw_data').find('Advisory')
        if adv is not None:
            return adv.find('Ref_Num').get('update')

    def resolve_reference_source(root, _info):
        adv = root.find('cert_bund_adv').find('raw_data').find('Advisory')
        if adv is not None:
            return get_text_from_element(adv, 'Reference_Source')

    def resolve_reference_url(root, _info):
        adv = root.find('cert_bund_adv').find('raw_data').find('Advisory')
        if adv is not None:
            return get_text_from_element(adv, 'Reference_URL')

    def resolve_revisions(root, _info):
        adv = root.find('cert_bund_adv').find('raw_data').find('Advisory')
        if adv is not None:
            return adv.find('RevisionHistory').findall('Revision')

    def resolve_risk(root, _info):
        adv = root.find('cert_bund_adv').find('raw_data').find('Advisory')
        if adv is not None:
            return get_text_from_element(adv, 'Risk')

    def resolve_software(root, _info):
        adv = root.find('cert_bund_adv').find('raw_data').find('Advisory')
        if adv is not None:
            return get_text_from_element(adv, 'Software')
