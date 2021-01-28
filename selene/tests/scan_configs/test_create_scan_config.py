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

from uuid import uuid4

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class CreateScanConfigTestCase(SeleneTestCase):
    def setUp(self):
        self.id1 = uuid4()
        self.id2 = uuid4()

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            f'''
            mutation {{
                createScanConfig( input: {{
                        configId: "{self.id1}",
                        name: "some_name",
                        comment: "some_comment"}}) {{
                    id
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_create_scan_config(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'create_config',
            f'''
            <create_config_response status="201" status_text="OK,
             resource created" id="{self.id2}"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                createScanConfig(input: {{
                        configId: "{self.id1}",
                        name: "some_name",
                        comment: "some_comment"}}) {{
                    id
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        created_config_id = json['data']['createScanConfig']['id']

        self.assertEqual(created_config_id, str(self.id2))

        mock_gmp.gmp_protocol.create_config.assert_called_with(
            config_id=str(self.id1), name='some_name', comment='some_comment'
        )
