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

from graphene import ObjectType, String, Schema, Field

from selene.schema.aggregates.queries import GetAggregate

from selene.schema.alerts.queries import (
    GetAlert,
    GetAlerts,
)

from selene.schema.alerts.mutations import (
    CloneAlert,
    CreateAlert,
    DeleteAlertsByFilter,
    DeleteAlertsByIds,
    ExportAlertsByFilter,
    ExportAlertsByIds,
    ModifyAlert,
    TestAlert,
)

from selene.schema.audits.queries import GetAudit, GetAudits

from selene.schema.audits.mutations import (
    CloneAudit,
    CreateAudit,
    DeleteAudit,
    DeleteAuditsByIds,
    DeleteAuditsByFilter,
    ModifyAudit,
    StartAudit,
    CreateContainerAudit,
    StopAudit,
    ResumeAudit,
    ExportAuditsByFilter,
    ExportAuditsByIds,
)

from selene.schema.authentication import (
    LoginMutation,
    LogoutMutation,
    CurrentUser,
    RenewSessionMutation,
)

from selene.schema.auth_methods.mutations import ModifyAuth

from selene.schema.auth_methods.queries import DescribeAuth

from selene.schema.capabilities import GetCapabilities

from selene.schema.cert_bund_advisories.queries import (
    GetCertBundAdvisories,
    GetCertBundAdvisory,
)

from selene.schema.cert_bund_advisories.mutations import (
    ExportCertBundAdvisoriesByFilter,
    ExportCertBundAdvisoriesByIds,
)

from selene.schema.credentials.queries import (
    GetCredentials,
    GetCredential,
)

from selene.schema.credentials.mutations import (
    CloneCredential,
    CreateCredential,
    DeleteCredentialsByFilter,
    DeleteCredentialsByIds,
    ExportCredentialsByFilter,
    ExportCredentialsByIds,
    ModifyCredential,
)

from selene.schema.cves.queries import GetCVE, GetCVEs

from selene.schema.cves.mutations import (
    ExportCVEsByFilter,
    ExportCVEsByIds,
)

from selene.schema.cpes.queries import GetCPE, GetCPEs

from selene.schema.cpes.mutations import (
    ExportCPEsByFilter,
    ExportCPEsByIds,
)

from selene.schema.dfn_cert_advisories.queries import (
    GetDFNCertAdvisories,
    GetDFNCertAdvisory,
)

from selene.schema.dfn_cert_advisories.mutations import (
    ExportDFNCertAdvisoriesByFilter,
    ExportDFNCertAdvisoriesByIds,
)

from selene.schema.feeds.queries import GetFeed, GetFeeds

from selene.schema.filters.queries import GetFilter, GetFilters

from selene.schema.filters.mutations import (
    CloneFilter,
    CreateFilter,
    DeleteFilter,
    DeleteFiltersByFilter,
    DeleteFiltersByIds,
    ExportFiltersByFilter,
    ExportFiltersByIds,
    ModifyFilter,
)

from selene.schema.hosts.mutations import (
    CreateHost,
    DeleteHost,
    DeleteHostsByFilter,
    DeleteHostsByIds,
    DeleteHostsByReport,
    ExportHostsByFilter,
    ExportHostsByIds,
    ModifyHost,
)

from selene.schema.hosts.queries import GetHost, GetHosts

from selene.schema.tasks.queries import GetTask, GetTasks

from selene.schema.operating_systems.queries import (
    GetOperatingSystem,
    GetOperatingSystems,
)

from selene.schema.operating_systems.mutations import (
    DeleteOperatingSystem,
    DeleteOperatingSystemsByIds,
    DeleteOperatingSystemsByFilter,
    DeleteOperatingSystemsByReport,
    ExportOperatingSystemsByFilter,
    ExportOperatingSystemsByIds,
    ModifyOperatingSystem,
)

from selene.schema.oval_definitions.queries import (
    GetOvalDefinition,
    GetOvalDefinitions,
)

from selene.schema.oval_definitions.mutations import (
    ExportOvalDefinitionsByFilter,
    ExportOvalDefinitionsByIds,
)

from selene.schema.permissions.queries import GetPermissions, GetPermission

from selene.schema.scanners.queries import (
    GetScanner,
    GetScanners,
)
from selene.schema.scanners.mutations import (
    CloneScanner,
    CreateScanner,
    ExportScannersByIds,
    ExportScannersByFilter,
    DeleteScanner,
    DeleteScannersByFilter,
    DeleteScannersByIds,
    ModifyScanner,
    VerifyScanner,
)

