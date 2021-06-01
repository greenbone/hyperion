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

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class GetPreferenceTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                scanConfigPreference (name: "<type>:<Name of preference>",
                    nvtOid:"Some NVT OID",
                    configId: "daba56c8-73ec-11df-a475-002264764cea"
                ) {
                    name
                    value
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_nvt_preference(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_scan_config_preference',
            '''
            <get_preferences_response status="200" status_text="OK">
            <preference>
                <id>42</id>
                <hr_name>Name of preference</hr_name>
                <name>Name of preference</name>
                <type>radio</type>
                <value>Some value</value>
                <alt>Some alternative1</alt>
                <alt>Some alternative2</alt>
                <default>Some default</default>
            </preference>
            </get_preferences_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query{
            scanConfigPreference(name: "<type>:<Name of preference>",
                nvtOid:"Some NVT OID",
                configId: "daba56c8-73ec-11df-a475-002264764cea"
            ){
                    hrName
                    name
                    type
                    value
                    alternativeValues
                    default
            }
            }
        '''
        )

        self.assertResponseNoErrors(response)

        json = response.json()
        preference = json['data']['scanConfigPreference']

        self.assertEqual(preference['hrName'], 'Name of preference')
        self.assertEqual(preference['name'], 'Name of preference')
        self.assertEqual(preference['type'], 'radio')
        self.assertEqual(preference['value'], 'Some value')
        self.assertEqual(
            preference['alternativeValues'],
            ['Some alternative1', 'Some alternative2'],
        )
        self.assertEqual(preference['default'], 'Some default')

        mock_gmp.gmp_protocol.get_scan_config_preference.assert_called_with(
            name="<type>:<Name of preference>",
            nvt_oid="Some NVT OID",
            config_id="daba56c8-73ec-11df-a475-002264764cea",
        )
