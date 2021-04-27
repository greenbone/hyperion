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

# pylint: disable=no-self-argument, no-member

from uuid import UUID

import graphene

from selene.schema.utils import (
    require_authentication,
    get_gmp,
    get_text_from_element,
)

from selene.schema.entities import (
    create_delete_by_ids_mutation,
    create_delete_by_filter_mutation,
    create_export_by_ids_mutation,
    create_export_by_filter_mutation,
)
from selene.schema.scanners.fields import ScannerType


class DeleteScanner(graphene.Mutation):
    """Deletes a scanner

    Args:
        id (UUID): UUID of scanner to delete.

    Returns:
        ok (Boolean)
    """

    class Arguments:
        scanner_id = graphene.UUID(required=True, name='id')

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, scanner_id):
        gmp = get_gmp(info)
        gmp.delete_scanner(str(scanner_id))
        return DeleteScanner(ok=True)


class CreateScannerInput(graphene.InputObjectType):
    """Input object for createScanner.

    Args:
        name (str): The name of the scanner.
        comment (str, optional): The comment on the scanner.
        scanner_type (int): Scanner type. 1 for OSP Scanner, 4 GMP scanner.
        host (str): Scanner host or socket path.
        port (str): Port which the scanner listen on. Default: 9391
        credential_id (UUID): UUID of the credential to use.
        ca_pub (str): CA public key.
    """

    name = graphene.String(required=True, description="Scanner name.")
    comment = graphene.String(description="Scanner comment.")
    scanner_type = ScannerType(
        name="type", required=True, description="Scanner type."
    )
    host = graphene.String(required=True, description="Scanner host or path.")
    port = graphene.Int(description="Scanner port.")
    credential_id = graphene.UUID(
        required=True, description=("UUID of credential."), name="credentialId"
    )
    ca_pub = graphene.String(description="CA public key.")


class CreateScanner(graphene.Mutation):
    """Creates a new scanner. Call with createScanner.

    Args:
        input (CreateScannerInput): Input object for CreateScanner

    """

    class Arguments:
        input_object = CreateScannerInput(required=True, name='input')

    scanner_id = graphene.UUID(name='id')

    @require_authentication
    def mutate(root, info, input_object):

        name = input_object.name
        comment = input_object.comment
        scanner_type = ScannerType.get(input_object.scanner_type)
        host = input_object.host
        credential_id = input_object.credential_id
        if input_object.port is not None:
            port = input_object.port
        else:
            port = 9391
        if scanner_type == ScannerType.OSP_SCANNER_TYPE:
            ca_pub = input_object.ca_pub
        else:
            ca_pub = None

        gmp = get_gmp(info)

        resp = gmp.create_scanner(
            name,
            host,
            port,
            scanner_type,
            credential_id,
            ca_pub=ca_pub,
            comment=comment,
        )
        return CreateScanner(scanner_id=resp.get('id'))


class ModifyScannerInput(graphene.InputObjectType):
    """Input object for modifyScanner.

    Args:
        id (UUID) – ID of scanner to modify.
        name (str): The name of the scanner.
        comment (str, optional): The comment on the scanner.
        scanner_type (int): Scanner type. 1 for OSP Scanner, 4 GMP scanner.
        host (str): Scanner host or socket path.
        port (str): Port which the scanner listen on. Default: 9391
        credential_id (UUID): UUID of the credential to use.
        ca_pub (str): CA public key.
    """

    scanner_id = graphene.UUID(
        required=True, description="ID of scanner to modify.", name='id'
    )
    name = graphene.String(description="Scanner name.")
    comment = graphene.String(description="Scanner comment.")
    scanner_type = ScannerType(name="type", description="Scanner type.")
    host = graphene.String(description="Scanner host or path.")
    port = graphene.Int(description="Scanner port.")
    credential_id = graphene.UUID(
        description=("UUID of credential."), name="credentialId"
    )
    ca_pub = graphene.String(description="CA public key.")