from selene.schema.scan_configs.queries import (
    GetScanConfig,
    GetScanConfigs,
)

from selene.schema.scan_configs.mutations import (
    CreateScanConfig,
    CreateScanConfigFromOspScanner,
    CloneScanConfig,
    DeleteScanConfig,
    DeleteScanConfigsByIds,
    DeleteScanConfigsByFilter,
    ImportScanConfig,
    ExportScanConfigsByIds,
    ExportScanConfigsByFilter,
    ModifyScanConfigSetName,
    ModifyScanConfigSetComment,
    ModifyScanConfigSetFamilySelection,
    ModifyScanConfigSetNvtPreference,
    ModifyScanConfigSetNvtSelection,
    ModifyScanConfigSetScannerPreference,
)

from selene.schema.system_reports.queries import (
    GetSystemReport,
    GetSystemReports,
)

from selene.schema.targets.queries import (
    GetTarget,
    GetTargets,
)

from selene.schema.targets.mutations import (
    DeleteTarget,
    DeleteTargetsByFilter,
    DeleteTargetsByIds,
    CloneTarget,
    CreateTarget,
    ModifyTarget,
    ExportTargetsByFilter,
    ExportTargetsByIds,
)

from selene.schema.tags.queries import (
    GetTags,
    GetTag,
)

from selene.schema.tags.mutations import (
    CloneTag,
    CreateTag,
    ModifyTag,
    ToggleTag,
    RemoveTag,
    DeleteTagsByFilter,
    DeleteTagsByIds,
    ExportTagsByFilter,
    ExportTagsByIds,
    AddTag,
    BulkTag,
)

from selene.schema.tickets.queries import GetTicket, GetTickets

from selene.schema.tickets.mutations import (
    CloneTicket,
    CreateTicket,
    DeleteTicketsByFilter,
    DeleteTicketsByIds,
    ExportTicketsByFilter,
    ExportTicketsByIds,
    ModifyTicket,
)

from selene.schema.results.queries import GetResults, GetResult

from selene.schema.results.mutations import (
    ExportResultsByFilter,
    ExportResultsByIds,
)


from selene.schema.user_settings.queries import GetUserSetting, GetUserSettings

from selene.schema.user_settings.mutations import (
    ModifyUserSetting,
    ModifyUserSettingByName,
)


from selene.schema.notes.queries import GetNotes, GetNote

from selene.schema.notes.mutations import (
    CloneNote,
    CreateNote,
    DeleteNote,
    DeleteNotesByFilter,
    DeleteNotesByIds,
    ExportNotesByFilter,
    ExportNotesByIds,
    ModifyNote,
)

from selene.schema.nvts.queries import (
    GetNvtFamilies,
    GetNVT,
    GetNVTs,
    GetScanConfigNvt,
    GetScanConfigNvts,
    GetPreference,
    GetPreferences,
)

from selene.schema.nvts.mutations import (
    ExportNVTsByFilter,
    ExportNVTsByIds,
)

from selene.schema.overrides.queries import GetOverrides, GetOverride

from selene.schema.overrides.mutations import (
    CloneOverride,
    CreateOverride,
    DeleteOverride,
    DeleteOverridesByFilter,
    DeleteOverridesByIds,
    ExportOverridesByFilter,
    ExportOverridesByIds,
    ModifyOverride,
)

from selene.schema.permissions.mutations import (
    ClonePermission,
    CreatePermission,
    DeletePermissionsByFilter,
    DeletePermissionsByIds,
    ExportPermissionsByFilter,
    ExportPermissionsByIds,
    ModifyPermission,
)

from selene.schema.policies.queries import (
    GetPolicy,
    GetPolicies,
)

from selene.schema.policies.mutations import (
    CreatePolicy,
    ClonePolicy,
    DeletePolicy,
    DeletePoliciesByIds,
    DeletePoliciesByFilter,
    ImportPolicy,
    ExportPoliciesByIds,
    ExportPoliciesByFilter,
    ModifyPolicySetName,
    ModifyPolicySetComment,
    ModifyPolicySetFamilySelection,
    ModifyPolicySetNvtPreference,
    ModifyPolicySetNvtSelection,
    ModifyPolicySetScannerPreference,
)

