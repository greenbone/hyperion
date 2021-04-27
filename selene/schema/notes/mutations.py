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

from selene.schema.utils import get_gmp, require_authentication

from selene.schema.entities import (
    create_delete_by_ids_mutation,
    create_delete_by_filter_mutation,
    create_export_by_ids_mutation,
    create_export_by_filter_mutation,
)


class CloneNote(graphene.Mutation):
    """Clones a note

    Args:
        id (UUID): UUID of note to clone.

    Returns:
        ok (Boolean)
    """

    class Arguments:
        copy_id = graphene.UUID(
            required=True, name='id', description='UUID of the note to clone.'
        )

    note_id = graphene.UUID(name='id')

    @require_authentication
    def mutate(root, info, copy_id):
        gmp = get_gmp(info)
        resp = gmp.clone_note(str(copy_id))
        return CloneNote(note_id=resp.get('id'))


class CreateNoteInput(graphene.InputObjectType):
    """Input object for createNote.

    Args:
        text (str): Text of the new note
        nvt (NVT): The NVT of the note
    """

    text = graphene.String(required=True, description='Text of the new note')
    nvt_oid = graphene.String(
        required=True, description='OID of the nvt to which note applies'
    )
    days_active = graphene.Int(
        description="Days note will be active. -1 on always, 0 off"
    )
    hosts = graphene.List(
        graphene.String, description="A list of hosts addresses"
    )
    port = graphene.String(description="Port to which the note applies")
    result_id = graphene.UUID(
        description="UUID of a result to which note applies"
    )
    severity = graphene.Float(description="Severity to which note applies")
    task_id = graphene.UUID(description="UUID of task to which note applies")


class CreateNote(graphene.Mutation):
    """Creates a new note. Call with createNote.

    Args:
        input (CreateNoteInput): Input object for CreateNote
    """

    class Arguments:
        input_object = CreateNoteInput(required=True, name='input')

    note_id = graphene.UUID(name='id')

    @require_authentication
    def mutate(root, info, input_object):
        text = input_object.text
        nvt_oid = input_object.nvt_oid
        days_active = input_object.days_active
        if input_object.hosts is not None:
            hosts = [str(host) for host in input_object.hosts]
        else:
            hosts = None
        port = input_object.port
        result_id = (
            str(input_object.result_id)
            if input_object.result_id is not None
            else None
        )
        severity = input_object.severity
        task_id = (
            str(input_object.task_id)
            if input_object.task_id is not None
            else None
        )

        gmp = get_gmp(info)

        resp = gmp.create_note(
            text,
            nvt_oid,
            days_active=days_active,
            hosts=hosts,
            port=port,
            result_id=result_id,
            severity=severity,
            task_id=task_id,
        )

        return CreateNote(note_id=resp.get('id'))


class ModifyNoteInput(graphene.InputObjectType):
    """Input object for modifyNote.

    Args:
        text (str): Text of the new note
        nvt (NVT): The NVT of the note
    """

    note_id = graphene.UUID(
        required=True, name='id', description='UUID of the note to modify'
    )
    text = graphene.String(description='Text of the note')
    days_active = graphene.Int(
        description="Days note will be active. -1 on always, 0 off"
    )
    hosts = graphene.List(
        graphene.String, description="A list of hosts addresses"
    )
    port = graphene.String(description="Port to which the note applies")
    result_id = graphene.UUID(
        description="UUID of a result to which note applies"
    )
    severity = graphene.Float(description="Severity to which note applies")
    task_id = graphene.UUID(description="UUID of task to which note applies")


class ModifyNote(graphene.Mutation):
    """Modifies a note. Call with modifyNote.

    Args:
        input (ModifyNoteInput): Input object for ModifyNote
    """

    class Arguments:
        input_object = ModifyNoteInput(required=True, name='input')

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, input_object):
        note_id = str(input_object.note_id)
        text = input_object.text
        days_active = input_object.days_active
        if input_object.hosts is not None:
            hosts = [str(host) for host in input_object.hosts]
        else:
            hosts = None
        port = input_object.port
        result_id = (
            str(input_object.result_id)
            if input_object.result_id is not None
            else None
        )
        severity = input_object.severity
        task_id = (
            str(input_object.task_id)
            if input_object.task_id is not None
            else None
        )

        gmp = get_gmp(info)

        gmp.modify_note(
            note_id,
            text,
            days_active=days_active,
            hosts=hosts,
            port=port,
            result_id=result_id,
            severity=severity,
            task_id=task_id,
        )

        return ModifyNote(ok=True)


class DeleteNote(graphene.Mutation):
    """Deletes a note

    Args:
        id (UUID): UUID of note to delete.
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.

    Returns:
        ok (Boolean)
    """

    class Arguments:
        note_id = graphene.UUID(required=True, name='id')
        ultimate = graphene.Boolean(name='ultimate')

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, note_id, ultimate):
        gmp = get_gmp(info)
        gmp.delete_note(str(note_id), ultimate=ultimate)
        return DeleteNote(ok=True)


# Explicit classes needed, else we get error
# 'AssertionError: Found different types with the same name in the
#   schema: ExportByIds, ExportByIds.'

ExportByIdsClass = create_export_by_ids_mutation(
    entity_name='note', with_details=True
)


class ExportNotesByIds(ExportByIdsClass):
    pass


ExportByFilterClass = create_export_by_filter_mutation(
    entity_name='note', with_details=True
)


class ExportNotesByFilter(ExportByFilterClass):
    pass


#   schema: DeleteByIds, DeleteByIds.'


DeleteByIdsClass = create_delete_by_ids_mutation(entity_name='note')


class DeleteNotesByIds(DeleteByIdsClass):
    """Deletes a list of notes

    Args:
        ids (List(UUID)): List of UUIDs of notes to delete.
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.

    Returns:
        ok (Boolean)

    Example

        mutation {
            deleteNotesByIds(
                ids: ["5f8e7b31-35ea-4b43-9797-6d77f058906b"],
                ultimate: false)
            {
                ok
            }
        }

        Response
        {
            "data": {
                "deleteNotesByIds": {
                    "ok": true
                }
            }
        }
    """


DeleteByFilterClass = create_delete_by_filter_mutation(entity_name='note')


class DeleteNotesByFilter(DeleteByFilterClass):
    """Deletes a filtered list of notes

    Args:
        filterString (str): Filter string for note list to delete.
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.

    Returns:
        ok (Boolean)

    Example

        mutation {
            deleteNotesByFilter(
                filterString:"name~Clone",
                ultimate: false)
            {
                ok
            }
        }

        Response
        {
            "data": {
                "deleteNotesByFilter": {
                    "ok": true
                }
            }
        }
    """
