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

from gvm.protocols.latest import TicketStatus as GvmTicketStatus
from selene.schema.resolver import text_resolver

from selene.schema.parser import parse_uuid
from selene.schema.utils import (
    get_boolean_from_element,
    get_datetime_from_element,
)
from selene.schema.entity import EntityObjectType
from selene.schema.severity import SeverityType
from selene.schema.tasks.fields import Task
from selene.schema.users.fields import User


class TicketStatus(graphene.Enum):
    class Meta:
        enum = GvmTicketStatus


class TicketReport(graphene.ObjectType):
    id = graphene.UUID()
    timestamp = graphene.DateTime()

    def resolve_id(root, _info):
        return parse_uuid(root.get('id'))

    def resolve_timestamp(root, _info):
        return get_datetime_from_element(root, 'timestamp')


class RemediationTicket(EntityObjectType):
    """Remediation Ticket object type.
    Can be used in GetTicket and GetTickets queries.

    Please query in camelCase e.g. task_id => taskId.
    """

    class Meta:
        default_resolver = text_resolver

    assigned_to = graphene.Field(User)
    severity = graphene.Field(SeverityType)
    host = graphene.String()
    location = graphene.String()
    solution_type = graphene.String()
    status = graphene.Field(TicketStatus)
    open_time = graphene.DateTime()
    open_note = graphene.String()
    fixed_time = graphene.DateTime()
    fixed_note = graphene.String()
    closed_time = graphene.DateTime()
    closed_note = graphene.String()
    nvt_oid = graphene.String()
    task = graphene.Field(Task)
    report = graphene.Field(TicketReport)
    result = graphene.UUID()
    orphan = graphene.Boolean()

    def resolve_assigned_to(root, _info):
        return root.find('assigned_to').find('user')

    def resolve_open_time(root, _info):
        return get_datetime_from_element(root, 'open_time')

    def resolve_fixed_time(root, _info):
        return get_datetime_from_element(root, 'fixed_time')

    def resolve_closed_time(root, _info):
        return get_datetime_from_element(root, 'closed_time')

    def resolve_nvt_oid(root, _info):
        return root.find('nvt').get('oid')

    def resolve_task(root, _info):
        return root.find("task")

    def resolve_report(root, _info):
        return root.find('report')

    def resolve_result(root, _info):
        return parse_uuid(root.find('result').get('id'))

    def resolve_orphan(root, _info):
        return get_boolean_from_element(root, 'orphan')