from selene.schema.port_list.queries import (
    GetPortList,
    GetPortLists,
)

from selene.schema.port_list.mutations import (
    ClonePortList,
    CreatePortList,
    CreatePortRange,
    DeletePortListsByIds,
    DeletePortListsByFilter,
    DeletePortRange,
    ExportPortListsByFilter,
    ExportPortListsByIds,
    ModifyPortList,
)

from selene.schema.reports.queries import (
    GetReport,
    GetReports,
)

from selene.schema.reports.mutations import (
    DeleteReport,
    DeleteReportsByFilter,
    DeleteReportsByIds,
    ExportReportsByFilter,
    ExportReportsByIds,
    ImportReport,
)

from selene.schema.report_formats.mutations import (
    ImportReportFormat,
    DeleteReportFormat,
    DeleteReportFormatsByFilter,
    DeleteReportFormatsByIds,
    ModifyReportFormat,
)

from selene.schema.report_formats.queries import (
    GetReportFormat,
    GetReportFormats,
)

from selene.schema.roles.mutations import (
    CloneRole,
    CreateRole,
    DeleteRole,
    DeleteRolesByFilter,
    DeleteRolesByIds,
    ExportRolesByFilter,
    ExportRolesByIds,
    ModifyRole,
)

from selene.schema.roles.queries import (
    GetRole,
    GetRoles,
)

from selene.schema.schedules.queries import (
    GetSchedule,
    GetSchedules,
)

from selene.schema.schedules.mutations import (
    CloneSchedule,
    CreateSchedule,
    DeleteSchedulesByFilter,
    DeleteSchedulesByIds,
    ExportSchedulesByFilter,
    ExportSchedulesByIds,
    ModifySchedule,
)

from selene.schema.tasks.mutations import (
    CloneTask,
    CreateTask,
    DeleteTask,
    DeleteTasksByIds,
    DeleteTasksByFilter,
    ModifyTask,
    StartTask,
    CreateContainerTask,
    StopTask,
    ResumeTask,
    ExportTasksByFilter,
    ExportTasksByIds,
)

from selene.schema.tls_certificates.queries import (
    GetTLSCertificate,
    GetTLSCertificates,
)

from selene.schema.tls_certificates.mutations import (
    CloneTLSCertificate,
    CreateTLSCertificate,
    DeleteTLSCertificate,
    DeleteTLSCertificatesByFilter,
    DeleteTLSCertificatesByIds,
    ExportTLSCertificatesByFilter,
    ExportTLSCertificatesByIds,
    ModifyTLSCertificate,
)
from selene.schema.users.queries import (
    GetUser,
    GetUsers,
)

from selene.schema.users.mutations import (
    CloneUser,
    CreateUser,
    DeleteUsersByFilter,
    DeleteUsersByIds,
    ExportUsersByFilter,
    ExportUsersByIds,
    ModifyUserSetName,
    ModifyUserSetComment,
    ModifyUserSetPassword,
    ModifyUserSetAuthSource,
    ModifyUserSetHosts,
    ModifyUserSetHostsAllow,
    ModifyUserSetIfaces,
    ModifyUserSetIfacesAllow,
    ModifyUserSetRoles,
    ModifyUserSetGroups,
)

from selene.schema.trash.mutations import EmptyTrashcan, RestoreFromTrashcan

from selene.schema.utils import get_gmp

from selene.schema.vulnerabilities.queries import (
    GetVulnerability,
    GetVulnerabilities,
)

from selene.schema.vulnerabilities.mutations import (
    ExportVulnerabilitiesByFilter,
    ExportVulnerabilitiesByIds,
)


