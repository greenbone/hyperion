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

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class VerifyScannerTestCase(SeleneTestCase):
    def setUp(self):
        self.xml = '''
            <verify_scanner_response status="200" status_text="OK">
                <version>OpenVAS 21.4.0</version>
            </verify_scanner_response>
            '''

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                verifyScanner(
                    id: "08b69003-5fc2-4037-a479-93b440211c73"
                ){
                    version
                 }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_verify_scanner(self, mock_gmp: GmpMockFactory):

        mock_gmp.mock_response('verify_scanner', self.xml)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                verifyScanner(
                    id: "08b69003-5fc2-4037-a479-93b440211c73"
                ){
                    version
                 }
            }
            '''
        )

        json = response.json()
        self.assertResponseNoErrors(response)
        version = json['data']['verifyScanner']['version']

        self.assertEqual(version, 'OpenVAS 21.4.0')