class ModifyScanner(graphene.Mutation):
    """Modifies a scanner. Call with modifyScanner.

    Args:
        input (ModifyScannerInput): Input object for CreateScanner

    """

    class Arguments:
        input_object = ModifyScannerInput(required=True, name='input')

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, input_object):

        scanner_id = str(input_object.scanner_id)
        name = input_object.name
        comment = input_object.comment
        scanner_type = ScannerType.get(input_object.scanner_type)
        host = input_object.host
        credential_id = input_object.credential_id
        if input_object.port is not None:
            port = input_object.port
        else:
            port = 9391
        if scanner_type == ScannerType.OSP_SCANNER_TYPE:
            ca_pub = input_object.ca_pub
        else:
            ca_pub = None

        gmp = get_gmp(info)

        gmp.modify_scanner(
            scanner_id,
            name=name,
            host=host,
            port=port,
            scanner_type=scanner_type,
            credential_id=credential_id,
            ca_pub=ca_pub,
            comment=comment,
        )

        return ModifyScanner(ok=True)


class VerifyScannerType(graphene.ObjectType):
    version = graphene.String()

    def resolve_version(root, _info):
        return get_text_from_element(root, 'version')


class VerifyScanner(graphene.Field):
    """Gets a single scanner.
    Args:
        id (str): UUID of scanner to verify.
    """

    def __init__(self):
        super().__init__(
            VerifyScannerType,
            scanner_id=graphene.UUID(required=True, name='id'),
            resolver=self.resolve,
        )

    @staticmethod
    @require_authentication
    def resolve(_root, info, scanner_id: UUID):
        gmp = get_gmp(info)

        return gmp.verify_scanner(str(scanner_id))


class CloneScanner(graphene.Mutation):
    """Clones a Scanner

    Args:
        id (UUID): UUID of scanner to clone.

    Returns:
        id (UUID)
    """

    class Arguments:
        scanner_id = graphene.UUID(required=True, name='id')

    scanner_id = graphene.UUID(name='id')

    @require_authentication
    def mutate(root, info, scanner_id):
        gmp = get_gmp(info)
        elem = gmp.clone_scanner(str(scanner_id))
        return CloneScanner(scanner_id=elem.get('id'))


# Explicit classes needed, else we get error
# 'AssertionError: Found different types with the same name in the
#   schema: ExportByIds, ExportByIds.'

ExportByIdsClass = create_export_by_ids_mutation(
    entity_name='scanner', with_details=True
)


class ExportScannersByIds(ExportByIdsClass):
    pass


ExportByFilterClass = create_export_by_filter_mutation(
    entity_name='scanner', with_details=True
)


class ExportScannersByFilter(ExportByFilterClass):
    pass


# Explicit classes needed, else we get error
# 'AssertionError: Found different types with the same name in the
#   schema: DeleteByIds, DeleteByIds.'

DeleteByIdsClass = create_delete_by_ids_mutation(entity_name='scanner')


class DeleteScannersByIds(DeleteByIdsClass):
    """Deletes a list of scanners

    Args:
        ids (List(UUID)): List of UUIDs of scanners to delete.
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.

    Returns:
        ok (Boolean)

    Example

        mutation {
            deleteScannersByIds(
                ids: ["5f8e7b31-35ea-4b43-9797-6d77f058906b"],
                ultimate: false)
            {
                ok
            }
        }

        Response
        {
            "data": {
                "deleteScannersByIds": {
                    "ok": true
                }
            }
        }
    """


DeleteByFilterClass = create_delete_by_filter_mutation(entity_name='scanner')


class DeleteScannersByFilter(DeleteByFilterClass):
    """Deletes a filtered list of scanners

    Args:
        filterString (str): Filter string for scanner list to delete.
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.

    Returns:
        ok (Boolean)

    Example

        mutation {
            deleteScannerByFilter(
                filterString:"name~Clone",
                ultimate: false)
            {
                ok
            }
        }

        Response
        {
            "data": {
                "deleteScannerByFilter": {
                    "ok": true
                }
            }
        }
    """
