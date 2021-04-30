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

from selene.schema.entities import (
    create_delete_by_ids_mutation,
    create_delete_by_filter_mutation,
    create_export_by_ids_mutation,
    create_export_by_filter_mutation,
)

from selene.schema.port_list.fields import PortRangeType

from selene.schema.utils import require_authentication, get_gmp


class CreatePortRangeInput(graphene.InputObjectType):
    """Input object for createPortRange"""

    port_list_id = graphene.UUID(
        required=True,
        description="UUID of the port list to which to add the range",
    )
    start = graphene.Int(
        required=True, description="The first port in the range"
    )
    end = graphene.Int(required=True, description="The last port in the range")
    port_range_type = graphene.Field(
        PortRangeType,
        required=True,
        description="The type of the ports: TCP, UDP",
    )
    comment = graphene.String(description="Comment for the port range")


class CreatePortRange(graphene.Mutation):
    """Creates a new port range. Call with createPortRange"""

    class Arguments:
        input_object = CreatePortRangeInput(
            required=True,
            name='input',
            description="Input ObjectType for creating a port range",
        )

    port_range_id = graphene.UUID(
        name='id', description="ID of the created port range"
    )

    @staticmethod
    @require_authentication
    def mutate(_root, info, input_object):
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
    """Delete a port range"""

    class Arguments:
        port_range_id = graphene.UUID(required=True, name='id')

    ok = graphene.Boolean()

    @staticmethod
    @require_authentication
    def mutate(_root, info, port_range_id):
        gmp = get_gmp(info)
        gmp.delete_port_range(str(port_range_id))
        return DeletePortRange(ok=True)


class ClonePortList(graphene.Mutation):
    """Clone a port list

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
        port_list_id = graphene.UUID(
            required=True, name='id', description="ID of the port list to clone"
        )

    port_list_id = graphene.UUID(
        name='id', description="ID of the new port list"
    )

    @staticmethod
    @require_authentication
    def mutate(_root, info, port_list_id):
        gmp = get_gmp(info)
        elem = gmp.clone_port_list(str(port_list_id))
        return ClonePortList(port_list_id=elem.get('id'))


class CreatePortListInput(graphene.InputObjectType):
    """Input object for createPortList"""

    name = graphene.String(required=True, description="Name of the port list")
    port_ranges = graphene.List(
        graphene.String,
        required=True,
        description="List of port ranges specifications like "
        "'T: 1-999' or 'U: 1000-1999'",
    )
    comment = graphene.String(description="PortList comment.")


class CreatePortList(graphene.Mutation):
    """Create a new port list"""

    class Arguments:
        input_object = CreatePortListInput(
            required=True,
            name='input',
            description="Input ObjectType to create a port list",
        )

    port_list_id = graphene.UUID(
        name='id', description="ID of the new port list"
    )

    @staticmethod
    @require_authentication
    def mutate(_root, info, input_object):

        name = input_object.name
        comment = input_object.comment
        port_range = ','.join(input_object.port_ranges)

        gmp = get_gmp(info)

        resp = gmp.create_port_list(
            name=name, port_range=port_range, comment=comment
        )
        return CreatePortList(port_list_id=resp.get('id'))


class ModifyPortListInput(graphene.InputObjectType):
    """Input object for modifyPortList"""

    port_list_id = graphene.UUID(
        name='id', required=True, description="ID of to be modified port list"
    )
    name = graphene.String(description="Port list name")
    comment = graphene.String(description="Port list comment")


class ModifyPortList(graphene.Mutation):
    """Modify a port list"""

    class Arguments:
        input_object = ModifyPortListInput(
            required=True,
            name='input',
            description='Input ObjectType for modifying a port list',
        )

    ok = graphene.Boolean(description="True if no error occurred")

    @staticmethod
    @require_authentication
    def mutate(_root, info, input_object):

        name = input_object.name
        comment = input_object.comment

        gmp = get_gmp(info)

        gmp.modify_port_list(
            port_list_id=str(input_object.port_list_id),
            name=name,
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
    """Delete a list of port lists

    Example

        mutation {
            deletePortListsByIds(ids: ["5f8e7b31-35ea-4b43-9797-6d77f058906b"])
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
    """Delete a filtered list of port lists

    Example

        mutation {
            deletePortListByFilter(filterString:"name~Clone")
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
