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

import graphene

from selene.schema.relay import FilterString
from selene.schema.tags.fields import EntityType, ResourceAction
from selene.schema.utils import get_gmp, require_authentication

from selene.schema.entities import (
    create_delete_by_ids_mutation,
    create_delete_by_filter_mutation,
    create_export_by_ids_mutation,
    create_export_by_filter_mutation,
)


class CloneTag(graphene.Mutation):
    """Clones a tag

    Args:
        id (UUID): UUID of tag to clone.

    Returns:
        ok (Boolean)
    """

    class Arguments:
        copy_id = graphene.UUID(
            required=True, name='id', description='UUID of the tag to clone.'
        )

    tag_id = graphene.UUID(name='id')

    @staticmethod
    @require_authentication
    def mutate(_root, info, copy_id):
        gmp = get_gmp(info)
        resp = gmp.clone_tag(str(copy_id))
        return CloneTag(tag_id=resp.get('id'))


class CreateTagInput(graphene.InputObjectType):
    """Input object for createTag.

    Args:
        name (str): Name of the tag. A full tag name consisting
            of namespace and predicate e.g. foo:bar.
        resource_type (EntityType): Entity type the tag is to
            be attached to.
        resource_ids (List[str], optional): IDs of the resources
            the tag is to be attached to.
        value (str, optional): Value associated with the tag.
        comment (str, optional): Comment for the tag.
        active (bool, optional): Whether the tag should be active.
    """

    name = graphene.String(
        required=True,
        description=(
            "Name of the tag. A full tag name consisting"
            "of namespace and predicate e.g. foo:bar."
        ),
    )
    resource_type = EntityType(
        required=True, description="Entity type the tag is to be attached to."
    )
    resource_ids = graphene.List(
        graphene.String,
        description=(
            "IDs of the resources the tag is to be attached to."
            "Only one of resource_filter or resource_ids can be provided."
        ),
    )
    value = graphene.String(description="Value associated with the tag.")
    comment = graphene.String(description="Comment for the tag.")
    active = graphene.Boolean(description="Whether the tag should be active.")


class CreateTag(graphene.Mutation):
    class Arguments:
        input_object = CreateTagInput(required=True, name='input')

    tag_id = graphene.UUID(name='id')

    @staticmethod
    @require_authentication
    def mutate(_root, info, input_object):
        gmp = get_gmp(info)

        resp = gmp.create_tag(
            input_object.name,
            EntityType.get(input_object.resource_type),
            resource_ids=input_object.resource_ids,
            value=input_object.value,
            comment=input_object.comment,
            active=input_object.active,
        )

        return CreateTag(tag_id=resp.get('id'))


class ModifyTagInput(graphene.InputObjectType):
    """Input object for modifyTag.

    Args:
        id (str): ID of target to modify.
        name (str, optional): Name of the tag. A full tag name consisting
            of namespace and predicate e.g. foo:bar.
        resource_type (EntityType, optional): Entity type the tag is to
            be attached to.
        resource_ids (List[str], optional): IDs of the resources
            the tag is to be attached to.
        resource_action (ResourceAction, optional): Whether to add or remove
            resources instead of overwriting. One of ADD,
            SET or REMOVE.
        value (str, optional): Value associated with the tag.
        comment (str, optional): Comment for the tag.
        active (bool, optional): Whether the tag should be active.
    """

    tag_id = graphene.UUID(
        name='id', required=True, description='ID of target to modify.'
    )
    name = graphene.String(
        description=(
            "Name of the tag. A full tag name consisting"
            "of namespace and predicate e.g. foo:bar."
        )
    )
    resource_type = EntityType(
        description="Entity type the tag is to be attached to."
    )
    resource_ids = graphene.List(
        graphene.String,
        description=("IDs of the resources the tag is to be attached to."),
    )
    resource_action = ResourceAction(
        description=(
            "Whether to add or remove "
            "resources instead of overwriting. One of ADD, "
            "SET or REMOVE."
        )
    )
    value = graphene.String(description="Value associated with the tag.")
    comment = graphene.String(description="Comment for the tag.")
    active = graphene.Boolean(description="Whether the tag should be active.")


#   schema: DeleteByIds, DeleteByIds.'

DeleteByIdsClass = create_delete_by_ids_mutation(entity_name='tag')


class DeleteTagsByIds(DeleteByIdsClass):
    """Deletes a list of tags

    Args:
        ids (List(UUID)): List of UUIDs of tag to delete.
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


DeleteByFilterClass = create_delete_by_filter_mutation(entity_name='tag')


class DeleteTagsByFilter(DeleteByFilterClass):
    """Deletes a filtered list of tag

    Args:
        filterString (str): Filter string for tag list to delete.
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

ExportByIdsClass = create_export_by_ids_mutation(entity_name='tag')


class ExportTagsByIds(ExportByIdsClass):
    pass


ExportByFilterClass = create_export_by_filter_mutation(entity_name='tag')


class ExportTagsByFilter(ExportByFilterClass):
    pass


