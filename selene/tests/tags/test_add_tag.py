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

from gvm.protocols.latest import get_entity_type_from_string

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class AddTagTestCase(SeleneTestCase):
    def setUp(self):
        self.tag_id = uuid4()
        self.resource = uuid4()

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            f'''
            mutation {{
                addTag(input: {{
                    id: "{self.tag_id}",
                    resourceIds: ["{self.resource}"],
                    resourceType: OPERATING_SYSTEM,
                }}) {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_add_tag(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'modify_tag',
            '''
            <modify_tag_response status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                addTag(input: {{
                    id: "{self.tag_id}",
                    resourceIds: ["{self.resource}"],
                    resourceType: OPERATING_SYSTEM,
                }}) {{
                    ok
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['addTag']['ok']

        self.assertEqual(ok, True)

        mock_gmp.gmp_protocol.modify_tag.assert_called_with(
            str(self.tag_id),
            resource_ids=[str(self.resource)],
            resource_type=get_entity_type_from_string('os'),
            resource_action='add',
        )
