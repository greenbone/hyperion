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

from gvm.protocols.latest import SnmpAuthAlgorithm, SnmpPrivacyAlgorithm

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class ModifyCredentialTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        credential_id = str(uuid4())

        response = self.query(
            f'''
            mutation {{
                modifyCredential(input: {{
                    id: "{credential_id}"
                    name: "foo",
                    login: "Hello",
                    password: "World",
                }}) {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_modify_username_password_credential(
        self, mock_gmp: GmpMockFactory
    ):
        credential_id = str(uuid4())

        mock_gmp.mock_response(
            'modify_credential',
            '''
            <modify_credential_response status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyCredential(input: {{
                    id: "{credential_id}"
                    name: "foo",
                    comment: "bar",
                    login: "Hello",
                    password: "World",
                    allowInsecure: false,
                }}) {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseNoErrors(response)

        json = response.json()

        ok = json['data']['modifyCredential']['ok']

        self.assertTrue(ok)

        mock_gmp.gmp_protocol.modify_credential.assert_called_with(
            credential_id,
            name="foo",
            allow_insecure=False,
            auth_algorithm=None,
            certificate=None,
            comment="bar",
            community=None,
            key_phrase=None,
            login='Hello',
            password='World',
            privacy_algorithm=None,
            privacy_password=None,
            private_key=None,
            public_key=None,
        )

    def test_modify_password_only_credential(self, mock_gmp: GmpMockFactory):
        credential_id = str(uuid4())

        mock_gmp.mock_response(
            'modify_credential',
            '''
            <modify_credential_response status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyCredential(input: {{
                    id: "{credential_id}"
                    name: "foo",
                    password: "World",
                    allowInsecure: true,
                }}) {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseNoErrors(response)

        json = response.json()

        ok = json['data']['modifyCredential']['ok']

        self.assertTrue(ok)

        mock_gmp.gmp_protocol.modify_credential.assert_called_with(
            credential_id,
            name="foo",
            allow_insecure=True,
            auth_algorithm=None,
            certificate=None,
            comment=None,
            community=None,
            key_phrase=None,
            login=None,
            password='World',
            privacy_algorithm=None,
            privacy_password=None,
            private_key=None,
            public_key=None,
        )

    def test_modify_client_certificate_credential(
        self, mock_gmp: GmpMockFactory
    ):
        credential_id = str(uuid4())

        mock_gmp.mock_response(
            'modify_credential',
            '''
            <modify_credential_response status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyCredential(input: {{
                    id: "{credential_id}"
                    name: "foo",
                    certificate: "-----BEGIN CERTIFICATE-----...",
                    keyPhrase: "test",
                    privateKey: "-----BEGIN PRIVATE KEY-----...",
                }}) {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseNoErrors(response)

        json = response.json()

        ok = json['data']['modifyCredential']['ok']

        self.assertTrue(ok)

        mock_gmp.gmp_protocol.modify_credential.assert_called_with(
            credential_id,
            name="foo",
            allow_insecure=None,
            auth_algorithm=None,
            certificate="-----BEGIN CERTIFICATE-----...",
            comment=None,
            community=None,
            key_phrase="test",
            login=None,
            password=None,
            privacy_algorithm=None,
            privacy_password=None,
            private_key="-----BEGIN PRIVATE KEY-----...",
            public_key=None,
        )

    def test_modify_pgp_key_credential(self, mock_gmp: GmpMockFactory):
        credential_id = str(uuid4())

        mock_gmp.mock_response(
            'modify_credential',
            '''
            <modify_credential_response status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyCredential(input: {{
                    id: "{credential_id}"
                    name: "foo",
                    publicKey: "-----BEGIN PGP PUBLIC KEY BLOCK-----...",
                }}) {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseNoErrors(response)

        json = response.json()

        ok = json['data']['modifyCredential']['ok']

        self.assertTrue(ok)

        mock_gmp.gmp_protocol.modify_credential.assert_called_with(
            credential_id,
            name="foo",
            allow_insecure=None,
            auth_algorithm=None,
            certificate=None,
            comment=None,
            community=None,
            key_phrase=None,
            login=None,
            password=None,
            privacy_algorithm=None,
            privacy_password=None,
            private_key=None,
            public_key="-----BEGIN PGP PUBLIC KEY BLOCK-----...",
        )

    def test_modify_smime_credential(self, mock_gmp: GmpMockFactory):
        credential_id = str(uuid4())

        mock_gmp.mock_response(
            'modify_credential',
            '''
            <modify_credential_response status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyCredential(input: {{
                    id: "{credential_id}"
                    name: "foo",
                    certificate: "-----BEGIN CERTIFICATE-----...",
                }}) {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseNoErrors(response)

        json = response.json()

        ok = json['data']['modifyCredential']['ok']

        self.assertTrue(ok)

        mock_gmp.gmp_protocol.modify_credential.assert_called_with(
            credential_id,
            name="foo",
            allow_insecure=None,
            auth_algorithm=None,
            certificate="-----BEGIN CERTIFICATE-----...",
            comment=None,
            community=None,
            key_phrase=None,
            login=None,
            password=None,
            privacy_algorithm=None,
            privacy_password=None,
            private_key=None,
            public_key=None,
        )

    def test_modify_snmp_credential(self, mock_gmp: GmpMockFactory):
        credential_id = str(uuid4())

        mock_gmp.mock_response(
            'modify_credential',
            '''
            <modify_credential_response status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyCredential(input: {{
                    id: "{credential_id}"
                    name: "foo",
                    community: "bar"
                    login: "Hello",
                    password: "World",
                    privacyPassword: "1234"
                    privacyAlgorithm: AES
                    authAlgorithm: SHA1
                }}) {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseNoErrors(response)

        json = response.json()

        ok = json['data']['modifyCredential']['ok']

        self.assertTrue(ok)

        mock_gmp.gmp_protocol.modify_credential.assert_called_with(
            credential_id,
            name="foo",
            allow_insecure=None,
            auth_algorithm=SnmpAuthAlgorithm.SHA1,
            certificate=None,
            comment=None,
            community="bar",
            key_phrase=None,
            login="Hello",
            password="World",
            privacy_algorithm=SnmpPrivacyAlgorithm.AES,
            privacy_password="1234",
            private_key=None,
            public_key=None,
        )

    def test_modify_username_ssh_credential(self, mock_gmp: GmpMockFactory):
        credential_id = str(uuid4())

        mock_gmp.mock_response(
            'modify_credential',
            '''
            <modify_credential_response status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyCredential(input: {{
                    id: "{credential_id}"
                    name: "foo",
                    login: "Hello",
                    keyPhrase: "test",
                    privateKey: "-----BEGIN PRIVATE KEY-----...",
                }}) {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseNoErrors(response)

        json = response.json()

        ok = json['data']['modifyCredential']['ok']

        self.assertTrue(ok)

        mock_gmp.gmp_protocol.modify_credential.assert_called_with(
            credential_id,
            name="foo",
            allow_insecure=None,
            auth_algorithm=None,
            certificate=None,
            comment=None,
            community=None,
            key_phrase="test",
            login="Hello",
            password=None,
            privacy_algorithm=None,
            privacy_password=None,
            private_key="-----BEGIN PRIVATE KEY-----...",
            public_key=None,
        )
