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
from lxml import etree

from selene.schema.severity import SeverityType

from selene.schema.base import BaseObjectType, UUIDObjectTypeMixin
from selene.schema.entity import (
    UserTagsObjectTypeMixin,
    CreationModifactionObjectTypeMixin,
    OwnerObjectTypeMixin,
)
from selene.schema.resolver import find_resolver, text_resolver
from selene.schema.utils import (
    get_text,
    get_int_from_element,
    get_text_from_element,
    get_boolean_from_element,
    get_datetime_from_element,
)
from selene.schema.parser import parse_uuid

from selene.schema.notes.fields import Note
from selene.schema.nvts.fields import ScanConfigNVT
from selene.schema.tickets.fields import RemediationTicket


class OriginResultDetail(graphene.ObjectType):
    """Details about the origin of a referenced result"""

    class Meta:
        default_resolver = text_resolver

    name = graphene.String()
    value = graphene.String()


class OriginResult(UUIDObjectTypeMixin, graphene.ObjectType):
    """Referenced Result that provides the information for the referencing
    result.
    For example a Local Security Check (LSC) NVT could reference a NVT that
    gathered a list of installed packages.
    """

    details = graphene.List(OriginResultDetail)

    def resolve_details(root, _info):
        details = root.find('details')
        if details is None or len(details) == 0:
            return None
        return details.findall('detail')


class ResultNVT(ScanConfigNVT):
    """NVT to which result applies."""

    class Meta:
        # default resolver is not inherited. Must be declared
        default_resolver = text_resolver

    version = graphene.String(description='Version of the NVT used in the scan')

    def resolve_version(root, _info):
        return get_text_from_element(root, 'version')


class ResultCVE(graphene.ObjectType):
    """CVE to which result applies."""

    oid = graphene.String(name='id', description='ID of the CVE')
    severity = graphene.Field(
        SeverityType, description='Severity of the CVE result.'
    )

    def resolve_oid(root, _info):
        return root.get('oid')

    def resolve_severity(root, _info):
        return get_text_from_element(root, 'cvss_base')


class ResultInformation(graphene.Union):
    """NVT or CVE to which the result applies."""

    class Meta:
        types = (ResultNVT, ResultCVE)

    @classmethod
    def resolve_type(cls, instance, info):
        info_type = get_text_from_element(instance, 'type')

        if info_type == 'nvt':
            return ResultNVT
        else:
            return ResultCVE


class ResultType(graphene.Enum):
    CVE = 'CVE'
    NVT = 'NVT'


class QoD(graphene.ObjectType):
    value = graphene.Int(description='The numeric QoD value.')
    qod_type = graphene.String(name="type", description='The QoD type.')

    def resolve_value(root, _info):
        return get_int_from_element(root, 'value')

    def resolve_qod_type(root, _info):
        return get_text_from_element(root, 'type')


class ResultHost(graphene.ObjectType):
    ip = graphene.String(description='The host the result applies to.')
    asset_id = graphene.UUID(
        name="id", description='ID of asset linked to host.'
    )
    hostname = graphene.String(
        description=(
            'If available, the hostname the result was created for, '
            'else the one from host details.'
        )
    )

    def resolve_ip(root, _info):
        return get_text(root)

    def resolve_asset_id(root, _info):
        asset = root.find('asset')
        return parse_uuid(asset.get('asset_id'))

    def resolve_hostname(root, _info):
        return get_text_from_element(root, 'hostname')


class ResultTask(BaseObjectType):
    """ A task referenced by ID and name """


class ResultReport(UUIDObjectTypeMixin, graphene.ObjectType):
    """ A report referenced by ID """


