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

from base64 import b64encode, b64decode

from collections import OrderedDict
from typing import List, Optional, Type, Tuple, Iterable

import graphene

from graphql import ResolveInfo
from graphql.language import ast

from selene.schema.parser import (
    parse_int,
    parse_filter_string,
    FilterString as FilterStringModel,
)
from selene.schema.utils import get_int_from_element, get_text, XmlElement


def get_cursor(entity_type_name: str, offset: int) -> str:
    str_cursor = f"{entity_type_name}:{offset}"
    # b64encode only takes bytes as argument
    encoded_cursor = b64encode(str_cursor.encode('utf-8'))
    return encoded_cursor.decode('utf-8')  # convert back to str


def get_offset_from_cursor(cursor: str) -> str:
    plain_cursor = b64decode(cursor.encode('utf-8')).decode('utf-8')
    _, offset = plain_cursor.split(':', 1)
    return parse_int(offset, safe=False)


def get_filter_string_for_pagination(
    filter_string: FilterStringModel,
    *,
    first: int = None,
    last: int = None,
    after: str = None,
    before: str = None,
) -> FilterStringModel:
    if not filter_string:
        filter_string = FilterStringModel()

    if first is not None:
        filter_string = filter_string.remove_rows()
        filter_string = filter_string.add_rows(first)
    elif last is not None:
        filter_string = filter_string.remove_rows()
        filter_string = filter_string.add_rows(last)

    if after is not None:
        offset = get_offset_from_cursor(after)
        # the edge node index is zero based the.
        # the filter index with first is one based.
        # this adds one to the offset.
        # because we want get the node AFTER the passed one we need to add
        # two to the offset
        offset += 2

        filter_string = filter_string.remove_first()
        filter_string = filter_string.add_first(offset)

    elif before is not None and last is not None:
        offset = get_offset_from_cursor(before)
        # the edge node index is zero based the.
        # the filter index with first is one based.
        # therefore last must be subtracted by one.
        # to get the index of the first entity we need to subtract last from
        # the offset
        offset -= last - 1

        if offset <= 0:
            offset = 1

        filter_string = filter_string.remove_first()
        filter_string = filter_string.add_first(offset)

    return filter_string


class EntitiesCounts(graphene.ObjectType):
    """Counts for the requested entity type"""

    filtered = graphene.Field(
        graphene.Int, description="Number of nodes available for the filter."
    )
    total = graphene.Field(
        graphene.Int,
        description="Number of nodes possible available without any filter.",
    )
    offset = graphene.Field(
        graphene.Int, description="Zero based offset to the first node."
    )
    limit = graphene.Field(
        graphene.Int, description="Number of requested nodes."
    )
    length = graphene.Field(
        graphene.Int, description="Number of nodes in the response."
    )

    def __init__(
        self, *, filtered=None, total=None, offset=None, limit=None, length=None
    ):
        super().__init__(
            filtered=filtered,
            total=total,
            offset=offset,
            limit=limit,
            length=length,
        )
        self.filtered = filtered or 0
        self.total = total or 0
        self.offset = offset or 0
        self.limit = limit or 0
        self.length = length or 0


class Entities:
    """A helper class to store XML elements for the entities"""

    def __init__(
        self,
        entity_elements: List[XmlElement],
        counts_element: XmlElement,
        requested_element: XmlElement,
    ):
        self.entity_elements = entity_elements
        self.counts_element = counts_element
        self.requested_element = requested_element

    def get_filtered_count(self) -> Optional[int]:
        """Return the number of entities available for this filter"""
        return get_int_from_element(self.counts_element, 'filtered')

    def get_total_count(self) -> Optional[int]:
        """Return the number of available entities without a filter"""
        value = get_text(self.counts_element)
        return int(value) if value is not None else value

    def get_offset(self) -> Optional[int]:
        """Return the index of the first entity"""
        value = self.requested_element.get('start')
        return int(value) - 1 if value is not None else value

    def get_limit(self) -> Optional[int]:
        """Return the maximum number of requested entities"""
        value = self.requested_element.get('max')
        return int(value) if value is not None else value

    def get_length(self) -> int:
        """Return the number of loaded entities"""
        return len(self.entity_elements)

    def get_entities_counts(self) -> EntitiesCounts:
        return EntitiesCounts(
            filtered=self.get_filtered_count(),
            total=self.get_total_count(),
            offset=self.get_offset(),
            limit=self.get_limit(),
            length=self.get_length(),
        )


