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

# pylint: disable=line-too-long
from pathlib import Path

from unittest.mock import patch

from gvm.protocols.next import InfoType as GvmInfoType

from selene.tests import SeleneTestCase, GmpMockFactory

from selene.tests.entity import make_test_get_entity

CWD = Path(__file__).absolute().parent


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class CertBundTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                certBundAdvisory(id: "CVE-1999-0001") {
                    id
                    name
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_cert_bund_advisory(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_info',
            '''
            <get_info_response>
                <info id="CB-K13/0093">
                    <name>foo</name>
                </info>
            </get_info_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                certBundAdvisory(id: "CB-K13/0093") {
                    id
                    name
                    owner
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        cert_bund = json['data']['certBundAdvisory']

        self.assertEqual(cert_bund['id'], 'CB-K13/0093')
        self.assertEqual(cert_bund['name'], 'foo')
        self.assertIsNone(cert_bund['owner'])

    def test_get_cert_bund_advisory_none_fields(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_info',
            '''
            <get_info_response>
                <info id="CB-K13/0093">
                    <name>foo</name>
                </info>
            </get_info_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                certBundAdvisory(id: "CB-K13/0093") {
                    id
                    name
                    owner
                    updateTime
                    description
                    cveRefs
                    cves
                    categories
                    infos {
                        infoIssuer
                        infoUrl
                    }
                    effect
                    remoteAttack
                    platform
                    referenceNumber
                    referenceId
                    referenceUrl
                    referenceSource
                    risk
                    software
                    revisions {
                        date
                        description
                        number
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        cert_bund = json['data']['certBundAdvisory']

        self.assertEqual(cert_bund['id'], 'CB-K13/0093')
        self.assertEqual(cert_bund['name'], 'foo')
        self.assertIsNone(cert_bund['owner'])
        self.assertIsNone(cert_bund['updateTime'])
        self.assertIsNone(cert_bund['description'])
        self.assertIsNone(cert_bund['cveRefs'])
        self.assertIsNone(cert_bund['cves'])
        self.assertIsNone(cert_bund['categories'])
        self.assertIsNone(cert_bund['infos'])
        self.assertIsNone(cert_bund['effect'])
        self.assertFalse(cert_bund['remoteAttack'])
        self.assertIsNone(cert_bund['platform'])
        self.assertIsNone(cert_bund['referenceNumber'])
        self.assertIsNone(cert_bund['referenceId'])
        self.assertIsNone(cert_bund['referenceUrl'])
        self.assertIsNone(cert_bund['risk'])
        self.assertIsNone(cert_bund['software'])
        self.assertIsNone(cert_bund['revisions'])

    def test_complex_cert_bund(self, mock_gmp: GmpMockFactory):
        cert_bund_xml_path = CWD / 'example-cert-bund.xml'
        cert_bund_xml_str = cert_bund_xml_path.read_text()

        mock_gmp.mock_response('get_info', cert_bund_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                certBundAdvisory(id: "CB-K13/0093") {
                    id
                    name
                    updateTime
                    description
                    cveRefs
                    cves
                    categories
                    infos {
                        infoIssuer
                        infoUrl
                    }
                    effect
                    remoteAttack
                    platform
                    referenceNumber
                    referenceId
                    referenceUrl
                    referenceSource
                    risk
                    software
                    title
                    revisions {
                        date
                        description
                        number
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        cert_bund = json['data']['certBundAdvisory']

        self.assertEqual(cert_bund['id'], 'CB-K13/0093')
        self.assertEqual(cert_bund['updateTime'], '2020-12-01T02:30:00+00:00')
        self.assertEqual(
            cert_bund['description'],
            '''GnuTLS (GNU Transport Layer Security Library) ist eine im Quelltext frei verfügbare Bibliothek, die Secure Sockets Layer (SSL) und Transport Layer Security (TLS) implementiert.
OpenSSL ist eine im Quelltext frei verfügbare Bibliothek, die Secure Sockets Layer (SSL) und Transport Layer Security (TLS) implementiert.Ein entfernter, anonymer Angreifer aus dem lokalen Netzwerk kann eine Schwachstelle in SSL, TLS und DTLS ausnutzen, um Sicherheitsvorkehrungen zu umgehen.''',
        )
        self.assertEqual(cert_bund['cveRefs'], 4)
        self.assertEqual(
            cert_bund['cves'],
            [
                'CVE-2013-0169',
                'CVE-2013-1618',
                'CVE-2013-1619',
                'CVE-2013-1620',
            ],
        )

        self.assertEqual(
            cert_bund['platform'], 'Applicance, Linux, UNIX, Windows'
        )
        self.assertEqual(cert_bund['referenceNumber'], 24)
        self.assertEqual(cert_bund['referenceId'], 'CB-K13/0093')
        self.assertEqual(
            cert_bund['referenceSource'],
            'Oracle Linux Security Advisory ELSA-2019-4747 vom 2019-08-16',
        )
        self.assertEqual(
            cert_bund['referenceUrl'],
            'http://linux.oracle.com/errata/ELSA-2019-4747.html',
        )
        self.assertEqual(cert_bund['remoteAttack'], True)
        self.assertEqual(cert_bund['effect'], 'SecurityWorkaround')
        self.assertEqual(cert_bund['risk'], 'medium')
        self.assertEqual(
            cert_bund['title'],
            'SSL, TLS, DTLS: Schwachstelle ermöglicht'
            ' Umgehen von Sicherheitsvorkehrungen',
        )

        self.assertEqual(
            cert_bund['categories'],
            [
                "Anwendung/Clients/Browser/Opera",
                "Betriebssystem/Linux_Unix",
                "Hardware",
                "Hardware",
                "Hardware",
                "Hardware",
                "Hardware",
                "Hardware",
                "Betriebssystem/Linux_Unix/Solaris",
                "Betriebssystem/Linux_Unix/Solaris",
                "Betriebssystem/Linux_Unix/Solaris",
                "Betriebssystem/Linux_Unix/Solaris",
                "Anwendung/Security/Crypto/GnuTLS",
                "Anwendung/Security/Crypto/GnuTLS",
                "Anwendung/Security/Crypto/GnuTLS",
                "Anwendung/Security/Crypto/OpenSSL",
                "Hardware",
                "Hardware",
                "Hardware",
                "Anwendung/Server/Backup_Storage/Tivoli_Storage_Manager",
                "Anwendung/Server/Backup_Storage/Tivoli_Storage_Manager",
                "Anwendung/Server/Backup_Storage/Tivoli_Storage_Manager",
                "Anwendung/Server/Backup_Storage/Tivoli_Storage_Manager",
                "Betriebssystem/Linux_Unix/SuSE",
                "Anwendung/Server/Web_Proxy_Fileserver/Apache_Webserver",
                "Anwendung/Server/Web_Proxy_Fileserver/Apache_Webserver",
                "Anwendung/Server/Web_Proxy_Fileserver/Apache_Webserver",
                "Anwendung/Server/Web_Proxy_Fileserver/Apache_Webserver",
            ],
        )
        self.assertIsNotNone(cert_bund['infos'])
        infos = cert_bund['infos']

        self.assertEqual(
            infos[0]['infoIssuer'],
            'Forschungsarbeit &quot;Lucky Thirteen: Breaking the TLS and DTLS Record Protocols&quot; vom 2013-02-04',
        )
        self.assertEqual(infos[0]['infoUrl'], 'http://www.isg.rhul.ac.uk/tls/')

        self.assertIsNotNone(cert_bund['revisions'])
        revisions = cert_bund['revisions']

        self.assertEqual(revisions[0]['date'], '2019-08-19T13:30:00+01:00')
        self.assertEqual(
            revisions[0]['description'],
            'Neue Updates von Oracle Linux aufgenommen',
        )
        self.assertEqual(revisions[0]['number'], 69)


class CertBundAdvisoryGetEntityTestCase(SeleneTestCase):
    gmp_name = 'info'
    selene_name = 'certBundAdvisory'
    test_get_entity = make_test_get_entity(
        gmp_name,
        selene_name=selene_name,
        info_type=GvmInfoType.CERT_BUND_ADV,
    )