class Mutations(ObjectType):
    login = LoginMutation.Field()
    logout = LogoutMutation.Field()
    renew_session = RenewSessionMutation.Field()
    # Alerts
    clone_alert = CloneAlert.Field()
    create_alert = CreateAlert.Field()
    delete_alerts_by_filter = DeleteAlertsByFilter.Field()
    delete_alerts_by_ids = DeleteAlertsByIds.Field()
    export_alerts_by_filter = ExportAlertsByFilter.Field()
    export_alerts_by_ids = ExportAlertsByIds.Field()
    modify_alert = ModifyAlert.Field()
    test_alert = TestAlert.Field()
    # Audits
    clone_audit = CloneAudit.Field()
    create_container_audit = CreateContainerAudit.Field()
    create_audit = CreateAudit.Field()
    delete_audit = DeleteAudit.Field()
    delete_audits_by_filter = DeleteAuditsByFilter.Field()
    delete_audits_by_ids = DeleteAuditsByIds.Field()
    export_audits_by_filter = ExportAuditsByFilter.Field()
    export_audits_by_ids = ExportAuditsByIds.Field()
    modify_audit = ModifyAudit.Field()
    resume_audit = ResumeAudit.Field()
    start_audit = StartAudit.Field()
    stop_audit = StopAudit.Field()
    # Authentication configuration
    modify_auth = ModifyAuth.Field()
    # Cert Bund Advisories
    export_cert_bund_advisories_by_filter = (
        ExportCertBundAdvisoriesByFilter.Field()
    )
    export_cert_bund_advisories_by_ids = ExportCertBundAdvisoriesByIds.Field()
    # Credentials
    clone_credential = CloneCredential.Field()
    create_credential = CreateCredential.Field()
    export_credentials_by_filter = ExportCredentialsByFilter.Field()
    export_credentials_by_ids = ExportCredentialsByIds.Field()
    delete_credentials_by_filter = DeleteCredentialsByFilter.Field()
    delete_credentials_by_ids = DeleteCredentialsByIds.Field()
    modify_credential = ModifyCredential.Field()
    # CVEs
    export_cves_by_filter = ExportCVEsByFilter.Field()
    export_cves_by_ids = ExportCVEsByIds.Field()
    # CPEs
    export_cpes_by_filter = ExportCPEsByFilter.Field()
    export_cpes_by_ids = ExportCPEsByIds.Field()
    # DFN Cert Advisories
    export_dfn_cert_advisories_by_filter = (
        ExportDFNCertAdvisoriesByFilter.Field()
    )
    export_dfn_cert_advisories_by_ids = ExportDFNCertAdvisoriesByIds.Field()
    # Filter
    clone_filter = CloneFilter.Field()
    create_filter = CreateFilter.Field()
    delete_filter = DeleteFilter.Field()
    delete_filters_by_ids = DeleteFiltersByIds.Field()
    delete_filters_by_filter = DeleteFiltersByFilter.Field()
    export_filters_by_ids = ExportFiltersByIds.Field()
    export_filters_by_filter = ExportFiltersByFilter.Field()
    modify_filter = ModifyFilter.Field()
    # Hosts
    create_host = CreateHost.Field()
    delete_host = DeleteHost.Field()
    delete_hosts_by_filter = DeleteHostsByFilter.Field()
    delete_hosts_by_ids = DeleteHostsByIds.Field()
    delete_hosts_by_report = DeleteHostsByReport.Field()
    export_hosts_by_filter = ExportHostsByFilter.Field()
    export_hosts_by_ids = ExportHostsByIds.Field()
    modify_host = ModifyHost.Field()
    # Notes
    clone_note = CloneNote.Field()
    create_note = CreateNote.Field()
    delete_note = DeleteNote.Field()
    delete_notes_by_ids = DeleteNotesByIds.Field()
    delete_notes_by_filter = DeleteNotesByFilter.Field()
    export_notes_by_ids = ExportNotesByIds.Field()
    export_notes_by_filter = ExportNotesByFilter.Field()
    modify_note = ModifyNote.Field()
    # NVTs
    export_nvts_by_filter = ExportNVTsByFilter.Field()
    export_nvts_by_ids = ExportNVTsByIds.Field()
    # OperatingSystems
    delete_operating_system = DeleteOperatingSystem.Field()
    delete_operating_systems_by_ids = DeleteOperatingSystemsByIds.Field()
    delete_operating_systems_by_filter = DeleteOperatingSystemsByFilter.Field()
    delete_operating_systems_by_report = DeleteOperatingSystemsByReport.Field()
    export_operating_systems_by_ids = ExportOperatingSystemsByIds.Field()
    export_operating_systems_by_filter = ExportOperatingSystemsByFilter.Field()
    modify_operating_system = ModifyOperatingSystem.Field()
    # Oval Definitions
    export_oval_definitions_by_filter = ExportOvalDefinitionsByFilter.Field()
    export_oval_definitions_by_ids = ExportOvalDefinitionsByIds.Field()
    # Overrides
    clone_override = CloneOverride.Field()
    create_override = CreateOverride.Field()
    delete_override = DeleteOverride.Field()
    delete_overrides_by_ids = DeleteOverridesByIds.Field()
    delete_overrides_by_filter = DeleteOverridesByFilter.Field()
    export_overrides_by_ids = ExportOverridesByIds.Field()
    export_overrides_by_filter = ExportOverridesByFilter.Field()
    modify_override = ModifyOverride.Field()
    # Permissions
    clone_permission = ClonePermission.Field()
    create_permission = CreatePermission.Field()
    delete_permissions_by_filter = DeletePermissionsByFilter.Field()
    delete_permissions_by_ids = DeletePermissionsByIds.Field()
    export_permissions_by_filter = ExportPermissionsByFilter.Field()
    export_permissions_by_ids = ExportPermissionsByIds.Field()
    modify_permission = ModifyPermission.Field()
    # Policies
    create_policy = CreatePolicy.Field()
    clone_policy = ClonePolicy.Field()
    delete_policy = DeletePolicy.Field()
    delete_policies_by_ids = DeletePoliciesByIds.Field()
    delete_policies_by_filter = DeletePoliciesByFilter.Field()
    import_policy = ImportPolicy.Field()
    export_policies_by_filter = ExportPoliciesByFilter.Field()
    export_policies_by_ids = ExportPoliciesByIds.Field()
    modify_policy_set_name = ModifyPolicySetName.Field()
    modify_policy_set_comment = ModifyPolicySetComment.Field()
    modify_policy_set_family_selection = ModifyPolicySetFamilySelection.Field()
    modify_policy_set_nvt_preference = ModifyPolicySetNvtPreference.Field()
    modify_policy_set_nvt_selection = ModifyPolicySetNvtSelection.Field()
    modify_policy_set_scanner_preference = (
        ModifyPolicySetScannerPreference.Field()
    )
    # PortLists
    clone_port_list = ClonePortList.Field()
    create_port_list = CreatePortList.Field()
    delete_port_lists_by_filter = DeletePortListsByFilter.Field()
    delete_port_lists_by_ids = DeletePortListsByIds.Field()
    export_port_lists_by_filter = ExportPortListsByFilter.Field()
    export_port_lists_by_ids = ExportPortListsByIds.Field()
    modify_port_list = ModifyPortList.Field()
    # PortRanges
    create_port_range = CreatePortRange.Field()
    delete_port_range = DeletePortRange.Field()
    # Reports
    delete_report = DeleteReport.Field()
    delete_reports_by_ids = DeleteReportsByIds.Field()
    delete_reports_by_filter = DeleteReportsByFilter.Field()
    export_reports_by_filter = ExportReportsByFilter.Field()
    export_reports_by_ids = ExportReportsByIds.Field()
    import_report = ImportReport.Field()
    # ReportFormats
    delete_report_format = DeleteReportFormat.Field()
    delete_report_formats_by_filter = DeleteReportFormatsByFilter.Field()
    delete_report_formats_by_ids = DeleteReportFormatsByIds.Field()
    import_report_format = ImportReportFormat.Field()
    modify_report_format = ModifyReportFormat.Field()
    export_results_by_filter = ExportResultsByFilter.Field()
    export_results_by_ids = ExportResultsByIds.Field()
    # Roles
    clone_role = CloneRole.Field()
    create_role = CreateRole.Field()
    delete_role = DeleteRole.Field()
    delete_roles_by_filter = DeleteRolesByFilter.Field()
    delete_roles_by_ids = DeleteRolesByIds.Field()
    export_roles_by_filter = ExportRolesByFilter.Field()
    export_roles_by_ids = ExportRolesByIds.Field()
    modify_role = ModifyRole.Field()
    # ScanConfigs
    create_scan_config = CreateScanConfig.Field()
    create_scan_config_from_osp_scanner = CreateScanConfigFromOspScanner.Field()
    clone_scan_config = CloneScanConfig.Field()
    delete_scan_config = DeleteScanConfig.Field()
    delete_scan_configs_by_ids = DeleteScanConfigsByIds.Field()
    delete_scan_configs_by_filter = DeleteScanConfigsByFilter.Field()
    import_scan_config = ImportScanConfig.Field()
    export_scan_configs_by_filter = ExportScanConfigsByFilter.Field()
    export_scan_configs_by_ids = ExportScanConfigsByIds.Field()
    modify_scan_config_set_name = ModifyScanConfigSetName.Field()
    modify_scan_config_set_comment = ModifyScanConfigSetComment.Field()
    modify_scan_config_set_family_selection = (
        ModifyScanConfigSetFamilySelection.Field()
    )
    modify_scan_config_set_nvt_preference = (
        ModifyScanConfigSetNvtPreference.Field()
    )
    modify_scan_config_set_nvt_selection = (
        ModifyScanConfigSetNvtSelection.Field()
    )
    modify_scan_config_set_scanner_preference = (
        ModifyScanConfigSetScannerPreference.Field()
    )
    # Scanner
    clone_scanner = CloneScanner.Field()
    create_scanner = CreateScanner.Field()
    delete_scanner = DeleteScanner.Field()
    delete_scanners_by_filter = DeleteScannersByFilter.Field()
    delete_scanners_by_ids = DeleteScannersByIds.Field()
    export_scanners_by_filter = ExportScannersByFilter.Field()
    export_scanners_by_ids = ExportScannersByIds.Field()
    modify_scanner = ModifyScanner.Field()
    # Schedule
    clone_schedule = CloneSchedule.Field()
    create_schedule = CreateSchedule.Field()
    export_schedules_by_filter = ExportSchedulesByFilter.Field()
    export_schedules_by_ids = ExportSchedulesByIds.Field()
    delete_schedules_by_filter = DeleteSchedulesByFilter.Field()
    delete_schedules_by_ids = DeleteSchedulesByIds.Field()
    modify_schedule = ModifySchedule.Field()
    # Tags
    add_tag = AddTag.Field()
    bulk_tag = BulkTag.Field()
    clone_tag = CloneTag.Field()
    create_tag = CreateTag.Field()
    delete_tags_by_ids = DeleteTagsByIds.Field()
    delete_tags_by_filter = DeleteTagsByFilter.Field()
    export_tags_by_ids = ExportTagsByIds.Field()
    export_tags_by_filter = ExportTagsByFilter.Field()
    modify_tag = ModifyTag.Field()
    remove_tag = RemoveTag.Field()
    toggle_tag = ToggleTag.Field()
    # Target
    clone_target = CloneTarget.Field()
    create_target = CreateTarget.Field()
    delete_target = DeleteTarget.Field()
    delete_targets_by_filter = DeleteTargetsByFilter.Field()
    delete_targets_by_ids = DeleteTargetsByIds.Field()
    export_targets_by_filter = ExportTargetsByFilter.Field()
    export_targets_by_ids = ExportTargetsByIds.Field()
    modify_target = ModifyTarget.Field()
    # Tasks
    clone_task = CloneTask.Field()
    create_container_task = CreateContainerTask.Field()
    create_task = CreateTask.Field()
    delete_task = DeleteTask.Field()
    delete_tasks_by_filter = DeleteTasksByFilter.Field()
    delete_tasks_by_ids = DeleteTasksByIds.Field()
    export_tasks_by_filter = ExportTasksByFilter.Field()
    export_tasks_by_ids = ExportTasksByIds.Field()
    modify_task = ModifyTask.Field()
    resume_task = ResumeTask.Field()
    start_task = StartTask.Field()
    stop_task = StopTask.Field()
    # Tickets
    create_ticket = CreateTicket.Field()
    clone_ticket = CloneTicket.Field()
    export_tickets_by_filter = ExportTicketsByFilter.Field()
    export_tickets_by_ids = ExportTicketsByIds.Field()
    delete_tickets_by_ids = DeleteTicketsByIds.Field()
    delete_tickets_by_filter = DeleteTicketsByFilter.Field()
    modify_ticket = ModifyTicket.Field()
    # TLS Certificates
    create_tls_certificate = CreateTLSCertificate.Field()
    clone_tls_certificate = CloneTLSCertificate.Field()
    modify_tls_certificate = ModifyTLSCertificate.Field()
    export_tls_certificates_by_filter = ExportTLSCertificatesByFilter.Field()
    export_tls_certificates_by_ids = ExportTLSCertificatesByIds.Field()
    delete_tls_certificate = DeleteTLSCertificate.Field()
    delete_tls_certificates_by_ids = DeleteTLSCertificatesByIds.Field()
    delete_tls_certificates_by_filter = DeleteTLSCertificatesByFilter.Field()
    # Trashcan
    empty_trashcan = EmptyTrashcan.Field()
    restore_from_trashcan = RestoreFromTrashcan.Field()
    # Users
    clone_user = CloneUser.Field()
    create_user = CreateUser.Field()
    delete_users_by_filter = DeleteUsersByFilter.Field()
    delete_users_by_ids = DeleteUsersByIds.Field()
    export_users_by_filter = ExportUsersByFilter.Field()
    export_users_by_ids = ExportUsersByIds.Field()
    modify_user_set_name = ModifyUserSetName.Field()
    modify_user_set_comment = ModifyUserSetComment.Field()
    modify_user_set_password = ModifyUserSetPassword.Field()
    modify_user_set_auth_source = ModifyUserSetAuthSource.Field()
    modify_user_set_hosts = ModifyUserSetHosts.Field()
    modify_user_set_hosts_allow = ModifyUserSetHostsAllow.Field()
    modify_user_set_ifaces = ModifyUserSetIfaces.Field()
    modify_user_set_ifaces_allow = ModifyUserSetIfacesAllow.Field()
    modify_user_set_roles = ModifyUserSetRoles.Field()
    modify_user_set_groups = ModifyUserSetGroups.Field()
    # User settings
    modify_user_setting = ModifyUserSetting.Field()
    modify_user_setting_by_name = ModifyUserSettingByName.Field()
    # Vulnerabilities
    export_vulnerabilities_by_ids = ExportVulnerabilitiesByIds.Field()
    export_vulnerabilities_by_filter = ExportVulnerabilitiesByFilter.Field()


