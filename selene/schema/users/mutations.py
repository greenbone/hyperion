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

from enum import auto
import string

import graphene

from gvm.protocols.gmpv214.gmpv214 import UserAuthType as GvmUserAuthType

from selene.schema.utils import (
    require_authentication,
    get_gmp,
)

from selene.schema.entities import (
    create_export_by_ids_mutation,
    create_export_by_filter_mutation,
)

from selene.schema.utils import (
    get_text_from_element,
)


class CloneUser(graphene.Mutation):
    """Clone an existing user.

    Args:
        id (UUID): UUID of an existing user to clone

    Example:

        .. code-block::

            mutation {
                cloneUser(
                    id: "b992601e-e0df-4078-b4b1-39e04f92f4cc",
                ) {
                    id
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "cloneUser": {
                    "id": "a569f3df-0f8d-4001-aeef-08cdee0cdf49"
                    }
                }
            }
    """

    class Arguments:
        user_id = graphene.UUID(required=True, name='id')

    user_id = graphene.UUID(name='id')

    @require_authentication
    def mutate(root, info, user_id):
        gmp = get_gmp(info)
        elem = gmp.clone_user(str(user_id))
        return CloneUser(user_id=elem.get('id'))


class CreateUserInput(graphene.InputObjectType):
    """Input Object for CreateUser

    Args:
        name (str): Name of the user
        password (Optional[str]): Password of the user
        hosts (Optional[List[str]]): A list of host addresses (IPs, DNS names)
        hosts_allow (Optional[bool]): If True allow only access to passed
            hosts otherwise deny access. Default is False for deny hosts.
        ifaces (Optional[List[str]]): A list of interface names
        ifaces_allow (Optional[bool]): If True allow only access to passed
            interfaces otherwise deny access. Default is False for deny
            interfaces.
        role_ids (Optional[List[str]]): A list of role UUIDs for the use
    """

    name = graphene.String(required=True, description="Name of the user.")
    password = graphene.String(
        required=True, description="Password of the user"
    )
    hosts = graphene.List(
        graphene.String, description="A list of host addresses (IPs, DNS names)"
    )
    hosts_allow = graphene.Boolean(
        description="Allow access only to passed hosts."
    )
    ifaces = graphene.List(
        graphene.String, description="A list of interface names"
    )
    ifaces_allow = graphene.Boolean(
        description="Allow access only to passed ifaces."
    )
    role_ids = graphene.List(
        graphene.UUID, description="A list of role UUIDs for the use"
    )


class CreateUser(graphene.Mutation):
    """Create a User.

    Args:
        Input (CreateUser): input object for CreateUser

    Example:

        .. code-block::

            mutation {
                createUser( input:{
                    name: "del_user",
                        password: "pass",
                        hosts: ["123.45.67.89","22.22.22.22"],
                        hostsAllow: true,
                        ifaces: ["iface1", "iface2"],
                        ifacesAllow: true,
                    roleIds: ["5be3c376-7577-4bad-bde6-3d07fb9ad027",
                        "881a3894-3312-4bce-8260-3f5cd09664a6"],
                    }
                ) {
                    id
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "createUser": {
                        "id": "a569f3df-0f8d-4001-aeef-08cdee0cdf49"
                    }
                }
            }
    """

    class Arguments:
        input_object = CreateUserInput(required=True, name='input')

    id_of_created_user = graphene.String(name='id')

    @require_authentication
    def mutate(root, info, input_object):
        gmp = get_gmp(info)

        name = input_object.name if input_object.name is not None else None
        password = (
            input_object.password if input_object.password is not None else None
        )
        hosts = input_object.hosts if input_object.hosts is not None else None
        hosts_allow = (
            input_object.hosts_allow
            if input_object.hosts_allow is not None
            else None
        )
        ifaces = (
            input_object.ifaces if input_object.ifaces is not None else None
        )
        ifaces_allow = (
            input_object.ifaces_allow
            if input_object.ifaces_allow is not None
            else None
        )
        role_ids = (
            input_object.role_ids if input_object.role_ids is not None else None
        )
        role_ids = [str(role) for role in role_ids]

        elem = gmp.create_user(
            name=name,
            password=password,
            hosts=hosts,
            hosts_allow=hosts_allow,
            ifaces=ifaces,
            ifaces_allow=ifaces_allow,
            role_ids=role_ids,
        )

        return CreateUser(id_of_created_user=elem.get('id'))


class DeleteUserByFilterInput(graphene.InputObjectType):
    """Input Object for DeleteUsersByFilter"""

    filter_string = graphene.String(
        required=True, description="Filter term for users to delete."
    )
    inheritor_id = graphene.String(
        required=False,
        description="The ID of the inheriting user. Overrides inheritior_name.",
    )
    inheritor_name = graphene.String(
        required=False, description="The name of the inheriting user."
    )


