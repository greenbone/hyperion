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
class GetScanConfigsNvtsTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                scanConfigNvts {
                    id
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_nvts(self, mock_gmp: GmpMockFactory):
        nvt_xml_path = CWD / 'example-scan-config-nvt.xml'
        nvt_xml_str = nvt_xml_path.read_text()

        mock_gmp.mock_response('get_nvts', nvt_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                scanConfigNvts (details:true) {
                    id
                    name
                    creationTime
                    modificationTime
                    category
                    summary
                    family
                    cvssBase
                    qod {
                        value
                        type
                    }
                    score
                    severities {
                        date
                        origin
                        score
                        type
                        vector
                    }
                    referenceWarning
                    certReferences{
                        id
                        type
                    }
                    cveReferences{
                        id
                        type
                    }
                    bidReferences{
                        id
                        type
                    }
                    otherReferences{
                        id
                        type
                    }
                    tags {
                        cvssBaseVector
                        summary
                        insight
                        impact
                        affected
                        vuldetect
                    }
                    preferenceCount
                    timeout
                    defaultTimeout
                    solution {
                    type
                    method
                    description
                    }
                    preferences {
                        nvt {
                            id
                            name
                        }
                        name
                        type
                        value
                        alt
                        default
                        hrName
                        id
                    }
                }
            }
            '''
        )

        json_response = response.json()
        self.assertResponseNoErrors(response)
        nvt = json_response['data']['scanConfigNvts'][0]

        self.assertEqual(nvt['id'], "1.3.6.1.4.1.25623.1.0.100315")
        self.assertEqual(nvt['name'], 'Some name')
        self.assertEqual(nvt['creationTime'], '2009-10-26T09:02:32Z')
        self.assertEqual(nvt['modificationTime'], '2020-05-11T05:36:14Z')
        self.assertEqual(nvt['category'], 1)
        self.assertEqual(nvt['summary'], 'Some summary')
        self.assertEqual(nvt['family'], 'Some family')
        self.assertEqual(nvt['cvssBase'], 5.0)
        self.assertEqual(nvt['score'], 50)
        self.assertEqual(
            nvt['qod'],
            {"value": 80, "type": "remote_banner"},
        )
        self.assertEqual(
            nvt['severities'],
            [
                {
                    "date": "2009-10-26T09:02:32+00:00",
                    "origin": "CVE-2011-9999",
                    "score": 50,
                    "type": "cvss_base_v2",
                    "vector": "AV:N/AC:M/Au:N/C:N/I:P/A:P",
                }
            ],
        )
        self.assertEqual(nvt['referenceWarning'], 'database not available')
        self.assertEqual(
            nvt['certReferences'],
            [
                {"id": "54321", "type": "cert-bund"},
                {"id": "12345", "type": "dfn-cert"},
            ],
        )
        self.assertEqual(
            nvt['bidReferences'],
            [
                {"id": "BID1337", "type": "bid"},
                {"id": "BID31337", "type": "bugtraq_id"},
            ],
        )
        self.assertEqual(
            nvt['otherReferences'],
            [
                {"id": "http://test.test", "type": "url"},
            ],
        )
        self.assertEqual(
            nvt['cveReferences'],
            [
                {"id": "CVE-2014-0682", "type": "cve"},
                {"id": "CVE-2014-0681", "type": "cve_id"},
            ],
        )
        self.assertIsNotNone(nvt['tags'])
        tags = nvt['tags']
        self.assertEqual(tags['cvssBaseVector'], 'vec')
        self.assertEqual(tags['summary'], 'sum')
        self.assertEqual(tags['insight'], 'ins')
        self.assertEqual(tags['impact'], 'imp')
        self.assertEqual(tags['affected'], 'aff')
        self.assertEqual(tags['vuldetect'], 'vul')

        self.assertEqual(nvt['preferenceCount'], -1)
        self.assertEqual(nvt['timeout'], None)
        self.assertEqual(nvt['defaultTimeout'], None)
        self.assertEqual(
            nvt['solution'],
            {
                "type": "VendorFix",
                "method": "",
                "description": "Just update.",
            },
        )

        self.assertEqual(
            nvt['preferences'],
            [
                {
                    "name": "Log failed nmap calls",
                    "id": 13,
                    "nvt": {
                        "name": "Ping Host",
                        "id": "1.3.6.1.4.1.25623.1.0.100315",
                    },
                    "hrName": "Log failed nmap calls",
                    "type": "checkbox",
                    "value": "no",
                    "default": "no",
                    "alt": None,
                },
                {
                    "name": "nmap timing policy",
                    "id": 14,
                    "nvt": {
                        "name": "Ping Host",
                        "id": "1.3.6.1.4.1.25623.1.0.100315",
                    },
                    "hrName": "nmap timing policy",
                    "type": "radio",
                    "value": "Normal",
                    "default": "Normal",
                    "alt": ["Paranid", "Sneaky"],
                },
            ],
        )

        mock_gmp.gmp_protocol.get_nvts.assert_called_with(
            config_id=None,
            details=True,
            family=None,
            preference_count=None,
            preferences=None,
            preferences_config_id=None,
            sort_field=None,
            sort_order=None,
            timeout=None,
        )
