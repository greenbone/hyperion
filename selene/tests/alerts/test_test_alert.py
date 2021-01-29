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

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class CloneAlertTestCase(SeleneTestCase):
    def setUp(self):
        self.alert_id = uuid4()

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            mutation {
                testAlert(id: "e1438fb2-ab2c-4f4a-ad6b-de97005256e8") {
                    ok
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_test_alert(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'test_alert',
            '''
            <create_alert_response status="201" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                testAlert(
                    id: "{self.alert_id}",
                ) {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.test_alert.assert_called_with(
            str(self.alert_id),
        )
