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

from selene.schema.permissions.fields import (
    PermissionEntityType,
    PermissionSubjectType,
)

from selene.schema.utils import require_authentication, get_gmp

from selene.schema.entities import (
    create_export_by_ids_mutation,
    create_export_by_filter_mutation,
    create_delete_by_ids_mutation,
    create_delete_by_filter_mutation,
)


class ClonePermission(graphene.Mutation):
    """Clone an existing permission

    Args:
        permission_id (UUID): UUID of an existing permission to clone

    Example:

        .. code-block::

            mutation {
                clonePermission(
                    id: "b992601e-e0df-4078-b4b1-39e04f92f4cc",
                ) {
                    id
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "clonePermission": {
                    "id": "a569f3df-0f8d-4001-aeef-08cdee0cdf49"
                    }
                }
            }
    """

    class Arguments:
        permission_id = graphene.UUID(required=True, name='id')

    permission_id = graphene.UUID(name='id')

    @staticmethod
    @require_authentication
    def mutate(_root, info, permission_id):
        gmp = get_gmp(info)
        elem = gmp.clone_permission(str(permission_id))
        return ClonePermission(permission_id=elem.get('id'))


class CreatePermissionInput(graphene.InputObjectType):
    """Input Object for CreatePermission
    Args:
        name (str): Name of the new permission
        subject_id (str): UUID of subject to whom the permission is granted
        subject_type (PermissionSubjectType): Type of the subject user,
            group or role
        comment (Optional[str]): Comment for the permission
        resource_id (Optional[str]): UUID of entity to which the permission
            applies
        resource_type (Optional[EntityType]): Type of the resource.
            For Super permissions user, group or role
    """

    name = graphene.String(
        required=True, description="Name of the new permission."
    )
    subject_id = graphene.UUID(
        required=True,
        description="UUID of subject to whom the permission is granted.",
    )
    subject_type = PermissionSubjectType(
        required=True, description="Type of the subject user, group or role."
    )

    comment = graphene.String(description="Comment for the permission.")
    resource_id = graphene.UUID(
        description="UUID of entity to which the permission applies."
    )
    resource_type = PermissionEntityType(
        description="Type of the resource. For Super permissions user,"
        " group or role."
    )


class CreatePermission(graphene.Mutation):
    """Create a Permission.

    Args:
        Input (CreatePermissionInput): input object for CreatePermission

    Example:

        .. code-block::

            mutation {
                createPermission( input" {
                    name: "create_alert",
                    subjectId: "085569ce-73ed-11df-83c3-002264764cea",
                    subjectType: ROLE,
                    resourceId: "085569ce-73ed-11df-83c3-002264764cea",
                    resourceType: ALERT,
                    comment: "some comment"}
                ) {
                    id
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "createPermission": {
                        "id": "a569f3df-0f8d-4001-aeef-08cdee0cdf49"
                    }
                }
            }
    """

    class Arguments:
        input_object = CreatePermissionInput(required=True, name='input')

    id_of_created_permission = graphene.String(name='id')

    @staticmethod
    @require_authentication
    def mutate(_root, info, input_object):
        gmp = get_gmp(info)

        # Required args
        name = input_object.name if input_object.name is not None else None
        subject_id = (
            str(input_object.subject_id)
            if input_object.subject_id is not None
            else None
        )
        subject_type = (
            PermissionSubjectType.get(input_object.subject_type)
            if input_object.subject_type is not None
            else None
        )
        # Optional args
        resource_id = (
            str(input_object.resource_id)
            if input_object.resource_id is not None
            else None
        )
        resource_type = (
            PermissionEntityType.get(input_object.resource_type)
            if input_object.resource_type is not None
            else None
        )
        comment = (
            input_object.comment if input_object.comment is not None else None
        )

        elem = gmp.create_permission(
            name=name,
            subject_id=subject_id,
            subject_type=subject_type,
            resource_id=resource_id,
            resource_type=resource_type,
            comment=comment,
        )

        return CreatePermission(id_of_created_permission=elem.get('id'))


class ModifyPermissionInput(graphene.InputObjectType):
    """Input object for modifyPermission.

    Args:
        id (UUID): UUID of permission to be modified.
        comment (str, optional): The comment on the permission.
        name (str, optional): Permission name, currently the name of a command.
        subject_id (str, optional): UUID of subject to whom the permission
            is granted.
        subject_type (PermissionSubjectType, optional): Type of the subject
            user, group or role.
        resource_id (str, optional): UUID of entity to which the
            permission applies.
        resource_type (PermissionEntityType, optional): Type of the resource.
            For Super permissions user, group or role.
    """

    permission_id = graphene.UUID(
        required=True, description="ID of permission to modify.", name='id'
    )

    comment = graphene.String(description="Permission comment.")
    name = graphene.String(description="Permission name.")
    subject_id = graphene.UUID(
        description="Id of subject whom the permission is granted."
    )
    subject_type = PermissionSubjectType(
        description="Type of the subject user, group or role."
    )

    resource_id = graphene.UUID(
        description="UUID of entity to which the permission applies."
    )
    resource_type = PermissionEntityType(
        description="Type of the resource. For Super permissions "
        "user, group or role."
    )


class ModifyPermission(graphene.Mutation):
    """Modifies an existing permission.

    Args:
        input (ModifyPermissionInput): Input object for ModifyPermission
    """

    class Arguments:
        input_object = ModifyPermissionInput(required=True, name='input')

    ok = graphene.Boolean()

    @staticmethod
    @require_authentication
    def mutate(_root, info, input_object):

        permission_id = (
            str(input_object.permission_id)
            if input_object.permission_id is not None
            else None
        )
        comment = (
            input_object.comment if input_object.comment is not None else None
        )
        name = input_object.name if input_object.name is not None else None
        subject_id = (
            str(input_object.subject_id)
            if input_object.subject_id is not None
            else None
        )
        subject_type = (
            PermissionSubjectType.get(input_object.subject_type)
            if input_object.subject_type is not None
            else None
        )
        resource_id = (
            str(input_object.resource_id)
            if input_object.resource_id is not None
            else None
        )
        resource_type = (
            PermissionEntityType.get(input_object.resource_type)
            if input_object.resource_type is not None
            else None
        )

        gmp = get_gmp(info)

        gmp.modify_permission(
            permission_id,
            comment=comment,
            name=name,
            resource_id=resource_id,
            resource_type=resource_type,
            subject_id=subject_id,
            subject_type=subject_type,
        )

        return ModifyPermission(ok=True)


# Explicit classes needed, else we get error
# 'AssertionError: Found different types with the same name in the
#   schema: ExportByIds, ExportByIds.'

ExportByIdsClass = create_export_by_ids_mutation(entity_name='permission')


class ExportPermissionsByIds(ExportByIdsClass):
    pass


ExportByFilterClass = create_export_by_filter_mutation(entity_name='permission')


class ExportPermissionsByFilter(ExportByFilterClass):
    pass


DeleteByIdsClass = create_delete_by_ids_mutation(entity_name='permission')


class DeletePermissionsByIds(DeleteByIdsClass):
    """Deletes a list of permissions"""


DeleteByFilterClass = create_delete_by_filter_mutation(entity_name='permission')


class DeletePermissionsByFilter(DeleteByFilterClass):
    """Deletes a filtered list of permissions"""
