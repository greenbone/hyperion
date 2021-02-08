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

from gvm.protocols.next import (
    FilterType as GvmFilterType,
    get_filter_type_from_string,
)

from selene.schema.entities import (
    create_delete_by_ids_mutation,
    create_delete_by_filter_mutation,
    create_export_by_ids_mutation,
    create_export_by_filter_mutation,
)
from selene.schema.utils import get_gmp, require_authentication


class FilterType(graphene.Enum):
    class Meta:
        enum = GvmFilterType


class CloneFilter(graphene.Mutation):
    """Clones a filter

    Args:
        id (UUID): UUID of filter to clone.

    Returns:
        ok (Boolean)
    """

    class Arguments:
        copy_id = graphene.UUID(
            required=True,
            name='id',
            description='UUID of the filter to clone.',
        )

    filter_id = graphene.UUID(name='id')

    @require_authentication
    def mutate(root, info, copy_id):
        gmp = get_gmp(info)
        resp = gmp.clone_filter(str(copy_id))
        return CloneFilter(filter_id=resp.get('id'))


class CreateFilterInput(graphene.InputObjectType):
    """Input object for createFilter.

    Args:
        name (str): Name of the filter.
        comment (str, optional): Comment for the filter.
        term (str): The filter term.
        entity_type (FilterType): The entity type applied to the filter
    """

    name = graphene.String(
        required=True,
        description=("Name of the filter."),
    )
    comment = graphene.String(description="Comment for the filter.")
    term = graphene.String(description='The filter term.')
    entity_type = graphene.Field(
        FilterType,
        name='type',
        description='The entity type applied to the filter',
    )


class CreateFilter(graphene.Mutation):
    class Arguments:
        input_object = CreateFilterInput(required=True, name='input')

    filter_id = graphene.UUID(name='id')

    @require_authentication
    def mutate(root, info, input_object):
        gmp = get_gmp(info)

        resp = gmp.create_filter(
            input_object.name,
            comment=input_object.comment,
            filter_type=get_filter_type_from_string(input_object.entity_type),
            term=input_object.term,
        )

        return CreateFilter(filter_id=resp.get('id'))


class DeleteFilter(graphene.Mutation):
    """Deletes a filter

    Args:
        id (UUID): UUID of filter to delete.
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.

    Returns:
        ok (Boolean)
    """

    class Arguments:
        filter_id = graphene.UUID(required=True, name='id')
        ultimate = graphene.Boolean(name='ultimate')

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, filter_id, ultimate):
        gmp = get_gmp(info)
        gmp.delete_filter(filter_id=str(filter_id), ultimate=ultimate)
        return DeleteFilter(ok=True)


#   schema: DeleteByIds, DeleteByIds.'

DeleteByIdsClass = create_delete_by_ids_mutation(entity_name='filter')


class DeleteFiltersByIds(DeleteByIdsClass):
    """Deletes a list of filters

    Args:
        ids (List(UUID)): List of UUIDs of filter to delete.
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.

    Returns:
        ok (Boolean)

    Example

        mutation {
            deleteFiltersByIds(
                ids: ["5f8e7b31-35ea-4b43-9797-6d77f058906b"],
                ultimate: false)
            {
                ok
            }
        }

        Response
        {
            "data": {
                "deleteFiltersByIds": {
                    "ok": true
                }
            }
        }
    """


DeleteByFilterClass = create_delete_by_filter_mutation(entity_name='filter')


class DeleteFiltersByFilter(DeleteByFilterClass):
    """Deletes a filtered list of filter

    Args:
        filterString (str): Filter string for filter list to delete.
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.

    Returns:
        ok (Boolean)

    Example

        mutation {
            deleteFilterByFilter(
                filterString:"name~Clone",
                ultimate: false)
            {
                ok
            }
        }

        Response
        {
            "data": {
                "deleteFilterByFilter": {
                    "ok": true
                }
            }
        }
    """


# Explicit classes needed, else we get error
# 'AssertionError: Found different types with the same name in the
#   schema: ExportByIds, ExportByIds.'

ExportByIdsClass = create_export_by_ids_mutation(entity_name='filter')


class ExportFiltersByIds(ExportByIdsClass):
    pass


ExportByFilterClass = create_export_by_filter_mutation(entity_name='filter')


class ExportFiltersByFilter(ExportByFilterClass):
    pass


class ModifyFilterInput(graphene.InputObjectType):
    """Input object for modifyFilter.

    Args:
        id (UUID): UUID of filter to modify.
        name (str): Name of the filter.
        comment (str, optional): The comment on the filter.
        term (str): The filter term.
        entity_type (FilterType): The entity type applied to the filter
    """

    filter_id = graphene.UUID(
        required=True, description="UUID of filter to modify.", name='id'
    )
    name = graphene.String(
        description=("Name of the filter."),
    )
    comment = graphene.String(description="Comment for the filter.")
    term = graphene.String(description='The filter term.')
    entity_type = graphene.Field(
        FilterType,
        name='type',
        description='The entity type applied to the filter',
    )


class ModifyFilter(graphene.Mutation):

    """Modifies an existing filter. Call with modifyFilter.

    Args:
        input (ModifyFilterInput): Input object for ModifyFilter

    Returns:
        ok (Boolean)
    """

    class Arguments:
        input_object = ModifyFilterInput(required=True, name='input')

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, input_object):

        filter_id = str(input_object.filter_id)

        gmp = get_gmp(info)

        gmp.modify_filter(
            filter_id,
            comment=input_object.comment,
            name=input_object.name,
            filter_type=get_filter_type_from_string(input_object.entity_type),
            term=input_object.term,
        )

        return ModifyFilter(ok=True)
