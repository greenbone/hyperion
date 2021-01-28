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

from selene.schema import schema

from selene.schema.alerts.helper import (
    append_alert_condition_data,
    append_alert_event_data,
    append_alert_method_data,
    append_data_value,
)

from selene.tests import SeleneTestCase


class AlertDataTestCase(SeleneTestCase):
    def test_append_data_value(self):
        data = {
            'abc': 'foo',
            'def': 'bar',
        }
        append_data_value(data, 'ghi', None)
        append_data_value(data, 'jkl', 'baz')
        self.assertEqual(
            data,
            {
                'abc': 'foo',
                'def': 'bar',
                'jkl': 'baz',
            },
        )

    def test_append_alert_condition_data(self):
        # We pull it from schema and make a ConditionData
        # instance with the below dict.
        condition_data_type = schema.get_type('ConditionData')
        condition_data = condition_data_type.create_container(
            {
                'at_least_count': 3,
                'at_least_filter_id': None,
                'severity': 5.6,
                'direction': None,
            }
        )
        with_direction = condition_data_type.create_container(
            {'direction': 'changed'}
        )
        empty_data = condition_data_type.create_container({})

        # should return None if there is no data to append
        self.assertIsNone(
            append_alert_condition_data('Filter count at least', empty_data)
        )

        # should append correct data
        self.assertEqual(
            append_alert_condition_data(
                'Filter count at least', condition_data
            ),
            {'count': '3'},
        )
        self.assertEqual(
            append_alert_condition_data('Severity at least', condition_data),
            {'severity': '5.6'},
        )

        # direction is None, so nothing is appended
        self.assertIsNone(
            append_alert_condition_data('Severity changed', condition_data)
        )
        self.assertEqual(
            append_alert_condition_data('Severity changed', with_direction),
            {'direction': 'changed'},
        )

    def test_append_alert_event_data(self):
        event_data_type = schema.get_type('EventData')
        event_data = event_data_type.create_container(
            {
                'feed_event': 'new',
                'status': None,
                'secinfo_type': 'nvt',
            }
        )
        with_status = event_data_type.create_container({'status': 'Done'})
        empty_data = event_data_type.create_container({})

        self.assertIsNone(
            append_alert_event_data('Task run status changed', empty_data)
        )
        self.assertIsNone(
            append_alert_event_data('Task run status changed', event_data)
        )
        self.assertEqual(
            append_alert_event_data('Task run status changed', with_status),
            {'status': 'Done'},
        )

        self.assertEqual(
            append_alert_event_data('Updated SecInfo arrived', event_data),
            {'secinfo_type': 'nvt'},
        )
        self.assertEqual(
            append_alert_event_data('New SecInfo arrived', event_data),
            {'secinfo_type': 'nvt'},
        )

    def test_append_alert_method_data(self):
        method_data_type = schema.get_type('MethodData')
        method_data = method_data_type.create_container(
            {
                'URL': "foo.bar",
                'composer_include_notes': True,
                'composer_include_overrides': True,
                'defense_center_ip': "123.456.789.0",
                'defense_center_port': 8307,
                'delta_report_id': "123",
                'delta_type': 'previous',
                'details_url': None,
                'from_address': "foo@bar.com",
                'message': "A quick brown fox jumped over the lazy dog.",
                'message_attach': "roses are red",
                'notice': "2",
                'notice_attach_format': "123",
                'notice_report_format': "123",
                'pkcs12': "MIILrgIBAzCCCy0GCSqGSIb3DQEHA",
                'pkcs12_credential': "123",
                'recipient_credential': "123",
                'scp_host': "localhost",
                'scp_known_hosts': "192.168.10.130",
                'scp_path': "report.xml",
                'scp_report_format': "123",
                'scp_credential': "123",
                'send_host': "localhost",
                'send_port': 8080,
                'send_report_format': "123",
                'smb_credential': "123",
                'smb_file_path': "report.xml",
                'smb_share_path': "gvm-reports",
                'snmp_agent': "localhost",
                'snmp_community': "public",
                'snmp_message': "$e",
                'start_task_task': "123",
                'subject': "[GVM] Task '$n': $e",
                'submethod': "syslog",
                'to_address': "foo@bar.com",
                'tp_sms_hostname': "fluffy",
                'tp_sms_tls_workaround': 0,
                'verinice_server_credential': "123",
                'verinice_server_report_format': "123",
                'verinice_server_url': "localhost",
            }
        )
        with_details_url = method_data_type.create_container(
            {
                'URL': "foo.bar",
                'composer_include_notes': True,
                'composer_include_overrides': True,
                'defense_center_ip': "123.456.789.0",
                'defense_center_port': 8307,
                'delta_report_id': "123",
                'delta_type': 'previous',
                'details_url': 'http://www.foo.com',
                'from_address': "foo@bar.com",
                'message': "A quick brown fox jumped over the lazy dog.",
                'message_attach': "roses are red",
                'notice': "2",
                'notice_attach_format': "123",
                'notice_report_format': "123",
                'pkcs12': "MIILrgIBAzCCCy0GCSqGSIb3DQEHA",
                'pkcs12_credential': "123",
                'recipient_credential': "123",
                'scp_host': "localhost",
                'scp_known_hosts': "192.168.10.130",
                'scp_path': "report.xml",
                'scp_report_format': "123",
                'scp_credential': "123",
                'send_host': "localhost",
                'send_port': 8080,
                'send_report_format': "123",
                'smb_credential': "123",
                'smb_file_path': "report.xml",
                'smb_share_path': "gvm-reports",
                'snmp_agent': "localhost",
                'snmp_community': "public",
                'snmp_message': "$e",
                'start_task_task': "123",
                'subject': "[GVM] Task '$n': $e",
                'submethod': "syslog",
                'to_address': "foo@bar.com",
                'tp_sms_hostname': "fluffy",
                'tp_sms_tls_workaround': 0,
                'verinice_server_credential': "123",
                'verinice_server_report_format': "123",
                'verinice_server_url': "localhost",
            }
        )

        empty_data = method_data_type.create_container({})

        self.assertIsNone(append_alert_method_data('SMB', empty_data))

        self.assertEqual(
            append_alert_method_data('SMB', method_data),
            {
                'smb_credential': '123',
                'smb_file_path': 'report.xml',
                'smb_share_path': 'gvm-reports',
                'delta_report_id': '123',
                'delta_type': 'previous',
                'composer_include_notes': 'True',
                'composer_include_overrides': 'True',
            },
        )

        self.assertEqual(
            append_alert_method_data('SMB', with_details_url),
            {
                'smb_credential': '123',
                'smb_file_path': 'report.xml',
                'smb_share_path': 'gvm-reports',
                'delta_report_id': '123',
                'delta_type': 'previous',
                'details_url': 'http://www.foo.com',
                'composer_include_notes': 'True',
                'composer_include_overrides': 'True',
            },
        )
