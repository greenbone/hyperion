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

from selene.schema.severity import SeverityType

from selene.schema.base import BaseObjectType, UUIDObjectTypeMixin
from selene.schema.entity import (
    SimpleEntityObjectType,
    UserTagsObjectTypeMixin,
)
from selene.schema.resolver import find_resolver, text_resolver
from selene.schema.utils import (
    get_text,
    get_int_from_element,
    get_text_from_element,
)
from selene.schema.parser import parse_uuid

from selene.schema.notes.fields import Note
from selene.schema.nvts.fields import ScanConfigNVT
from selene.schema.overrides.fields import Override
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


class QoD(graphene.ObjectType):
    value = graphene.Int()
    type = graphene.String()

    def resolve_value(root, _info):
        return get_int_from_element(root, 'value')

    def resolve_type(root, _info):
        return get_text_from_element(root, 'type')


class ResultHost(graphene.ObjectType):
    ip = graphene.String()
    asset_id = graphene.UUID(name="id")
    hostname = graphene.String()

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


class Result(UserTagsObjectTypeMixin, SimpleEntityObjectType):
    """An object type representing a Result entity"""

    class Meta:
        default_resolver = find_resolver

    description = graphene.String(description='Description of the result')

    origin_result = graphene.Field(
        OriginResult,
        description='Referenced result that provided information for creating '
        'this result',
    )

    report = graphene.Field(
        ResultReport, description='Report the result belongs to'
    )
    task = graphene.Field(ResultTask, description='Task the result belongs to')
    host = graphene.Field(ResultHost, description='Host the result belongs to')
    location = graphene.String(
        description='The location on the host where the result is detected'
    )

    nvt = graphene.Field(ScanConfigNVT, description='NVT the result belongs to')

    scan_nvt_version = graphene.String(
        description='Version of the NVT used in scan'
    )

    qod = graphene.Field(
        QoD, description='The quality of detection (QoD) of the result'
    )

    severity = SeverityType(
        description='Severity with possible applied overrides'
    )
    original_severity = SeverityType(
        description='Original severity when overridden'
    )

    notes = graphene.List(Note, description='List of notes on the result')
    overrides = graphene.List(
        Override, description='List of overrides on the result'
    )
    tickets = graphene.List(
        RemediationTicket, description='List of tickets on the result'
    )

    def resolve_description(root, _info):
        return get_text_from_element(root, 'description')

    def resolve_detection_result(root, _info):
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

    def resolve_scan_nvt_version(root, _info):
        return get_text_from_element(root, 'scan_nvt_version')

    def resolve_severity(root, _info):
        return get_text_from_element(root, 'severity')

    def resolve_original_severity(root, _info):
        return get_text_from_element(root, 'original_severity')

    def resolve_notes(root, _info):
        notes = root.find('notes')
        if notes is None or len(notes) == 0:
            return None
        return notes.findall('note')

    def resolve_tickets(root, _info):
        tickets = root.find('tickets')
        if tickets is None or len(tickets) == 0:
            return None
        return tickets.findall('ticket')
