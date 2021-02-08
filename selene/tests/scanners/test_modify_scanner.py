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
class ModifyScannerTestCase(SeleneTestCase):
    def setUp(self):
        self.up_credential_id = uuid4()

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        scanner_id = str(uuid4())
        response = self.query(
            f'''
            mutation {{
                modifyScanner(input: {{
                    id: "{scanner_id}"
                    name: "foo",
                }}) {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_modify_scanner(self, mock_gmp: GmpMockFactory):
        scanner_id = uuid4()

        mock_gmp.mock_response(
            'modify_scanner',
            '<modify_scanner_response status="200" status_text="OK"/>',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyScanner(input: {{
                    id: "{scanner_id}"
   	            name:"foo",
                    comment:"bar",
                    credentialId: "{self.up_credential_id}",
                    host:"localhost",
                    port:5501,
                    type: OSP_SCANNER_TYPE
                }}) {{
	            ok
	        }}
            }}
            '''
        )

        self.assertResponseNoErrors(response)

        json = response.json()

        ok = json['data']['modifyScanner']['ok']

        self.assertEqual(ok, True)

        mock_gmp.gmp_protocol.modify_scanner.assert_called_with(
            str(scanner_id),
            name="foo",
            host="localhost",
            port=5501,
            scanner_type=GvmScannerType.OSP_SCANNER_TYPE,
            ca_pub=None,
            comment="bar",
            credential_id=self.up_credential_id,
        )
