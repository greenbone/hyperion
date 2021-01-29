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

from pathlib import Path

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory

CWD = Path(__file__).absolute().parent


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class ReportTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                report(id: "05d1edfa-3df8-11ea-9651-7b09b3acce77") {
                    id
                    name
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_report(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_report',
            '''
            <get_report_response>
                <report id="e501545c-0c4d-47d9-a9f8-28da34c6b958">
                    <name>a</name>
                </report>
            </get_report_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                report(id: "e501545c-0c4d-47d9-a9f8-28da34c6b958") {
                    id
                    name
                    owner
                }
            }
            '''
        )

        mock_gmp.gmp_protocol.get_report.assert_called_with(
            'e501545c-0c4d-47d9-a9f8-28da34c6b958',
            report_format_id=None,
            delta_report_id=None,
            details=True,
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        report = json['data']['report']

        self.assertEqual(report['name'], 'a')
        self.assertEqual(report['id'], 'e501545c-0c4d-47d9-a9f8-28da34c6b958')
        self.assertIsNone(report['owner'])

    def test_complex_report(self, mock_gmp: GmpMockFactory):
        report_xml_path = CWD / 'example-report-2.xml'
        report_xml_str = report_xml_path.read_text()

        mock_gmp.mock_response('get_report', report_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
        query {
            report(
                id: "52704aa8-0576-4a5c-993c-c4d25ca130f5"
                reportFormatId: "5057e5cc-b825-11e4-9d0e-28d24461215b"
            ) {
                id
                name
                owner
                comment
                creationTime
                modificationTime
                inUse
                writable
                reportFormat {
                    id
                }
                scanRunStatus
                closedCves {
                    counts {
                        current
                    }
                }
                vulnerabilities {
                    counts {
                        current
                    }
                }
                operatingSystems {
                    counts {
                        current
                    }
                }
                applications {
                    counts {
                        current
                    }
                }
                tlsCertificates {
                    counts {
                        current
                    }
                }
                task {
                    id
                    comment
                    target {
                        id
                        name
                        trash
                    }
                }
                timestamp
                timezone
                timezoneAbbrev
                portsCount {
                    current
                }
                ports {
                    port
                    host
                }
                resultsCount {
                    current
                    filtered
                    total
                }
                results {
                    name
                    comment
                    creationTime
                    host {
                        ip
                        id
                        hostname
                    }
                    port
                    threat
                    severity
                    qod {
                        value
                        type
                    }
                }
                severity {
                    total
                    filtered
                }
                hostsCount {
                    current
                }
                hosts {
                    ip
                    id
                    start
                    end
                    ports {
                        counts {
                            current
                        }
                    }
                    details {
                        name
                        value
                        source {
                            type
                            name
                            description
                        }
                        extra
                    }
                }
                scanStart
                scanEnd
                errors{
                    counts {
                        current
                    }
                    errors {
                        host {
                            name
                        }
                    }
                }
            }
        }
            '''
        )

        mock_gmp.gmp_protocol.get_report.assert_called_with(
            '52704aa8-0576-4a5c-993c-c4d25ca130f5',
            report_format_id='5057e5cc-b825-11e4-9d0e-28d24461215b',
            delta_report_id=None,
            details=True,
        )

        json = response.json()
        self.assertResponseNoErrors(response)

        report = json['data']['report']

        self.assertEqual(report['name'], 'Example')
        self.assertEqual(report['id'], '52704aa8-0576-4a5c-993c-c4d25ca130f5')
        self.assertEqual(report['owner'], 'admin')
        self.assertIsNone(report['comment'])
        self.assertEqual(report['creationTime'], '2020-02-24T13:30:54+00:00')
        self.assertEqual(
            report['modificationTime'], '2020-02-24T13:30:54+00:00'
        )
        self.assertFalse(report['inUse'])
        self.assertFalse(report['writable'])
        self.assertIsNotNone(report['reportFormat'])

        # inner report

        # report = report['report']

        self.assertEqual(
            report["reportFormat"]['id'], 'a994b278-1f62-11e1-96ac-406186ea4fc5'
        )

        self.assertEqual(report['timestamp'], '2021-01-07T12:48:31+01:00')
        self.assertEqual(report['timezone'], 'Europe/Berlin')
        self.assertEqual(report['timezoneAbbrev'], 'CET')

        self.assertIsNone(report['scanStart'])
        self.assertIsNone(report['scanEnd'])
        self.assertEqual(report['scanRunStatus'], "Done")

        self.assertIsNotNone(report['hostsCount'])
        self.assertIsNotNone(report['closedCves'])
        self.assertIsNotNone(report['vulnerabilities'])
        self.assertIsNotNone(report['operatingSystems'])
        self.assertIsNotNone(report['applications'])
        self.assertIsNotNone(report['tlsCertificates'])
        self.assertIsNotNone(report['resultsCount'])
        self.assertIsNotNone(report['results'])

        results = report['results']

        self.assertIsNotNone(results)

        self.assertIsNotNone(report['task'])

        self.assertEqual(report['severity']['total'], 5.0)
        self.assertEqual(report['severity']['filtered'], 5.0)

        self.assertEqual(report['errors']['counts']['current'], 0)
        self.assertListEqual(report['errors']['errors'], [])

    def test_report_sub_objects(self, mock_gmp: GmpMockFactory):
        report_xml_path = CWD / 'example-report-2.xml'
        report_xml_str = report_xml_path.read_text()

        mock_gmp.mock_response('get_report', report_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
        query {
            report(id: "52704aa8-0576-4a5c-993c-c4d25ca130f5") {
                id
                name
                owner
                comment
                creationTime
                modificationTime
                inUse
                writable
                reportFormat {
                    id
                    name
                }
                scanRunStatus
                closedCves {
                    counts {
                        current
                    }
                }
                vulnerabilities {
                    counts {
                        current
                    }
                }
                operatingSystems {
                    counts {
                        current
                    }
                }
                applications {
                    counts {
                        current
                    }
                }
                tlsCertificates {
                    counts {
                        current
                    }
                }
                task {
                    id
                    comment
                    name
                    target {
                        id
                        name
                        trash
                    }
                }
                timestamp
                timezone
                timezoneAbbrev
                portsCount {
                    current
                }
                ports {
                    port
                    host
                }
                resultsCount {
                    current
                    filtered
                    total
                }
                results {
                    name
                    comment
                    scanNvtVersion
                    originalThreat
                    originalSeverity
                    creationTime
                    host {
                        ip
                        id
                        hostname
                    }
                    port
                    nvt {
                        name
                        family
                        cvssBase
                        refs {
                            warning
                            refList{
                                id
                                type
                            }
                        }
                        tags {
                            cvssBaseVector
                            summary
                            insight
                            impact
                            affected
                            vuldetect
                        }
                        severities {
                            score
                            severitiesList {
                                type
                                score
                                vector
                            }
                        }
                    }
                    threat
                    severity
                    qod {
                        value
                        type
                    }
                }
                severity {
                    total
                    filtered
                }
                hostsCount {
                    current
                }
                hosts{
                    ip
                    id
                    start
                    end
                    ports {
                        counts {
                            current
                        }
                    }
                    results {
                        counts {
                            current
                            high
                            medium
                            low
                            log
                            falsePositive
                        }
                    }
                    details {
                        name
                        value
                        source {
                            type
                            name
                            description
                        }
                        extra
                    }
                }
                scanStart
                scanEnd
                errors{
                    errors {
                        host {
                            name
                        }
                    }
                }
            }
        }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.get_report.assert_called_with(
            '52704aa8-0576-4a5c-993c-c4d25ca130f5',
            report_format_id=None,
            delta_report_id=None,
            details=True,
        )

        # outer report

        report = json['data']['report']

        self.assertEqual(report['name'], 'Example')
        self.assertEqual(report['id'], '52704aa8-0576-4a5c-993c-c4d25ca130f5')
        self.assertEqual(report['owner'], 'admin')
        self.assertIsNone(report['comment'])

        # inner report

        # report0 = report['report']

        # task

        task = report['task']
        self.assertIsNotNone(task)

        self.assertEqual(task['id'], 'a5a4d348-95a2-42ee-bc25-730a78c943c3')
        self.assertEqual(task['name'], 'sd')
        self.assertEqual(task['comment'], 'sd')

        # hosts

        self.assertIsNotNone(report['hostsCount'])

        self.assertEqual(report['hostsCount']['current'], 2)

        hosts = report['hosts']
        self.assertIsNotNone(hosts)
        self.assertEqual(len(hosts), 1)

        host0 = hosts[0]
        self.assertEqual(host0['ip'], '127.0.0.1')
        self.assertEqual(host0['id'], '1533f9fe-6c82-4388-a0cd-6f947af87314')

        port_counts = host0['ports']['counts']
        self.assertIsNotNone(port_counts)
        self.assertEqual(port_counts['current'], 1)

        result_counts = host0['results']['counts']
        self.assertIsNotNone(result_counts)
        self.assertEqual(result_counts['current'], 1)
        self.assertEqual(result_counts['high'], 0)
        self.assertEqual(result_counts['medium'], 1)
        self.assertEqual(result_counts['low'], 0)
        self.assertEqual(result_counts['log'], 0)
        self.assertEqual(result_counts['falsePositive'], 0)

        # ports

        self.assertIsNotNone(report['portsCount'])
        self.assertIsNotNone(report['ports'])

        port_counts = report['portsCount']
        ports = report['ports']

        self.assertEqual(port_counts['current'], 3)

        self.assertEqual(ports[0]['port'], '63410/udp')
        self.assertEqual(ports[0]['host'], '127.0.0.1')

        # results

        self.assertIsNotNone(report['resultsCount'])
        self.assertIsNotNone(report['results'])

        result_counts = report['resultsCount']
        results = report['results']

        self.assertEqual(result_counts['current'], 5)
        self.assertEqual(result_counts['total'], 5)
        self.assertEqual(result_counts['filtered'], 1)

        result0 = results[0]

        self.assertEqual(result0['name'], '/doc directory browsable')
        self.assertIsNone(result0['comment'])

        self.assertIsNone(result0['scanNvtVersion'])
        self.assertEqual(result0['originalThreat'], 'Medium')
        self.assertEqual(result0['originalSeverity'], 5.0)
        self.assertEqual(result0['threat'], 'Medium')
        self.assertEqual(result0['severity'], 5.0)

        self.assertIsNotNone(result0['qod'])

        qod = result0['qod']

        self.assertEqual(qod['value'], 75)
        self.assertIsNone(qod['type'])

        self.assertIsNotNone(result0['host'])

        rhost = result0['host']

        self.assertEqual(rhost['ip'], '127.0.0.1')
        self.assertEqual(rhost['hostname'], 'host1.example.com')
        self.assertEqual(rhost['id'], '1533f9fe-6c82-4388-a0cd-6f947af87314')

        self.assertIsNotNone(result0['nvt'])

        nvt = result0['nvt']

        self.assertEqual(nvt['name'], '/doc directory browsable')
        self.assertEqual(nvt['family'], 'Web application abuses')
        self.assertEqual(nvt['cvssBase'], '5.0')
        self.assertEqual(
            nvt['refs'],
            {
                "warning": None,
                "refList": [
                    {"id": "CVE-1999-0678", "type": "cve"},
                    {"id": "318", "type": "bid"},
                ],
            },
        )

        severities = nvt['severities']
        self.assertEqual(severities['score'], 50)
        self.assertEqual(
            severities['severitiesList'][0]['type'], 'cvss_base_v2'
        )

    def test_delta_report(self, mock_gmp: GmpMockFactory):
        report_xml_path = CWD / 'example-report.xml'
        report_xml_str = report_xml_path.read_text()

        mock_gmp.mock_response('get_report', report_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                report(
                    id:"e501545c-0c4d-47d9-a9f8-28da34c6b958"
                    deltaReportId:"88f353d3-4535-49a3-a4f7-fdc427af29cb"
                ) {
                    id
                    task{
                        id
                    }
                    deltaReport {
                        id
                        scanRunStatus
                        timestamp
                        scanStart
                        scanEnd
                    }
                    hosts {
                        ip
                        details {
                            name
                        }
                    }
                    results {
                        id
                        host {
                            ip
                            id
                            hostname
                        }
                        threat
                        severity
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.get_report.assert_called_with(
            'e501545c-0c4d-47d9-a9f8-28da34c6b958',
            report_format_id=None,
            delta_report_id='88f353d3-4535-49a3-a4f7-fdc427af29cb',
            details=True,
        )

        # outer report
        report = json['data']['report']

        self.assertEqual(report['id'], 'e501545c-0c4d-47d9-a9f8-28da34c6b958')
        # self.assertIsNotNone(report['report'])

        # inner report
        # report0 = report['report']

        self.assertIsNotNone(report['deltaReport'])

        delta = report['deltaReport']

        # self.assertIsNotNone(delta['report'])

        # delta report
        # dreport = delta['report']

        self.assertEqual(delta['id'], '88f353d3-4535-49a3-a4f7-fdc427af29cb')
        self.assertEqual(delta['scanRunStatus'], 'Done')
        self.assertEqual(delta['timestamp'], '2020-02-24T13:30:47+00:00')
        self.assertEqual(delta['scanStart'], '2020-02-24T13:30:48+00:00')
        self.assertEqual(delta['scanEnd'], '2020-02-24T13:30:48+00:00')
