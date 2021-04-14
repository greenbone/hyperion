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


class QoDType(graphene.Enum):
    """Type of the Quality of Detection

    Describes how a vulnerability has been discovered
    """

    # 100 %
    # The detection happened via an exploit and is therefore fully verified.
    EXPLOIT = 'exploit'

    # 99 %
    # Remote active checks (code execution, traversal attack, SQL injection
    # etc.) in which the response clearly shows the presence of the
    # vulnerability.
    REMOTE_VULNERABILITY = 'remote_vul'

    # 98 %
    # Remote active checks (code execution, traversal attack, SQL injection
    # etc.) in which the response clearly shows the presence of the vulnerable
    # application.
    REMOTE_APP = 'remote_app'

    # 97 %
    # Authenticated package-based checks for Linux(oid) systems.
    PACKAGE = 'package'

    # 97 %
    # Authenticated registry based checks for Windows systems.
    REGISTRY = 'registry'

    # 95 %
    # Remote active checks (code execution, traversal attack, SQL injection
    # etc.) in which the response shows the likely presence of the vulnerable
    # application or of the vulnerability. “Likely” means that only rare
    # circumstances are possible in which the detection would be wrong.
    REMOTE_ACTIVE = 'remote_active'

    # 80 %
    # Remote banner check of applications that offer patch level in version.
    # Many proprietary products do so.
    REMOTE_BANNER = 'remote_banner'

    # 80 %
    # Authenticated executable version checks for Linux(oid) or Windows systems
    # where applications offer patch level in version.
    EXECUTABLE_VERSION = 'executable_version'

    # 70 %
    # Remote checks that do some analysis but which are not always fully
    # reliable.
    REMOTE_ANALYSIS = 'remote_analysis'

    # 50 %
    # Remote checks in which intermediate systems such as firewalls might
    # pretend correct detection so that it is actually not clear whether the
    # application itself answered. For example, this can happen for non-TLS
    # connections.
    REMOTE_PROBE = 'remote_probe'

    # 30 %
    # Remote banner checks of applications that do not offer patch level in
    # version identification. For example, this is the case for many open source
    # products due to backport patches.
    REMOTE_BANNER_UNRELIABLE = 'remote_banner_unreliable'

    # 30 %
    # Authenticated executable version checks for Linux(oid) systems where
    # applications do not offer patch level in version identification.
    EXECUTABLE_VERSION_UNRELIABLE = 'executable_version_unreliable'

    # 1 %
    # General note on potential vulnerability without finding any present
    # application.
    GENERAL_NOTE = 'general_note'


class QoD(graphene.ObjectType):
    value = graphene.Int(description='The numeric QoD value.')
    qod_type = graphene.Field(QoDType, name="type", description='The QoD type.')

    def resolve_value(root, _info):
        return get_int_from_element(root, 'value')

    def resolve_qod_type(root, _info):
        return get_text_from_element(root, 'type')


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


class NvtReference(graphene.ObjectType):
    """Reference of a NVT. """

    reference_id = graphene.String(
        name='id', description='ID of the corrosponding reference'
    )
    reference_type = graphene.String(
        name='type',
        description=(
            'Type of the reference, e.g. "cve", "bid", "dfn-cert", "cert-bund"'
        ),
    )

    def resolve_reference_id(root, _info):
        return root.get('id')

    def resolve_reference_type(root, _info):
        return root.get('type')


class NvtPreferenceNvt(graphene.ObjectType):
    """"NVT to which the NVT preference applies."""

    oid = graphene.String(name='id')
    name = graphene.String()

    def resolve_oid(root, _info):
        return root.get('oid')

    def resolve_name(root, _info):
        return get_text_from_element(root, 'name')


