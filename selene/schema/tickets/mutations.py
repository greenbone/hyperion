# -*- coding: utf-8 -*-
# Copyright (C) 2019 Greenbone Networks GmbH
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
    create_export_by_filter_mutation,
    create_export_by_ids_mutation,
    create_delete_by_ids_mutation,
    create_delete_by_filter_mutation,
)

from selene.schema.utils import (
    get_gmp,
    require_authentication,
)
from selene.schema.tickets.fields import TicketStatus


class CloneTicket(graphene.Mutation):
    """Clones a ticket

    Args:
        id (UUID): UUID of ticket to clone.

    Returns:
        id (UUID)
    """

    class Arguments:
        ticket_id = graphene.UUID(required=True, name='id')

    ticket_id = graphene.UUID(name='id')

    @require_authentication
    def mutate(root, info, ticket_id):
        gmp = get_gmp(info)
        elem = gmp.clone_ticket(str(ticket_id))
        return CloneTicket(ticket_id=elem.get('id'))


# Explicit classes needed, else we get error
# 'AssertionError: Found different types with the same name in the
#   schema: DeleteByIds, DeleteByIds.'

DeleteByIdsClass = create_delete_by_ids_mutation(entity_name='ticket')


class DeleteTicketsByIds(DeleteByIdsClass):
    """Deletes a list of tickets

    Args:
        ids (List(UUID)): List of UUIDs of tickets to delete.

    Returns:
        ok (Boolean)
    """


DeleteByFilterClass = create_delete_by_filter_mutation(entity_name='ticket')


class DeleteTicketsByFilter(DeleteByFilterClass):
    """Deletes a filtered list of tickets
    Args:
        filterString (str): Filter string for ticket list to delete.
    Returns:
        ok (Boolean)
    """


class CreateTicketInput(graphene.InputObjectType):
    """Input object for createTicket.

    Args:
        note (str): A note to the ticket.
        result_id (UUID): UUID of result for the ticket
        assigned_to_user_id (UUID): UUID of assigned user.
        comment (str, optional): The comment on the ticket.
    """

    note = graphene.String(required=True, description="Ticket note.")
    comment = graphene.String(description="Ticket comment.")
    result_id = graphene.UUID(
        required=True,
        description=("UUID of result for the ticket."),
    )
    assigned_to_user_id = graphene.UUID(
        required=True, description="UUID of assigned user."
    )


class CreateTicket(graphene.Mutation):
    """Creates a new ticket. Call with createTicket.

    Args:
        input (CreateTicketInput): Input object for CreateTicket

    """

    class Arguments:
        input_object = CreateTicketInput(required=True, name='input')

    ticket_id = graphene.UUID(name='id')

    @require_authentication
    def mutate(root, info, input_object):

        note = input_object.note
        comment = input_object.comment

        if input_object.result_id is not None:
            result_id = str(input_object.result_id)
        else:
            result_id = None
        if input_object.assigned_to_user_id is not None:
            assigned_to_user_id = str(input_object.assigned_to_user_id)
        else:
            assigned_to_user_id = None

        gmp = get_gmp(info)

        resp = gmp.create_ticket(
            note=note,
            comment=comment,
            result_id=result_id,
            assigned_to_user_id=assigned_to_user_id,
        )
        return CreateTicket(ticket_id=resp.get('id'))


class ModifyTicketInput(graphene.InputObjectType):
    """Input object for modifyTicket.

    Args:
        id (UUID): UUID of ticket to modify.
        note (str, optional): A note to the ticket.
        assigned_to_user_id (UUID, optional): UUID of assigned user.
        comment (str, optional): The comment on the ticket.
        status (TicketStatus, optional): New status for the ticket
    """

    ticket_id = graphene.UUID(
        required=True, description="UUID of ticket to modify.", name='id'
    )
    note = graphene.String(description="Ticket note.")
    comment = graphene.String(description="Ticket comment.")
    assigned_to_user_id = graphene.UUID(description="UUID of assigned user.")
    ticket_status = TicketStatus(description="Status of the Ticket")


class ModifyTicket(graphene.Mutation):

    """Modifies an existing ticket. Call with modifyTicket.

    Args:
        input (ModifyTicketInput): Input object for ModifyTicket

    Returns:
        ok (Boolean)
    """

    class Arguments:
        input_object = ModifyTicketInput(required=True, name='input')

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, input_object):

        ticket_id = str(input_object.ticket_id)

        note = input_object.note
        comment = input_object.comment

        if input_object.assigned_to_user_id is not None:
            assigned_to_user_id = str(input_object.assigned_to_user_id)
        else:
            assigned_to_user_id = None

        gmp = get_gmp(info)

        gmp.modify_ticket(
            ticket_id,
            note=note,
            comment=comment,
            assigned_to_user_id=assigned_to_user_id,
            status=TicketStatus.get(input_object.ticket_status),
        )

        return ModifyTicket(ok=True)


# Explicit classes needed, else we get error
# 'AssertionError: Found different types with the same name in the
#   schema: ExportByIds, ExportByIds.'

ExportByIdsClass = create_export_by_ids_mutation(entity_name='ticket')


class ExportTicketsByIds(ExportByIdsClass):
    pass


ExportByFilterClass = create_export_by_filter_mutation(entity_name='ticket')


class ExportTicketsByFilter(ExportByFilterClass):
    pass
