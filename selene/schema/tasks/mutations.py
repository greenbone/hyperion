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

from selene.schema.tasks.fields import HostsOrdering

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
)


class CloneTask(graphene.Mutation):
    """Clones a task

    Args:
        id (UUID): UUID of task to clone.

    Returns:
        id (UUID)
    """

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
    """Deletes a list of tasks

    Args:
        ids (List(UUID)): List of UUIDs of tasks to delete.

    Returns:
        ok (Boolean)
    """


DeleteByFilterClass = create_delete_by_filter_mutation(entity_name='task')


class DeleteTasksByFilter(DeleteByFilterClass):
    """Deletes a filtered list of tasks
    Args:
        filterString (str): Filter string for task list to delete.
    Returns:
        ok (Boolean)
    """


class CreateContainerTaskInput(graphene.InputObjectType):
    """Input object type for createContainerTask"""

    name = graphene.String(required=True)
    comment = graphene.String()


class CreateContainerTask(graphene.Mutation):
    class Arguments:
        input_object = CreateContainerTaskInput(required=True, name="input")

    task_id = graphene.UUID(name='id')

    @staticmethod
    @require_authentication
    def mutate(_root, info, input_object: CreateContainerTaskInput):
        gmp = get_gmp(info)

        resp = gmp.create_container_task(
            input_object.name, comment=input_object.comment
        )
        return CreateContainerTask(task_id=resp.get('id'))


