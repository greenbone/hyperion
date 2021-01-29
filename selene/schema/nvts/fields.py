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

# pylint: disable=no-self-argument, no-member

import graphene

from selene.schema.utils import (
    get_datetime_from_element,
    get_int_from_element,
    get_text_from_element,
    get_text,
)
from selene.schema.severity import SeverityType

from selene.schema.entity import EntityObjectType

from selene.schema.resolver import text_resolver, nvt_tags_resolver


class NvtSeverity(graphene.ObjectType):
    """Severity info item of an NVT. """

    date = graphene.DateTime()
    origin = graphene.String()
    score = graphene.Int()
    severity_type = graphene.String(name='type')
    vector = graphene.String(
        description='The CVSS Vector resposible for the Score.'
    )

    def resolve_date(root, _info):
        return get_datetime_from_element(root, 'date')

    def resolve_origin(root, _info):
        return get_text_from_element(root, 'origin')

    def resolve_score(root, _info):
        return get_int_from_element(root, 'score')

    def resolve_severity_type(root, _info):
        return root.get('type')

    def resolve_vector(root, _info):
        return get_text_from_element(root, 'value')


class NvtSeverities(graphene.ObjectType):
    """Severities of an NVT. """

    score = graphene.Int()
    severities_list = graphene.List(NvtSeverity)

    def resolve_score(root, _info):
        return root.get('score')

    def resolve_severities_list(root, _info):
        return root.findall('severity')


class NvtDefinitionQod(graphene.ObjectType):
    """QOD of a NVT."""

    value = graphene.Int()
    qod_type = graphene.String(name='type')

    def resolve_value(root, _info):
        return get_int_from_element(root, 'value')

    def resolve_qod_type(root, _info):
        return get_text_from_element(root, 'type')


class NvtDefinitionRef(graphene.ObjectType):
    """Reference of a NVT. """

    ref_id = graphene.String(name='id')
    # Type of the reference, for example "cve", "bid", "dfn-cert", "cert-bund".
    ref_type = graphene.String(name='type')

    def resolve_ref_id(root, _info):
        return root.get('id')

    def resolve_ref_type(root, _info):
        return root.get('type')


class NvtDefinitionRefs(graphene.ObjectType):
    """List of references of various types for a NVT."""

    warning = graphene.String()
    ref_list = graphene.List(NvtDefinitionRef)

    def resolve_warning(root, _info):
        return get_text_from_element(root, 'warning')

    def resolve_ref_list(root, _info):
        return root.findall('ref')


class NvtPreferenceNvt(graphene.ObjectType):
    """"NVT to which the NVT preference applies."""

    oid = graphene.String(name='oid')
    name = graphene.String()

    def resolve_oid(root, _info):
        return root.get('oid')

    def resolve_name(root, _info):
        return get_text_from_element(root, 'name')


class NvtPreference(graphene.ObjectType):
    """Nvt preference."""

    nvt = graphene.Field(NvtPreferenceNvt)
    hr_name = graphene.String()
    name = graphene.String()
    pref_id = graphene.Int(name='id')
    pref_type = graphene.String(name='type')
    value = graphene.String()
    default = graphene.String()
    alt = graphene.List(graphene.String)

    def resolve_hr_name(root, _info):
        return get_text_from_element(root, 'hr_name')

    def resolve_name(root, _info):
        return get_text_from_element(root, 'name')

    def resolve_pref_type(root, _info):
        return get_text_from_element(root, 'type')

    def resolve_value(root, _info):
        return get_text_from_element(root, 'value')

    def resolve_default(root, _info):
        return get_text_from_element(root, 'default')

    def resolve_pref_id(root, _info):
        return get_int_from_element(root, 'id')

    def resolve_nvt(root, _info):
        return root.find('nvt')

    def resolve_alt(root, _info):
        alt_elements = root.findall('alt')
        alts = []
        for alt_elem in alt_elements:
            alts.append(get_text(alt_elem))
        if not alts:
            return None
        return alts


class NvtPreferences(graphene.ObjectType):
    """preferences of a NVT."""

    timeout = graphene.Int()
    default_timeout = graphene.Int()
    preference_list = graphene.List(NvtPreference)

    def resolve_timeout(root, _info):
        return get_int_from_element(root, 'timeout')

    def resolve_default_timeout(root, _info):
        return get_int_from_element(root, 'default_timeout')

    def resolve_preference_list(root, _info):
        return root.findall('preference')


class NvtSolution(graphene.ObjectType):
    """Solution of a NVT."""

    solution_type = graphene.String(name='type')
    solution_method = graphene.String(name='method')
    solution_text = graphene.String(name='description')

    def resolve_solution_type(root, _info):
        return root.get('type')

    def resolve_solution_method(root, _info):
        return root.get('method')

    def resolve_solution_text(root, _info):
        return root.text


