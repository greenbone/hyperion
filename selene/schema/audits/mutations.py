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


class AuditPreferencesInput(graphene.InputObjectType):
    """Input ObjectType for creating audit preferences"""

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


class CreateAuditInput(graphene.InputObjectType):
    """Input ObjectType for creating an audit"""

    name = graphene.String(required=True, description="Audit name")
    policy_id = graphene.UUID(
        required=True,
        description="UUID of the to be used policy. Only for OpenVAS scanners.",
    )
    target_id = graphene.UUID(
        required=True, description="UUID of the target to be used"
    )
    scanner_id = graphene.UUID(
        required=True, description="UUID of the scanner to be used"
    )

    alert_ids = graphene.List(
        graphene.UUID,
        description="List of UUIDs for alerts to be used for the audit",
    )
    alterable = graphene.Boolean(
        description="Whether the audit should be alterable"
    )
    comment = graphene.String(description="Audit comment")
    observers = graphene.List(
        graphene.UUID,
        description="List of UUIDs for users which should be allowed to "
        "observe the audit",
    )
    preferences = graphene.Field(
        AuditPreferencesInput, description="Preferences to set for the audit"
    )
    schedule_id = graphene.UUID(
        description="UUID of a schedule when the audit should be run"
    )
    schedule_periods = graphene.Int(
        description=(
            "A limit to the number of times the "
            "audit will be scheduled, or 0 for no limit"
        )
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

        preferences = {}

        input_preferences = input_object.preferences
        if input_preferences:
            if input_preferences.create_assets_apply_overrides is not None:
                preferences['assets_apply_overrides'] = to_yes_no(
                    input_preferences.create_assets_apply_overrides
                )

            if input_preferences.create_assets_min_qod is not None:
                preferences[
                    'assets_min_qod'
                ] = input_preferences.create_assets_min_qod

            if input_preferences.auto_delete_reports is not None:
                preferences['auto_delete'] = "keep"
                preferences[
                    'auto_delete_data'
                ] = input_preferences.auto_delete_reports
            else:
                preferences['auto_delete'] = "no"

            if input_preferences.create_assets is not None:
                preferences['in_assets'] = to_yes_no(
                    input_preferences.create_assets
                )

            if input_preferences.max_concurrent_nvts is not None:
                preferences[
                    'max_checks'
                ] = input_preferences.max_concurrent_nvts

            if input_preferences.max_concurrent_hosts is not None:
                preferences[
                    'max_hosts'
                ] = input_preferences.max_concurrent_hosts

        gmp = get_gmp(info)

        resp = gmp.create_audit(
            name,
            str(policy_id),
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
        return CreateAudit(audit_id=resp.get('id'))


class ModifyAuditInput(graphene.InputObjectType):
    """Input ObjectType for modifying an audit"""

    audit_id = graphene.UUID(
        required=True, description="UUID of the audit to modify.", name='id'
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
    comment = graphene.String(description="Audit comment")
    observers = graphene.List(graphene.String)
    preferences = graphene.Field(
        AuditPreferencesInput, description="Preferences to set for the audit"
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


class ModifyAudit(graphene.Mutation):
    """Modify an existing audit"""

    class Arguments:
        input_object = ModifyAuditInput(
            required=True,
            name='input',
            description="Input ObjectType for modifying an audit",
        )

    ok = graphene.Boolean(
        description="True on success. Otherwise the response contains an error"
    )

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

        preferences = {}
        input_preferences = input_object.preferences
        if input_preferences:
            if input_preferences.create_assets_apply_overrides is not None:
                preferences['assets_apply_overrides'] = to_yes_no(
                    input_preferences.create_assets_apply_overrides
                )

            if input_preferences.create_assets_min_qod is not None:
                preferences[
                    'assets_min_qod'
                ] = input_preferences.create_assets_min_qod

            if input_preferences.auto_delete_reports is not None:
                preferences['auto_delete'] = "keep"
                preferences[
                    'auto_delete_data'
                ] = input_preferences.auto_delete_reports
            else:
                preferences['auto_delete'] = "no"

            if input_preferences.create_assets is not None:
                preferences['in_assets'] = to_yes_no(
                    input_preferences.create_assets
                )

            if input_preferences.max_concurrent_nvts is not None:
                preferences[
                    'max_checks'
                ] = input_preferences.max_concurrent_nvts

            if input_preferences.max_concurrent_hosts is not None:
                preferences[
                    'max_hosts'
                ] = input_preferences.max_concurrent_hosts

        gmp = get_gmp(info)

        gmp.modify_audit(
            audit_id,
            name=name,
            policy_id=policy_id,
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

        return ModifyAudit(ok=True)


class StartAudit(graphene.Mutation):
    """Start an audit"""

    class Arguments:
        audit_id = graphene.UUID(
            required=True,
            name='id',
            description="UUID of the audit to start a scan for",
        )

    report_id = graphene.UUID(
        description="UUID of the report for the started scan"
    )

    @staticmethod
    @require_authentication
    def mutate(_root, info, audit_id):
        gmp = get_gmp(info)
        resp = gmp.start_audit(str(audit_id))

        report_id = get_text_from_element(resp, 'report_id')
        return StartAudit(report_id)


class StopAudit(graphene.Mutation):
    """Stop an audit"""

    class Arguments:
        audit_id = graphene.UUID(
            required=True,
            name='id',
            description="UUID of the audit to stop the current scan",
        )

    ok = graphene.Boolean(
        description="True on success. Otherwise the response contains an error"
    )

    @staticmethod
    @require_authentication
    def mutate(_root, info, audit_id):
        gmp = get_gmp(info)
        resp = gmp.stop_audit(str(audit_id))
        status = int(resp.get('status'))
        ok = status == 200
        return StopAudit(ok)


class ResumeAudit(graphene.Mutation):
    """Resume an audit"""

    class Arguments:
        audit_id = graphene.UUID(
            required=True,
            name='id',
            description="UUID of the audit which scan should be resumed",
        )

    ok = graphene.Boolean(
        description="True on success. Otherwise the response contains an error"
    )

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
