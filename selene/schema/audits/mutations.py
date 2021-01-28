# -*- coding: utf-8 -*-
# Copyright (C) 2019 Greenbone Networks GmbH
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

from gvm.protocols.latest import (
    HostsOrdering as GvmHostsOrdering,
    get_hosts_ordering_from_string,
)

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


class HostsOrdering(graphene.Enum):
    class Meta:
        enum = GvmHostsOrdering


class CloneAudit(graphene.Mutation):
    """Clones a audit

    Args:
        id (UUID): UUID of audit to clone.

    Returns:
        id (UUID)
    """

    class Arguments:
        audit_id = graphene.UUID(required=True, name='id')

    audit_id = graphene.UUID(name='id')

    @require_authentication
    def mutate(root, info, audit_id):
        gmp = get_gmp(info)
        elem = gmp.clone_audit(str(audit_id))
        return CloneAudit(audit_id=elem.get('id'))


class DeleteAudit(graphene.Mutation):
    """Deletes a audit

    Args:
        id (UUID): UUID of audit to delete.

    Returns:
        ok (Boolean)
    """

    class Arguments:
        audit_id = graphene.UUID(required=True, name='id')

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, audit_id):
        gmp = get_gmp(info)
        gmp.delete_audit(str(audit_id))
        return DeleteAudit(ok=True)


# Explicit classes needed, else we get error
# 'AssertionError: Found different types with the same name in the
#   schema: DeleteByIds, DeleteByIds.'

DeleteByIdsClass = create_delete_by_ids_mutation(
    entity_name='audit', gmp_entity_response='task'
)


class DeleteAuditsByIds(DeleteByIdsClass):
    """Deletes a list of audits

    Args:
        ids (List(UUID)): List of UUIDs of audits to delete.

    Returns:
        ok (Boolean)
    """


DeleteByFilterClass = create_delete_by_filter_mutation(
    entity_name='audit', gmp_entity_response='task'
)


class DeleteAuditsByFilter(DeleteByFilterClass):
    """Deletes a filtered list of audits
    Args:
        filterString (str): Filter string for audit list to delete.
    Returns:
        ok (Boolean)
    """


class CreateContainerAuditInput(graphene.InputObjectType):
    """Input object type for createContainerAudit"""

    name = graphene.String(required=True)
    comment = graphene.String()


class CreateContainerAudit(graphene.Mutation):
    class Arguments:
        input_object = CreateContainerAuditInput(required=True, name="input")

    audit_id = graphene.UUID(name='id')

    @require_authentication
    def mutate(root, info, input_object: CreateContainerAuditInput):
        gmp = get_gmp(info)

        resp = gmp.create_container_audit(
            input_object.name, comment=input_object.comment
        )
        return CreateContainerAudit(audit_id=resp.get('id'))


