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

from typing import Dict

import graphene

from selene.schema.resolver import find_resolver, text_resolver

from selene.schema.parser import parse_int, parse_yes_no
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
from selene.schema.scan_configs.fields import ScanConfigType


class TaskReportsCounts(graphene.ObjectType):
    """Report counts for tasks"""

    total = graphene.Int(description="Total count of reports for the task")
    finished = graphene.Int(
        description="Number of finished reports for the task"
    )

    @staticmethod
    def resolve_finished(parent, _info):
        return get_text_from_element(parent, 'finished')

    @staticmethod
    def resolve_total(parent, _info):
        return get_text(parent)


class LastReport(graphene.ObjectType):
    """The last report of a task for a finished scan"""

    uuid = graphene.String(name='id', description="UUID of the last report")
    severity = graphene.Field(
        SeverityType, description="Maximum severity of the last report"
    )
    scan_start = graphene.DateTime(description="Start time of the scan")
    scan_end = graphene.DateTime(description="End time of the scan")
    creation_time = graphene.DateTime(
        description="Date and time when the report has ben created"
    )

    @staticmethod
    def resolve_uuid(parent, _info):
        report = parent.find('report')
        uuid = report.get('id')
        return uuid

    @staticmethod
    def resolve_severity(parent, _info):
        report = parent.find('report')
        severity = report.find('severity')
        return get_text(severity)

    @staticmethod
    def resolve_creation_time(parent, _info):
        report = parent.find('report')
        return get_datetime_from_element(report, 'timestamp')

    @staticmethod
    def resolve_scan_start(parent, _info):
        report = parent.find('report')
        return get_datetime_from_element(report, 'scan_start')

    @staticmethod
    def resolve_scan_end(parent, _info):
        report = parent.find('report')
        return get_datetime_from_element(report, 'scan_end')


class CurrentReport(graphene.ObjectType):
    """The current report of a task is only available during a running scan"""

    uuid = graphene.String(name='id', description="UUID of the current report")
    scan_start = graphene.DateTime(description="Start time of the scan")
    scan_end = graphene.DateTime(description="End time of the scan")
    creation_time = graphene.DateTime(
        description="Date and time when the report has ben created"
    )

    @staticmethod
    def resolve_uuid(parent, _info):
        report = parent.find('report')
        return report.get('id')

    @staticmethod
    def resolve_scan_start(parent, _info):
        report = parent.find('report')
        return get_datetime_from_element(report, 'scan_start')

    @staticmethod
    def resolve_scan_end(parent, _info):
        report = parent.find('report')
        return get_datetime_from_element(report, 'scan_end')

    @staticmethod
    def resolve_creation_time(parent, _info):
        report = parent.find('report')
        return get_datetime_from_element(report, 'timestamp')


class TaskReports(graphene.ObjectType):
    """Report information of a task"""

    counts = graphene.Field(
        TaskReportsCounts,
        description="Counts information for reports of the task",
    )
    current_report = graphene.Field(
        CurrentReport,
        description='Report of the current running scan for this task',
    )
    last_report = graphene.Field(
        LastReport, description='Last finished report of the task'
    )

    class Meta:
        default_resolver = find_resolver

    @staticmethod
    def resolve_counts(root, _info):
        return get_subelement(root, 'report_count')


class TaskSubObjectType(BaseObjectType):

    trash = graphene.Boolean(
        description="Whether the object is in the trashcan"
    )

    @staticmethod
    def resolve_trash(root, _info):
        return get_boolean_from_element(root, 'trash')


class TaskScanConfig(TaskSubObjectType):
    """A scan config for a task"""

    scan_config_type = graphene.Field(
        ScanConfigType, name="type", description="Type of the scan config"
    )

    @staticmethod
    def resolve_scan_config_type(parent, _info):
        return ScanConfigType.get(get_text_from_element(parent, 'type'))


