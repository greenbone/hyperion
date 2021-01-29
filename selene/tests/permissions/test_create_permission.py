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

# pylint: disable=no-member

from uuid import uuid4

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory
from selene.schema.permissions.fields import PermissionSubjectType
from selene.schema.permissions.fields import PermissionEntityType


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class CreatePermissionTestCase(SeleneTestCase):
    def setUp(self):
        self.id1 = uuid4()
        self.id2 = uuid4()

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            f'''
            mutation {{
                createPermission( input: {{
                        name: "some_name",
                        subjectId: "{self.id1}",
                        subjectType: ROLE}}) {{
                    id
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_create_permission(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'create_permission',
            f'''
            <create_permission_response status="201"
             status_text="OK, resource created"
             id="{self.id2}"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                createPermission( input: {{
                        name: "create_alert",
                        subjectId: "{self.id1}",
                        subjectType: ROLE,
                        resourceId:"{self.id1}",
                        resourceType: ALERT,
                        comment: "some comment"}}) {{
                    id
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        created_permission_id = json['data']['createPermission']['id']

        self.assertEqual(created_permission_id, str(self.id2))

        mock_gmp.gmp_protocol.create_permission.assert_called_with(
            name="create_alert",
            subject_id=str(self.id1),
            subject_type=PermissionSubjectType.ROLE,
            resource_id=str(self.id1),
            resource_type=PermissionEntityType.ALERT,
            comment="some comment",
        )
