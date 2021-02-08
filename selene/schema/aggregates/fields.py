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

from gvm.protocols.next import (
    EntityType as GvmEntityType,
    AggregateStatistic as GvmAggregateStatistic,
    SortOrder as GvmSortOrder,
)

from selene.schema.utils import get_text_from_element, get_int_from_element


class AggregateEntityType(graphene.Enum):
    """
    Enum class for entity types
    """

    class Meta:
        enum = GvmEntityType


class AggregateMode(graphene.Enum):
    """
    Enum class for aggregate modes
    """

    WORD_COUNTS = 'word_counts'


class AggregateStatistic(graphene.Enum):
    """
    Enum class for aggregate group statistics
    """

    class Meta:
        enum = GvmAggregateStatistic


class SortOrder(graphene.Enum):
    """
    Enum class for sort order (ascending or descending)
    """

    class Meta:
        enum = GvmSortOrder


class AggregateStats(graphene.ObjectType):
    """
    Object class representing aggregated data statistics within a data group
    or subgroup.
    """

    column = graphene.String(
        description='Name of the column the statistics are calculated for'
    )
    minimum = graphene.Float(
        name='min', description='The minimum value within the (sub)group'
    )
    maximum = graphene.Float(
        name='max', description='The maximum value within the (sub)group'
    )
    mean = graphene.Float(
        description='The arithmetic mean of the values within the (sub)group'
    )
    sum = graphene.Float(description='Sum of values within the (sub)group')
    cumulative_sum = graphene.Float(
        description='Cumulative sum of values up to and including the current'
        ' (sub)group'
    )

    @staticmethod
    def resolve_column(root, _info):
        return root.attrib.get('column')

    @staticmethod
    def resolve_minimum(root, _info):
        return get_text_from_element(root, 'min')

    @staticmethod
    def resolve_maximum(root, _info):
        return get_text_from_element(root, 'max')

    @staticmethod
    def resolve_mean(root, _info):
        return get_text_from_element(root, 'mean')

    @staticmethod
    def resolve_sum(root, _info):
        return get_text_from_element(root, 'sum')

    @staticmethod
    def resolve_cumulative_sum(root, _info):
        return get_text_from_element(root, 'c_sum')


class AggregateTextColumn(graphene.ObjectType):
    """
    Object class representing a text column value
    """

    column = graphene.String(description='Column the text is fetched from')
    text = graphene.String(description='Text value of the column')

    @staticmethod
    def resolve_column(root, _info):
        return root.attrib.get('column')

    @staticmethod
    def resolve_text(root, _info):
        return root.text


class _BaseAggregateGroup(graphene.ObjectType):
    """
    Base object class representing an aggregate group.
    """

    value = graphene.String(
        description='Value of the field the data is (sub)grouped by.'
    )
    count = graphene.Int(description='Number of items within the (sub)group')
    cumulative_count = graphene.Int(
        description='Cumulative number of items up to and including the'
        ' current (sub)group'
    )
    stats = graphene.List(
        AggregateStats,
        description='Statistics collected from data columns within the'
        ' (sub)group',
    )
    text_columns = graphene.List(
        AggregateTextColumn,
        description='Simple text columns without statistics within the'
        ' (sub)group',
    )

    @staticmethod
    def resolve_value(root, _info):
        return get_text_from_element(root, 'value')

    @staticmethod
    def resolve_count(root, _info):
        return get_int_from_element(root, 'count')

    @staticmethod
    def resolve_cumulative_count(root, _info):
        return get_int_from_element(root, 'c_count')

    @staticmethod
    def resolve_stats(root, _info):
        return root.findall('stats')

    @staticmethod
    def resolve_text_columns(root, _info):
        return root.findall('text')


class AggregateSubgroup(_BaseAggregateGroup):
    """
    Object class representing an aggregate subgroup.

    """


class AggregateGroup(_BaseAggregateGroup):
    """
    Object class representing an aggregate group.
    """

    subgroups = graphene.List(
        AggregateSubgroup,
        description='List of subgroups and their statistics within the group',
    )

    @staticmethod
    def resolve_subgroups(root, _info):
        return root.findall('subgroup')


class AggregateColumnInfo(graphene.ObjectType):
    """
    Object class for metadata describing an aggregate column
    """

    name = graphene.String(
        description='Compound descriptor made up from the statistic and'
        'column used, e.g. "severity_max"'
    )
    stat = AggregateStatistic(
        description='Name of the statistic, e.g. "min", "max", etc.'
    )
    entity_type = AggregateEntityType(
        description='The entity type of the the statistic is collected from'
    )
    column = graphene.String(
        description='The column the statistic is collected from'
    )
    data_type = graphene.String(
        description='The data type of the statistic, e.g. integer, text'
    )

    @staticmethod
    def resolve_name(root, _info):
        return get_text_from_element(root, 'name')

    @staticmethod
    def resolve_stat(root, _info):
        return get_text_from_element(root, 'stat')

    @staticmethod
    def resolve_entity_type(root, _info):
        return get_text_from_element(root, 'type')

    @staticmethod
    def resolve_column(root, _info):
        return get_text_from_element(root, 'column')

    @staticmethod
    def resolve_data_type(root, _info):
        return get_text_from_element(root, 'data_type')


class Aggregate(graphene.ObjectType):
    """
    Object class representing a collection of aggregated .
    """

    overall = graphene.Field(
        AggregateGroup, description='Overall aggregate statistics'
    )

    groups = graphene.List(AggregateGroup, description='List of groups')

    subgroup_values = graphene.List(
        graphene.String,
        description='List of subgroup values collected from all groups',
    )

    column_info = graphene.List(
        AggregateColumnInfo,
        description='List of metadata items describing the columns',
    )

    @staticmethod
    def resolve_overall(root, _info):
        return root.find('overall')

    @staticmethod
    def resolve_groups(root, _info):
        return root.findall('group')

    @staticmethod
    def resolve_subgroup_values(root, _info):
        subgroups_elem = root.find('subgroups')
        if subgroups_elem is not None:
            subgroups = []
            for elem in subgroups_elem.findall('value'):
                subgroups.append(elem.text if elem.text is not None else '')
            return subgroups
        else:
            return None

    @staticmethod
    def resolve_column_info(root, _info):
        return root.find('column_info').findall('aggregate_column')
