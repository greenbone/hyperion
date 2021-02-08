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

from gvm.protocols.next import get_entity_type_from_string

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class CreateTagTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            mutation {
                createTag(input: {
                    name: "foo",
                    resourceType: OPERATING_SYSTEM,
                }) {
                    id
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_create_tag(self, mock_gmp: GmpMockFactory):
        tag_id = uuid4()

        resource1 = uuid4()
        resource2 = uuid4()

        mock_gmp.mock_response(
            'create_tag',
            f'''
            <create_tag_response id="{tag_id}" status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                createTag(input: {{
                    name: "foo",
                    resourceType: OPERATING_SYSTEM,
                    comment: "bar",
                    value: "lorem",
                    resourceIds: ["{resource1}", "{resource2}"],
                    active: true
                }}) {{
                    id
                }}
            }}
            '''
        )

        self.assertResponseNoErrors(response)

        json = response.json()

        uuid = json['data']['createTag']['id']

        self.assertEqual(uuid, str(tag_id))

        mock_gmp.gmp_protocol.create_tag.assert_called_with(
            "foo",
            get_entity_type_from_string('os'),
            comment="bar",
            active=True,
            resource_ids=[str(resource1), str(resource2)],
            value="lorem",
        )
