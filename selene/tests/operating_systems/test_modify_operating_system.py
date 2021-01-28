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
class ModifyOperatingSystemTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        operating_system_id = str(uuid4())
        response = self.query(
            f'''
            mutation {{
                modifyOperatingSystem(input: {{
                    id: "{operating_system_id}",
                    comment: "foo",
                }}) {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_modify_asset(self, mock_gmp: GmpMockFactory):
        operating_system_id = str(uuid4())

        mock_gmp.mock_response(
            'modify_asset',
            '''
            <modify_asset_response status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyOperatingSystem(input: {{
                    id: "{operating_system_id}",
                    comment: "bar"
                    }}) {{
                    ok
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['modifyOperatingSystem']['ok']

        self.assertEqual(ok, True)

        mock_gmp.gmp_protocol.modify_asset.assert_called_with(
            asset_id=str(operating_system_id),
            comment="bar",
        )