# Override imports Result; importing Override will cause
# circular imports. Also, gsa does not need all fields
class ResultOverride(
    graphene.ObjectType, UUIDObjectTypeMixin, CreationModifactionObjectTypeMixin
):
    active = graphene.Boolean(description='Whether the Override is active')
    severity = graphene.Field(
        SeverityType,
        description='Minimum severity of results the Override applies to',
    )
    new_severity = graphene.Field(
        SeverityType,
        description='Severity level results are changed to by the Override',
    )
    text = graphene.String(description='Text of the Override')
    end_time = graphene.DateTime(
        description='Override end time in case of limit, else empty.'
    )

    def resolve_active(root, _info):
        return get_boolean_from_element(root, 'active')

    def resolve_severity(root, _info):
        return get_text_from_element(root, 'severity')

    def resolve_new_severity(root, _info):
        return get_text_from_element(root, 'new_severity')

    def resolve_text(root, _info):
        return get_text_from_element(root, 'text')

    def resolve_end_time(root, _info):
        return get_datetime_from_element(root, 'end_time')


class Result(  # changed mixin to remove comment mixin
    UserTagsObjectTypeMixin,
    OwnerObjectTypeMixin,
    CreationModifactionObjectTypeMixin,
    BaseObjectType,
):
    """An object type representing a Result entity"""

    class Meta:
        default_resolver = find_resolver

    description = graphene.String(description='Description of the result')

    origin_result = graphene.Field(
        OriginResult,
        description='Referenced result that provided information for creating '
        'this result',
    )

    result_type = graphene.Field(
        ResultType,
        name='type',
        description='Type of result. Currently it can be a NVT or CVE based '
        'result',
    )

    report = graphene.Field(
        ResultReport, description='Report the result belongs to'
    )
    task = graphene.Field(ResultTask, description='Task the result belongs to')
    host = graphene.Field(ResultHost, description='Host the result belongs to')
    location = graphene.String(
        description='The location on the host where the result is detected'
    )

    information = graphene.Field(
        ResultInformation,
        description='Detailed information about the detected result. Currently '
        'it can be a NVT or CVE',
    )

    severity = SeverityType()

    qod = graphene.Field(
        QoD, description='The quality of detection (QoD) of the result'
    )

    original_severity = SeverityType(
        description='Original severity when overridden'
    )

    notes = graphene.List(Note, description='List of notes on the result')
    overrides = graphene.List(
        ResultOverride, description='List of overrides on the result'
    )
    tickets = graphene.List(
        RemediationTicket, description='List of tickets on the result'
    )

    def resolve_description(root, _info):
        return get_text_from_element(root, 'description')

    def resolve_origin_result(root, _info):
        detection = root.find('detection')
        if detection is None or len(detection) == 0:
            return None
        return detection.find('result')

    def resolve_report_id(root, _info):
        report = root.find('report')
        if report is not None:
            return parse_uuid(root.find('report').get('id'))

    def resolve_task(root, _info):
        return root.find('task')

    def resolve_location(root, _info):
        return get_text_from_element(root, 'port')

    def resolve_severity(root, _info):
        return get_text_from_element(root, 'severity')

    def resolve_original_severity(root, _info):
        return get_text_from_element(root, 'original_severity')

    def resolve_notes(root, _info):
        notes = root.find('notes')
        if notes is None or len(notes) == 0:
            return None
        return notes.findall('note')

    def resolve_overrides(root, _info):
        overrides = root.find('overrides')
        if overrides is None or len(overrides) == 0:
            return None
        return overrides.findall('override')

    def resolve_tickets(root, _info):
        tickets = root.find('tickets')
        if tickets is None or len(tickets) == 0:
            return None
        return tickets.findall('ticket')

    def resolve_information(root, _info):
        result_info = root.find('nvt')
        info_type = get_text_from_element(result_info, 'type')

        scan_nvt_version = get_text_from_element(root, 'scan_nvt_version')

        if info_type == 'nvt':
            # append scan_nvt_version as version element
            # to nvt result type for parsing
            version_element = etree.Element('version')
            version_element.text = scan_nvt_version
            result_info.append(version_element)

        return result_info

    def resolve_result_type(root, _info):
        nvt = root.find('nvt')

        if nvt is not None:
            return get_text_from_element(nvt, 'type').upper()
        return None
