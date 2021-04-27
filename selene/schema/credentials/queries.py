# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Greenbone Networks GmbH
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

from uuid import UUID

import graphene

from graphql import ResolveInfo

from selene.schema.credentials.fields import Credential, CredentialFormat

from selene.schema.parser import FilterString

from selene.schema.relay import (
    EntityConnectionField,
    Entities,
    get_filter_string_for_pagination,
)

from selene.schema.utils import get_gmp, require_authentication, XmlElement


class GetCredential(graphene.Field):
    """Gets a single credential.

    Args:
        id (UUID): UUID of the credential being queried

    Example:

        .. code-block::

            query {
                credential (id: "4846b497-936b-4816-aa4a-1a997cf9ab8d"){
                        id
                        name
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "credential": {
                        "id": "4846b497-936b-4816-aa4a-1a997cf9ab8d",
                        "name": "foo"
                    }
                }
            }

    """

    def __init__(self):
        super().__init__(
            Credential,
            credential_id=graphene.UUID(required=True, name='id'),
            scanners=graphene.Boolean(default_value=True),
            targets=graphene.Boolean(default_value=True),
            credential_format=graphene.String(
                default_value=None, name='format'
            ),
            resolver=self.resolve,
        )

    @staticmethod
    @require_authentication
    def resolve(
        _root,
        info,
        credential_id: UUID,
        targets,
        scanners,
        credential_format=None,
    ):
        gmp = get_gmp(info)

        cred_format = (
            CredentialFormat.get(credential_format)
            if credential_format
            else None
        )

        xml = gmp.get_credential(
            str(credential_id),
            scanners=scanners,
            targets=targets,
            credential_format=cred_format,
        )
        return xml.find('credential')


class GetCredentials(EntityConnectionField):
    """Gets a list of credentials with pagination

    Args:
        filter_string (str, optional): Optional filter string to be
            used with query.

    Example:

        .. code-block::

            query {
                credentials (filterString: "name~Foo rows=2") {
                    nodes {
                        id
                        name
                    }
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "credentials": {
                        "nodes": [
                            {
                                "id": "1fb47870-47ce-4b9f-a8f9-8b4b19624c59",
                                "name": "Foo"
                            },
                            {
                                "id": "5d07b6eb-27f9-424a-a206-34babbba7b4d",
                                "name": "Foo Bar"
                            },
                        ]
                    }
                }
            }

    """

    entity_type = Credential

    @staticmethod
    @require_authentication
    def resolve_entities(  # pylint: disable=arguments-differ
        _root,
        info: ResolveInfo,
        filter_string: FilterString = None,
        after: str = None,
        before: str = None,
        first: int = None,
        last: int = None,
    ) -> Entities:
        gmp = get_gmp(info)

        filter_string = get_filter_string_for_pagination(
            filter_string, first=first, last=last, after=after, before=before
        )

        xml: XmlElement = gmp.get_credentials(
            filter=filter_string.filter_string
        )

        credential_elements = xml.findall('credential')
        counts = xml.find('credential_count')
        requested = xml.find('credentials')

        return Entities(credential_elements, counts, requested)
