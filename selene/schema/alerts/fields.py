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

from gvm.protocols.next import (
    AlertEvent as GvmAlertEvent,
    AlertCondition as GvmAlertCondition,
    AlertMethod as GvmAlertMethod,
)

from selene.schema.base import BaseObjectType
from selene.schema.entity import EntityObjectType


from selene.schema.resolver import text_resolver, find_resolver

from selene.schema.utils import (
    get_text,
    get_boolean_from_element,
    get_int_from_element,
)


class SeverityDirection(graphene.Enum):
    CHANGED = 'changed'
    INCREASED = 'increased'
    DECREASED = 'decreased'


class FeedEvent(graphene.Enum):
    NEW = 'new'
    UPDATED = 'updated'


class SecInfoType(graphene.Enum):
    NVT = 'nvt'
    CVE = 'cve'
    CPE = 'cpe'
    CERT_BUND_ADV = 'cert_bund_adv'
    DFN_CERT_ADV = "dfn_cert_adv"
    OVALDEF = "ovaldef"


class AlertTaskStatus(graphene.Enum):
    """Status changes of a Task"""

    DONE = 'Done'
    NEW = 'New'
    REQUESTED = 'Requested'
    RUNNING = 'Running'
    STOP_REQUESTED = 'Stop Requested'
    STOPPED = 'Stopped'


class DeltaType(graphene.Enum):
    NONE = 'None'
    REPORT = 'Report'
    PREVIOUS = 'Previous'


class AlertEvent(graphene.Enum):
    class Meta:
        enum = GvmAlertEvent


class AlertCondition(graphene.Enum):
    class Meta:
        enum = GvmAlertCondition


class AlertMethod(graphene.Enum):
    class Meta:
        enum = GvmAlertMethod


class AlertTask(BaseObjectType):
    pass


class AlertFilter(BaseObjectType):
    trash = graphene.Int()

    @staticmethod
    def resolve_trash(root, _info):
        return get_int_from_element(root, 'trash')


class PropertyData(graphene.ObjectType):
    class Meta:
        default_resolver = text_resolver

    name = graphene.String()
    value = graphene.String()

    @staticmethod
    def resolve_value(root, _info):
        name = root.find('name')
        return name.tail


class AlertProperty(graphene.ObjectType):
    property_type = graphene.String(name='type')
    data = graphene.List(PropertyData)

    @staticmethod
    def resolve_property_type(root, _info):
        return get_text(root)

    @staticmethod
    def resolve_data(root, _info):
        return root.findall('data')


class Alert(EntityObjectType):
    """Alert entity"""

    class Meta:
        default_resolver = find_resolver

    method = graphene.Field(AlertProperty)
    active = graphene.Boolean()
    tasks = graphene.List(AlertTask)
    condition = graphene.Field(AlertProperty)
    event = graphene.Field(AlertProperty)
    alert_filter = graphene.Field(AlertFilter, name="filter")

    @staticmethod
    def resolve_active(root, _info):
        return get_boolean_from_element(root, 'active')

    @staticmethod
    def resolve_tasks(root, _info):
        tasks = root.find('tasks')
        if len(tasks) == 0:
            return None
        return tasks.findall('task')

    @staticmethod
    def resolve_alert_filter(root, _info):
        return root.find('filter')