class CreateTaskInput(graphene.InputObjectType):
    """Input object for createTask.

    Args:
        name (str): The name of the task.
        config_id (UUID): UUID of scan config to use by the task;
            OpenVAS Default scanners only
        target_id (UUID): UUID of target to be scanned
        scanner_id (UUID): UUID of scanner to use
        alert_ids (List(UUID), optional): List of UUIDs for alerts to
            be applied to the task
        alterable (bool, optional): Whether the task is alterable.
        apply_overrides (bool, optional): Whether to apply overrides
        auto_delete (str, optional): Whether to automatically delete reports,
            And if yes, "keep", if no, "no"
        auto_delete_data (int, optional): if auto_delete is "keep", how many
            of the latest reports to keep
        comment (str, optional): The comment on the task.
        hosts_ordering (str, optional): The order hosts are scanned in;
            OpenVAS Default scanners only
        in_assets (bool, optional): Whether to add the task's results to assets
        max_checks (int, optional): Maximum concurrently executed NVTs per host;
            OpenVAS Default scanners only
        max_hosts (int, optional): Maximum concurrently scanned hosts;
            OpenVAS Default scanners only
        observers (Observers, optional): List of names or ids of users which
            should be allowed to observe this task
        min_qod (int, optional): Minimum quality of detection
        scanner_type (int, optional): Type of scanner, 1-5
        schedule_id (UUID, optional): UUID of a schedule when the task
            should be run.
        schedule_periods (int, optional): A limit to the number of times the
            task will be scheduled, or 0 for no limit.
        source_iface (str, optional): Network Source Interface;
            OpenVAS Default scanners only
    """

    name = graphene.String(required=True, description="Task name.")
    scan_config_id = graphene.UUID(
        required=True,
        description=("UUID of scan config. " "OpenVAS Default scanners only."),
    )
    target_id = graphene.UUID(required=True, description="UUID of target.")
    scanner_id = graphene.UUID(required=True, description="UUID of scanner.")

    alert_ids = graphene.List(
        graphene.UUID, description="List of UUIDs for alerts."
    )
    alterable = graphene.Boolean(description="Whether the task is alterable.")
    apply_overrides = graphene.Boolean(
        description="Whether to apply overrides."
    )
    auto_delete = graphene.String(
        description=(
            "Whether to automatically delete reports, "
            "if yes, 'keep', if no, 'no'"
        )
    )  # will be enum or bool once frontend is implemented
    auto_delete_data = graphene.Int(
        description=(
            "if auto_delete is 'keep', "
            "how many of the latest reports to keep"
        )
    )
    comment = graphene.String(description="Task comment.")
    hosts_ordering = graphene.Field(
        HostsOrdering,
        description="The order hosts are scanned in. "
        "Only for OpenVAS scanners.",
    )
    in_assets = graphene.Boolean(
        description="Whether to add the task's results to assets."
    )
    max_checks = graphene.Int(
        description=(
            "Maximum concurrently executed NVTs per host; "
            "OpenVAS Default scanners only."
        )
    )
    max_hosts = graphene.Int(
        description=(
            "Maximum concurrently scanned hosts; "
            "OpenVAS Default scanners only."
        )
    )
    min_qod = graphene.Int(description="Minimum quality of detection.")
    observers = graphene.List(graphene.String)
    schedule_id = graphene.UUID(
        description="UUID of a schedule when the task should be run."
    )
    schedule_periods = graphene.Int(
        description=(
            "A limit to the number of times the "
            "task will be scheduled, or 0 for no limit."
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
        if input_object.hosts_ordering is not None:
            hosts_ordering = HostsOrdering.get(input_object.hosts_ordering)
        else:
            hosts_ordering = None

        preferences = {}

        if input_object.apply_overrides is not None:
            preferences['assets_apply_overrides'] = (
                "yes" if input_object.apply_overrides == 1 else "no"
            )
        if input_object.min_qod is not None:
            preferences['assets_min_qod'] = input_object.min_qod
        if input_object.auto_delete is not None:
            preferences['auto_delete'] = input_object.auto_delete
        if input_object.auto_delete_data is not None:
            preferences['auto_delete_data'] = input_object.auto_delete_data
        if input_object.in_assets is not None:
            preferences['in_assets'] = (
                "yes" if input_object.in_assets == 1 else "no"
            )

        if input_object.max_checks is not None:
            preferences['max_checks'] = input_object.max_checks
        if input_object.max_hosts is not None:
            preferences['max_hosts'] = input_object.max_hosts

        gmp = get_gmp(info)

        resp = gmp.create_task(
            name,
            str(config_id),
            str(target_id),
            str(scanner_id),
            alterable=alterable,
            comment=comment,
            alert_ids=alert_ids,
            hosts_ordering=hosts_ordering,
            schedule_id=schedule_id,
            schedule_periods=schedule_periods,
            observers=observers,
            preferences=preferences,
        )
        return CreateTask(task_id=resp.get('id'))


class ModifyTaskInput(graphene.InputObjectType):
    """Input object for modifyTask.

    Args:
        id (UUID): UUID of task to modify.
        name (str, optional): The name of the task.
        config_id (UUID, optional): UUID of scan config to use by the task;
            OpenVAS Default scanners only
        target_id (UUID, optional): UUID of target to be scanned
        scanner_id (UUID, optional): UUID of scanner to use
        alert_ids (List(UUID), optional): List of UUIDs for alerts to
            be applied to the task
        alterable (bool, optional): Whether the task is alterable.
        apply_overrides (bool, optional): Whether to apply overrides
        auto_delete (str, optional): Whether to automatically delete reports,
            And if yes, "keep", if no, "no"
        auto_delete_data (int, optional): if auto_delete is "keep", how many
            of the latest reports to keep
        comment (str, optional): The comment on the task.
        hosts_ordering (str, optional): The order hosts are scanned in;
            OpenVAS Default scanners only
        in_assets (bool, optional): Whether to add the task's results to assets
        max_checks (int, optional): Maximum concurrently executed NVTs per host;
            OpenVAS Default scanners only
        max_hosts (int, optional): Maximum concurrently scanned hosts;
            OpenVAS Default scanners only
        observers (Observers, optional): List of names or ids of users which
            should be allowed to observe this task
        min_qod (int, optional): Minimum quality of detection
        scanner_type (int, optional): Type of scanner, 1-5
        schedule_id (UUID, optional): UUID of a schedule when the task
            should be run.
        schedule_periods (int, optional): A limit to the number of times the
            task will be scheduled, or 0 for no limit.
        source_iface (str, optional): Network Source Interface;
            OpenVAS Default scanners only
    """

    task_id = graphene.UUID(
        required=True, description="UUID of task to modify.", name='id'
    )
    name = graphene.String(description="Task name.")
    scan_config_id = graphene.UUID(
        description=(
            "UUID of the scan config to use for the scanner. "
            "Only for OpenVAS scanners"
        ),
    )
    target_id = graphene.UUID(description="UUID of target.")
    scanner_id = graphene.UUID(description="UUID of scanner.")

    alert_ids = graphene.List(
        graphene.UUID, description="List of UUIDs for alerts."
    )
    alterable = graphene.Boolean(description="Whether the task is alterable.")
    apply_overrides = graphene.Boolean(
        description="Whether to apply overrides."
    )
    auto_delete = graphene.String(
        description=(
            "Whether to automatically delete reports, "
            "if yes, 'keep', if no, 'no'"
        )
    )  # will be enum or bool once frontend is implemented
    auto_delete_data = graphene.Int(
        description=(
            "if auto_delete is 'keep', "
            "how many of the latest reports to keep"
        )
    )
    comment = graphene.String(description="Task comment.")
    hosts_ordering = graphene.Field(
        HostsOrdering,
        description="The order hosts are scanned in. "
        "Only for OpenVAS scanners.",
    )
    in_assets = graphene.Boolean(
        description="Whether to add the task's results to assets."
    )
    max_checks = graphene.Int(
        description=(
            "Maximum concurrently executed NVTs per host; "
            "OpenVAS Default scanners only."
        )
    )
    max_hosts = graphene.Int(
        description=(
            "Maximum concurrently scanned hosts; "
            "OpenVAS Default scanners only."
        )
    )
    min_qod = graphene.Int(description="Minimum quality of detection.")
    observers = graphene.List(graphene.String)
    schedule_id = graphene.UUID(
        description="UUID of a schedule when the task should be run."
    )
    schedule_periods = graphene.Int(
        description=(
            "A limit to the number of times the "
            "task will be scheduled, or 0 for no limit."
        )
    )


class ModifyTask(graphene.Mutation):

    """Modifies an existing task. Call with modifyTask.

    Args:
        input (ModifyTaskInput): Input object for ModifyTask

    Returns:
        ok (Boolean)
    """

    class Arguments:
        input_object = ModifyTaskInput(required=True, name='input')

    ok = graphene.Boolean()

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

        if input_object.hosts_ordering is not None:
            hosts_ordering = HostsOrdering.get(input_object.hosts_ordering)
        else:
            hosts_ordering = None

        preferences = {}

        if input_object.apply_overrides is not None:
            preferences['assets_apply_overrides'] = (
                "yes" if input_object.apply_overrides == 1 else "no"
            )
        if input_object.min_qod is not None:
            preferences['assets_min_qod'] = input_object.min_qod
        if input_object.auto_delete is not None:
            preferences['auto_delete'] = input_object.auto_delete
        if input_object.auto_delete_data is not None:
            preferences['auto_delete_data'] = input_object.auto_delete_data
        if input_object.in_assets is not None:
            preferences['in_assets'] = (
                "yes" if input_object.in_assets == 1 else "no"
            )

        if input_object.max_checks is not None:
            preferences['max_checks'] = input_object.max_checks
        if input_object.max_hosts is not None:
            preferences['max_hosts'] = input_object.max_hosts

        gmp = get_gmp(info)

        gmp.modify_task(
            task_id,
            name=name,
            config_id=config_id,
            target_id=target_id,
            scanner_id=scanner_id,
            alterable=alterable,
            hosts_ordering=hosts_ordering,
            schedule_id=schedule_id,
            schedule_periods=schedule_periods,
            comment=comment,
            alert_ids=alert_ids,
            observers=observers,
            preferences=preferences,
        )

        return ModifyTask(ok=True)


class StartTask(graphene.Mutation):
    """Starts a task

    Args:
        id (UUID): UUID of task to start.

    Returns:
        report_id (UUID)
    """

    class Arguments:
        task_id = graphene.UUID(required=True, name='id')

    report_id = graphene.UUID()

    @staticmethod
    @require_authentication
    def mutate(_root, info, task_id):
        gmp = get_gmp(info)
        resp = gmp.start_task(str(task_id))

        report_id = get_text_from_element(resp, 'report_id')
        return StartTask(report_id)


class StopTask(graphene.Mutation):
    """Stops a task

    Args:
        id (UUID): UUID of task to stop.

    Returns:
       ok (Boolean)
    """

    class Arguments:
        task_id = graphene.UUID(required=True, name='id')

    ok = graphene.Boolean()

    @staticmethod
    @require_authentication
    def mutate(_root, info, task_id):
        gmp = get_gmp(info)
        resp = gmp.stop_task(str(task_id))
        status = int(resp.get('status'))
        ok = status == 200
        return StopTask(ok)


class ResumeTask(graphene.Mutation):
    """Resumes a task

    Args:
        id (UUID): UUID of task to resume.

    Returns:
       ok (Boolean)
    """

    class Arguments:
        task_id = graphene.UUID(required=True, name='id')

    ok = graphene.Boolean()

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