class ModifyTag(graphene.Mutation):
    class Arguments:
        input_object = ModifyTagInput(required=True, name='input')

    ok = graphene.Boolean()

    @staticmethod
    @require_authentication
    def mutate(_root, info, input_object):
        gmp = get_gmp(info)

        if input_object.resource_type is not None:
            resource_type = EntityType.get(input_object.resource_type)
        else:
            resource_type = None

        gmp.modify_tag(
            str(input_object.tag_id),
            name=input_object.name,
            comment=input_object.comment,
            value=input_object.value,
            active=input_object.active,
            resource_action=input_object.resource_action,
            resource_type=resource_type,
            resource_ids=input_object.resource_ids,
        )

        return ModifyTag(ok=True)


class ToggleTagInput(graphene.InputObjectType):
    """Input object for toggleTag.

    Args:
        id (str): ID of target to toggle.
        active (bool): Whether the tag should be active.
    """

    tag_id = graphene.UUID(
        name='id', required=True, description='ID of target to modify.'
    )
    active = graphene.Boolean(
        required=True, description="Whether the tag should be active."
    )


class ToggleTag(graphene.Mutation):
    class Arguments:
        input_object = ToggleTagInput(required=True, name='input')

    ok = graphene.Boolean()

    @staticmethod
    @require_authentication
    def mutate(_root, info, input_object):
        gmp = get_gmp(info)

        gmp.modify_tag(str(input_object.tag_id), active=input_object.active)

        return ToggleTag(ok=True)


class RemoveTagInput(graphene.InputObjectType):
    """Input object for removeTag.

    Args:
        id (str): ID of target to remove.
        resource_type (EntityType): Entity type the tag is to
            be removed from.
        resource_ids (List[str]): IDs of the resources
            the tag is to be removed from.
    """

    tag_id = graphene.UUID(
        name='id', required=True, description='ID of target to remove.'
    )
    resource_type = EntityType(
        required=True, description="Entity type the tag is to be removed from."
    )
    resource_ids = graphene.List(
        graphene.String,
        required=True,
        description=("IDs of the resources the tag is to be removed from."),
    )


class RemoveTag(graphene.Mutation):
    class Arguments:
        input_object = RemoveTagInput(required=True, name='input')

    ok = graphene.Boolean()

    @staticmethod
    @require_authentication
    def mutate(_root, info, input_object):
        gmp = get_gmp(info)

        gmp.modify_tag(
            str(input_object.tag_id),
            resource_ids=input_object.resource_ids,
            resource_type=EntityType.get(input_object.resource_type),
            resource_action='remove',
        )

        return RemoveTag(ok=True)


class AddTagInput(graphene.InputObjectType):
    """Input object for addTag.

    Args:
        id (str): ID of target to add.
        resource_type (EntityType): Entity type the tag is to
            be added to.
        resource_ids (List[str]): IDs of the resources
            the tag is to be added to.
    """

    tag_id = graphene.UUID(
        name='id', required=True, description='ID of target to add.'
    )
    resource_type = EntityType(
        required=True, description="Entity type the tag is to be added to."
    )
    resource_ids = graphene.List(
        graphene.String,
        required=True,
        description=("IDs of the resources the tag is to be added to."),
    )


class AddTag(graphene.Mutation):
    class Arguments:
        input_object = AddTagInput(required=True, name='input')

    ok = graphene.Boolean()

    @staticmethod
    @require_authentication
    def mutate(_root, info, input_object):
        gmp = get_gmp(info)

        gmp.modify_tag(
            str(input_object.tag_id),
            resource_ids=input_object.resource_ids,
            resource_type=EntityType.get(input_object.resource_type),
            resource_action='add',
        )

        return AddTag(ok=True)


class BulkTagInput(graphene.InputObjectType):
    """Input object for bulkTag.

    Args:
        id (str): ID of target to add.
        resource_type (EntityType): Entity type the tag is to
            be attached to.
        resource_ids (List[str], optional): IDs of the resources
            the tag is to be attached to. If resource_filter
            is given, this argument is not used.
        resource_filter (FilterString, optional) – Filter term to select
            resources the tag is to be attached to. If this
            argument is given, resource_ids is not used
    """

    tag_id = graphene.UUID(
        name='id', required=True, description='ID of target to add.'
    )
    resource_type = EntityType(
        required=True, description="Entity type the tag is to be attached to."
    )
    resource_ids = graphene.List(
        graphene.String,
        description=("IDs of the resources the tag is to be attached to."),
    )
    resource_filter = FilterString(
        description=(
            "Filter term to select resources the tag is to be attached to."
        )
    )


class BulkTag(graphene.Mutation):
    class Arguments:
        input_object = BulkTagInput(required=True, name='input')

    ok = graphene.Boolean()

    @staticmethod
    @require_authentication
    def mutate(_root, info, input_object):
        gmp = get_gmp(info)

        if input_object.resource_filter is not None:
            gmp.modify_tag(
                str(input_object.tag_id),
                resource_filter=input_object.resource_filter.filter_string,
                resource_type=EntityType.get(input_object.resource_type),
                resource_action='add',
            )
        else:
            gmp.modify_tag(
                str(input_object.tag_id),
                resource_ids=input_object.resource_ids,
                resource_type=EntityType.get(input_object.resource_type),
                resource_action='add',
            )

        return RemoveTag(ok=True)
