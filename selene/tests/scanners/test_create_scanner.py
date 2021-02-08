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

from gvm.protocols.next import ScannerType as GvmScannerType

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class CreateScannerTestCase(SeleneTestCase):
    def setUp(self):
        self.up_credential_id = uuid4()

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            f'''
            mutation {{
                createScanner(input: {{
                    name: "foo",
                    credentialId: "{self.up_credential_id}",
                    host:"localhost",
                    port:5500,
                    type: OSP_SCANNER_TYPE
                }}) {{
                    id
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_create_scanner(self, mock_gmp: GmpMockFactory):
        scanner_id = uuid4()

        mock_gmp.mock_response(
            'create_scanner',
            f'''
            <create_scanner_response id="{scanner_id}"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                createScanner(input: {{
   	            name:"foo",
                    comment:"bar",
                    credentialId: "{self.up_credential_id}",
                    host:"localhost",
                    port:5500,
                    type: OSP_SCANNER_TYPE
                }}) {{
	            id
	        }}
            }}
            '''
        )

        self.assertResponseNoErrors(response)

        json = response.json()

        uuid = json['data']['createScanner']['id']

        self.assertEqual(uuid, str(scanner_id))

        mock_gmp.gmp_protocol.create_scanner.assert_called_with(
            "foo",
            "localhost",
            5500,
            GvmScannerType.OSP_SCANNER_TYPE,
            ca_pub=None,
            comment="bar",
            credential_id=self.up_credential_id,
        )