class TaskScanner(TaskSubObjectType):
    """A scanner for a task"""

    scanner_type = graphene.Field(
        ScannerType, name="type", description="Type of the scanner"
    )

    @staticmethod
    def resolve_scanner_type(root, _info):
        return get_text_from_element(root, 'type')


class Observers(graphene.ObjectType):
    """Observers of a task"""

    users = graphene.List(graphene.String, description="List of usernames")
    groups = graphene.List(
        BaseObjectType, description="List of UUIDs of groups"
    )
    roles = graphene.List(BaseObjectType, description="List of UUIDS of roles")

    @staticmethod
    def resolve_users(root, _info):
        user_string = get_text(root)
        if not user_string:
            return None
        return user_string.split(' ')

    @staticmethod
    def resolve_groups(root, _info):
        return root.findall('group')

    @staticmethod
    def resolve_roles(root, _info):
        return root.findall('role')


class TaskSchedule(TaskSubObjectType):
    """A schedule for a task"""

    class Meta:
        default_resolver = text_resolver

    icalendar = graphene.String(
        description="Calendar information for a task in the iCal format"
    )
    duration = graphene.Int(
        description="Maximum duration of a schedule in seconds. A scheduled "
        "scan will be stopped if the duration is exceeded"
    )
    timezone = graphene.String(description="Timezone of the schedule")

    @staticmethod
    def resolve_duration(root, _info):
        return get_int_from_element(root, 'duration')


class TaskPreferences(graphene.ObjectType):
    """A preference for a task"""

    auto_delete_reports = graphene.Int(
        description=(
            "Number of latest reports to keep. If no value is set no report"
            " is deleted automatically"
        )
    )
    create_assets = graphene.Boolean(
        description="Whether to create assets from scan results"
    )
    create_assets_apply_overrides = graphene.Boolean(
        description="Consider overrides for calculating the severity when "
        "creating assets"
    )

    create_assets_min_qod = graphene.Int(
        description="Minimum quality of detection to consider for "
        "calculating the severity creating assets"
    )
    max_concurrent_nvts = graphene.Int(
        description="Maximum concurrently executed NVTs per host. "
        "Only for OpenVAS scanners"
    )
    max_concurrent_hosts = graphene.Int(
        description=(
            "Maximum concurrently scanned hosts. Only for OpenVAS scanners"
        )
    )

    @staticmethod
    def resolve_auto_delete_reports(root: Dict[str, str], _info) -> int:
        auto_delete = root.get("auto_delete")
        if auto_delete == "keep":
            return parse_int(root.get("auto_delete_data"))
        return None

    @staticmethod
    def resolve_create_assets(root: Dict[str, str], _info) -> bool:
        return parse_yes_no(root.get('in_assets'))

    @staticmethod
    def resolve_create_assets_apply_overrides(
        root: Dict[str, str], _info
    ) -> bool:
        return parse_yes_no(root.get("assets_apply_overrides"))

    @staticmethod
    def resolve_create_assets_min_qod(root: Dict[str, str], _info) -> int:
        return parse_int(root.get("assets_min_qod"))

    @staticmethod
    def resolve_max_concurrent_nvts(root: Dict[str, str], _info) -> int:
        return parse_int(root.get("max_checks"))

    @staticmethod
    def resolve_max_concurrent_hosts(root: Dict[str, str], _info) -> int:
        return parse_int(root.get("max_hosts"))


class BaseCounts(graphene.ObjectType):
    current = graphene.Int()


class TaskResultsCounts(BaseCounts):
    """Result count information of a task"""

    @staticmethod
    def resolve_current(current: int, _info):
        return current


class TaskResults(graphene.ObjectType):
    """Result information of a task"""

    counts = graphene.Field(
        TaskResultsCounts,
        description="Count information for results of the task",
    )

    @staticmethod
    def resolve_counts(result_count: XmlElement, _info):
        current = get_text(result_count)
        return parse_int(current)


