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

import graphene

from selene.schema.entities import (
    create_export_by_filter_mutation,
    create_export_by_ids_mutation,
    create_delete_by_ids_mutation,
    create_delete_by_filter_mutation,
)

from selene.schema.utils import (
    get_gmp,
    require_authentication,
    get_text_from_element,
    to_yes_no,
)


class CloneTask(graphene.Mutation):
    """Clone a task"""

    class Arguments:
        task_id = graphene.UUID(required=True, name='id')

    task_id = graphene.UUID(name='id')

    @staticmethod
    @require_authentication
    def mutate(_root, info, task_id):
        gmp = get_gmp(info)
        elem = gmp.clone_task(str(task_id))
        return CloneTask(task_id=elem.get('id'))


# Explicit classes needed, else we get error
# 'AssertionError: Found different types with the same name in the
#   schema: DeleteByIds, DeleteByIds.'

DeleteByIdsClass = create_delete_by_ids_mutation(entity_name='task')


class DeleteTasksByIds(DeleteByIdsClass):
    """Delete a list of tasks"""


DeleteByFilterClass = create_delete_by_filter_mutation(entity_name='task')


class DeleteTasksByFilter(DeleteByFilterClass):
    """Delete a filtered list of tasks"""


class CreateContainerTaskInput(graphene.InputObjectType):
    """Input ObjectType for create a task container"""

    name = graphene.String(required=True)
    comment = graphene.String()


class CreateContainerTask(graphene.Mutation):
    """Create a new container task"""

    class Arguments:
        input_object = CreateContainerTaskInput(
            required=True,
            name="input",
            description="Input ObjectType for creating a new container task",
        )

    task_id = graphene.UUID(
        name='id', description="UUID of the new task container"
    )

    @staticmethod
    @require_authentication
    def mutate(_root, info, input_object: CreateContainerTaskInput):
        gmp = get_gmp(info)

        resp = gmp.create_container_task(
            input_object.name, comment=input_object.comment
        )
        return CreateContainerTask(task_id=resp.get('id'))


class TaskPreferencesInput(graphene.InputObjectType):
    """Input ObjectType for creating task preferences"""

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
        "calculating the severity when creating assets"
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


class CreateTaskInput(graphene.InputObjectType):
    """Input ObjectType for creating a task"""

    name = graphene.String(required=True, description="Task name")
    scan_config_id = graphene.UUID(
        required=True,
        description=(
            "UUID of the scan config to use for the scanner. "
            "Only for OpenVAS scanners"
        ),
    )
    target_id = graphene.UUID(
        required=True, description="UUID of the target to be used"
    )
    scanner_id = graphene.UUID(
        required=True, description="UUID of the scanner to be used"
    )

    alert_ids = graphene.List(
        graphene.UUID,
        description="List of UUIDs for alerts to be used for the task",
    )
    alterable = graphene.Boolean(
        description="Whether the task should be alterable"
    )
    comment = graphene.String(description="Task comment")
    observers = graphene.List(
        graphene.String,
        description="List of UUIDs for users which should be allowed to "
        "observe the task",
    )
    preferences = graphene.Field(
        TaskPreferencesInput, description="Preferences to set for the task"
    )
    schedule_id = graphene.UUID(
        description="UUID of a schedule when the task should be run"
    )
    schedule_periods = graphene.Int(
        description=(
            "A limit to the number of times the "
            "task will be scheduled, or 0 for no limit"
        )
    )