class DeleteUsersByFilter(graphene.Mutation):
    """Deletes a filtered list of users"""

    class Arguments:
        input_object = DeleteUserByFilterInput(required=True, name='input')

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, input_object):
        filter_string = (
            input_object.filter_string
            if input_object.filter_string is not None
            else None
        )
        inheritor_id = (
            input_object.inheritor_id
            if input_object.inheritor_id is not None
            else None
        )
        inheritor_name = (
            input_object.inheritor_name
            if input_object.inheritor_name is not None
            else None
        )

        gmp = get_gmp(info)
        get_users_xml_response = gmp.get_users(filter=filter_string)
        xml_users = get_users_xml_response.findall("user")

        found_ids = []
        for user in xml_users:
            found_ids.append(user.get('id'))

        for user_id in found_ids:
            gmp.delete_user(
                user_id=str(user_id),
                inheritor_id=inheritor_id,
                inheritor_name=inheritor_name,
            )

        return DeleteUsersByFilter(ok=True)


class DeleteUserByIdsInput(graphene.InputObjectType):
    """Input Object for DeleteUsersByIds"""

    user_ids = graphene.List(
        graphene.UUID,
        required=True,
        name='ids',
        description="List of UUIDs of users to delete..",
    )
    inheritor_id = graphene.String(
        required=False,
        description="The ID of the inheriting user. Overrides inheritior_name.",
    )
    inheritor_name = graphene.String(
        required=False, description="The name of the inheriting user."
    )


class DeleteUsersByIds(graphene.Mutation):
    """Deletes a list of users"""

    class Arguments:
        input_object = DeleteUserByIdsInput(required=True, name='input')

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, input_object):
        user_ids = (
            input_object.user_ids if input_object.user_ids is not None else None
        )
        if user_ids is None:
            return DeleteUsersByIds(ok=False)
        inheritor_id = (
            input_object.inheritor_id
            if input_object.inheritor_id is not None
            else None
        )
        inheritor_name = (
            input_object.inheritor_name
            if input_object.inheritor_name is not None
            else None
        )

        gmp = get_gmp(info)
        filter_string = ''
        for user_id in user_ids:
            filter_string += f'uuid={str(user_id)} '

        get_users_xml_response = gmp.get_users(filter=filter_string)
        xml_users = get_users_xml_response.findall("user")

        found_ids = []
        for user in xml_users:
            found_ids.append(user.get('id'))

        # Users only get deleted if all Users were found.
        if len(user_ids) != len(found_ids):
            return DeleteUsersByIds(ok=False)
        else:
            for user_id in user_ids:
                gmp.delete_user(
                    user_id=str(user_id),
                    inheritor_id=inheritor_id,
                    inheritor_name=inheritor_name,
                )

        return DeleteUsersByIds(ok=True)


class UserAuthType(graphene.Enum):
    class Meta:
        enum = GvmUserAuthType


class ModifyUserInput(graphene.InputObjectType):
    """Input object for ModifyUser.

    Args:
        id (UUID): ID of user to modify.
        name (str, optional): The name of the user.
        comment (str, optional): The comment on the user.
        password (str, optional): Password of the user. Auth Sources need to
            be set with separately if needed.
        role_ids (List(UUID)): A list of role UUIDs for the user.
        group_ids (List(UUID)): A list of group UUIDs for the user.
        hosts (List(str)): A list of hosts for the user.
        hosts_allow (bool, optional): Defines how the hosts list is to be
            interpreted. If False (default) the list is treated as a deny list.
            All hosts are allowed by default except those provided by the
            hosts parameter. If True the list is treated as a allow list.
            All hosts are denied by default except those provided by the
            hosts parameter.
        ifaces (List(str)): A list of ifaces for the user.
        ifaces_allow (bool, optional): Defines how the ifaces list is to be
            interpreted. If False (default) the list is treated as a deny list.
            All ifaces are allowed by default except those provided by the
            ifaces parameter. If True the list is treated as a allow list.
            All ifaces are denied by default except those provided by the
            ifaces parameter.
        auth_source (UserAuthType): Source allowed for authentication for this
            user.
    """

    user_id = graphene.UUID(
        required=True,
        description="UUID of the user to be modified.",
        name='id',
    )
    name = graphene.String(
        description="The name for the user.",
    )
    comment = graphene.String(description="The comment for the user.")
    password = graphene.String(
        description="The password for the user.",
    )
    role_ids = graphene.List(
        graphene.UUID, description="A list of role UUIDs for the user."
    )
    group_ids = graphene.List(
        graphene.UUID, description="A list of group UUIDs for the user."
    )

    hosts = graphene.List(
        graphene.String, description="A list of hosts for the user."
    )
    hosts_allow = graphene.Boolean(
        description="Treat hosts list either as deny list (false)"
        "or allow list (true)"
    )
    ifaces = graphene.List(
        graphene.String, description="A list of ifaces for the user."
    )
    ifaces_allow = graphene.Boolean(
        description="Treat ifaces list either as deny list (false)"
        "or allow list (true)"
    )
    auth_source = UserAuthType(
        description="Source allowed for authentication for this user"
    )