class TaskTrend(graphene.Enum):
    """Vulnerability trend of a task"""

    UP = "up"
    DOWN = "down"
    MORE = "more"
    LESS = "less"
    SAME = "same"


class TaskStatus(graphene.Enum):
    """Status of a task"""

    QUEUED = 'Queued'
    RUNNING = 'Running'
    STOP_REQUESTED = 'Stop Requested'
    DELETE_REQUESTED = 'Delete Requested'
    ULTIMATE_DELETE_REQUESTED = 'Ultimate Delete Requested'
    RESUME_REQUESTED = 'Resume Requested'
    REQUESTED = 'Requested'
    STOPPED = 'Stopped'
    NEW = 'New'
    INTERRUPTED = 'Interrupted'
    CONTAINER = 'Container'
    UPLOADING = 'Uploading'
    DONE = 'Done'


class Task(EntityObjectType):
    """Task object type"""

    class Meta:
        default_resolver = find_resolver

    average_duration = graphene.Int(
        description="Average duration of scans for this task in seconds"
    )

    trend = graphene.Field(
        TaskTrend, description="Vulnerability trend of the task"
    )
    status = graphene.Field(
        TaskStatus, description="Status of the last or current scan of the task"
    )

    alterable = graphene.Boolean(description="Whether the task is alterable")

    progress = graphene.Int(description="Progress of the current scan")

    scan_config = graphene.Field(
        TaskScanConfig, description="Used scan config for the task"
    )
    target = graphene.Field(
        TaskSubObjectType, description="Used target of the task"
    )
    scanner = graphene.Field(TaskScanner, description="Used target of the task")
    alerts = graphene.List(
        TaskSubObjectType, description="List of alerts used for the task"
    )

    observers = graphene.Field(Observers, description="Observers of the task")

    schedule = graphene.Field(
        TaskSchedule, description="Used schedule for the task"
    )
    schedule_periods = graphene.Int(
        description="Number of recurrences for the schedule"
    )

    preferences = graphene.Field(
        TaskPreferences, description="Preferences set for the task"
    )
    reports = graphene.Field(
        TaskReports, description="Report information for the task"
    )
    results = graphene.Field(
        TaskResults, description="Result information for the task"
    )

    @staticmethod
    def resolve_average_duration(root, _info):
        return get_int_from_element(root, 'average_duration')

    @staticmethod
    def resolve_trend(root, _info):
        return get_text_from_element(root, 'trend')

    @staticmethod
    def resolve_status(root, _info):
        return get_text_from_element(root, 'status')

    @staticmethod
    def resolve_alterable(root, _info):
        return get_boolean_from_element(root, 'alterable')

    @staticmethod
    def resolve_progress(root, _info):
        return get_int_from_element(root, 'progress')

    @staticmethod
    def resolve_scan_config(root, _info):
        return get_sub_element_if_id_available(root, 'config')

    @staticmethod
    def resolve_target(root, _info):
        return get_sub_element_if_id_available(root, 'target')

    @staticmethod
    def resolve_scanner(root, _info):
        return get_sub_element_if_id_available(root, 'scanner')

    @staticmethod
    def resolve_alerts(root, _info):
        alerts = root.findall('alert')
        if not alerts:
            return None
        return alerts

    @staticmethod
    def resolve_schedule(root, _info):
        return get_sub_element_if_id_available(root, 'schedule')

    @staticmethod
    def resolve_schedule_periods(root, _info):
        return get_int_from_element(root, 'schedule_periods')

    @staticmethod
    def resolve_preferences(root, _info):
        preferences = root.find('preferences')
        if preferences is None:
            return None

        preferences_dict = {}
        for preference in preferences.findall('preference'):
            preferences_dict[
                get_text_from_element(preference, "scanner_name")
            ] = get_text_from_element(preference, "value")

        return preferences_dict

    @staticmethod
    def resolve_results(root, _info):
        return get_subelement(root, 'result_count')

    @staticmethod
    def resolve_reports(root, _info):
        return root
