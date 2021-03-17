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
from selene.schema.resolver import find_resolver
from selene.schema.utils import (
    get_boolean_from_element,
    get_text,
    get_datetime_from_element,
    get_int_from_element,
    get_owner,
    get_text_from_element,
)
from selene.schema.parser import parse_uuid

from selene.schema.nvts.fields import ScanConfigNVT
from selene.schema.tickets.fields import RemediationTicket


class QoD(graphene.ObjectType):
    value = graphene.Int()
    type = graphene.String()

    def resolve_value(root, _info):
        return get_int_from_element(root, 'value')

    def resolve_type(root, _info):
        return get_text_from_element(root, 'type')


class ResultNote(graphene.ObjectType):
    uuid = graphene.UUID(name='id')

    creation_time = graphene.DateTime()
    modification_time = graphene.DateTime()

    active = graphene.Boolean()

    text = graphene.String()

    def resolve_uuid(root, _info):
        return parse_uuid(root.get('id'))

    def resolve_creation_time(root, _info):
        return get_datetime_from_element(root, 'creation_time')

    def resolve_modification_time(root, _info):
        return get_datetime_from_element(root, 'modification_time')

    def resolve_active(root, _info):
        return get_boolean_from_element(root, 'active')

    def resolve_text(root, _info):
        return get_text_from_element(root, 'text')


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
        creation_time (DateTime)
        modification_time (DateTime)
        report_id (UUID)
        host (ResultHost)
        port (str)
        nvt (NVT)
        scan_nvt_version (str)
        thread (str)
        severity (str)
        qod (QOD)
        original_thread (str)
        original_severity (str)

    """

    class Meta:
        default_resolver = find_resolver

    comment = graphene.String()
    description = graphene.String()
    owner = graphene.String()

    creation_time = graphene.DateTime()
    modification_time = graphene.DateTime()

    report_id = graphene.UUID(description="ID of the corresponding report")
    task = graphene.Field(ResultTask)
    host = graphene.Field(ResultHost)
    port = graphene.String()

    nvt = graphene.Field(ScanConfigNVT)

    scan_nvt_version = graphene.String()
    threat = graphene.String()
    severity = SeverityType()

    qod = graphene.Field(QoD)

    original_threat = graphene.String()
    original_severity = SeverityType()

    notes = graphene.List(ResultNote)
    tickets = graphene.List(RemediationTicket)

    user_tags = graphene.Field(EntityUserTags)

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