class UserFieldToModifyType(graphene.Enum):
    """Enum for specifying what user field is to be modified."""

    NAME = auto()
    COMMENT = auto()
    PASSWORD = auto()
    AUTH_SOURCE = auto()
    ROLES = auto()
    HOSTS = auto()
    HOSTS_ALLOW = auto()
    IFACES = auto()
    IFACES_ALLOW = auto()
    GROUPS = auto()


class AbstractModifyUser(graphene.ObjectType):
    class Arguments:
        input_object = ModifyUserInput(required=True, name='input')

    ok = graphene.Boolean()


def create_modify_user_mutation(
    field_to_modify=None,
):
    class ModifyUser(graphene.Mutation, AbstractModifyUser):
        @require_authentication
        def mutate(root, info, input_object):
            gmp = get_gmp(info)

            # No fields given to be modify
            if field_to_modify is None:
                return AbstractModifyUser(ok=False)

            user_id = (
                str(input_object.user_id)
                if input_object.user_id is not None
                else None
            )
            if not user_id:
                return AbstractModifyUser(ok=False)

            # Set the inputs

            name = input_object.name if input_object.name is not None else None
            comment = (
                input_object.comment
                if input_object.comment is not None
                else None
            )
            password = (
                input_object.password
                if input_object.password is not None
                else None
            )
            auth_source = (
                UserAuthType.get(input_object.auth_source)
                if input_object.auth_source is not None
                else None
            )
            hosts = (
                input_object.hosts if input_object.hosts is not None else None
            )
            hosts_allow = (
                input_object.hosts_allow
                if input_object.hosts_allow is not None
                else None
            )
            ifaces = (
                input_object.ifaces if input_object.ifaces is not None else None
            )
            ifaces_allow = (
                input_object.ifaces_allow
                if input_object.ifaces_allow is not None
                else None
            )
            role_ids = (
                [str(id) for id in input_object.role_ids]
                if input_object.role_ids is not None
                else None
            )
            group_ids = (
                [str(id) for id in input_object.group_ids]
                if input_object.group_ids is not None
                else None
            )

            # Get the User which is to be modified
            user_xml = None
            if user_id is not None:
                get_user_xml_response = gmp.get_user(user_id=user_id)
                user_xml = (
                    get_user_xml_response.find('user')
                    if get_user_xml_response is not None
                    else None
                )

            # No user found in reply, so no user to modify
            if user_xml is None:
                return AbstractModifyUser(ok=False)

            # Get all current (not yet modified) fields of the user
            # This is needed because else most of the not supplied fields are
            # replaces by an empty value.

            # Name
            name_old = get_text_from_element(user_xml, 'name')
            # Comment
            comment_old = get_text_from_element(user_xml, 'comment')
            # Hosts
            hosts_old = []
            hosts_string = get_text_from_element(user_xml, 'hosts')
            if hosts_string is not None:
                hosts_string = hosts_string.translate(
                    str.maketrans('', '', string.whitespace)
                )
                hosts_old = hosts_string.split(',')
            # Ifaces list
            ifaces_old = []
            ifaces_string = get_text_from_element(user_xml, 'ifaces')
            if ifaces_string is not None:
                ifaces_string = ifaces_string.translate(
                    str.maketrans('', '', string.whitespace)
                )
                ifaces_old = ifaces_string.split(',')

            # Allow ifaces
            ifaces_allow_old = None
            ifaces_xml = user_xml.find("ifaces")
            if ifaces_xml is not None:
                ifaces_allow_old = bool(int(ifaces_xml.get("allow")))

            # Allow hosts
            hosts_allow_old = None
            hosts_xml = user_xml.find("hosts")
            if hosts_xml is not None:
                hosts_allow_old = bool(int(hosts_xml.get("allow")))

            # Role Ids
            role_ids_old = []
            roles_xml = user_xml.findall('role')
            for role_xml in roles_xml:
                role_ids_old.append(role_xml.get("id"))

            # Use old value if no new value was supplied or field was not set
            # to be modified

            name = (
                name_old
                if name is None
                or field_to_modify is not UserFieldToModifyType.NAME
                else name
            )
            comment = (
                comment_old
                if comment is None
                or field_to_modify is not UserFieldToModifyType.COMMENT
                else comment
            )
            password = (
                password
                if field_to_modify is UserFieldToModifyType.PASSWORD
                else None
            )
            auth_source = (
                auth_source
                if field_to_modify is UserFieldToModifyType.AUTH_SOURCE
                else None
            )
            hosts = (
                hosts_old
                if hosts is None
                or field_to_modify is not UserFieldToModifyType.HOSTS
                else hosts
            )
            ifaces = (
                ifaces_old
                if ifaces is None
                or field_to_modify is not UserFieldToModifyType.IFACES
                else ifaces
            )
            ifaces_allow = (
                ifaces_allow_old
                if ifaces_allow is None
                or field_to_modify is not UserFieldToModifyType.IFACES_ALLOW
                else ifaces_allow
            )
            hosts_allow = (
                hosts_allow_old
                if hosts_allow is None
                or field_to_modify is not UserFieldToModifyType.HOSTS_ALLOW
                else hosts_allow
            )
            role_ids = (
                role_ids_old
                if role_ids is None
                or field_to_modify is not UserFieldToModifyType.ROLES
                else role_ids
            )
            group_ids = (
                None
                if field_to_modify is not UserFieldToModifyType.GROUPS
                else group_ids
            )

            gmp.modify_user(
                user_id=user_id,
                name=name,
                comment=comment,
                password=password,
                auth_source=auth_source,
                role_ids=role_ids,
                hosts=hosts,
                hosts_allow=hosts_allow,
                ifaces=ifaces,
                ifaces_allow=ifaces_allow,
                group_ids=group_ids,
            )

            return AbstractModifyUser(ok=True)

    return ModifyUser


