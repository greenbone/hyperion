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

from selene.schema.permissions.fields import (
    PermissionEntityType,
    PermissionSubjectType,
)

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class ModifyPermissionTestCase(SeleneTestCase):
    def setUp(self):
        self.id1 = uuid4()

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            f'''
            mutation {{
                modifyPermission(input: {{
                    id: "{self.id1}"
                    name: "foo",
                }}) {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_modify_permission(self, mock_gmp: GmpMockFactory):

        mock_gmp.mock_response(
            'modify_permission',
            '<modify_permission_response status="200" status_text="OK"/>',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyPermission(input: {{
                    id: "{self.id1}"
   	                name:"foo",
                    comment:"bar",
                    subjectId: "{self.id1}",
                    subjectType: ROLE,
                    resourceId:"{self.id1}",
                    resourceType: ALERT,
                }}) {{
	            ok
	        }}
            }}
            '''
        )

        self.assertResponseNoErrors(response)

        json = response.json()

        ok = json['data']['modifyPermission']['ok']

        self.assertEqual(ok, True)

        mock_gmp.gmp_protocol.modify_permission.assert_called_with(
            f'{self.id1}',
            comment="bar",
            name="foo",
            resource_id=f'{self.id1}',
            resource_type=PermissionEntityType.ALERT,  # pylint: disable=no-member
            subject_id=f'{self.id1}',
            subject_type=PermissionSubjectType.ROLE,  # pylint: disable=no-member
        )
