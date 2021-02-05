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

from graphql import GraphQLError
import graphene

from selene.schema.severity import SeverityType

from selene.schema.resolver import find_resolver


from selene.schema.utils import (
    get_boolean_from_element,
    get_datetime_from_element,
    get_text_from_element,
)

from selene.schema.entity import EntityObjectType
from selene.schema.nvts.fields import ScanConfigNVT as NVT
from selene.schema.results.queries import Result
from selene.schema.tasks.fields import Task


class Override(EntityObjectType):
    class Meta:
        default_resolver = find_resolver

    end_time = graphene.DateTime()

    active = graphene.Boolean()
    in_use = graphene.Boolean()
    orphan = graphene.Boolean()
    writable = graphene.Boolean()

    hosts = graphene.List(graphene.String)
    name = graphene.String()
    owner = graphene.String()
    text = graphene.String()

    severity = SeverityType()
    new_severity = SeverityType()

    nvt = graphene.Field(NVT)
    task = graphene.Field(Task)
    result = graphene.Field(Result)

    def resolve_name(root, _info):
        raise GraphQLError(
            f'Cannot query field "{_info.field_name}"'
            ' on type "{_info.parent_type}".'
        )

    def resolve_end_time(root, _info):
        return get_datetime_from_element(root, 'end_time')

    def resolve_active(root, _info):
        return get_boolean_from_element(root, 'active')

    def resolve_orphan(root, _info):
        return get_boolean_from_element(root, 'orphan')

    def resolve_text(root, _info):
        return get_text_from_element(root, 'text')

    def resolve_hosts(root, _info):
        hosts = get_text_from_element(root, 'hosts')
        if hosts is None:
            return []
        return [host.strip() for host in hosts.split(',')]

    def resolve_severity(root, _info):
        return get_text_from_element(root, 'severity')

    def resolve_new_severity(root, _info):
        return get_text_from_element(root, 'new_severity')