class NvtPreference(graphene.ObjectType):
    """Nvt preference."""

    nvt = graphene.Field(
        NvtPreferenceNvt,
        description='Crossreference to the NVT this preference belongs to',
    )
    hr_name = graphene.String(
        description='Human readable name of the preference'
    )
    name = graphene.String(description='Name of the preference')
    preference_id = graphene.Int(
        name='id', description='ID of this preference [1..]'
    )
    preference_type = graphene.String(
        name='type',
        description=(
            'The value type of the preference. '
            'One of ratio, checkbox, entry, password'
        ),
    )
    value = graphene.String(description='Current value for this preference')
    default = graphene.String(description='default value for this preference')
    alternative_values = graphene.List(
        graphene.String,
        description=(
            'alternative value(s) for this preference '
            '(preference type: ratio)'
        ),
    )

    def resolve_hr_name(root, _info):
        return get_text_from_element(root, 'hr_name')

    def resolve_name(root, _info):
        return get_text_from_element(root, 'name')

    def resolve_preference_type(root, _info):
        return get_text_from_element(root, 'type')

    def resolve_value(root, _info):
        return get_text_from_element(root, 'value')

    def resolve_default(root, _info):
        return get_text_from_element(root, 'default')

    def resolve_preference_id(root, _info):
        return get_int_from_element(root, 'id')

    def resolve_nvt(root, _info):
        return root.find('nvt')

    def resolve_alternative_values(root, _info):
        alts = root.findall('alt')
        if alts is not None and len(alts) > 0:
            return [get_text(alt) for alt in alts]
        return None


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

    cvss_base_vector = graphene.String(
        description='Highest related Cvss Base Vector for this NVT'
    )
    summary = graphene.String(description='Summary/description of the NVT')
    insight = graphene.String(description='Overview of CVEs related to the NVT')
    impact = graphene.String(
        description='Impact of the vulnerability for the host system'
    )
    affected = graphene.String(description='Affected Software and Version(s)')
    vuldetect = graphene.String(
        name='detectionMethod', description='The detection Method of this NVT'
    )


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


class ScanConfigNVT(graphene.ObjectType):
    """Definition of a NVT for a scan config. (API call: get_nvt/get_nvts)"""

    class Meta:
        default_resolver = text_resolver

    oid = graphene.String(name='id')
    name = graphene.String()
    family = graphene.String()
    cvss_base = graphene.Field(SeverityType)
    score = graphene.Int()
    tags = graphene.Field(NvtTags)

    creation_time = graphene.String()
    modification_time = graphene.String()
    category = graphene.Int()
    summary = graphene.String()
    preference_count = graphene.Int()
    timeout = graphene.Int()
    default_timeout = graphene.Int()

    qod = graphene.Field(QoD, description='Quality of detection for this NVT')
    severities = graphene.List(
        NvtSeverity, description='Severities List to related sec infos'
    )
    reference_warning = graphene.String(
        description='Warning if the CERT DB is not available'
    )
    other_references = graphene.List(
        NvtReference, description='Other references List to related sec infos'
    )
    cve_references = graphene.List(
        NvtReference, description='CVE references List to related sec infos'
    )
    bid_references = graphene.List(
        NvtReference, description='Bugtraq references List to related sec infos'
    )
    cert_references = graphene.List(
        NvtReference, description='CERT references List to related sec infos'
    )
    preferences = graphene.List(
        NvtPreference, description='List of preferences for this NVT'
    )
    solution = graphene.Field(
        NvtSolution, description='Fix solution for this NVT'
    )

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

    def resolve_score(root, _info):
        severities = root.find('severities')
        if severities is not None:
            return severities.get('score')

    def resolve_severities(root, _info):
        severities = root.find('severities')
        if severities is not None:
            return severities.findall('severity')

    def resolve_reference_warning(root, _info):
        refs = root.find('refs')
        if refs is not None:
            return get_text_from_element(refs, 'warning')

    def resolve_other_references(root, _info):
        refs = root.find('refs')
        if refs is not None:
            return [
                ref for ref in refs.findall('ref') if ref.get('type') == 'url'
            ]

    def resolve_cert_references(root, _info):
        refs = root.find('refs')
        if refs is not None:
            return [
                ref
                for ref in refs.findall('ref')
                if (
                    ref.get('type') == 'dfn-cert'
                    or ref.get('type') == 'cert-bund'
                )
            ]

    def resolve_bid_references(root, _info):
        refs = root.find('refs')
        if refs is not None:
            return [
                ref
                for ref in refs.findall('ref')
                if (ref.get('type') == 'bid' or ref.get('type') == 'bugtraq_id')
            ]

    def resolve_cve_references(root, _info):
        refs = root.find('refs')
        if refs is not None:
            return [
                ref
                for ref in refs.findall('ref')
                if (ref.get('type') == 'cve' or ref.get('type') == 'cve_id')
            ]

    def resolve_tags(root, _info):
        return root.find('tags')

    def resolve_preferences(root, _info):
        preferences = root.find('preferences')
        if preferences is not None:
            return preferences.findall('preference')

    def resolve_solution(root, _info):
        return root.find('solution')


