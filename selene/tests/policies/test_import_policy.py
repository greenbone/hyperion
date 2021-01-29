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
class ImportPolicyTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            mutation {
                importPolicy(policy: "xml_of_policy") {
                   id
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_import_policy(self, mock_gmp: GmpMockFactory):
        self.login('foo', 'bar')

        policy_xml = (
            '<get_configs_response status=\\"200\\" status_text=\\"OK\\">'
            '<config id=\\"d21f4c81-2b88-4ac1-b7b4-a2a9f2ad4663\\">'
            '<name>\\"Name\\"</name>'
            '<nvt_selectors>'
            '<nvt_selector>'
            '<name>f187d4cf-a157-471c-81a6-74990b5da181</name>'
            '<include>1</include>'
            '<type>2</type>'
            '<family_or_nvt>1.3.6.1.4.1.25623.1.0.100315'
            '</family_or_nvt>'
            '</nvt_selector>'
            '</nvt_selectors>'
            '<preferences></preferences>'
            '</config>'
            '</get_configs_response>'
        )

        response_xml = (
            '<create_config_response status="201" status_text="OK,'
            'resource created" id="1dc12755-564a-4344-bf5e-e9c457329a48">'
            '<config id="1dc12755-564a-4344-bf5e-e9c457329a48">'
            '<name>"Name" 2</name>'
            '</config>'
            '</create_config_response>'
        )

        mock_gmp.mock_response('import_config', response_xml)

        response = self.query(
            f'''
            mutation {{
                importPolicy(policy: "{policy_xml}")
                {{
                   id
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        id_new_policy = json['data']['importPolicy']['id']

        self.assertEqual(id_new_policy, "1dc12755-564a-4344-bf5e-e9c457329a48")

        mock_gmp.gmp_protocol.import_config.assert_called_with(
            config=policy_xml.replace('\\', '')
        )
