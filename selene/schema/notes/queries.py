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

from selene.schema.notes.fields import Note
from selene.schema.parser import FilterString

from selene.schema.relay import (
    EntityConnectionField,
    Entities,
    get_filter_string_for_pagination,
)

from selene.schema.utils import (
    get_gmp,
    require_authentication,
    XmlElement,
)


class GetNote(graphene.Field):
    """Gets a single note.

    Args:
        id (UUID): UUID of the note being queried

    Example:

        .. code-block::

            query {
                note(id: "6e618e3a-bdfb-4495-9571-22c84b022b13"){
                    id
                    text
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "note": {
                        "id": "6e618e3a-bdfb-4495-9571-22c84b022b13",
                        "text": "Test Note"
                    }
                }
            }

    """

    def __init__(self):
        super().__init__(
            Note,
            note_id=graphene.UUID(required=True, name='id'),
            resolver=self.resolve,
        )

    @staticmethod
    @require_authentication
    def resolve(_root, info, note_id: UUID):
        gmp = get_gmp(info)

        xml = gmp.get_note(str(note_id))
        return xml.find('note')


class GetNotes(EntityConnectionField):
    """Gets a list of notes with pagination

    Args:
        filter_string (str, optional): Optional filter string to be
            used with query.

    Example:

        .. code-block::

            query {
                notes (filterString: "Test"){
                    nodes {
                        id
                        text
                    }
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "notes": {
                        "nodes": [
                            {
                                "id": "08b69003-5fc2-4037-a479-93b440211c73"
                                "text": "Test Note 1",
                            },
                            {
                                "id": "6b2db524-9fb0-45b8-9b56-d958f84cb546"
                                "text": "Test Note 2",
                            }
                        ]
                    }
                }
            }

    """

    entity_type = Note

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

        xml: XmlElement = gmp.get_notes(
            filter=filter_string.filter_string, details=True
        )

        note_elements = xml.findall('note')
        counts = xml.find('note_count')
        requested = xml.find('notes')

        return Entities(note_elements, counts, requested)
