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

from selene.schema.resolver import find_resolver

from selene.schema.utils import (
    get_boolean_from_element,
    get_int_from_element,
    get_subelement,
    get_sub_element_if_id_available,
    get_text_from_element,
)
from selene.schema.entity import EntityObjectType
from selene.schema.tasks.fields import (
    TaskReports,
    TaskSubObjectType,
    TaskScanConfig,
    TaskScanner,
    Observers,
    TaskSchedule,
    TaskPreference,
    TaskResults,
)


class Audit(EntityObjectType):
    """Audit object type. Can be used in GetAudit and GetAudits queries.

    Please query in camelCase e.g. audit_id => auditId.
    """

    class Meta:
        default_resolver = find_resolver

    trend = graphene.String()
    status = graphene.String()

    hosts_ordering = graphene.String()

    alterable = graphene.Boolean()

    progress = graphene.Int()

    policy = graphene.Field(TaskScanConfig)
    target = graphene.Field(TaskSubObjectType)
    scanner = graphene.Field(TaskScanner)
    alerts = graphene.List(TaskSubObjectType)

    observers = graphene.Field(Observers)

    schedule = graphene.Field(TaskSchedule)
    schedule_periods = graphene.Int()

    preferences = graphene.List(TaskPreference)
    reports = graphene.Field(TaskReports)
    results = graphene.Field(TaskResults)

    def resolve_trend(root, _info):
        return get_text_from_element(root, 'trend')

    def resolve_status(root, _info):
        return get_text_from_element(root, 'status')

    def resolve_alterable(root, _info):
        return get_boolean_from_element(root, 'alterable')

    def resolve_hosts_ordering(root, _info):
        return get_text_from_element(root, 'hosts_ordering')

    def resolve_progress(root, _info):
        return get_int_from_element(root, 'progress')

    def resolve_policy(root, _info):
        return get_sub_element_if_id_available(root, 'config')

    def resolve_target(root, _info):
        return get_sub_element_if_id_available(root, 'target')

    def resolve_scanner(root, _info):
        return get_sub_element_if_id_available(root, 'scanner')

    def resolve_alerts(root, _info):
        alerts = root.findall('alert')
        if not alerts:
            return None
        return alerts

    def resolve_schedule(root, _info):
        return get_sub_element_if_id_available(root, 'schedule')

    def resolve_schedule_periods(root, _info):
        return get_int_from_element(root, 'schedule_periods')

    def resolve_preferences(root, _info):
        preferences = root.find('preferences')
        if preferences is None:
            return None
        return preferences.findall('preference')

    def resolve_results(root, _info):
        return get_subelement(root, 'result_count')

    def resolve_reports(root, _info):
        return root
