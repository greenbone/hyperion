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
class RestoreFromTrashcanTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            mutation {
                restoreFromTrashcan (
                    id: "3ad2c2cd-00b2-4b34-b185-5fc61bad653e"
                ) {
                    ok
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_restore(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'restore',
            '''
            <restore_response status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            mutation {
                restoreFromTrashcan (
                    id: "3ad2c2cd-00b2-4b34-b185-5fc61bad653e"
                ) {
                    ok
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['restoreFromTrashcan']['ok']

        self.assertTrue(ok)

        mock_gmp.gmp_protocol.restore.assert_called_with(
            '3ad2c2cd-00b2-4b34-b185-5fc61bad653e'
        )