# Modify Name
ModifyUserNameClass = create_modify_user_mutation(
    field_to_modify=UserFieldToModifyType.NAME
)


class ModifyUserSetName(ModifyUserNameClass):
    pass


# Modify Comment
ModifyUserCommentClass = create_modify_user_mutation(
    field_to_modify=UserFieldToModifyType.COMMENT
)


class ModifyUserSetComment(ModifyUserCommentClass):
    pass


# Modify Password
ModifyUserPasswordClass = create_modify_user_mutation(
    field_to_modify=UserFieldToModifyType.PASSWORD
)


class ModifyUserSetPassword(ModifyUserPasswordClass):
    pass


# Modify AuthSource
ModifyUserAuthSourceClass = create_modify_user_mutation(
    field_to_modify=UserFieldToModifyType.AUTH_SOURCE
)


class ModifyUserSetAuthSource(ModifyUserAuthSourceClass):
    pass


# Modify Hosts
ModifyUserHostsClass = create_modify_user_mutation(
    field_to_modify=UserFieldToModifyType.HOSTS
)


class ModifyUserSetHosts(ModifyUserHostsClass):
    pass


# Modify Hosts_allow
ModifyUserHostsAllowClass = create_modify_user_mutation(
    field_to_modify=UserFieldToModifyType.HOSTS_ALLOW
)


class ModifyUserSetHostsAllow(ModifyUserHostsAllowClass):
    pass


# Modify Ifaces
ModifyUserIfacesClass = create_modify_user_mutation(
    field_to_modify=UserFieldToModifyType.IFACES
)


class ModifyUserSetIfaces(ModifyUserIfacesClass):
    pass


# Modify Ifaces_allow
ModifyUserIfacesAllowClass = create_modify_user_mutation(
    field_to_modify=UserFieldToModifyType.IFACES_ALLOW
)


class ModifyUserSetIfacesAllow(ModifyUserIfacesAllowClass):
    pass


# Modify Roles
ModifyUserRolesClass = create_modify_user_mutation(
    field_to_modify=UserFieldToModifyType.ROLES
)


class ModifyUserSetRoles(ModifyUserRolesClass):
    pass


# Modify Groups
ModifyUserGroupsClass = create_modify_user_mutation(
    field_to_modify=UserFieldToModifyType.GROUPS
)


class ModifyUserSetGroups(ModifyUserGroupsClass):
    pass


ExportByIdsClass = create_export_by_ids_mutation(entity_name='user')


class ExportUsersByIds(ExportByIdsClass):
    pass


ExportByFilterClass = create_export_by_filter_mutation(
    entity_name='user',
)


class ExportUsersByFilter(ExportByFilterClass):
    pass