class CreateAuditInput(graphene.InputObjectType):
    """Input object for createAudit.

    Args:
        name (str): The name of the audit.
        policy_id (UUID): UUID of policy to use by the audit;
            OpenVAS Default scanners only
        target_id (UUID): UUID of target to be scanned
        scanner_id (UUID): UUID of scanner to use
        alert_ids (List(UUID), optional): List of UUIDs for alerts to
            be applied to the audit
        alterable (bool, optional): Whether the audit is alterable.
        apply_overrides (bool, optional): Whether to apply overrides
        auto_delete (str, optional): Whether to automatically delete reports,
            And if yes, "keep", if no, "no"
        auto_delete_data (int, optional): if auto_delete is "keep", how many
            of the latest reports to keep
        comment (str, optional): The comment on the audit.
        hosts_ordering (str, optional): The order hosts are scanned in;
            OpenVAS Default scanners only
        in_assets (bool, optional): Whether to add the audit's results to assets
        max_checks (int, optional): Maximum concurrently executed NVTs per host;
            OpenVAS Default scanners only
        max_hosts (int, optional): Maximum concurrently scanned hosts;
            OpenVAS Default scanners only
        observers (Observers, optional): List of names or ids of users which
            should be allowed to observe this audit
        min_qod (int, optional): Minimum quality of detection
        scanner_type (int, optional): Type of scanner, 1-5
        schedule_id (UUID, optional): UUID of a schedule when the audit
            should be run.
        schedule_periods (int, optional): A limit to the number of times the
            audit will be scheduled, or 0 for no limit.
        source_iface (str, optional): Network Source Interface;
            OpenVAS Default scanners only
    """

    name = graphene.String(required=True, description="Audit name.")
    policy_id = graphene.UUID(
        required=True,
        description=("UUID of policy. " "OpenVAS Default scanners only."),
    )
    target_id = graphene.UUID(required=True, description="UUID of target.")
    scanner_id = graphene.UUID(required=True, description="UUID of scanner.")

    alert_ids = graphene.List(
        graphene.UUID, description="List of UUIDs for alerts."
    )
    alterable = graphene.Boolean(description="Whether the audit is alterable.")
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
    comment = graphene.String(description="Audit comment.")
    hosts_ordering = graphene.String(
        description=(
            "The order hosts are scanned in; " "OpenVAS Default scanners only."
        )
    )
    in_assets = graphene.Boolean(
        description="Whether to add the audit's results to assets."
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
    scanner_type = graphene.Int(
        description="Type of scanner, 1-5."
    )  # will be enum once frontend is implemented
    schedule_id = graphene.UUID(
        description="UUID of a schedule when the audit should be run."
    )
    schedule_periods = graphene.Int(
        description=(
            "A limit to the number of times the "
            "audit will be scheduled, or 0 for no limit."
        )
    )
    source_iface = graphene.String(
        description=(
            "Network Source Interface; " "OpenVAS Default scanners only"
        )
    )


class CreateAudit(graphene.Mutation):
    """Creates a new audit. Call with createAudit.

    Args:
        input (CreateAuditInput): Input object for CreateAudit

    """

    class Arguments:
        input_object = CreateAuditInput(required=True, name='input')

    audit_id = graphene.UUID(name='id')

    @require_authentication
    def mutate(root, info, input_object):

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
        policy_id = (
            str(input_object.policy_id)
            if input_object.policy_id is not None
            else None
        )
        if input_object.hosts_ordering is not None:
            hosts_ordering = get_hosts_ordering_from_string(
                input_object.hosts_ordering
            )
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

        if input_object.scanner_type == 2:
            if input_object.max_checks is not None:
                preferences['max_checks'] = input_object.max_checks
            if input_object.max_hosts is not None:
                preferences['max_hosts'] = input_object.max_hosts
            if input_object.source_iface is not None:
                preferences['source_iface'] = input_object.source_iface
        else:
            hosts_ordering = None

        gmp = get_gmp(info)

        resp = gmp.create_audit(
            name,
            str(policy_id),
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
        return CreateAudit(audit_id=resp.get('id'))


class ModifyAuditInput(graphene.InputObjectType):
    """Input object for modifyAudit.

    Args:
        id (UUID): UUID of audit to modify.
        name (str, optional): The name of the audit.
        policy_id (UUID, optional): UUID of policy to use by the audit;
            OpenVAS Default scanners only
        target_id (UUID, optional): UUID of target to be scanned
        scanner_id (UUID, optional): UUID of scanner to use
        alert_ids (List(UUID), optional): List of UUIDs for alerts to
            be applied to the audit
        alterable (bool, optional): Whether the audit is alterable.
        apply_overrides (bool, optional): Whether to apply overrides
        auto_delete (str, optional): Whether to automatically delete reports,
            And if yes, "keep", if no, "no"
        auto_delete_data (int, optional): if auto_delete is "keep", how many
            of the latest reports to keep
        comment (str, optional): The comment on the audit.
        hosts_ordering (str, optional): The order hosts are scanned in;
            OpenVAS Default scanners only
        in_assets (bool, optional): Whether to add the audit's results to assets
        max_checks (int, optional): Maximum concurrently executed NVTs per host;
            OpenVAS Default scanners only
        max_hosts (int, optional): Maximum concurrently scanned hosts;
            OpenVAS Default scanners only
        observers (Observers, optional): List of names or ids of users which
            should be allowed to observe this audit
        min_qod (int, optional): Minimum quality of detection
        scanner_type (int, optional): Type of scanner, 1-5
        schedule_id (UUID, optional): UUID of a schedule when the audit
            should be run.
        schedule_periods (int, optional): A limit to the number of times the
            audit will be scheduled, or 0 for no limit.
        source_iface (str, optional): Network Source Interface;
            OpenVAS Default scanners only
    """

    audit_id = graphene.UUID(
        required=True, description="UUID of audit to modify.", name='id'
    )
    name = graphene.String(description="Audit name.")
    policy_id = graphene.UUID(
        description=("UUID of policy. " "OpenVAS Default scanners only.")
    )
    target_id = graphene.UUID(description="UUID of target.")
    scanner_id = graphene.UUID(description="UUID of scanner.")

    alert_ids = graphene.List(
        graphene.UUID, description="List of UUIDs for alerts."
    )
    alterable = graphene.Boolean(description="Whether the audit is alterable.")
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
    comment = graphene.String(description="Audit comment.")
    hosts_ordering = graphene.String(
        description=(
            "The order hosts are scanned in; " "OpenVAS Default scanners only."
        )
    )
    in_assets = graphene.Boolean(
        description="Whether to add the audit's results to assets."
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
    scanner_type = graphene.Int(
        description="Type of scanner, 1-5."
    )  # will be enum once frontend is implemented
    schedule_id = graphene.UUID(
        description="UUID of a schedule when the audit should be run."
    )
    schedule_periods = graphene.Int(
        description=(
            "A limit to the number of times the "
            "audit will be scheduled, or 0 for no limit."
        )
    )
    source_iface = graphene.String(
        description=(
            "Network Source Interface; " "OpenVAS Default scanners only"
        )
    )


class ModifyAudit(graphene.Mutation):

    """Modifies an existing audit. Call with modifyAudit.

    Args:
        input (ModifyAuditInput): Input object for ModifyAudit

    Returns:
        ok (Boolean)
    """

    class Arguments:
        input_object = ModifyAuditInput(required=True, name='input')

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, input_object):

        audit_id = str(input_object.audit_id)
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
        policy_id = (
            str(input_object.policy_id)
            if input_object.policy_id is not None
            else None
        )

        if input_object.hosts_ordering is not None:
            hosts_ordering = get_hosts_ordering_from_string(
                input_object.hosts_ordering
            )
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

        if input_object.scanner_type == 2:
            if input_object.max_checks is not None:
                preferences['max_checks'] = input_object.max_checks
            if input_object.max_hosts is not None:
                preferences['max_hosts'] = input_object.max_hosts
            if input_object.source_iface is not None:
                preferences['source_iface'] = input_object.source_iface
        else:
            policy_id = None
            hosts_ordering = None

        gmp = get_gmp(info)

        gmp.modify_audit(
            audit_id,
            name=name,
            policy_id=policy_id,
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

        return ModifyAudit(ok=True)


class StartAudit(graphene.Mutation):
    """Starts a audit

    Args:
        id (UUID): UUID of audit to start.

    Returns:
        report_id (UUID)
    """

    class Arguments:
        audit_id = graphene.UUID(required=True, name='id')

    report_id = graphene.UUID()

    @require_authentication
    def mutate(root, info, audit_id):
        gmp = get_gmp(info)
        resp = gmp.start_audit(str(audit_id))

        report_id = get_text_from_element(resp, 'report_id')
        return StartAudit(report_id)


class StopAudit(graphene.Mutation):
    """Stops a audit

    Args:
        id (UUID): UUID of audit to stop.

    Returns:
       ok (Boolean)
    """

    class Arguments:
        audit_id = graphene.UUID(required=True, name='id')

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, audit_id):
        gmp = get_gmp(info)
        resp = gmp.stop_audit(str(audit_id))
        status = int(resp.get('status'))
        ok = status == 200
        return StopAudit(ok)


class ResumeAudit(graphene.Mutation):
    """Resumes a audit

    Args:
        id (UUID): UUID of audit to resume.

    Returns:
       ok (Boolean)
    """

    class Arguments:
        audit_id = graphene.UUID(required=True, name='id')

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, audit_id):
        gmp = get_gmp(info)
        resp = gmp.resume_audit(str(audit_id))
        status = int(resp.get('status'))

        ok = status == 202
        return ResumeAudit(ok)


# Explicit classes needed, else we get error
# 'AssertionError: Found different types with the same name in the
#   schema: ExportByIds, ExportByIds.'

ExportByIdsClass = create_export_by_ids_mutation(
    entity_name='audit', with_details=True
)


class ExportAuditsByIds(ExportByIdsClass):
    pass


ExportByFilterClass = create_export_by_filter_mutation(
    entity_name='audit', with_details=True
)


class ExportAuditsByFilter(ExportByFilterClass):
    pass