class CreateTask(graphene.Mutation):
    """Create a new task"""

    class Arguments:
        input_object = CreateTaskInput(
            required=True,
            name='input',
            description="Input ObjectType for creating a new task",
        )

    task_id = graphene.UUID(name='id', description="UUID of the new task")

    @staticmethod
    @require_authentication
    def mutate(_root, info, input_object):

        name = input_object.name
        alterable = input_object.alterable
        schedule_periods = input_object.schedule_periods
        comment = input_object.comment

        if input_object.alert_ids is not None:
            alert_ids = [str(alert_id) for alert_id in input_object.alert_ids]
        else:
            alert_ids = None
        if input_object.observers is not None:
            observers = [str(observer) for observer in input_object.observers]
        else:
            observers = None
        schedule_id = (
            str(input_object.schedule_id)
            if input_object.schedule_id is not None
            else None
        )
        scanner_id = (
            str(input_object.scanner_id)
            if input_object.scanner_id is not None
            else None
        )
        target_id = (
            str(input_object.target_id)
            if input_object.target_id is not None
            else None
        )
        config_id = (
            str(input_object.scan_config_id)
            if input_object.scan_config_id is not None
            else None
        )

        preferences = {}

        input_preferences = input_object.preferences

        if (
            input_preferences
            and input_preferences.create_assets_apply_overrides is not None
        ):
            preferences['assets_apply_overrides'] = to_yes_no(
                input_preferences.create_assets_apply_overrides
            )

        if (
            input_preferences
            and input_preferences.create_assets_min_qod is not None
        ):
            preferences[
                'assets_min_qod'
            ] = input_preferences.create_assets_min_qod

        if (
            input_preferences
            and input_preferences.auto_delete_reports is not None
        ):
            preferences['auto_delete'] = "keep"
            preferences[
                'auto_delete_data'
            ] = input_preferences.auto_delete_reports

        if input_preferences and input_preferences.create_assets is not None:
            preferences['in_assets'] = to_yes_no(
                input_preferences.create_assets
            )

        if (
            input_preferences
            and input_preferences.max_concurrent_nvts is not None
        ):
            preferences['max_checks'] = input_preferences.max_concurrent_nvts

        if (
            input_preferences
            and input_preferences.max_concurrent_hosts is not None
        ):
            preferences['max_hosts'] = input_preferences.max_concurrent_hosts

        gmp = get_gmp(info)

        resp = gmp.create_task(
            name,
            str(config_id),
            str(target_id),
            str(scanner_id),
            alterable=alterable,
            comment=comment,
            alert_ids=alert_ids,
            schedule_id=schedule_id,
            schedule_periods=schedule_periods,
            observers=observers,
            preferences=preferences,
        )
        return CreateTask(task_id=resp.get('id'))


class ModifyTaskInput(graphene.InputObjectType):
    """Input ObjectType for modifying a task"""

    task_id = graphene.UUID(
        required=True, description="UUID of task to modify.", name='id'
    )
    name = graphene.String(description="Task name")
    scan_config_id = graphene.UUID(
        description=(
            "UUID of the scan config to use for the scanner. "
            "Only for OpenVAS scanners"
        ),
    )
    target_id = graphene.UUID(description="UUID of the target to be used")
    scanner_id = graphene.UUID(description="UUID of the scanner to be used")

    alert_ids = graphene.List(
        graphene.UUID,
        description="List of UUIDs for alerts to be used for the task",
    )
    alterable = graphene.Boolean(
        description="Whether the task should be alterable"
    )
    comment = graphene.String(description="Task comment")
    observers = graphene.List(
        graphene.String,
        description="List of UUIDs for users which should be allowed to "
        "observe the task",
    )
    preferences = graphene.Field(
        TaskPreferencesInput, description="Preferences to set for the task"
    )
    schedule_id = graphene.UUID(
        description="UUID of a schedule when the task should be run"
    )
    schedule_periods = graphene.Int(
        description=(
            "A limit to the number of times the "
            "task will be scheduled, or 0 for no limit."
        )
    )