def create_edge_graphene_type(
    name: str, type_name, entity: Type[graphene.ObjectType]
) -> Type[graphene.ObjectType]:
    """Dynamically create a new class for the edge representation"""

    class EdgeBase(graphene.ObjectType):
        node = graphene.Field(
            entity, description="The entity item of the edge", required=True
        )
        cursor = graphene.Field(
            graphene.String,
            description="A cursor to the entity for use in pagination",
            required=True,
        )

        @staticmethod
        def resolve_node(root: Tuple[int, XmlElement], _info: ResolveInfo):
            _, element = root
            return element

        @classmethod
        def resolve_cursor(
            cls, root: Tuple[int, XmlElement], _info: ResolveInfo
        ):
            offset, _ = root
            return cls.get_cursor(offset)

        @classmethod
        def get_cursor(cls, entity_id: str):
            return get_cursor(type_name, entity_id)

    class EdgeMeta:
        description = f"A edge containing a `{name}` entity and its cursor."

    return type(f'{name}Edge', (EdgeBase,), {'Meta': EdgeMeta})


class EntitiesPageInfo(graphene.PageInfo):
    last_page_cursor = graphene.String(description="A cursor to the last page.")

    @staticmethod
    def resolve_has_next_page(
        root: Tuple[graphene.ObjectType, EntitiesCounts], _info: ResolveInfo
    ) -> bool:
        _, counts = root
        return (
            counts.length > 0
            and counts.length + counts.offset < counts.filtered
        )

    @staticmethod
    def resolve_has_previous_page(
        root: Tuple[graphene.ObjectType, EntitiesCounts], _info: ResolveInfo
    ) -> bool:
        _, counts = root
        return counts.length > 0 and counts.offset > 0

    @staticmethod
    def resolve_start_cursor(
        root: Tuple[graphene.ObjectType, EntitiesCounts], _info: ResolveInfo
    ) -> str:
        edge, counts = root
        return edge.get_cursor(counts.offset)

    @staticmethod
    def resolve_end_cursor(
        root: Tuple[graphene.ObjectType, EntitiesCounts], _info: ResolveInfo
    ) -> str:
        edge, counts = root
        offset = 0 if counts.length <= 0 else counts.offset + counts.length - 1
        return edge.get_cursor(offset)

    @staticmethod
    def resolve_last_page_cursor(
        root: Tuple[graphene.ObjectType, EntitiesCounts], _info: ResolveInfo
    ) -> str:
        edge, counts = root
        if (
            counts.length <= 0  # no entities
            or counts.filtered < counts.limit  # only one page
            or counts.limit is None  # all entities are requested
            or counts.limit <= 0  # all entities are requested
        ):
            offset = 0
        else:
            offset = counts.filtered - (counts.filtered % counts.limit) - 1

        return edge.get_cursor(offset)


