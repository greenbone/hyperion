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
# but WITHOUT ANY WARRANTY; without even the im plied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


def pluralize_name(entity_name):
    return entity_name + 's'


def compose_mock_command(entity_name):
    command = 'get_' + entity_name + 's'
    return command


def return_gmp_methods(mock_object):
    gmp_methods = {
        'get_alert': mock_object.get_alert,
        'get_alerts': mock_object.get_alerts,
        'get_audit': mock_object.get_audit,
        'get_audits': mock_object.get_audits,
        'get_cpe': mock_object.get_cpe,
        'get_cpe_list': mock_object.get_cpe_list,
        'get_credential': mock_object.get_credential,
        'get_credentials': mock_object.get_credentials,
        'get_cve': mock_object.get_cve,
        'get_cve_list': mock_object.get_cve_list,
        'get_dfn_cert_advisory': mock_object.get_dfn_cert_advisory,
        'get_dfn_cert_advisory_list': mock_object.get_dfn_cert_advisory_list,
        'get_host': mock_object.get_host,
        'get_hosts': mock_object.get_hosts,
        'get_filter': mock_object.get_filter,
        'get_filters': mock_object.get_filters,
        'get_info': mock_object.get_info,
        'get_info_list': mock_object.get_info_list,
        'get_note': mock_object.get_note,
        'get_notes': mock_object.get_notes,
        'get_nvt': mock_object.get_nvt,
        'get_nvt_list': mock_object.get_nvt_list,
        'get_operating_system': mock_object.get_operating_system,
        'get_operating_systems': mock_object.get_operating_systems,
        'get_override': mock_object.get_override,
        'get_overrides': mock_object.get_overrides,
        'get_policy': mock_object.get_policy,
        'get_policies': mock_object.get_policies,
        'get_permission': mock_object.get_permission,
        'get_permissions': mock_object.get_permissions,
        'get_port_lists': mock_object.get_port_lists,
        'get_reports': mock_object.get_reports,
        'get_report_format': mock_object.get_report_format,
        'get_report_formats': mock_object.get_report_formats,
        'get_result': mock_object.get_result,
        'get_results': mock_object.get_results,
        'get_role': mock_object.get_role,
        'get_roles': mock_object.get_roles,
        'get_scan_config': mock_object.get_scan_config,
        'get_scan_configs': mock_object.get_scan_configs,
        'get_scan_config_nvt': mock_object.get_scan_config_nvt,
        'get_scan_config_nvts': mock_object.get_scan_config_nvts,
        'get_scanner': mock_object.get_scanner,
        'get_scanners': mock_object.get_scanners,
        'get_schedule': mock_object.get_schedule,
        'get_schedules': mock_object.get_schedules,
        'get_user_settings': mock_object.get_user_settings,
        'get_tags': mock_object.get_tags,
        'get_target': mock_object.get_target,
        'get_targets': mock_object.get_targets,
        'get_task': mock_object.get_task,
        'get_tasks': mock_object.get_tasks,
        'get_tls_certificate': mock_object.get_tls_certificate,
        'get_tls_certificates': mock_object.get_tls_certificates,
        'get_tickets': mock_object.get_tickets,
        'get_ticket': mock_object.get_ticket,
        'get_user': mock_object.get_user,
        'get_users': mock_object.get_users,
        'get_vulnerabilities': mock_object.get_vulnerabilities,
    }
    return gmp_methods