class NvtTags(graphene.ObjectType):
    """A NVT Tags field, dissolving the tags element of an NVT"""

    class Meta:
        default_resolver = nvt_tags_resolver

    cvss_base_vector = graphene.String()
    summary = graphene.String()
    insight = graphene.String()
    impact = graphene.String()
    affected = graphene.String()
    vuldetect = graphene.String()


class ScanConfigNVT(graphene.ObjectType):
    """Definition of a NVT for a scan config."""

    class Meta:
        default_resolver = text_resolver

    oid = graphene.String()
    name = graphene.String()
    family = graphene.String()
    cvss_base = graphene.String()
    tags = graphene.Field(NvtTags)

    creation_time = graphene.String()
    modification_time = graphene.String()
    category = graphene.Int()
    summary = graphene.String()
    preference_count = graphene.Int()
    timeout = graphene.Int()
    default_timeout = graphene.Int()

    qod = graphene.Field(NvtDefinitionQod)
    severities = graphene.Field(NvtSeverities)
    refs = graphene.Field(NvtDefinitionRefs)
    preferences = graphene.Field(NvtPreferences)
    solution = graphene.Field(NvtSolution)

    def resolve_oid(root, _info):
        return root.get('oid')

    def resolve_category(root, _info):
        return get_int_from_element(root, 'category')

    def resolve_preference_count(root, _info):
        return get_int_from_element(root, 'preference_count')

    def resolve_timeout(root, _info):
        return get_int_from_element(root, 'timeout')

    def resolve_default_timeout(root, _info):
        return get_int_from_element(root, 'default_timeout')

    def resolve_qod(root, _info):
        return root.find('qod')

    def resolve_severities(root, _info):
        return root.find('severities')

    def resolve_refs(root, _info):
        return root.find('refs')

    def resolve_tags(root, _info):
        return root.find('tags')

    def resolve_preferences(root, _info):
        return root.find('preferences')

    def resolve_solution(root, _info):
        return root.find('solution')


class BaseNvtFamily(graphene.ObjectType):
    """NVT family"""

    name = graphene.String()
    max_nvt_count = graphene.Int()

    def resolve_name(root, _info):
        return get_text_from_element(root, 'name')

    def resolve_max_nvt_count(root, _info):
        return get_int_from_element(root, 'max_nvt_count')


class NvtFamily(BaseNvtFamily):
    pass


class NVT(EntityObjectType):
    """Definition of a secinfo NVT"""

    uuid = graphene.String(name='id')
    update_time = graphene.DateTime()

    qod = graphene.Field(NvtDefinitionQod)
    severities = graphene.Field(NvtSeverities)
    refs = graphene.Field(NvtDefinitionRefs)
    preferences = graphene.Field(NvtPreferences)
    solution = graphene.Field(NvtSolution)
    cvss_base = graphene.Field(SeverityType)

    family = graphene.String()
    tags = graphene.Field(NvtTags)
    category = graphene.Int()
    preference_count = graphene.Int()
    timeout = graphene.Int()
    default_timeout = graphene.Int()

    def resolve_uuid(root, _info):
        return root.get('id')

    def resolve_update_time(root, _info):
        return get_datetime_from_element(root, 'update_time')

    def resolve_family(root, _info):
        nvt = root.find('nvt')
        if nvt:
            return get_text_from_element(nvt, 'family')
        return None

    def resolve_cvss_base(root, _info):
        nvt = root.find('nvt')
        if nvt:
            return get_text_from_element(nvt, 'cvss_base')
        return None

    def resolve_tags(root, _info):
        nvt = root.find('nvt')
        if nvt:
            return nvt.find('tags')
        return None

    def resolve_category(root, _info):
        nvt = root.find('nvt')
        if nvt:
            return get_int_from_element(nvt, 'category')

    def resolve_preference_count(root, _info):
        nvt = root.find('nvt')
        if nvt:
            return get_int_from_element(nvt, 'preference_count')

    def resolve_timeout(root, _info):
        nvt = root.find('nvt')
        if nvt:
            return get_int_from_element(nvt, 'timeout')

    def resolve_default_timeout(root, _info):
        nvt = root.find('nvt')
        if nvt:
            return get_int_from_element(nvt, 'default_timeout')

    def resolve_qod(root, _info):
        nvt = root.find('nvt')
        if nvt:
            return nvt.find('qod')

    def resolve_severities(root, _info):
        nvt = root.find('nvt')
        if nvt:
            return nvt.find('severities')

    def resolve_refs(root, _info):
        nvt = root.find('nvt')
        if nvt:
            return nvt.find('refs')

    def resolve_preferences(root, _info):
        nvt = root.find('nvt')
        if nvt:
            return nvt.find('preferences')

    def resolve_solution(root, _info):
        nvt = root.find('nvt')
        if nvt:
            return nvt.find('solution')