class EntityConnection(graphene.ObjectType):
    """Relay compliant `Connection` type for entities"""

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(
        cls,
        name: str = None,
        entity_type: Type[graphene.ObjectType] = None,
        entity_type_name: str = None,
        **options,
    ):  # pylint: disable=arguments-differ
        if not name:
            name = cls.__name__

        if not entity_type_name:
            entity_type_name = entity_type.__name__.lower()

        edge = create_edge_graphene_type(
            entity_type.__name__, entity_type_name, entity_type
        )
        _meta = graphene.types.objecttype.ObjectTypeOptions(cls)
        _meta.edge = edge
        _meta.fields = OrderedDict(
            [
                (
                    "page_info",
                    graphene.Field(
                        EntitiesPageInfo,
                        name="pageInfo",
                        required=True,
                        description="Pagination data for this connection.",
                    ),
                ),
                (
                    'edges',
                    graphene.Field(
                        graphene.NonNull(graphene.List(edge)),
                        description="List of edges for this connection.",
                    ),
                ),
                (
                    'nodes',
                    graphene.Field(
                        graphene.NonNull(graphene.List(entity_type)),
                        description="List of entities for this connection.",
                    ),
                ),
                ('counts', graphene.Field(EntitiesCounts, required=True)),
            ]
        )
        return super().__init_subclass_with_meta__(
            _meta=_meta, name=name, **options
        )

    @staticmethod
    def resolve_nodes(root: Entities, _info: ResolveInfo) -> List[XmlElement]:
        return root.entity_elements

    @classmethod
    def resolve_page_info(
        cls, root: Entities, _info: ResolveInfo
    ) -> Tuple[graphene.ObjectType, EntitiesCounts]:
        return cls._meta.edge, root.get_entities_counts()

    @staticmethod
    def resolve_edges(
        root: Entities, _info: ResolveInfo
    ) -> Iterable[Tuple[int, XmlElement]]:
        offset = root.get_offset()
        return enumerate(root.entity_elements, offset)

    @staticmethod
    def resolve_counts(root: Entities, _info: ResolveInfo):
        return root.get_entities_counts()


def create_entity_connection_type(
    entity_type: graphene.ObjectType,
) -> Type[EntityConnection]:
    entity_type_name = entity_type.__name__
    connection_type = type(
        f"{entity_type_name}Connection",
        (EntityConnection,),
        {
            "Meta": {
                'entity_type': entity_type,
                'description': f"A Relay `Connection` type for "
                f"`{entity_type_name}`.",
            }
        },
    )
    return connection_type


class FilterString(graphene.Scalar):
    """A scalar type representing a filter string"""

    @staticmethod
    def serialize(filter_string):
        return str(filter_string)

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return parse_filter_string(node.value)

    @staticmethod
    def parse_value(value):
        return parse_filter_string(value)


class EntityConnectionField(graphene.Field):
    """A graphene field for creating a Relay `Connection` based on an
    entity type

    Used to implement forward and backward pagination. For forward pagination
    the arguments after and first must be provided and for backward pagination
    the arguments before and last must be used.

    To use forward pagination, two arguments are required.

    first takes a non‐negative integer.
    after takes the cursor pointing to a position in a list after that nodes
    should be returned.

    To enable backward pagination, two arguments are required.

    last takes a non‐negative integer.
    before takes the cursor pointing to a position in a list before that nodes
    should be returned.

    Args:
        filter_string (str, optional): Optional filter string to be
            used with query.
        after (str, optional): Show nodes after this cursor. Must be used in
            conjunction with first argument.
        before (str, optional): Show nodes before this cursor. Must be used
            in conjunction with the last argument.
        first (int, optional): Show first number of nodes using the after
            cursor.
        last (int, optional): Show the last number of nodes using the before
            cursor.
    """

    connection_type = None
    entity_type = None

    def __init__(
        self,
        connection_type: Type[EntityConnection] = None,
        entity_type: Type[graphene.ObjectType] = None,
        description: str = None,
        **kwargs,
    ):
        entity_type = entity_type or self.entity_type
        connection_type = connection_type or self.connection_type

        if not connection_type:
            connection_type = create_entity_connection_type(entity_type)

        if description is None:
            description = self.__doc__

        super().__init__(
            connection_type,
            filter_string=FilterString(
                description="Optional filter string to be used with the query"
            ),
            details=graphene.Boolean(
                description="DO NOT USE. Will be removed."
            ),
            after=graphene.String(
                description="Show nodes after this cursor. Must be used in "
                "conjunction with first argument"
            ),
            before=graphene.String(
                description="Show nodes before this cursor. Must be used"
                "in conjunction with the last argument"
            ),
            first=graphene.Int(
                description="Show first number of nodes using the after cursor"
            ),
            last=graphene.Int(
                description="Show the last number of nodes using the before "
                "cursor"
            ),
            resolver=self.resolve_entities,
            description=description,
            **kwargs,
        )

    @staticmethod
    def resolve_entities(*args, **kwargs) -> Entities:
        """Implementation should return an Entities instance"""
        raise NotImplementedError()
