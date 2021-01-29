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

from uuid import uuid4

from unittest.mock import patch
from gvm.protocols.latest import InfoType as GvmInfoType

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class ExportDfnCertAdvisoriesByIdsTestCase(SeleneTestCase):
    def setUp(self):
        self.id1 = uuid4()
        self.id2 = uuid4()

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            f'''
            mutation {{
                exportDfnCertAdvisoriesByIds(ids:
                    ["{self.id1}", "{self.id2}"])
                {{
                   exportedEntities
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_export_dfn_cert_advisories_by_ids(self, mock_gmp: GmpMockFactory):
        self.login('foo', 'bar')

        mock_xml = (
            '<get_info_list_response status="200" status_text="OK">'
            f'<info id="{self.id1}">'
            '<name>some_name1</name>'
            '</info>'
            f'<info id="{self.id2}">'
            '<name>some_name2</name>'
            '</info>'
            '</get_info_list_response>'
        )

        mock_gmp.mock_response('get_info_list', mock_xml)

        response = self.query(
            f'''
            mutation {{
                exportDfnCertAdvisoriesByIds(
                    ids: ["{self.id1}", "{self.id2}"])
                {{
                   exportedEntities
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        oval_definitions_xml = json['data']['exportDfnCertAdvisoriesByIds'][
            'exportedEntities'
        ]

        self.assertEqual(mock_xml, oval_definitions_xml)
        mock_gmp.gmp_protocol.get_info_list.assert_called_with(
            filter=f'uuid= uuid={self.id1} uuid={self.id2} ',
            details=True,
            info_type=GvmInfoType.DFN_CERT_ADV,
        )

    def test_export_dfn_cert_advisories_empty_ids_array(
        self, mock_gmp: GmpMockFactory
    ):
        self.login('foo', 'bar')

        mock_xml = (
            '<get_info_list_response status=\"200\" status_text=\"OK\">'
            '<filters id=\"\"><term>uuid= first=1 rows=10 sort=name</term>'
            '<keywords><keyword><column>uuid</column><relation>=</relation>'
            '<value /></keyword><keyword><column>first</column><relation>'
            '=</relation><value>1</value></keyword><keyword><column>rows'
            '</column><relation>=</relation><value>10</value></keyword>'
            '<keyword><column>sort</column><relation>=</relation><value>name'
            '</value></keyword></keywords></filters><sort><field>name<order>'
            'ascending</order></field></sort><info_list max=\"10\" '
            'start=\"1\" /><info_count>16<filtered>0</filtered>'
            '<page>0</page></info_count></get_info_list_response>'
        )
        mock_gmp.mock_response('get_info_list', bytes(mock_xml, 'utf-8'))

        response = self.query(
            '''
            mutation {
                exportDfnCertAdvisoriesByIds(ids: []) {
                   exportedEntities
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        oval_definitions_xml = json['data']['exportDfnCertAdvisoriesByIds'][
            'exportedEntities'
        ]

        self.assertEqual(mock_xml, oval_definitions_xml)

        mock_gmp.gmp_protocol.get_info_list.assert_called_with(
            filter='uuid= ', details=True, info_type=GvmInfoType.DFN_CERT_ADV
        )
