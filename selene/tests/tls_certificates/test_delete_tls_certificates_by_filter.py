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
class DeleteTLSCertificatesByFilterTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            mutation {
                deleteTlsCertificatesByFilter(filterString: "name~Clone") {
                   ok
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_delete_filtered_tls_certificates(self, mock_gmp: GmpMockFactory):
        self.login('foo', 'bar')

        id1 = uuid4()
        id2 = uuid4()

        mock_gmp.mock_response(
            'get_tls_certificates',
            f'''
            <get_tls_certificates_response status="200" status_text="OK">
                <apply_overrides>0</apply_overrides>
                <tls_certificate id="{id1}">
                    <name>Foo Clone 1</name>
                </tls_certificate>
                <tls_certificate id="{id2}">
                    <name>Foo Clone 2</name>
                </tls_certificate>
            </get_tls_certificates_response>
            ''',
        )

        response = self.query(
            '''
            mutation {
                deleteTlsCertificatesByFilter(filterString: "name~Clone") {
                   ok
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['deleteTlsCertificatesByFilter']['ok']

        self.assertTrue(ok)

        mock_gmp.gmp_protocol.delete_tls_certificate.assert_any_call(
            tls_certificate_id=str(id1)
        )

        mock_gmp.gmp_protocol.delete_tls_certificate.assert_any_call(
            tls_certificate_id=str(id2)
        )
