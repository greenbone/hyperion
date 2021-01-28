# -*- coding: utf-8 -*-
# Copyright (C) 2020 Greenbone Networks GmbH
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


def append_data_value(data, key, value):
    if value is not None:
        data[key] = str(value)


def append_alert_condition_data(condition, condition_data):
    if not condition or not condition_data:
        return None
    data = dict()
    for key, value in condition_data.items():
        if condition == "Filter count at least":
            if key == 'at_least_count':
                append_data_value(data, 'count', value)
            elif key == 'at_least_filter_id':
                append_data_value(data, 'filter_id', value)
        elif condition == "Severity at least":
            if key == "severity":
                append_data_value(data, key, value)
        elif condition == "Severity changed":
            if key == "direction":
                append_data_value(data, key, value)
    # ALWAYS sends no data, will result in empty dict
    return data if data != {} else None


def append_alert_event_data(event, event_data):
    if not event or not event_data:
        return None
    data = dict()
    for key, value in event_data.items():
        if event == "Task run status changed":
            if key == "status":
                append_data_value(data, key, value)
        elif (
            event == "Updated SecInfo arrived" or event == "New SecInfo arrived"
        ):
            if key == "secinfo_type":
                append_data_value(data, key, value)
    return data if data != {} else None


alert_methods = {
    'HTTP Get': ['URL'],
    'Send': ['send_host', 'send_port', 'send_report_format'],
    'SCP': [
        'scp_credential',
        'scp_host',
        'scp_known_hosts',
        'scp_path',
        'scp_report_format',
    ],
    'SMB': [
        'smb_credential',
        'smb_file_path',
        'smb_report_format',
        'smb_share_path',
    ],
    'SNMP': ['snmp_community', 'snmp_agent', 'snmp_message'],
    'TippingPoint SMS': [
        'tp_sms_credential',
        'tp_sms_hostname',
        'tp_sms_tls_certificate',
        'tp_sms_tls_workaround',
    ],
    'verinice Connector': [
        'verinice_server_credential',
        'verinice_server_url',
        'verinice_server_report_format',
    ],
    'Alemba vFire': [
        'vfire_base_url',
        'vfire_call_description',
        'vfire_call_impact_name',
        'vfire_call_partition_name',
        'vfire_call_template_name',
        'vfire_call_type_name',
        'vfire_call_urgency_name',
        'vfire_client_id',
        'vfire_credential',
        'vfire_session_type',
    ],
    'Syslog': ['submethod'],
    'Start Task': [
        'start_task_task',
    ],
    'Sourcefire Connector': [
        'defense_center_ip',
        'defense_center_port',
        'pkcs12',
        'pkcs12_credential',
    ],
}


def should_append_email_data(notice, key):
    append_data = (
        (key == 'to_address')
        or (key == 'from_address')
        or (key == 'subject')
        or (key == 'notice')
        or (notice == 0 and key == "message")
        or (notice == 2 and key == "message_attach")
        or (notice == 0 and key == 'notice_report_format')
        or (notice == 2 and key == 'notice_attach_format')
        or (key == 'recipient_credential')
    )
    return append_data


# IMO report_formats should be an attribute of Alemba vFire already
# possibly with name vfire_report_formats, because it is only
# used with Alemba vFire. But since in gsa, create shares
# many things with modify we should wait until that is
# implemented before making this change
def append_alert_method_data(method, method_data, *, report_formats=None):
    if not method or not method_data:
        return None
    data = dict()
    if report_formats and method == "Alemba vFire":
        ids_string = ''
        for index, rf in enumerate(report_formats):
            if index > 0:
                ids_string += ", " + str(rf)
            else:
                ids_string += str(rf)
        data['report_formats'] = ids_string

    if method_data.notice is not None:
        notice = int(method_data.notice)

    other_fields = [
        'details_url',
        'delta_type',
        'delta_report_id',
        'composer_include_notes',
        'composer_include_overrides',
    ]

    for key, value in method_data.items():
        if method == 'Email':
            if should_append_email_data(notice, key):
                append_data_value(data, key, value)
            if key in other_fields:
                append_data_value(data, key, value)
        elif key in other_fields and method != 'Sourcefire Connector':
            append_data_value(data, key, value)
        if method in alert_methods:
            if key in alert_methods[method]:
                append_data_value(data, key, value)

    return data if data != {} else None