class ModifyTask(graphene.Mutation):
    """Modify an existing task"""

    class Arguments:
        input_object = ModifyTaskInput(
            required=True,
            name='input',
            description="Input ObjectType for modifying an existing task",
        )

    ok = graphene.Boolean(
        description="True on success. Otherwise the response contains an error"
    )

    @staticmethod
    @require_authentication
    def mutate(_root, info, input_object):

        task_id = str(input_object.task_id)
        name = input_object.name
        comment = input_object.comment
        schedule_periods = input_object.schedule_periods
        alterable = input_object.alterable

        if input_object.alert_ids is not None:
            alert_ids = [str(alert_id) for alert_id in input_object.alert_ids]
        else:
            alert_ids = None

        if input_object.observers is not None:
            observers = [str(observer) for observer in input_object.observers]
        else:
            observers = None

        schedule_id = (
            str(input_object.schedule_id)
            if input_object.schedule_id is not None
            else None
        )
        scanner_id = (
            str(input_object.scanner_id)
            if input_object.scanner_id is not None
            else None
        )
        target_id = (
            str(input_object.target_id)
            if input_object.target_id is not None
            else None
        )
        config_id = (
            str(input_object.scan_config_id)
            if input_object.scan_config_id is not None
            else None
        )

        preferences = {}

        input_preferences = input_object.preferences

        if (
            input_preferences
            and input_preferences.create_assets_apply_overrides is not None
        ):
            preferences['assets_apply_overrides'] = to_yes_no(
                input_preferences.create_assets_apply_overrides
            )

        if (
            input_preferences
            and input_preferences.create_assets_min_qod is not None
        ):
            preferences[
                'assets_min_qod'
            ] = input_preferences.create_assets_min_qod

        if (
            input_preferences
            and input_preferences.auto_delete_reports is not None
        ):
            preferences['auto_delete'] = "keep"
            preferences[
                'auto_delete_data'
            ] = input_preferences.auto_delete_reports

        if input_preferences and input_preferences.create_assets is not None:
            preferences['in_assets'] = to_yes_no(
                input_preferences.create_assets
            )

        if (
            input_preferences
            and input_preferences.max_concurrent_nvts is not None
        ):
            preferences['max_checks'] = input_preferences.max_concurrent_nvts

        if (
            input_preferences
            and input_preferences.max_concurrent_hosts is not None
        ):
            preferences['max_hosts'] = input_preferences.max_concurrent_hosts

        gmp = get_gmp(info)

        gmp.modify_task(
            task_id,
            name=name,
            config_id=config_id,
            target_id=target_id,
            scanner_id=scanner_id,
            alterable=alterable,
            schedule_id=schedule_id,
            schedule_periods=schedule_periods,
            comment=comment,
            alert_ids=alert_ids,
            observers=observers,
            preferences=preferences,
        )

        return ModifyTask(ok=True)


class StartTask(graphene.Mutation):
    """Starts a scan for a task"""

    class Arguments:
        task_id = graphene.UUID(
            required=True,
            name='id',
            description="UUID of the task to start a scan for",
        )

    report_id = graphene.UUID(
        description="UUID of the report for the started scan"
    )

    @staticmethod
    @require_authentication
    def mutate(_root, info, task_id):
        gmp = get_gmp(info)
        resp = gmp.start_task(str(task_id))

        report_id = get_text_from_element(resp, 'report_id')
        return StartTask(report_id)


class StopTask(graphene.Mutation):
    """Stop a task"""

    class Arguments:
        task_id = graphene.UUID(
            required=True,
            name='id',
            description="UUID of the task to stop the current task",
        )

    ok = graphene.Boolean(
        description="True on success. Otherwise the response contains an error"
    )

    @staticmethod
    @require_authentication
    def mutate(_root, info, task_id):
        gmp = get_gmp(info)
        resp = gmp.stop_task(str(task_id))
        status = int(resp.get('status'))
        ok = status == 200
        return StopTask(ok)


class ResumeTask(graphene.Mutation):
    """Resume a task"""

    class Arguments:
        task_id = graphene.UUID(
            required=True,
            name='id',
            description="UUID of the task which scan should be resumed",
        )

    ok = graphene.Boolean(
        description="True on success. Otherwise the response contains an error"
    )

    @staticmethod
    @require_authentication
    def mutate(_root, info, task_id):
        gmp = get_gmp(info)
        resp = gmp.resume_task(str(task_id))
        status = int(resp.get('status'))

        ok = status == 202
        return ResumeTask(ok)


# Explicit classes needed, else we get error
# 'AssertionError: Found different types with the same name in the
#   schema: ExportByIds, ExportByIds.'

ExportByIdsClass = create_export_by_ids_mutation(
    entity_name='task', with_details=True
)


class ExportTasksByIds(ExportByIdsClass):
    pass


ExportByFilterClass = create_export_by_filter_mutation(
    entity_name='task', with_details=True
)


class ExportTasksByFilter(ExportByFilterClass):
    pass
