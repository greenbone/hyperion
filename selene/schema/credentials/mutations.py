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

# pylint: disable=no-self-argument, no-member


import graphene


from selene.schema.credentials.fields import (
    CredentialType,
    AuthAlgorithm,
    PrivacyAlgorithm,
)
from selene.schema.entities import (
    create_export_by_ids_mutation,
    create_export_by_filter_mutation,
    create_delete_by_ids_mutation,
    create_delete_by_filter_mutation,
)
from selene.schema.utils import (
    require_authentication,
    get_gmp,
)


class CloneCredential(graphene.Mutation):
    """Clone a credential

    Args:
        id (UUID): UUID of credential to clone.

    Example:

        .. code-block::

            mutation {
                cloneCredential(
                    id: "b992601e-e0df-4078-b4b1-39e04f92f4cc",
                ) {
                    id
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "cloneCredential": {
                    "id": "a569f3df-0f8d-4001-aeef-08cdee0cdf49"
                    }
                }
            }
    """

    class Arguments:
        credential_id = graphene.UUID(required=True, name='id')

    credential_id = graphene.UUID(name='id')

    @require_authentication
    def mutate(root, info, credential_id):
        gmp = get_gmp(info)
        elem = gmp.clone_credential(str(credential_id))
        return CloneCredential(credential_id=elem.get('id'))


class CreateCredentialInput(graphene.InputObjectType):
    """Input object for createCredential.

    Args:
        name (str): Name of the new credential
        credential_type (CredentialType): The credential type.
        comment (str, optional): Comment for the credential
        allow_insecure (bool, optional): Whether to allow insecure use of
            the credential
        certificate (str, optional): Certificate for the credential. Required
            for client-certificate and smime credential types.
        key_phrase (str, optional): Key passphrase for the private key. Used
            for the username+ssh-key credential type.
        private_key (str, optional): Private key to use for login. Required
            for usk credential type. Also used for the cc credential type.
            The supported key types (dsa, rsa, ecdsa, …) and formats
            (PEM, PKC#12, OpenSSL, …) depend on your installed GnuTLS version.
        login (str, optional): Username for the credential. Required for
            username+password, username+ssh-key and snmp credential type.
        password (str, optional): Password for the credential. Used for
            username+password and snmp credential types.
        community (str, optional): The SNMP community
        auth_algorithm (SnmpAuthAlgorithm, optional): The SNMP authentication
            algorithm. Required for snmp credential type.
        privacy_algorithm (SnmpPrivacyAlgorithm, optional): The SNMP privacy
            algorithm
        privacy_password (str, optional): The SNMP privacy
            password
        public_key (str, optional): PGP public key in armor plain text format.
            Required for pgp credential type.

    """

    name = graphene.String(required=True, description="Credential name.")
    credential_type = CredentialType(
        required=True, description="Credential type", name="type"
    )

    comment = graphene.String(description="Comment for the credential.")
    allow_insecure = graphene.Boolean(
        description="Whether to allow insecure use"
    )

    certificate = graphene.String(
        description=(
            "Certificate for the credential."
            "Required for client-certificate"
            "and smime credential types."
        )
    )
    key_phrase = graphene.String(
        description=(
            "Key passphrase for the private key. Used"
            "for the username+ssh-key credential type."
        )
    )
    private_key = graphene.String(
        description=(
            "Private key to use for login. Required"
            "for usk credential type. Also used for"
            "the cc credential type."
        )
    )

    login = graphene.String(
        description=(
            "Username for the credential. Required for"
            "username+password, username+ssh-key and"
            "snmp credential type."
        )
    )
    password = graphene.String(
        description=(
            "Password for the credential. Used for"
            "username+password and snmp credential types."
        )
    )

    community = graphene.String(description="SNMP community")
    auth_algorithm = AuthAlgorithm(
        description=(
            "The SNMP authentication algorithm."
            "Required for snmp credential type."
        )
    )
    privacy_algorithm = PrivacyAlgorithm(description="SNMP privacy algorithm")
    privacy_password = graphene.String(description="SNMP privacy password")

    public_key = graphene.String(
        description=(
            "PGP public key in armor plain text format."
            "Required for pgp credential type."
        )
    )


