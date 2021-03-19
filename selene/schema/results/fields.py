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

from selene.schema.base import BaseObjectType
from selene.schema.entity import EntityUserTags
from selene.schema.resolver import find_resolver, text_resolver
from selene.schema.utils import (
    get_text,
    get_datetime_from_element,
    get_int_from_element,
    get_owner,
    get_text_from_element,
)
from selene.schema.parser import parse_uuid

from selene.schema.notes.fields import Note
from selene.schema.nvts.fields import ScanConfigNVT
from selene.schema.tickets.fields import RemediationTicket


class DetectionResultDetail(graphene.ObjectType):
    class Meta:
        default_resolver = text_resolver

    name = graphene.String()
    value = graphene.String()


class DetectionResult(graphene.ObjectType):
    uuid = graphene.UUID(name='id')

    details = graphene.List(DetectionResultDetail)

    def resolve_uuid(root, _info):
        return parse_uuid(root.get('id'))

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
    pass


class Result(BaseObjectType):
    """Result object type. Is part of the Result object.

    Args:
        name (str): Name of result
        id (UUID): UUID of result
        comment (str): Comment for this result
        description (str): Description of the result
        owner (str): Owner of the result
        creation_time (DateTime): Date and time the result was created
        modification_time (DateTime): Date and time the result was last modified
        detection_result (DetectionResult): Detection result
        report_id (UUID): ID of the corresponding report
        task (ResultTask): Task the result belongs to
        host (ResultHost): Host the result belongs to
        port (str): The port on the host
        nvt (NVT): NVT the result belongs to
        scan_nvt_version (str): Version of the NVT used in scan
        thread (str)
        severity (str)
        qod (QOD): The quality of detection (QoD) of the result
        original_thread (str): Original threat when overriden
        original_severity (str): Original severity when overriden
        notes (List(Note)): List of notes on the result
        tickets (List(RemediationTicket)): List of tickets on the result
        user_tags (List(EntityUserTag)): Tags attached to the result

    """

    class Meta:
        default_resolver = find_resolver

    comment = graphene.String(description='Comment for this result')
    description = graphene.String(description='Description of the result')
    owner = graphene.String(description='Owner of the result')

    creation_time = graphene.DateTime(
        description='Date and time the result was created'
    )
    modification_time = graphene.DateTime(
        description='Date and time the result was last modified'
    )

    detection_result = graphene.Field(
        DetectionResult, description='Detection result'
    )

    report_id = graphene.UUID(description="ID of the corresponding report")
    task = graphene.Field(ResultTask, description='Task the result belongs to')
    host = graphene.Field(ResultHost, description='Host the result belongs to')
    port = graphene.String(description='The port on the host')

    nvt = graphene.Field(ScanConfigNVT, description='NVT the result belongs to')

    scan_nvt_version = graphene.String(
        description='Version of the NVT used in scan'
    )
    threat = graphene.String()
    severity = SeverityType()

    qod = graphene.Field(
        QoD, description='The quality of detection (QoD) of the result'
    )

    original_threat = graphene.String(
        description='Original threat when overriden'
    )
    original_severity = SeverityType(
        description='Original severity when overriden'
    )

    notes = graphene.List(Note, description='List of notes on the result')
    tickets = graphene.List(
        RemediationTicket, description='List of tickets on the result'
    )

    user_tags = graphene.Field(
        EntityUserTags, description='Tags attached to the result'
    )

    def resolve_comment(root, _info):
        return get_text_from_element(root, 'comment')

    def resolve_description(root, _info):
        return get_text_from_element(root, 'description')

    def resolve_owner(root, _info):
        return get_owner(root)

    def resolve_creation_time(root, _info):
        return get_datetime_from_element(root, 'creation_time')

    def resolve_modification_time(root, _info):
        return get_datetime_from_element(root, 'modification_time')

    def resolve_detection_result(root, _info):
        detection = root.find('detection')
        if detection is None or len(detection) == 0:
            return None
        return detection.find('result')

    def resolve_report_id(root, _info):
        return parse_uuid(root.find('report').get('id'))

    def resolve_task(root, _info):
        return root.find('task')

    def resolve_port(root, _info):
        return get_text_from_element(root, 'port')

    def resolve_scan_nvt_version(root, _info):
        return get_text_from_element(root, 'scan_nvt_version')

    def resolve_threat(root, _info):
        return get_text_from_element(root, 'threat')

    def resolve_severity(root, _info):
        return get_text_from_element(root, 'severity')

    def resolve_original_threat(root, _info):
        return get_text_from_element(root, 'original_threat')

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