class Query(ObjectType):

    aggregate = GetAggregate()
    alert = GetAlert()
    alerts = GetAlerts()
    audit = GetAudit()
    audits = GetAudits()
    auth = DescribeAuth()
    capabilities = GetCapabilities()
    cert_bund_advisory = GetCertBundAdvisory()
    cert_bund_advisories = GetCertBundAdvisories()
    credential = GetCredential()
    credentials = GetCredentials()
    current_user = Field(CurrentUser)
    cpe = GetCPE()
    cpes = GetCPEs()
    cve = GetCVE()
    cves = GetCVEs()
    dfn_cert_advisory = GetDFNCertAdvisory()
    dfn_cert_advisories = GetDFNCertAdvisories()
    feed = GetFeed()
    feeds = GetFeeds()
    filter = GetFilter()
    filters = GetFilters()
    host = GetHost()
    hosts = GetHosts()
    note = GetNote()
    notes = GetNotes()
    nvt = GetNVT()
    nvts = GetNVTs()
    scan_config_nvt = GetScanConfigNvt()
    scan_config_nvts = GetScanConfigNvts()
    nvt_families = GetNvtFamilies()
    operating_system = GetOperatingSystem()
    operating_systems = GetOperatingSystems()
    oval_definition = GetOvalDefinition()
    oval_definitions = GetOvalDefinitions()
    override = GetOverride()
    overrides = GetOverrides()
    permission = GetPermission()
    permissions = GetPermissions()
    policy = GetPolicy()
    policies = GetPolicies()
    port_list = GetPortList()
    port_lists = GetPortLists()
    preference = GetPreference()
    preferences = GetPreferences()
    report_format = GetReportFormat()
    report_formats = GetReportFormats()
    report = GetReport()
    reports = GetReports()
    result = GetResult()
    results = GetResults()
    role = GetRole()
    roles = GetRoles()
    scan_config = GetScanConfig()
    scan_configs = GetScanConfigs()
    scanner = GetScanner()
    scanners = GetScanners()
    schedule = GetSchedule()
    schedules = GetSchedules()
    system_report = GetSystemReport()
    system_reports = GetSystemReports()
    tag = GetTag()
    tags = GetTags()
    target = GetTarget()
    targets = GetTargets()
    task = GetTask()
    tasks = GetTasks()
    tls_certificate = GetTLSCertificate()
    tls_certificates = GetTLSCertificates()
    ticket = GetTicket()
    tickets = GetTickets()
    user = GetUser()
    users = GetUsers()
    user_setting = GetUserSetting()
    user_settings = GetUserSettings()
    verify_scanner = VerifyScanner()
    version = String()
    vulnerability = GetVulnerability()
    vulnerabilities = GetVulnerabilities()

    @staticmethod
    def resolve_version(_root, info) -> str:
        gmp = get_gmp(info)
        xml = gmp.get_version()
        return xml.find('version').text

    @staticmethod
    def resolve_current_user(_root, _info):
        return True  # needs to return something to access child resolvers


schema = Schema(query=Query, mutation=Mutations)  # pylint: disable=invalid-name