class NVT(EntityObjectType):
    """Definition of a secinfo NVT (API call: get_info/get_info_list)"""

    uuid = graphene.String(name='id', description='OID of the vulnerability')
    update_time = graphene.DateTime(
        description='Time stamp of the last update of the vulnerability'
    )

    # Not sure if this is needed anymore
    cvss_base = graphene.Field(SeverityType)
    score = graphene.Int(
        description='Describes the severity of this vulnerability'
    )

    family = graphene.String()
    tags = graphene.Field(NvtTags)
    category = graphene.Int()
    preference_count = graphene.Int()
    timeout = graphene.Int()
    default_timeout = graphene.Int()

    qod = graphene.Field(QoD, description='Quality of detection for this NVT')
    severities = graphene.List(
        NvtSeverity, description='Severities List to related sec infos'
    )
    reference_warning = graphene.String(
        description='Warning if the CERT DB is not available'
    )
    other_references = graphene.List(
        NvtReference, description='Other references List to related sec infos'
    )
    cve_references = graphene.List(
        NvtReference, description='CVE references List to related sec infos'
    )
    bid_references = graphene.List(
        NvtReference, description='Bugtraq references List to related sec infos'
    )
    cert_references = graphene.List(
        NvtReference, description='CERT references List to related sec infos'
    )
    preferences = graphene.List(
        NvtPreference, description='List of preferences for this NVT'
    )
    solution = graphene.Field(
        NvtSolution, description='Fix solution for this NVT'
    )

    def resolve_uuid(root, _info):
        return root.get('id')

    def resolve_update_time(root, _info):
        return get_datetime_from_element(root, 'update_time')

    def resolve_family(root, _info):
        nvt = root.find('nvt')
        if nvt is not None:
            return get_text_from_element(nvt, 'family')
        return None

    def resolve_cvss_base(root, _info):
        nvt = root.find('nvt')
        if nvt is not None:
            return get_text_from_element(nvt, 'cvss_base')
        return None

    def resolve_score(root, _info):
        severities = root.find('nvt/severities')
        if severities is not None:
            return severities.get('score')

    def resolve_tags(root, _info):
        nvt = root.find('nvt')
        if nvt is not None:
            return nvt.find('tags')
        return None

    def resolve_category(root, _info):
        nvt = root.find('nvt')
        if nvt is not None:
            return get_int_from_element(nvt, 'category')

    def resolve_preference_count(root, _info):
        nvt = root.find('nvt')
        if nvt is not None:
            return get_int_from_element(nvt, 'preference_count')

    def resolve_timeout(root, _info):
        nvt = root.find('nvt')
        if nvt is not None:
            return get_int_from_element(nvt, 'timeout')

    def resolve_default_timeout(root, _info):
        nvt = root.find('nvt')
        if nvt is not None:
            return get_int_from_element(nvt, 'default_timeout')

    def resolve_qod(root, _info):
        nvt = root.find('nvt')
        if nvt is not None:
            return nvt.find('qod')

    def resolve_severities(root, _info):
        severities = root.find('nvt/severities')
        if severities is not None:
            return severities.findall('severity')

    def resolve_other_references(root, _info):
        refs = root.find('nvt/refs')
        if refs is not None:
            return [
                ref for ref in refs.findall('ref') if ref.get('type') == 'url'
            ]

    def resolve_cert_references(root, _info):
        refs = root.find('nvt/refs')
        if refs is not None:
            return [
                ref
                for ref in refs.findall('ref')
                if (
                    ref.get('type') == 'dfn-cert'
                    or ref.get('type') == 'cert-bund'
                )
            ]

    def resolve_bid_references(root, _info):
        refs = root.find('nvt/refs')
        if refs is not None:
            return [
                ref
                for ref in refs.findall('ref')
                if (ref.get('type') == 'bid' or ref.get('type') == 'bugtraq_id')
            ]

    def resolve_cve_references(root, _info):
        refs = root.find('nvt/refs')
        if refs is not None:
            return [
                ref
                for ref in refs.findall('ref')
                if (ref.get('type') == 'cve' or ref.get('type') == 'cve_id')
            ]

    def resolve_reference_warning(root, _info):
        refs = root.find('nvt/refs')
        if refs is not None:
            return get_text_from_element(refs, 'warning')

    def resolve_preferences(root, _info):
        preferences = root.find('nvt/preferences')
        if preferences is not None:
            return preferences.findall('preference')

    def resolve_solution(root, _info):
        nvt = root.find('nvt')
        if nvt is not None:
            return nvt.find('solution')
