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

import graphene

from selene.schema.utils import require_authentication, get_gmp

from selene.schema.entities import (
    create_export_by_ids_mutation,
    create_export_by_filter_mutation,
    create_delete_by_ids_mutation,
    create_delete_by_filter_mutation,
)


class CloneRole(graphene.Mutation):
    """Clone an existing Role.

    Args:
        id (UUID): UUID of an existing Role to clone

    Example:

        .. code-block::

            mutation {
                cloneRole(
                    id: "b992601e-e0df-4078-b4b1-39e04f92f4cc",
                ) {
                    id
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "cloneRole": {
                    "id": "a569f3df-0f8d-4001-aeef-08cdee0cdf49"
                    }
                }
            }
    """

    class Arguments:
        role_id = graphene.UUID(required=True, name='id')

    role_id = graphene.UUID(name='id')

    @require_authentication
    def mutate(root, info, role_id):
        gmp = get_gmp(info)
        elem = gmp.clone_role(str(role_id))
        return CloneRole(role_id=elem.get('id'))


class CreateRoleInput(graphene.InputObjectType):
    """Input Object for CreateRole

    Args:
        name (str): Name of the role
        comment (str, optional): Comment for the role
        users (List[str], optional): List of user names to add to the role
    """

    name = graphene.String(required=True, description="Name of the role.")
    comment = graphene.String(description="Comment for the role.")
    users = graphene.List(
        graphene.String, description="List of user names to add to the role."
    )


class CreateRole(graphene.Mutation):
    """Create a Role.

    Args:
        Input (CreateRole): input object for CreateRole

    Example:

        .. code-block::

            mutation {
                createRole( input" {
                    name: "some name",
                    comment: "some comment",
                    users: ["user1","user2"]}
                ) {
                    id
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "createRole": {
                        "id": "a569f3df-0f8d-4001-aeef-08cdee0cdf49"
                    }
                }
            }
    """

    class Arguments:
        input_object = CreateRoleInput(required=True, name='input')

    id_of_created_role = graphene.String(name='id')

    @require_authentication
    def mutate(root, info, input_object):
        gmp = get_gmp(info)

        name = input_object.name if input_object.name is not None else None

        comment = (
            input_object.comment if input_object.comment is not None else None
        )
        users = input_object.users if input_object.users is not None else None

        elem = gmp.create_role(name=name, comment=comment, users=users)

        return CreateRole(id_of_created_role=elem.get('id'))


class ModifyRoleInput(graphene.InputObjectType):
    """Input object for modifyRole.

    Args:
        role_id (str): UUID of role to modify.
        comment (str, optional): Name of role.
        name (str, optional): Comment on role.
        users (List[str], optional): List of user names.
    """

    role_id = graphene.UUID(
        required=True, description="UUID of role to modify.", name='id'
    )

    comment = graphene.String(description="Comment of role.")
    name = graphene.String(description="Name of role.")
    users = graphene.List(graphene.String, description="List of user names.")


class ModifyRole(graphene.Mutation):
    """Modifies an existing role.

    Args:
        input (ModifyRoleInput): Input object for ModifyRole
    """

    class Arguments:
        input_object = ModifyRoleInput(required=True, name='input')

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, input_object):
        role_id = (
            str(input_object.role_id)
            if input_object.role_id is not None
            else None
        )

        comment = (
            input_object.comment if input_object.comment is not None else None
        )
        name = input_object.name if input_object.name is not None else None
        users = input_object.users if input_object.users is not None else None

        gmp = get_gmp(info)

        gmp.modify_role(
            role_id=role_id, name=name, comment=comment, users=users
        )

        return ModifyRole(ok=True)


class DeleteRole(graphene.Mutation):
    """Deletes a role

    Args:
        id (UUID): UUID of role to delete.
        ultimate (bool, optional): Whether to remove entirely,
            or to the trashcan.

    Returns:
        ok (Boolean)

    Example

        mutation {
            deleteRole(id: "5f8e7b31-35ea-4b43-9797-6d77f058906b",
                         ultimate: false)
            {
                ok
            }
        }

        Response
        {
            "data": {
                "deleteRole": {
                    "ok": true
                }
            }
        }
    """

    class Arguments:
        role_id = graphene.UUID(required=True, name='id')
        ultimate = graphene.Boolean(required=False)

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, role_id, ultimate):
        gmp = get_gmp(info)
        gmp.delete_role(str(role_id), ultimate=ultimate)
        return DeleteRole(ok=True)


# Explicit classes needed, else we get error
# 'AssertionError: Found different types with the same name in the
#   schema: DeleteByIds, DeleteByIds.'

DeleteByIdsClass = create_delete_by_ids_mutation(entity_name='role')


class DeleteRolesByIds(DeleteByIdsClass):
    """Deletes a list of roles"""


DeleteByFilterClass = create_delete_by_filter_mutation(entity_name='role')


class DeleteRolesByFilter(DeleteByFilterClass):
    """Deletes a filtered list of roles"""


ExportByIdsClass = create_export_by_ids_mutation(entity_name='role')


class ExportRolesByIds(ExportByIdsClass):
    pass


ExportByFilterClass = create_export_by_filter_mutation(entity_name='role')


class ExportRolesByFilter(ExportByFilterClass):
    pass
