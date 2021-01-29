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

from gvm.protocols.latest import PortRangeType as GvmPortRangeType

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class CreatePortListTestCase(SeleneTestCase):
    def setUp(self):
        self.port_list_id = uuid4()
        self.uuid = uuid4()

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            f'''
            mutation {{
                createPortRange(input: {{
                    portListId: "{str(self.port_list_id)}",
                    start: 3,
                    end: 15,
                    portRangeType: TCP,
                    comment: "port range",
                }}) {{
                    id
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_create_port_range(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'create_port_range',
            f'''
            <create_port_range_response id="{self.uuid}"
            status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                createPortRange(input: {{
                    portListId: "{str(self.port_list_id)}",
                    start: 3,
                    end: 15,
                    portRangeType: TCP,
                    comment: "port range",
                }}) {{
                    id
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        uuid = json['data']['createPortRange']['id']

        self.assertEqual(uuid, str(self.uuid))

        mock_gmp.gmp_protocol.create_port_range.assert_called_with(
            port_list_id=str(self.port_list_id),
            start=3,
            end=15,
            port_range_type=GvmPortRangeType.TCP,
            comment="port range",
        )
