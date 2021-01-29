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
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# pylint: disable=too-many-lines

from uuid import uuid4

from unittest.mock import patch

from gvm.protocols.latest import (
    AlertCondition,
    AlertEvent,
    AlertMethod,
)

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class ModifyAlertTestCase(SeleneTestCase):
    def setUp(self):
        self.alert_id = uuid4()
        self.xml = '''
        <modify_alert_response
            status="200"
            status_text="OK"
        />
        '''
        self.cmd = 'modify_alert'
        self.id1 = uuid4()
        self.id2 = uuid4()

    def compose_no_method_query(self):
        query = f'''
        mutation {{
            modifyAlert(input: {{
                id: "{self.alert_id}",
                name: "foo",
                event: TASK_RUN_STATUS_CHANGED,
                condition: ALWAYS,
                methodData: {{
                    URL: "foo.bar",
                    composer_include_notes: true,
                    composer_include_overrides: true,
                    defense_center_ip: "123.456.789.0",
                    defense_center_port: 8307,
                    verinice_server_url: "localhost",
                    vfire_base_url: "127.0.0.1",
                    vfire_call_impact_name: "five",
                    vfire_call_partition_name: "first partition",
                    vfire_call_template_name: "six",
                    vfire_call_type_name: "seven",
                    vfire_call_urgency_name: "eight",
                    vfire_client_id: "fakeID",
                    vfire_credential: "ebc2a770-f56b-41d2-a425-dfbe19402ebf",
                }}
            }}
            ) {{
                ok
            }}
        }}
        '''
        return query

    def compose_method_query(self, method, *, notice: str = "1"):
        query = f'''
        mutation {{
            modifyAlert(input: {{
                id: "{self.alert_id}",
                name: "foo",
                event: TASK_RUN_STATUS_CHANGED,
                condition: ALWAYS,
                method: {method},
                reportFormats: ["{self.id1}", "{self.id2}"],
                methodData: {{
                    URL: "foo.bar",
                    composer_include_notes: true,
                    composer_include_overrides: true,
                    defense_center_ip: "123.456.789.0",
                    defense_center_port: 8307,
                    delta_report_id: "{self.id1}",
                    delta_type: PREVIOUS,
                    details_url: "https://secinfo.greenbone.net/etc",
                    from_address: "foo@bar.com",
                    message: "A quick brown fox jumped over the lazy dog.",
                    message_attach: "roses are red",
                    notice: "{notice}",
                    notice_attach_format: "{self.id1}",
                    notice_report_format: "{self.id1}",
                    pkcs12: "MIILrgIBAzCCCy0GCSqGSIb3DQEHA",
                    pkcs12_credential: "{self.id1}",
                    recipient_credential: "{self.id1}",
                    scp_host: "localhost",
                    scp_known_hosts: "192.168.10.130",
                    scp_path: "report.xml",
                    scp_report_format: "{self.id1}",
                    scp_credential: "{self.id1}",
                    send_host: "localhost",
                    send_port: 8080,
                    send_report_format: "{self.id1}",
                    smb_credential: "{self.id1}",
                    smb_file_path: "report.xml",
                    smb_share_path: "gvm-reports",
                    snmp_agent: "localhost",
                    snmp_community: "public",
                    snmp_message: "$e",
                    start_task_task: "{self.id1}",
                    subject: "[GVM] Task '$n': $e",
                    submethod: "syslog",
                    to_address: "foo@bar.com",
                    tp_sms_hostname: "fluffy",
                    tp_sms_tls_workaround: 0,
                    tp_sms_credential: "{self.id1}",
                    tp_sms_tls_certificate: "a quick brown fox jumped",
                    verinice_server_credential: "{self.id1}",
                    verinice_server_report_format: "{self.id1}",
                    verinice_server_url: "localhost",
                    vfire_base_url: "127.0.0.1",
                    vfire_call_impact_name: "five",
                    vfire_call_partition_name: "first partition",
                    vfire_call_template_name: "six",
                    vfire_call_type_name: "seven",
                    vfire_call_urgency_name: "eight",
                    vfire_client_id: "fakeID",
                    vfire_credential: "ebc2a770-f56b-41d2-a425-dfbe19402ebf",
                }}
            }}
            ) {{
                ok
            }}
        }}
        '''
        return query

    def compose_no_condition_query(self):
        query = f'''
        mutation {{
            modifyAlert(input: {{
                id: "{self.alert_id}",
                name: "foo",
                event: TASK_RUN_STATUS_CHANGED,
                method: START_TASK,
                conditionData: {{
                    at_least_count: 1,
                    count: 1,
                    direction: DECREASED,
                    severity: 0.1,
                }}
            }}
            ) {{
                ok
            }}
        }}
        '''
        return query

    def compose_condition_query(self, condition):
        query = f'''
        mutation {{
            modifyAlert(input: {{
                id: "{self.alert_id}",
                name: "foo",
                event: TASK_RUN_STATUS_CHANGED,
                condition: {condition},
                method: START_TASK,
                conditionData: {{
                    at_least_count: 1,
                    count: 1,
                    direction: DECREASED,
                    severity: 0.1,
                }}
            }}
            ) {{
                ok
            }}
        }}
        '''
        return query

    def compose_event_query(self, event):
        query = f'''
        mutation {{
            modifyAlert(input: {{
                id: "{self.alert_id}",
                name: "foo",
                event: {event},
                condition: ALWAYS,
                method: START_TASK,
                eventData: {{
                    feed_event: NEW,
                    secinfo_type: DFN_CERT_ADV,
                    status: STOP_REQUESTED,
                }}
            }}
            ) {{
                ok
            }}
        }}
        '''
        return query

    def compose_no_event_query(self):
        query = f'''
        mutation {{
            modifyAlert(input: {{
                id: "{self.alert_id}",
                name: "foo",
                condition: ALWAYS,
                method: START_TASK,
                eventData: {{
                    feed_event: NEW,
                    secinfo_type: DFN_CERT_ADV,
                    status: STOP_REQUESTED,
                }}
            }}
            ) {{
                ok
            }}
        }}
        '''
        return query

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            f'''
            mutation {{
                modifyAlert(input: {{
                    id: "{self.alert_id}",
                    name: "foo",
                }}) {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_modify_alert(self, mock_gmp: GmpMockFactory):

        mock_gmp.mock_response(self.cmd, self.xml)

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyAlert(input: {{
                    id: "{self.alert_id}",
                    name: "foo",
                    event: TASK_RUN_STATUS_CHANGED,
                    condition: ALWAYS,
                    method: START_TASK
                }}) {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_alert.assert_called_with(
            alert_id=str(self.alert_id),
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.START_TASK,
            comment=None,
            method_data=None,
            event_data=None,
            condition_data=None,
            filter_id=None,
        )

    def test_modify_alert_without_changes(self, mock_gmp: GmpMockFactory):

        mock_gmp.mock_response(self.cmd, self.xml)

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyAlert(input: {{
                    id: "{self.alert_id}",
                }}) {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_alert.assert_called_with(
            alert_id=str(self.alert_id),
            name=None,
            condition=None,
            event=None,
            method=None,
            comment=None,
            method_data=None,
            event_data=None,
            condition_data=None,
            filter_id=None,
        )

    def test_modify_alert_method_data_without_method(
        self, mock_gmp: GmpMockFactory
    ):
        mock_gmp.mock_response(self.cmd, self.xml)

        self.login('foo', 'bar')

        response = self.query(self.compose_no_method_query())

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_alert.assert_called_with(
            alert_id=str(self.alert_id),
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=None,
            comment=None,
            method_data=None,
            event_data=None,
            condition_data=None,
            filter_id=None,
        )

    def test_modify_alert_method_scp(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(self.cmd, self.xml)

        self.login('foo', 'bar')

        response = self.query(self.compose_method_query('SCP'))

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_alert.assert_called_with(
            alert_id=str(self.alert_id),
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.SCP,
            comment=None,
            method_data={
                'scp_host': 'localhost',
                'scp_known_hosts': '192.168.10.130',
                'scp_path': 'report.xml',
                'scp_report_format': str(self.id1),
                'scp_credential': str(self.id1),
                'delta_report_id': str(self.id1),
                'delta_type': 'Previous',
                'details_url': 'https://secinfo.greenbone.net/etc',
                'composer_include_notes': 'True',
                'composer_include_overrides': 'True',
            },
            event_data=None,
            condition_data=None,
            filter_id=None,
        )

    def test_modify_alert_method_send(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(self.cmd, self.xml)

        self.login('foo', 'bar')

        response = self.query(self.compose_method_query('SEND'))

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_alert.assert_called_with(
            alert_id=str(self.alert_id),
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.SEND,
            comment=None,
            method_data={
                'send_host': 'localhost',
                'send_port': '8080',
                'send_report_format': str(self.id1),
                'delta_report_id': str(self.id1),
                'delta_type': 'Previous',
                'details_url': 'https://secinfo.greenbone.net/etc',
                'composer_include_notes': 'True',
                'composer_include_overrides': 'True',
            },
            event_data=None,
            condition_data=None,
            filter_id=None,
        )

    def test_modify_alert_method_smb(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(self.cmd, self.xml)

        self.login('foo', 'bar')

        response = self.query(self.compose_method_query('SMB'))

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_alert.assert_called_with(
            alert_id=str(self.alert_id),
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.SMB,
            comment=None,
            method_data={
                'smb_credential': str(self.id1),
                'smb_file_path': 'report.xml',
                'smb_share_path': 'gvm-reports',
                'delta_report_id': str(self.id1),
                'delta_type': 'Previous',
                'details_url': 'https://secinfo.greenbone.net/etc',
                'composer_include_notes': 'True',
                'composer_include_overrides': 'True',
            },
            event_data=None,
            condition_data=None,
            filter_id=None,
        )

    def test_modify_alert_method_snmp(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(self.cmd, self.xml)

        self.login('foo', 'bar')

        response = self.query(self.compose_method_query('SNMP'))

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_alert.assert_called_with(
            alert_id=str(self.alert_id),
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.SNMP,
            comment=None,
            method_data={
                'snmp_agent': "localhost",
                'snmp_community': "public",
                'snmp_message': "$e",
                'delta_report_id': str(self.id1),
                'delta_type': 'Previous',
                'details_url': 'https://secinfo.greenbone.net/etc',
                'composer_include_notes': 'True',
                'composer_include_overrides': 'True',
            },
            event_data=None,
            condition_data=None,
            filter_id=None,
        )

    def test_modify_alert_method_syslog(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(self.cmd, self.xml)

        self.login('foo', 'bar')

        response = self.query(self.compose_method_query('SYSLOG'))

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_alert.assert_called_with(
            alert_id=str(self.alert_id),
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.SYSLOG,
            comment=None,
            method_data={
                'submethod': "syslog",
                'delta_report_id': str(self.id1),
                'delta_type': 'Previous',
                'details_url': 'https://secinfo.greenbone.net/etc',
                'composer_include_notes': 'True',
                'composer_include_overrides': 'True',
            },
            event_data=None,
            condition_data=None,
            filter_id=None,
        )

    def test_modify_alert_method_start_task(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(self.cmd, self.xml)

        self.login('foo', 'bar')

        response = self.query(self.compose_method_query('START_TASK'))

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_alert.assert_called_with(
            alert_id=str(self.alert_id),
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.START_TASK,
            comment=None,
            method_data={
                'start_task_task': str(self.id1),
                'delta_report_id': str(self.id1),
                'delta_type': 'Previous',
                'details_url': 'https://secinfo.greenbone.net/etc',
                'composer_include_notes': 'True',
                'composer_include_overrides': 'True',
            },
            event_data=None,
            condition_data=None,
            filter_id=None,
        )

    def test_modify_alert_method_http_get(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(self.cmd, self.xml)

        self.login('foo', 'bar')

        response = self.query(self.compose_method_query('HTTP_GET'))

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_alert.assert_called_with(
            alert_id=str(self.alert_id),
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.HTTP_GET,
            comment=None,
            method_data={
                'URL': 'foo.bar',
                'delta_report_id': str(self.id1),
                'delta_type': 'Previous',
                'details_url': 'https://secinfo.greenbone.net/etc',
                'composer_include_notes': 'True',
                'composer_include_overrides': 'True',
            },
            event_data=None,
            condition_data=None,
            filter_id=None,
        )

    def test_modify_alert_method_sourcefire_connector(
        self, mock_gmp: GmpMockFactory
    ):
        mock_gmp.mock_response(self.cmd, self.xml)

        self.login('foo', 'bar')

        response = self.query(self.compose_method_query('SOURCEFIRE_CONNECTOR'))

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_alert.assert_called_with(
            alert_id=str(self.alert_id),
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.SOURCEFIRE_CONNECTOR,
            comment=None,
            method_data={
                'defense_center_ip': '123.456.789.0',
                'defense_center_port': '8307',
                'pkcs12_credential': str(self.id1),
                'pkcs12': "MIILrgIBAzCCCy0GCSqGSIb3DQEHA",
            },
            event_data=None,
            condition_data=None,
            filter_id=None,
        )

    def test_modify_alert_method_verinice_connector(
        self, mock_gmp: GmpMockFactory
    ):
        mock_gmp.mock_response(self.cmd, self.xml)

        self.login('foo', 'bar')

        response = self.query(self.compose_method_query('VERINICE_CONNECTOR'))

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_alert.assert_called_with(
            alert_id=str(self.alert_id),
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.VERINICE_CONNECTOR,
            comment=None,
            method_data={
                'verinice_server_credential': str(self.id1),
                'verinice_server_report_format': str(self.id1),
                'verinice_server_url': "localhost",
                'delta_report_id': str(self.id1),
                'delta_type': 'Previous',
                'details_url': 'https://secinfo.greenbone.net/etc',
                'composer_include_notes': 'True',
                'composer_include_overrides': 'True',
            },
            event_data=None,
            condition_data=None,
            filter_id=None,
        )

    def test_modify_alert_method_email_notice_1(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(self.cmd, self.xml)

        self.login('foo', 'bar')

        response = self.query(self.compose_method_query('EMAIL'))

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_alert.assert_called_with(
            alert_id=str(self.alert_id),
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.EMAIL,
            comment=None,
            method_data={
                'from_address': 'foo@bar.com',
                'notice': '1',
                'recipient_credential': str(self.id1),
                'subject': "[GVM] Task '$n': $e",
                'to_address': 'foo@bar.com',
                'delta_report_id': str(self.id1),
                'delta_type': 'Previous',
                'details_url': 'https://secinfo.greenbone.net/etc',
                'composer_include_notes': 'True',
                'composer_include_overrides': 'True',
            },
            event_data=None,
            condition_data=None,
            filter_id=None,
        )

    def test_modify_alert_method_alemba_vfire(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(self.cmd, self.xml)

        self.login('foo', 'bar')

        response = self.query(self.compose_method_query('ALEMBA_VFIRE'))

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_alert.assert_called_with(
            alert_id=str(self.alert_id),
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.ALEMBA_VFIRE,
            comment=None,
            method_data={
                'delta_report_id': str(self.id1),
                'delta_type': 'Previous',
                'details_url': 'https://secinfo.greenbone.net/etc',
                'composer_include_notes': 'True',
                'composer_include_overrides': 'True',
                'vfire_base_url': "127.0.0.1",
                'vfire_call_impact_name': "five",
                'vfire_call_partition_name': "first partition",
                'vfire_call_template_name': "six",
                'vfire_call_type_name': "seven",
                'vfire_call_urgency_name': "eight",
                'vfire_client_id': "fakeID",
                'vfire_credential': "ebc2a770-f56b-41d2-a425-dfbe19402ebf",
                'report_formats': str(self.id1) + ', ' + str(self.id2),
            },
            event_data=None,
            condition_data=None,
            filter_id=None,
        )

    def test_modify_alert_method_tp_sms(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(self.cmd, self.xml)

        self.login('foo', 'bar')

        response = self.query(self.compose_method_query('TIPPINGPOINT'))

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_alert.assert_called_with(
            alert_id=str(self.alert_id),
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.TIPPINGPOINT,
            comment=None,
            method_data={
                'delta_report_id': str(self.id1),
                'delta_type': 'Previous',
                'details_url': 'https://secinfo.greenbone.net/etc',
                'composer_include_notes': 'True',
                'composer_include_overrides': 'True',
                'tp_sms_hostname': "fluffy",
                'tp_sms_tls_workaround': '0',
                'tp_sms_credential': str(self.id1),
                'tp_sms_tls_certificate': "a quick brown fox jumped",
            },
            event_data=None,
            condition_data=None,
            filter_id=None,
        )

    def test_modify_alert_method_email_notice_0(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(self.cmd, self.xml)

        self.login('foo', 'bar')

        response = self.query(self.compose_method_query('EMAIL', notice="0"))

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_alert.assert_called_with(
            alert_id=str(self.alert_id),
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.EMAIL,
            comment=None,
            method_data={
                'from_address': 'foo@bar.com',
                'notice': '0',
                'recipient_credential': str(self.id1),
                'subject': "[GVM] Task '$n': $e",
                'to_address': 'foo@bar.com',
                'message': "A quick brown fox jumped over the lazy dog.",
                'notice_report_format': str(self.id1),
                'delta_report_id': str(self.id1),
                'delta_type': 'Previous',
                'details_url': 'https://secinfo.greenbone.net/etc',
                'composer_include_notes': 'True',
                'composer_include_overrides': 'True',
            },
            event_data=None,
            condition_data=None,
            filter_id=None,
        )

    def test_modify_alert_method_email_notice_2(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(self.cmd, self.xml)

        self.login('foo', 'bar')

        response = self.query(self.compose_method_query('EMAIL', notice="2"))

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_alert.assert_called_with(
            alert_id=str(self.alert_id),
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.EMAIL,
            comment=None,
            method_data={
                'from_address': 'foo@bar.com',
                'notice': '2',
                'recipient_credential': str(self.id1),
                'subject': "[GVM] Task '$n': $e",
                'to_address': 'foo@bar.com',
                'notice_attach_format': str(self.id1),
                'message_attach': 'roses are red',
                'delta_report_id': str(self.id1),
                'delta_type': 'Previous',
                'details_url': 'https://secinfo.greenbone.net/etc',
                'composer_include_notes': 'True',
                'composer_include_overrides': 'True',
            },
            event_data=None,
            condition_data=None,
            filter_id=None,
        )

    def test_modify_alert_condition_data_without_condition(
        self, mock_gmp: GmpMockFactory
    ):
        mock_gmp.mock_response(self.cmd, self.xml)

        self.login('foo', 'bar')

        response = self.query(self.compose_no_condition_query())

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_alert.assert_called_with(
            alert_id=str(self.alert_id),
            name="foo",
            condition=None,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.START_TASK,
            comment=None,
            method_data=None,
            event_data=None,
            condition_data=None,
            filter_id=None,
        )

    def test_modify_alert_condition_always(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(self.cmd, self.xml)

        self.login('foo', 'bar')

        response = self.query(self.compose_condition_query('ALWAYS'))

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_alert.assert_called_with(
            alert_id=str(self.alert_id),
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.START_TASK,
            comment=None,
            method_data=None,
            event_data=None,
            condition_data=None,
            filter_id=None,
        )

    def test_modify_alert_condition_filter_count_at_least(
        self, mock_gmp: GmpMockFactory
    ):
        mock_gmp.mock_response(self.cmd, self.xml)

        self.login('foo', 'bar')

        response = self.query(
            self.compose_condition_query('FILTER_COUNT_AT_LEAST')
        )

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_alert.assert_called_with(
            alert_id=str(self.alert_id),
            name="foo",
            condition=AlertCondition.FILTER_COUNT_AT_LEAST,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.START_TASK,
            comment=None,
            method_data=None,
            event_data=None,
            condition_data={'count': '1'},
            filter_id=None,
        )

    def test_modify_alert_condition_severity_at_least(
        self, mock_gmp: GmpMockFactory
    ):
        mock_gmp.mock_response(self.cmd, self.xml)

        self.login('foo', 'bar')

        response = self.query(self.compose_condition_query('SEVERITY_AT_LEAST'))

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_alert.assert_called_with(
            alert_id=str(self.alert_id),
            name="foo",
            condition=AlertCondition.SEVERITY_AT_LEAST,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.START_TASK,
            comment=None,
            method_data=None,
            event_data=None,
            condition_data={'severity': '0.1'},
            filter_id=None,
        )

    def test_modify_alert_condition_severity_changed(
        self, mock_gmp: GmpMockFactory
    ):
        mock_gmp.mock_response(self.cmd, self.xml)

        self.login('foo', 'bar')

        response = self.query(self.compose_condition_query('SEVERITY_CHANGED'))

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_alert.assert_called_with(
            alert_id=str(self.alert_id),
            name="foo",
            condition=AlertCondition.SEVERITY_CHANGED,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.START_TASK,
            comment=None,
            method_data=None,
            event_data=None,
            condition_data={'direction': 'decreased'},
            filter_id=None,
        )

    def test_modify_alert_event_updated_secinfo(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(self.cmd, self.xml)

        self.login('foo', 'bar')

        response = self.query(
            self.compose_event_query('UPDATED_SECINFO_ARRIVED')
        )

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_alert.assert_called_with(
            alert_id=str(self.alert_id),
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.UPDATED_SECINFO_ARRIVED,
            method=AlertMethod.START_TASK,
            comment=None,
            method_data=None,
            event_data={'secinfo_type': 'dfn_cert_adv'},
            condition_data=None,
            filter_id=None,
        )

    def test_modify_alert_event_new_secinfo(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(self.cmd, self.xml)

        self.login('foo', 'bar')

        response = self.query(self.compose_event_query('NEW_SECINFO_ARRIVED'))

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_alert.assert_called_with(
            alert_id=str(self.alert_id),
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.NEW_SECINFO_ARRIVED,
            method=AlertMethod.START_TASK,
            comment=None,
            method_data=None,
            event_data={'secinfo_type': 'dfn_cert_adv'},
            condition_data=None,
            filter_id=None,
        )

    def test_modify_alert_event_task_status_changed(
        self, mock_gmp: GmpMockFactory
    ):
        mock_gmp.mock_response(self.cmd, self.xml)

        self.login('foo', 'bar')

        response = self.query(
            self.compose_event_query('TASK_RUN_STATUS_CHANGED')
        )

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_alert.assert_called_with(
            alert_id=str(self.alert_id),
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.START_TASK,
            comment=None,
            method_data=None,
            event_data={'status': 'Stop Requested'},
            condition_data=None,
            filter_id=None,
        )

    def test_modify_alert_event_ticket_received(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(self.cmd, self.xml)

        self.login('foo', 'bar')

        response = self.query(self.compose_event_query('TICKET_RECEIVED'))

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_alert.assert_called_with(
            alert_id=str(self.alert_id),
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TICKET_RECEIVED,
            method=AlertMethod.START_TASK,
            comment=None,
            method_data=None,
            event_data=None,
            condition_data=None,
            filter_id=None,
        )

    def test_modify_alert_event_owned_ticket_changed(
        self, mock_gmp: GmpMockFactory
    ):
        mock_gmp.mock_response(self.cmd, self.xml)

        self.login('foo', 'bar')

        response = self.query(self.compose_event_query('OWNED_TICKET_CHANGED'))

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_alert.assert_called_with(
            alert_id=str(self.alert_id),
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.OWNED_TICKET_CHANGED,
            method=AlertMethod.START_TASK,
            comment=None,
            method_data=None,
            event_data=None,
            condition_data=None,
            filter_id=None,
        )

    def test_modify_alert_event_data_without_event(
        self, mock_gmp: GmpMockFactory
    ):
        mock_gmp.mock_response(self.cmd, self.xml)

        self.login('foo', 'bar')

        response = self.query(self.compose_no_event_query())

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_alert.assert_called_with(
            alert_id=str(self.alert_id),
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=None,
            method=AlertMethod.START_TASK,
            comment=None,
            method_data=None,
            event_data=None,
            condition_data=None,
            filter_id=None,
        )

    def test_modify_alert_event_assigned_ticket_changed(
        self, mock_gmp: GmpMockFactory
    ):
        mock_gmp.mock_response(self.cmd, self.xml)

        self.login('foo', 'bar')

        response = self.query(
            self.compose_event_query('ASSIGNED_TICKET_CHANGED')
        )

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_alert.assert_called_with(
            alert_id=str(self.alert_id),
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.ASSIGNED_TICKET_CHANGED,
            method=AlertMethod.START_TASK,
            comment=None,
            method_data=None,
            event_data=None,
            condition_data=None,
            filter_id=None,
        )
