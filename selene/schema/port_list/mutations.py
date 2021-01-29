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


from selene.schema.entities import (
    create_delete_by_ids_mutation,
    create_delete_by_filter_mutation,
    create_export_by_ids_mutation,
    create_export_by_filter_mutation,
)

from selene.schema.port_list.fields import PortRangeType

from selene.schema.utils import (
    require_authentication,
    get_gmp,
)


class CreatePortRangeInput(graphene.InputObjectType):
    """Input object for createPortRange.

    Args:
        port_list_id (UUID): UUID of the port list to which to add the range
        start (int): The first port in the range
        end (int): The last port in the range
        port_range_type (PortRangeType): The type of the ports: TCP, UDP
        comment (str, optional): Comment for the port range
    """

    port_list_id = graphene.UUID(
        required=True,
        description="UUID of the port list to which to add the range",
    )
    start = graphene.Int(
        required=True, description="The first port in the range"
    )
    end = graphene.Int(required=True, description="The last port in the range")
    port_range_type = PortRangeType(
        required=True, description="The type of the ports: TCP, UDP"
    )
    comment = graphene.String(description="Comment for the port range")


class CreatePortRange(graphene.Mutation):
    """Creates a new port range. Call with createPortRange.

    Args:
        input (CreatePortRangeInput): Input object for CreatePortRange

    """

    class Arguments:
        input_object = CreatePortRangeInput(required=True, name='input')

    port_range_id = graphene.UUID(name='id')

    @require_authentication
    def mutate(root, info, input_object):
        gmp = get_gmp(info)

        resp = gmp.create_port_range(
            str(input_object.port_list_id),
            input_object.start,
            input_object.end,
            PortRangeType.get(input_object.port_range_type),
            comment=input_object.comment,
        )
        return CreatePortRange(port_range_id=resp.get('id'))


class DeletePortRange(graphene.Mutation):
    """Deletes a port range

    Args:
        id (UUID): UUID of port range to delete.

    Returns:
        ok (Boolean)
    """

    class Arguments:
        port_range_id = graphene.UUID(required=True, name='id')

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, port_range_id):
        gmp = get_gmp(info)
        gmp.delete_port_range(str(port_range_id))
        return DeletePortRange(ok=True)


class ClonePortList(graphene.Mutation):
    """Clone a port_list

    Args:
        id (UUID): UUID of port_list to clone.

    Example:

        .. code-block::

            mutation {
                clonePortList(
                    id: "b992601e-e0df-4078-b4b1-39e04f92f4cc",
                ) {
                    id
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "clonePortList": {
                    "id": "a569f3df-0f8d-4001-aeef-08cdee0cdf49"
                    }
                }
            }
    """

    class Arguments:
        port_list_id = graphene.UUID(required=True, name='id')

    port_list_id = graphene.UUID(name='id')

    @require_authentication
    def mutate(root, info, port_list_id):
        gmp = get_gmp(info)
        elem = gmp.clone_port_list(str(port_list_id))
        return ClonePortList(port_list_id=elem.get('id'))


class CreatePortListInput(graphene.InputObjectType):
    """Input object for createPortList.

    Args:
        name (str): The name of the port_list.
        comment (str, optional): The comment on the port_list.
        port_range (list): Port range list, array of string port ranges
    """

    name = graphene.String(required=True, description="PortList name.")
    port_range = graphene.List(graphene.String, required=True)
    comment = graphene.String(description="PortList comment.")


class CreatePortList(graphene.Mutation):
    """Creates a new port_list. Call with createPortList.

    Args:
        input (CreatePortListInput): Input object for CreatePortList

    """

    class Arguments:
        input_object = CreatePortListInput(required=True, name='input')

    port_list_id = graphene.UUID(name='id')

    @require_authentication
    def mutate(root, info, input_object):

        name = input_object.name
        comment = input_object.comment
        port_range = ','.join(input_object.port_range)

        gmp = get_gmp(info)

        resp = gmp.create_port_list(
            name=name,
            port_range=port_range,
            comment=comment,
        )
        return CreatePortList(port_list_id=resp.get('id'))


class ModifyPortListInput(graphene.InputObjectType):
    """Input object for createPortList.

    Args:
        port_list_id (UUID): The port_list to modify
        name (str): The name of the port_list.
        comment (str, optional): The comment on the port_list.
        port_range (list): Port range list, array of string port ranges
    """

    port_list_id = graphene.UUID(name='id', required=True)
    name = graphene.String(description="PortList name.")
    port_range = graphene.List(graphene.String)
    comment = graphene.String(description="PortList comment.")


class ModifyPortList(graphene.Mutation):
    """Modifys a new port_list. Call with createPortList.

    Args:
        input (ModifyPortListInput): Input object for ModifyPortList

    """

    class Arguments:
        input_object = ModifyPortListInput(required=True, name='input')

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, input_object):

        name = input_object.name
        comment = input_object.comment
        # port_range = ','.join(input_object.port_range)

        gmp = get_gmp(info)

        gmp.modify_port_list(
            port_list_id=str(input_object.port_list_id),
            name=name,
            # port_range=port_range, #not supported by python-gvm now ...
            comment=comment,
        )
        return ModifyPortList(ok=True)


# Explicit classes needed, else we get error
# 'AssertionError: Found different types with the same name in the
#   schema: ExportByIds, ExportByIds.'

ExportByIdsClass = create_export_by_ids_mutation(
    entity_name='port_list', with_details=True
)


class ExportPortListsByIds(ExportByIdsClass):
    pass


ExportByFilterClass = create_export_by_filter_mutation(
    entity_name='port_list', with_details=True
)


class ExportPortListsByFilter(ExportByFilterClass):
    pass


#   schema: DeleteByIds, DeleteByIds.'

DeleteByIdsClass = create_delete_by_ids_mutation(entity_name='port_list')


class DeletePortListsByIds(DeleteByIdsClass):
    """Deletes a list of port_lists

    Args:
        ids (List(UUID)): List of UUIDs of port_lists to delete.
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.

    Returns:
        ok (Boolean)

    Example

        mutation {
            deletePortListsByIds(
                ids: ["5f8e7b31-35ea-4b43-9797-6d77f058906b"],
                ultimate: false)
            {
                ok
            }
        }

        Response
        {
            "data": {
                "deletePortListsByIds": {
                    "ok": true
                }
            }
        }
    """


DeleteByFilterClass = create_delete_by_filter_mutation(entity_name='port_list')


class DeletePortListsByFilter(DeleteByFilterClass):
    """Deletes a filtered list of port_lists

    Args:
        filterString (str): Filter string for port_list list to delete.
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.

    Returns:
        ok (Boolean)

    Example

        mutation {
            deletePortListByFilter(
                filterString:"name~Clone",
                ultimate: false)
            {
                ok
            }
        }

        Response
        {
            "data": {
                "deletePortListByFilter": {
                    "ok": true
                }
            }
        }
    """
