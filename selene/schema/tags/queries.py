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


from uuid import UUID

import graphene

from graphql import ResolveInfo

from selene.schema.parser import FilterString

from selene.schema.relay import (
    EntityConnectionField,
    Entities,
    get_filter_string_for_pagination,
)

from selene.schema.tags.fields import Tag

from selene.schema.utils import get_gmp, require_authentication, XmlElement


class GetTag(graphene.Field):
    """Gets a single tag.

    Args:
        id (UUID): UUID of the tag being queried

    Example:

        .. code-block::

            query {
                tag(id: "e9b98e26-9fff-4ee8-9378-bc44fe3d6f2b"){
                    name
                    id
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "tag": {
                        "name": "foo",
                        "id": "e9b98e26-9fff-4ee8-9378-bc44fe3d6f2b"
                    }
                }
            }

    """

    def __init__(self):
        super().__init__(
            Tag,
            tag_id=graphene.UUID(required=True, name='id'),
            resolver=self.resolve,
        )

    @staticmethod
    @require_authentication
    def resolve(_root, info, tag_id: UUID):
        gmp = get_gmp(info)

        xml = gmp.get_tag(str(tag_id))
        return xml.find('tag')


class GetTags(EntityConnectionField):
    """Gets a list of tags with pagination

    Args:
        filter_string (str, optional): Optional filter string to be
            used with query.

    Example:

        .. code-block::

            query {
                tags (filterString: "foo"){
                    nodes {
                        name
                        comment
                        id
                        value
                    }
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "tags": {
                        "nodes": [
                            {
                                "name": "cat",
                                "id": "e9b98e26-9fff-4ee8-9378-bc44fe3d6f2b",
                                "value": "goat",
                                "comment": "dog"
                            },
                            {
                                "name": "fooTag",
                                "id": "0eac8783-96c0-4486-bbf2-170c26dec1de",
                                "value": "bar",
                                "comment": "hello world"
                            }
                        ]
                    }
                }
            }

    """

    entity_type = Tag

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

        xml: XmlElement = gmp.get_tags(
            filter_string=filter_string.filter_string
        )

        tag_elements = xml.findall('tag')
        counts = xml.find('tag_count')
        requested = xml.find('tags')

        return Entities(tag_elements, counts, requested)