class CreateCredential(graphene.Mutation):
    """Creates a new credential. Call with createCredential.

    Args:
        input (CreateCredentialInput): Input object for CreateCredential

    """

    class Arguments:
        input_object = CreateCredentialInput(required=True, name='input')

    credential_id = graphene.UUID(name='id')

    @require_authentication
    def mutate(root, info, input_object):

        name = input_object.name
        credential_type = CredentialType.get(input_object.credential_type)

        comment = input_object.comment
        allow_insecure = input_object.allow_insecure

        certificate = input_object.certificate
        key_phrase = input_object.key_phrase
        private_key = input_object.private_key

        login = input_object.login
        password = input_object.password

        community = input_object.community

        if input_object.auth_algorithm is not None:
            auth_algorithm = AuthAlgorithm.get(input_object.auth_algorithm)
        else:
            auth_algorithm = None

        if input_object.privacy_algorithm is not None:
            privacy_algorithm = PrivacyAlgorithm.get(
                input_object.privacy_algorithm
            )
        else:
            privacy_algorithm = None

        privacy_password = input_object.privacy_password

        public_key = input_object.public_key

        gmp = get_gmp(info)

        resp = gmp.create_credential(
            name,
            credential_type,
            comment=comment,
            allow_insecure=allow_insecure,
            certificate=certificate,
            key_phrase=key_phrase,
            private_key=private_key,
            login=login,
            password=password,
            community=community,
            auth_algorithm=auth_algorithm,
            privacy_algorithm=privacy_algorithm,
            privacy_password=privacy_password,
            public_key=public_key,
        )
        return CreateCredential(credential_id=resp.get('id'))


class ModifyCredentialInput(graphene.InputObjectType):
    """Input object for createCredential.

    Args:
        name (str): Name of the new credential
        credential_type (CredentialType): The credential type.
        comment (str, optional): Comment for the credential
        allow_insecure (bool, optional): Whether to allow insecure use of
            the credential
        certificate (str, optional): Certificate for the credential. Required
            for client-certificate and smime credential types.
        key_phrase (str, optional): Key passphrase for the private key. Used
            for the username+ssh-key credential type.
        private_key (str, optional): Private key to use for login. Required
            for usk credential type. Also used for the cc credential type.
            The supported key types (dsa, rsa, ecdsa, …) and formats
            (PEM, PKC#12, OpenSSL, …) depend on your installed GnuTLS version.
        login (str, optional): Username for the credential. Required for
            username+password, username+ssh-key and snmp credential type.
        password (str, optional): Password for the credential. Used for
            username+password and snmp credential types.
        community (str, optional): The SNMP community
        auth_algorithm (SnmpAuthAlgorithm, optional): The SNMP authentication
            algorithm. Required for snmp credential type.
        privacy_algorithm (SnmpPrivacyAlgorithm, optional): The SNMP privacy
            algorithm
        privacy_password (str, optional): The SNMP privacy
            password
        public_key (str, optional): PGP public key in armor plain text format.
            Required for pgp credential type.

    """

    credential_id = graphene.UUID(
        name='id', required=True, description="Credential ID."
    )
    name = graphene.String(description="Credential name.")

    comment = graphene.String(description="Comment for the credential.")
    allow_insecure = graphene.Boolean(
        description="Whether to allow insecure use"
    )

    certificate = graphene.String(
        description=(
            "Certificate for the credential."
            "Required for client-certificate"
            "and smime credential types."
        )
    )
    key_phrase = graphene.String(
        description=(
            "Key passphrase for the private key. Used"
            "for the username+ssh-key credential type."
        )
    )
    private_key = graphene.String(
        description=(
            "Private key to use for login. Required"
            "for usk credential type. Also used for"
            "the cc credential type."
        )
    )

    login = graphene.String(
        description=(
            "Username for the credential. Required for"
            "username+password, username+ssh-key and"
            "snmp credential type."
        )
    )
    password = graphene.String(
        description=(
            "Password for the credential. Used for"
            "username+password and snmp credential types."
        )
    )

    community = graphene.String(description="SNMP community")
    auth_algorithm = AuthAlgorithm(
        description=(
            "The SNMP authentication algorithm."
            "Required for snmp credential type."
        )
    )
    privacy_algorithm = PrivacyAlgorithm(description="SNMP privacy algorithm")
    privacy_password = graphene.String(description="SNMP privacy password")

    public_key = graphene.String(
        description=(
            "PGP public key in armor plain text format."
            "Required for pgp credential type."
        )
    )


