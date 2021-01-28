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

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class CreateTLSCertificateTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            mutation {
                createTlsCertificate(input: {
                    name: "foo",
                    certificate: "bar",
                }) {
                    id
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_create_tls_certificate(self, mock_gmp: GmpMockFactory):
        tls_certificate_id = uuid4()

        mock_gmp.mock_response(
            'create_tls_certificate',
            f'<create_tls_certificate_response id="{tls_certificate_id}" '
            'status="200" status_text="OK"/>',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            mutation {
                createTlsCertificate(input: {
                    name: "foo",
                    certificate: "bar",
                    comment: "bar",
                }) {
                    id
                }
            }
            '''
        )

        self.assertResponseNoErrors(response)

        json = response.json()

        uuid = json['data']['createTlsCertificate']['id']

        self.assertEqual(uuid, str(tls_certificate_id))

        mock_gmp.gmp_protocol.create_tls_certificate.assert_called_with(
            "foo",
            certificate="bar",
            comment="bar",
            trust=None,
        )
