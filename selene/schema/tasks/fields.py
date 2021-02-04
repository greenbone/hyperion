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

from selene.schema.resolver import find_resolver, text_resolver

from selene.schema.parser import parse_int
from selene.schema.utils import (
    get_text,
    get_boolean_from_element,
    get_datetime_from_element,
    get_int_from_element,
    get_subelement,
    get_sub_element_if_id_available,
    get_text_from_element,
    XmlElement,
)
from selene.schema.severity import SeverityType
from selene.schema.base import BaseObjectType
from selene.schema.entity import EntityObjectType
from selene.schema.scanners.fields import ScannerType


class TaskReportsCounts(graphene.ObjectType):
    total = graphene.Int(description="Total count of reports for the task")
    finished = graphene.Int(
        description="Number of finished reports for the task"
    )

    def resolve_finished(parent, _info):
        return get_text_from_element(parent, 'finished')

    def resolve_total(parent, _info):
        return get_text(parent)


class LastReport(graphene.ObjectType):
    """ The last report of a task for a finished scan """

    uuid = graphene.String(name='id')
    severity = SeverityType()
    scan_start = graphene.DateTime()
    scan_end = graphene.DateTime()
    timestamp = graphene.DateTime()

    def resolve_uuid(parent, _info):
        report = parent.find('report')
        uuid = report.get('id')
        return uuid

    def resolve_severity(parent, _info):
        report = parent.find('report')
        severity = report.find('severity')
        return get_text(severity)

    def resolve_timestamp(parent, _info):
        report = parent.find('report')
        return get_datetime_from_element(report, 'timestamp')

    def resolve_scan_start(parent, _info):
        report = parent.find('report')
        return get_datetime_from_element(report, 'scan_start')

    def resolve_scan_end(parent, _info):
        report = parent.find('report')
        return get_datetime_from_element(report, 'scan_end')


class CurrentReport(graphene.ObjectType):
    """ The current report of a task is only available during a running scan"""

    uuid = graphene.String(name='id')
    scan_start = graphene.DateTime()
    scan_end = graphene.DateTime()
    timestamp = graphene.DateTime()

    def resolve_uuid(parent, _info):
        report = parent.find('report')
        return report.get('id')

    def resolve_scan_start(parent, _info):
        report = parent.find('report')
        return get_datetime_from_element(report, 'scan_start')

    def resolve_scan_end(parent, _info):
        report = parent.find('report')
        return get_datetime_from_element(report, 'scan_end')

    def resolve_timestamp(parent, _info):
        report = parent.find('report')
        return get_datetime_from_element(report, 'timestamp')


class TaskReports(graphene.ObjectType):
    counts = graphene.Field(TaskReportsCounts)
    current_report = graphene.Field(
        CurrentReport,
        description='Report of the current running scan for this task',
    )
    last_report = graphene.Field(
        LastReport, description='Last finished report of the task'
    )

    class Meta:
        default_resolver = find_resolver

    def resolve_counts(root, _info):
        return get_subelement(root, 'report_count')


class TaskSubObjectType(BaseObjectType):

    trash = graphene.Boolean()

    def resolve_trash(root, _info):
        return get_boolean_from_element(root, 'trash')


class TaskScanConfig(TaskSubObjectType):

    scan_config_type = graphene.Int(
        name="type", description="Type of the scan config"
    )

    def resolve_scan_config_type(parent, _info):
        return get_int_from_element(parent, 'type')


class TaskScanner(TaskSubObjectType):
    scanner_type = graphene.Field(
        ScannerType, name="type", description="Type of the scanner"
    )

    def resolve_scanner_type(root, _info):
        return get_text_from_element(root, 'type')


class Observers(graphene.ObjectType):
    users = graphene.List(graphene.String)
    groups = graphene.List(BaseObjectType)
    roles = graphene.List(BaseObjectType)

    def resolve_users(root, _info):
        user_string = get_text(root)
        if not user_string:
            return None
        return user_string.split(' ')

    def resolve_groups(root, _info):
        return root.findall('group')

    def resolve_roles(root, _info):
        return root.findall('role')


class TaskSchedule(TaskSubObjectType):
    class Meta:
        default_resolver = text_resolver

    icalendar = graphene.String()
    duration = graphene.Int()
    timezone = graphene.String()

    def resolve_duration(root, _info):
        return get_int_from_element(root, 'duration')


class TaskPreference(graphene.ObjectType):
    class Meta:
        default_resolver = text_resolver

    description = graphene.String()
    name = graphene.String()
    value = graphene.String()

    def resolve_name(root, _info):
        return get_text_from_element(root, 'scanner_name')

    def resolve_description(root, _info):
        return get_text_from_element(root, 'name')


class BaseCounts(graphene.ObjectType):
    current = graphene.Int()


class TaskResultsCounts(BaseCounts):
    def resolve_current(current: int, _info):
        return current


class TaskResults(graphene.ObjectType):
    counts = graphene.Field(TaskResultsCounts)

    def resolve_counts(result_count: XmlElement, _info):
        current = get_text(result_count)
        return parse_int(current)


class Task(EntityObjectType):
    """Task object type. Can be used in GetTask and GetTasks queries.

    Please query in camelCase e.g. task_id => taskId.
    """

    class Meta:
        default_resolver = find_resolver

    average_duration = graphene.Int()

    trend = graphene.String()
    status = graphene.String()

    hosts_ordering = graphene.String()

    alterable = graphene.Boolean()

    progress = graphene.Int()

    scan_config = graphene.Field(TaskScanConfig)
    target = graphene.Field(TaskSubObjectType)
    scanner = graphene.Field(TaskScanner)
    alerts = graphene.List(TaskSubObjectType)

    observers = graphene.Field(Observers)

    schedule = graphene.Field(TaskSchedule)
    schedule_periods = graphene.Int()

    preferences = graphene.List(TaskPreference)
    reports = graphene.Field(TaskReports)
    results = graphene.Field(TaskResults)

    def resolve_average_duration(root, _info):
        return get_int_from_element(root, 'average_duration')

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

    def resolve_scan_config(root, _info):
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