class ModifyCredential(graphene.Mutation):
    """Modify a new credential. Call with createCredential.

    Args:
        input (ModifyCredentialInput): Input object for CreateCredential

    """

    class Arguments:
        input_object = ModifyCredentialInput(required=True, name='input')

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, input_object):
        credential_id = str(input_object.credential_id)
        name = input_object.name

        comment = input_object.comment
        allow_insecure = input_object.allow_insecure

        certificate = input_object.certificate
        key_phrase = input_object.key_phrase
        private_key = input_object.private_key

        login = input_object.login
        password = input_object.password

        community = input_object.community

        if input_object.auth_algorithm is not None:
            auth_algorithm = AuthAlgorithm.get(input_object.auth_algorithm)
        else:
            auth_algorithm = None

        if input_object.privacy_algorithm is not None:
            privacy_algorithm = PrivacyAlgorithm.get(
                input_object.privacy_algorithm
            )
        else:
            privacy_algorithm = None

        privacy_password = input_object.privacy_password

        public_key = input_object.public_key

        gmp = get_gmp(info)

        gmp.modify_credential(
            credential_id,
            name=name,
            comment=comment,
            allow_insecure=allow_insecure,
            certificate=certificate,
            key_phrase=key_phrase,
            private_key=private_key,
            login=login,
            password=password,
            auth_algorithm=auth_algorithm,
            community=community,
            privacy_algorithm=privacy_algorithm,
            privacy_password=privacy_password,
            public_key=public_key,
        )
        return ModifyCredential(ok=True)


# Explicit classes needed, else we get error
# 'AssertionError: Found different types with the same name in the
#   schema: ExportByIds, ExportByIds.'

ExportByIdsClass = create_export_by_ids_mutation(entity_name='credential')


class ExportCredentialsByIds(ExportByIdsClass):
    pass


ExportByFilterClass = create_export_by_filter_mutation(entity_name='credential')


class ExportCredentialsByFilter(ExportByFilterClass):
    pass


# Explicit classes needed, else we get error
# 'AssertionError: Found different types with the same name in the
#   schema: DeleteByIds, DeleteByIds.'


DeleteByIdsClass = create_delete_by_ids_mutation(entity_name='credential')


class DeleteCredentialsByIds(DeleteByIdsClass):
    """Deletes a list of credentials

    Args:
        ids (List(UUID)): List of UUIDs of credentials to delete.
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.

    Returns:
        ok (Boolean)

    Example

        mutation {
            deleteCredentialByIds(
                ids: ["5f8e7b31-35ea-4b43-9797-6d77f058906b"],
                ultimate: false)
            {
                ok
            }
        }

        Response
        {
            "data": {
                "deleteCredentialByIds": {
                    "ok": true
                }
            }
        }
    """


DeleteByFilterClass = create_delete_by_filter_mutation(entity_name='credential')


class DeleteCredentialsByFilter(DeleteByFilterClass):
    """Deletes a filtered list of credentials

    Args:
        filterString (str): Filter string for credential list to delete.
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.

    Returns:
        ok (Boolean)

    Example

        mutation {
            deleteCredentialByFilter(
                filterString:"name~Clone",
                ultimate: false)
            {
                ok
            }
        }

        Response
        {
            "data": {
                "deleteCredentialByFilter": {
                    "ok": true
                }
            }
        }
    """
