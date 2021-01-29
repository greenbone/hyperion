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

from gvm.protocols.latest import (
    get_aggregate_statistic_from_string,
    get_sort_order_from_string,
)

from selene.schema.aggregates.fields import (
    Aggregate,
    AggregateEntityType,
    AggregateMode,
    AggregateStatistic,
    SortOrder,
)

from selene.schema.utils import (
    require_authentication,
    get_gmp,
)


class GetAggregateSortInput(graphene.InputObjectType):
    """
    Input object type for aggregate sort criteria.
    """

    field = graphene.String(description='Field to sort the data by')
    stat = AggregateStatistic(description='Statistic to sort the data by')
    order = SortOrder(description='Order in which to sort the data')


class GetAggregateInput(graphene.InputObjectType):
    """
    Input object type for getting an aggregates.
    """

    data_type = graphene.InputField(
        AggregateEntityType,
        required=True,
        description='The entity type the data is aggregated from',
    )
    filter_string = graphene.InputField(
        graphene.String,
        description='Filter term to use to filter query of the entities'
        ' to aggregate',
    )
    data_columns = graphene.List(
        graphene.String, description='List of fields to collect statistics of'
    )
    group_column = graphene.String(description='Field to group the data by')
    subgroup_column = graphene.String(
        description='Field to further group the resources inside groups by'
    )
    text_columns = graphene.List(
        graphene.String,
        description='List of text columns which no statistics are'
        ' calculated for',
    )
    sort_criteria = graphene.List(
        GetAggregateSortInput,
        description='List of criteria to sort the aggregate groups by',
    )
    first_group = graphene.Int(
        description='Index of the first aggregate group to return'
    )
    max_groups = graphene.Int(
        description='Maximum number of aggregate groups to return'
    )
    mode = AggregateMode(
        description='Special aggregation mode like word counts'
    )


def _sort_input_to_python_gvm(sort_input):
    """
    Helper to convert a GetAggregateSortInput to a dict used by python-gvm
    """
    new_item = {}

    field = sort_input.get('field')
    if field:
        new_item['field'] = field

    stat = sort_input.get('stat')
    if stat:
        new_item['stat'] = get_aggregate_statistic_from_string(stat)

    order = sort_input.get('order')
    if order:
        new_item['order'] = get_sort_order_from_string(order)

    return new_item


class GetAggregate(graphene.Field):
    def __init__(self):
        super().__init__(
            Aggregate,
            resolver=self.resolve,
            input_object=GetAggregateInput(required=True, name='input'),
            description='Gets a collection of aggregated data of a given'
            ' entity type.',
        )

    @staticmethod
    @require_authentication
    def resolve(
        _root,
        info,
        input_object: GetAggregateInput,
    ):
        gmp = get_gmp(info)

        data_type_enum = (
            AggregateEntityType.get(input_object.data_type)
            if input_object.data_type is not None
            else None
        )

        if input_object.sort_criteria:
            sort_criteria = []
            for sort_input in input_object.sort_criteria:
                new_item = _sort_input_to_python_gvm(sort_input)
                sort_criteria.append(new_item)

        else:
            sort_criteria = None

        xml = gmp.get_aggregates(
            resource_type=data_type_enum,
            filter=input_object.filter_string,
            data_columns=input_object.data_columns,
            group_column=input_object.group_column,
            subgroup_column=input_object.subgroup_column,
            text_columns=input_object.text_columns,
            sort_criteria=sort_criteria,
            first_group=input_object.first_group,
            max_groups=input_object.max_groups,
            mode=input_object.mode,
        )
        return xml.find('aggregate')
