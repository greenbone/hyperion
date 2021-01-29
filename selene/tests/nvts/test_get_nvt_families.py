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

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class GetNvtFamiliesTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                nvtFamilies(sortOrder:"descending"){
                    name
                    maxNvtCount
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_nvt_families(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_nvt_families',
            '''
            <get_nvt_families_response status="200" status_text="OK">
                <families>
                    <family>
                    <name>Windows : Microsoft Bulletins</name>
                    <max_nvt_count>3031</max_nvt_count>
                    </family>
                    <family>
                    <name>Windows</name>
                    <max_nvt_count>248</max_nvt_count>
                    </family>
                </families>
            </get_nvt_families_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                nvtFamilies(sortOrder:"descending"){
                    name
                    maxNvtCount
                }
            }
            '''
        )

        json_response = response.json()

        self.assertResponseNoErrors(response)
        self.assertEqual(
            json_response['data']['nvtFamilies'],
            [
                {"name": "Windows : Microsoft Bulletins", "maxNvtCount": 3031},
                {"name": "Windows", "maxNvtCount": 248},
            ],
        )

        mock_gmp.gmp_protocol.get_nvt_families.assert_called_with(
            sort_order="descending"
        )
