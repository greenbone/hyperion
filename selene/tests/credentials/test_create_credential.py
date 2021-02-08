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

from gvm.protocols.next import (
    CredentialType as GvmCredentialType,
    SnmpAuthAlgorithm,
    SnmpPrivacyAlgorithm,
)

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class CreateCredentialTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            mutation {
                createCredential(input: {
                    name: "foo",
                    type: USERNAME_PASSWORD,
                    login: "Hello",
                    password: "World",
                }) {
                    id
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_create_username_password_credential(
        self, mock_gmp: GmpMockFactory
    ):
        credential_id = uuid4()

        mock_gmp.mock_response(
            'create_credential',
            f'''
            <create_credential_response id="{credential_id}"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            mutation {
                createCredential(input: {
                    name: "foo",
                    comment: "bar",
                    type: USERNAME_PASSWORD,
                    login: "Hello",
                    password: "World",
                    allowInsecure: false,
                }) {
                    id
                }
            }
            '''
        )

        self.assertResponseNoErrors(response)

        json = response.json()

        uuid = json['data']['createCredential']['id']

        self.assertEqual(uuid, str(credential_id))

        mock_gmp.gmp_protocol.create_credential.assert_called_with(
            "foo",
            GvmCredentialType.USERNAME_PASSWORD,
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

    def test_create_password_only_credential(self, mock_gmp: GmpMockFactory):
        credential_id = uuid4()

        mock_gmp.mock_response(
            'create_credential',
            f'''
            <create_credential_response id="{credential_id}"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            mutation {
                createCredential(input: {
                    name: "foo",
                    type: PASSWORD_ONLY,
                    password: "World",
                    allowInsecure: true,
                }) {
                    id
                }
            }
            '''
        )

        self.assertResponseNoErrors(response)

        json = response.json()

        uuid = json['data']['createCredential']['id']

        self.assertEqual(uuid, str(credential_id))

        mock_gmp.gmp_protocol.create_credential.assert_called_with(
            "foo",
            GvmCredentialType.PASSWORD_ONLY,
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

    def test_create_client_certificate_credential(
        self, mock_gmp: GmpMockFactory
    ):
        credential_id = uuid4()

        mock_gmp.mock_response(
            'create_credential',
            f'''
            <create_credential_response id="{credential_id}"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            mutation {
                createCredential(input: {
                    name: "foo",
                    type: CLIENT_CERTIFICATE,
                    certificate: "-----BEGIN CERTIFICATE-----...",
                    keyPhrase: "test",
                    privateKey: "-----BEGIN PRIVATE KEY-----...",
                }) {
                    id
                }
            }
            '''
        )

        self.assertResponseNoErrors(response)

        json = response.json()

        uuid = json['data']['createCredential']['id']

        self.assertEqual(uuid, str(credential_id))

        mock_gmp.gmp_protocol.create_credential.assert_called_with(
            "foo",
            GvmCredentialType.CLIENT_CERTIFICATE,
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

    def test_create_pgp_key_credential(self, mock_gmp: GmpMockFactory):
        credential_id = uuid4()

        mock_gmp.mock_response(
            'create_credential',
            f'''
            <create_credential_response id="{credential_id}"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            mutation {
                createCredential(input: {
                    name: "foo",
                    type: PGP_ENCRYPTION_KEY,
                    publicKey: "-----BEGIN PGP PUBLIC KEY BLOCK-----...",
                }) {
                    id
                }
            }
            '''
        )

        self.assertResponseNoErrors(response)

        json = response.json()

        uuid = json['data']['createCredential']['id']

        self.assertEqual(uuid, str(credential_id))

        mock_gmp.gmp_protocol.create_credential.assert_called_with(
            "foo",
            GvmCredentialType.PGP_ENCRYPTION_KEY,
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

    def test_create_smime_credential(self, mock_gmp: GmpMockFactory):
        credential_id = uuid4()

        mock_gmp.mock_response(
            'create_credential',
            f'''
            <create_credential_response id="{credential_id}"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            mutation {
                createCredential(input: {
                    name: "foo",
                    type: SMIME_CERTIFICATE,
                    certificate: "-----BEGIN CERTIFICATE-----...",
                }) {
                    id
                }
            }
            '''
        )

        self.assertResponseNoErrors(response)

        json = response.json()

        uuid = json['data']['createCredential']['id']

        self.assertEqual(uuid, str(credential_id))

        mock_gmp.gmp_protocol.create_credential.assert_called_with(
            "foo",
            GvmCredentialType.SMIME_CERTIFICATE,
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

    def test_create_snmp_credential(self, mock_gmp: GmpMockFactory):
        credential_id = uuid4()

        mock_gmp.mock_response(
            'create_credential',
            f'''
            <create_credential_response id="{credential_id}"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            mutation {
                createCredential(input: {
                    name: "foo",
                    type: SNMP,
                    community: "bar"
                    login: "Hello",
                    password: "World",
                    privacyPassword: "1234"
                    privacyAlgorithm: AES
                    authAlgorithm: SHA1
                }) {
                    id
                }
            }
            '''
        )

        self.assertResponseNoErrors(response)

        json = response.json()

        uuid = json['data']['createCredential']['id']

        self.assertEqual(uuid, str(credential_id))

        mock_gmp.gmp_protocol.create_credential.assert_called_with(
            "foo",
            GvmCredentialType.SNMP,
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

    def test_create_username_ssh_credential(self, mock_gmp: GmpMockFactory):
        credential_id = uuid4()

        mock_gmp.mock_response(
            'create_credential',
            f'''
            <create_credential_response id="{credential_id}"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            mutation {
                createCredential(input: {
                    name: "foo",
                    type: USERNAME_SSH_KEY,
                    login: "Hello",
                    keyPhrase: "test",
                    privateKey: "-----BEGIN PRIVATE KEY-----...",
                }) {
                    id
                }
            }
            '''
        )

        self.assertResponseNoErrors(response)

        json = response.json()

        uuid = json['data']['createCredential']['id']

        self.assertEqual(uuid, str(credential_id))

        mock_gmp.gmp_protocol.create_credential.assert_called_with(
            "foo",
            GvmCredentialType.USERNAME_SSH_KEY,
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
