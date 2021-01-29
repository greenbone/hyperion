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

# pylint: disable=no-self-argument

import graphene

from selene.schema.entities import (
    create_delete_by_ids_mutation,
    create_delete_by_filter_mutation,
    create_export_by_ids_mutation,
    create_export_by_filter_mutation,
)
from selene.schema.utils import get_gmp, require_authentication


class CreateTLSCertificateInput(graphene.InputObjectType):
    """Input object for createTLSCertificate.

    Args:
        name (str): Name of the tls certificate.
            Must be an IPv4 or IPv6 address as string.
        comment (str, optional): Comment for the tls certificate.
    """

    name = graphene.String(
        required=True,
        description=("Name of tls certificate."),
    )
    certificate = graphene.String(
        required=True,
        description="The Base64 encoded certificate data (x.509 DER or PEM)",
    )
    comment = graphene.String(description="Comment for the tls certificate.")
    trust = graphene.Boolean(description="Whether the certificate is trusted.")


class CreateTLSCertificate(graphene.Mutation):
    class Arguments:
        input_object = CreateTLSCertificateInput(required=True, name='input')

    tls_certificate_id = graphene.UUID(name='id')

    @require_authentication
    def mutate(root, info, input_object):
        gmp = get_gmp(info)

        resp = gmp.create_tls_certificate(
            input_object.name,
            certificate=input_object.certificate,
            comment=input_object.comment,
            trust=input_object.trust,
        )

        return CreateTLSCertificate(tls_certificate_id=resp.get('id'))


class CloneTLSCertificate(graphene.Mutation):
    """Clones a tls certificate

    Args:
        id (UUID): UUID of tls certificate to clone.

    Returns:
        ok (Boolean)
    """

    class Arguments:
        tls_certificate_id = graphene.UUID(required=True, name='id')

    cloned_tls_certificate_id = graphene.UUID(name='id')

    @require_authentication
    def mutate(root, info, tls_certificate_id):
        gmp = get_gmp(info)
        resp = gmp.clone_tls_certificate(str(tls_certificate_id))
        return CloneTLSCertificate(cloned_tls_certificate_id=resp.get('id'))


class DeleteTLSCertificate(graphene.Mutation):
    """Deletes a tls certificate

    Args:
        id (UUID): UUID of tls certificate to delete.

    Returns:
        ok (Boolean)
    """

    class Arguments:
        tls_certificate_id = graphene.UUID(required=True, name='id')

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, tls_certificate_id):
        gmp = get_gmp(info)
        gmp.delete_tls_certificate(str(tls_certificate_id))
        return DeleteTLSCertificate(ok=True)


#   schema: DeleteByIds, DeleteByIds.'

DeleteByIdsClass = create_delete_by_ids_mutation(entity_name='tls_certificate')


class DeleteTLSCertificatesByIds(DeleteByIdsClass):
    """Deletes a list of tls certificates

    Args:
        ids (List(UUID)): List of UUIDs of tls certificates to delete.

    Returns:
        ok (Boolean)

    Example

        mutation {
            deleteTLSCertificatesByIds(
                ids: ["5f8e7b31-35ea-4b43-9797-6d77f058906b"],
            ) {
                ok
            }
        }

        Response
        {
            "data": {
                "deleteTLSCertificatesByIds": {
                    "ok": true
                }
            }
        }
    """


DeleteByFilterClass = create_delete_by_filter_mutation(
    entity_name='tls_certificate'
)


class DeleteTLSCertificatesByFilter(DeleteByFilterClass):
    """Deletes a filtered list of tls certificate

    Args:
        filterString (str): Filter string for tls certificate list to delete.

    Returns:
        ok (Boolean)

    Example

        mutation {
            deleteTLSCertificateByFilter(
                filterString:"name~Clone",
            ) {
                ok
            }
        }

        Response
        {
            "data": {
                "deleteTLSCertificateByFilter": {
                    "ok": true
                }
            }
        }
    """


# Explicit classes needed, else we get error
# 'AssertionError: Found different types with the same name in the
#   schema: ExportByIds, ExportByIds.'

ExportByIdsClass = create_export_by_ids_mutation(entity_name='tls_certificate')


class ExportTLSCertificatesByIds(ExportByIdsClass):
    pass


ExportByFilterClass = create_export_by_filter_mutation(
    entity_name='tls_certificate'
)


class ExportTLSCertificatesByFilter(ExportByFilterClass):
    pass


class ModifyTLSCertificateInput(graphene.InputObjectType):
    """Input object for modifyTLSCertificate.

    Args:
        id (UUID): UUID of tls certificate to modify.
        comment (str, optional): The comment on the tls certificate.
    """

    tls_certificate_id = graphene.UUID(
        required=True,
        description="UUID of tls certificate to modify.",
        name='id',
    )
    name = graphene.String(description="TLSCertificate name to change.")
    comment = graphene.String(description="TLSCertificate comment to change.")
    trust = graphene.Boolean(description="TLSCertificate trust to change.")


class ModifyTLSCertificate(graphene.Mutation):

    """Modifies an existing tls certificate. Call with modifyTLSCertificate.

    Args:
        input (ModifyTLSCertificateInput): Input object for ModifyTLSCertificate

    Returns:
        ok (Boolean)
    """

    class Arguments:
        input_object = ModifyTLSCertificateInput(required=True, name='input')

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, input_object):
        tls_certificate_id = (
            str(input_object.tls_certificate_id)
            if input_object.tls_certificate_id is not None
            else None
        )

        gmp = get_gmp(info)

        gmp.modify_tls_certificate(
            tls_certificate_id,
            name=input_object.name,
            comment=input_object.comment,
            trust=input_object.trust,
        )

        return ModifyTLSCertificate(ok=True)
