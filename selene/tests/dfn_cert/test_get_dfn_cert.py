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

# pylint: disable=line-too-long

from pathlib import Path

from unittest.mock import patch

from gvm.protocols.latest import InfoType as GvmInfoType

from selene.tests import SeleneTestCase, GmpMockFactory

from selene.tests.entity import make_test_get_entity

CWD = Path(__file__).absolute().parent


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class DFNCertAdvisoryTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                dfnCertAdvisory(id: "DFN-CERT-2008-0644") {
                    id
                    name
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_dfn_cert_advisory(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_info',
            '''
            <get_info_response>
                <info id="DFN-CERT-2008-0644">
                    <name>foo</name>
                </info>
            </get_info_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                dfnCertAdvisory(id:"DFN-CERT-2008-0644") {
                    id
                    name
                    owner
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        dfn_cert_advisory = json['data']['dfnCertAdvisory']

        self.assertEqual(
            dfn_cert_advisory['id'],
            'DFN-CERT-2008-0644',
        )
        self.assertEqual(dfn_cert_advisory['name'], 'foo')
        self.assertIsNone(dfn_cert_advisory['owner'])

    def test_complex_dfn_cert_advisory(self, mock_gmp: GmpMockFactory):
        dfn_cert_advisory_xml_path = CWD / 'example-dfn-cert.xml'
        dfn_cert_advisory_xml_str = dfn_cert_advisory_xml_path.read_text()

        mock_gmp.mock_response('get_info', dfn_cert_advisory_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                dfnCertAdvisory(id:
                    "DFN-CERT-2008-0644"
                ) {
                    id
                    name
                    updateTime
                    title
                    summary
                    maxCvss
                    cveRefs
                    cves
                    link
                    author {
                        name
                        uri
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        dfn_cert_advisory = json['data']['dfnCertAdvisory']

        self.assertEqual(
            dfn_cert_advisory['name'],
            'DFN-CERT-2008-0644',
        )
        self.assertEqual(
            dfn_cert_advisory['id'],
            'DFN-CERT-2008-0644',
        )
        self.assertEqual(
            dfn_cert_advisory['title'],
            'Schwachstelle im HP Software Update (Windows)',
        )
        self.assertEqual(
            dfn_cert_advisory['summary'],
            '''Aufgrund mehrerer fehlerhafter ActiveX Controls im HP Software Update
kann ein entfernter Angreifer im schlimmsten Fall beliebige Befehle
mit den Rechten der Anwendung ausführen.''',
        )
        self.assertEqual(dfn_cert_advisory['maxCvss'], 6.8)
        self.assertEqual(dfn_cert_advisory['cveRefs'], 1)
        self.assertEqual(
            dfn_cert_advisory['link'],
            'https://adv-archiv.dfn-cert.de/adv/2008-0644/',
        )
        self.assertEqual(dfn_cert_advisory['cves'], ['CVE-2008-0712'])
        self.assertEqual(dfn_cert_advisory['cveRefs'], 1)
        self.assertEqual(dfn_cert_advisory['cveRefs'], 1)

        self.assertIsNotNone(dfn_cert_advisory['author'])
        author = dfn_cert_advisory['author']

        self.assertEqual(author['name'], 'DFN-CERT Services GmbH')


class DFNCertAdvisoryGetEntityTestCase(SeleneTestCase):
    gmp_name = 'info'
    selene_name = 'dfnCertAdvisory'
    test_get_entity = make_test_get_entity(
        gmp_name,
        selene_name=selene_name,
        info_type=GvmInfoType.DFN_CERT_ADV,
    )
