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

from selene.schema.audits.fields import AuditHostsOrdering

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


class CloneAudit(graphene.Mutation):
    """Clone an audit"""

    class Arguments:
        audit_id = graphene.UUID(
            required=True,
            name='id',
            description="UUID of the to be cloned Audit",
        )

    audit_id = graphene.UUID(name='id', description="UUID of the new Audit")

    @staticmethod
    @require_authentication
    def mutate(_root, info, audit_id):
        gmp = get_gmp(info)
        elem = gmp.clone_audit(str(audit_id))
        return CloneAudit(audit_id=elem.get('id'))


# Explicit classes needed, else we get error
# 'AssertionError: Found different types with the same name in the
#   schema: DeleteByIds, DeleteByIds.'

DeleteByIdsClass = create_delete_by_ids_mutation(
    entity_name='audit', gmp_entity_response='task'
)


class DeleteAuditsByIds(DeleteByIdsClass):
    """Delete a list of audits"""


DeleteByFilterClass = create_delete_by_filter_mutation(
    entity_name='audit', gmp_entity_response='task'
)


class DeleteAuditsByFilter(DeleteByFilterClass):
    """Delete a filtered list of audits"""


class CreateAuditInput(graphene.InputObjectType):
    """Input object for creating an audit"""

    name = graphene.String(required=True, description="Audit name")
    policy_id = graphene.UUID(
        required=True,
        description="UUID of the to be used policy. Only for OpenVAS scanners.",
    )
    target_id = graphene.UUID(
        required=True, description="UUID of to be used target"
    )
    scanner_id = graphene.UUID(
        required=True, description="UUID of to be used scanner"
    )

    alert_ids = graphene.List(
        graphene.UUID,
        description="List of UUIDs for alerts to be used in the audit",
    )
    alterable = graphene.Boolean(
        description="Whether the audit should be alterable"
    )
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
    comment = graphene.String(description="Audit comment")
    hosts_ordering = graphene.Field(
        AuditHostsOrdering,
        description="The order hosts are scanned in. "
        "Only for OpenVAS scanners",
    )
    in_assets = graphene.Boolean(
        description="Whether to add the audit's results to assets."
    )
    max_checks = graphene.Int(
        description="Maximum concurrently executed NVTs per host. "
        "Only for OpenVAS scanners."
    )
    max_hosts = graphene.Int(
        description=(
            "Maximum concurrently scanned hosts. Only for OpenVAS scanners"
        )
    )
    min_qod = graphene.Int(description="Minimum quality of detection")
    observers = graphene.List(
        graphene.UUID,
        description="List of UUIDs for users which should be allowed to "
        "observer the audit",
    )
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
        description=("Network Source Interface. Only for OpenVAS scanners")
    )


class CreateAudit(graphene.Mutation):
    """Create a new audit"""

    class Arguments:
        input_object = CreateAuditInput(
            required=True,
            name='input',
            description="Input ObjectType for creating a new audit",
        )

    audit_id = graphene.UUID(name='id', description="UUID of the new audit")

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
        policy_id = (
            str(input_object.policy_id)
            if input_object.policy_id is not None
            else None
        )

        if input_object.hosts_ordering:
            hosts_ordering = AuditHostsOrdering.get(input_object.hosts_ordering)
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
        if input_object.source_iface is not None:
            preferences['source_iface'] = input_object.source_iface

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
    """Input object for modifying an audit"""

    audit_id = graphene.UUID(
        required=True, description="UUID of audit to modify.", name='id'
    )
    name = graphene.String(description="Audit name")
    policy_id = graphene.UUID(
        description=("UUID of policy. OpenVAS Default scanners only")
    )
    target_id = graphene.UUID(description="UUID of target")
    scanner_id = graphene.UUID(description="UUID of scanner")

    alert_ids = graphene.List(
        graphene.UUID, description="List of UUIDs for alerts"
    )
    alterable = graphene.Boolean(description="Whether the audit is alterable")
    apply_overrides = graphene.Boolean(description="Whether to apply overrides")
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
    hosts_ordering = graphene.Field(
        AuditHostsOrdering,
        description="The order hosts are scanned in. "
        "Only for OpenVAS scanners",
    )
    in_assets = graphene.Boolean(
        description="Whether to add the audit's results to assets"
    )
    max_checks = graphene.Int(
        description=(
            "Maximum concurrently executed NVTs per host. "
            "OpenVAS Default scanners only"
        )
    )
    max_hosts = graphene.Int(
        description=(
            "Maximum concurrently scanned hosts. "
            "OpenVAS Default scanners only"
        )
    )
    min_qod = graphene.Int(description="Minimum quality of detection")
    observers = graphene.List(graphene.String)
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

    @staticmethod
    @require_authentication
    def mutate(_root, info, input_object):

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

        if input_object.hosts_ordering:
            hosts_ordering = AuditHostsOrdering.get(input_object.hosts_ordering)
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
        if input_object.source_iface is not None:
            preferences['source_iface'] = input_object.source_iface

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

    @staticmethod
    @require_authentication
    def mutate(_root, info, audit_id):
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

    @staticmethod
    @require_authentication
    def mutate(_root, info, audit_id):
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

    @staticmethod
    @require_authentication
    def mutate(_root, info, audit_id):
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
