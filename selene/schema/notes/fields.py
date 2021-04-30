# -*- coding: utf-8 -*-
# Copyright (C) 2019-2021 Greenbone Networks GmbH
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

from graphql import GraphQLError

from selene.schema.severity import SeverityType

from selene.schema.resolver import find_resolver

from selene.schema.utils import (
    csv_to_list,
    get_boolean_from_element,
    get_datetime_from_element,
    get_text_from_element,
)
from selene.schema.base import BaseObjectType
from selene.schema.entity import EntityObjectType
from selene.schema.nvts.fields import ScanConfigNVT as NVT
from selene.schema.tasks.fields import Task


class NoteResult(BaseObjectType):
    pass


class Note(EntityObjectType):
    class Meta:
        default_resolver = find_resolver

    end_time = graphene.DateTime()
    active = graphene.Boolean()
    orphan = graphene.Boolean()

    text = graphene.String()
    hosts = graphene.List(graphene.String)
    port = graphene.String()
    severity = SeverityType()
    threat = graphene.String()

    nvt = graphene.Field(NVT)
    task = graphene.Field(Task)
    result = graphene.Field(NoteResult)

    @staticmethod
    def resolve_name(root, _info):
        raise GraphQLError(
            f'Cannot query field "{_info.field_name}"'
            f' on type "{_info.parent_type}".'
        )

    @staticmethod
    def resolve_end_time(root, _info):
        return get_datetime_from_element(root, 'end_time')

    @staticmethod
    def resolve_active(root, _info):
        return get_boolean_from_element(root, 'active')

    @staticmethod
    def resolve_orphan(root, _info):
        return get_boolean_from_element(root, 'orphan')

    @staticmethod
    def resolve_text(root, _info):
        return get_text_from_element(root, 'text')

    @staticmethod
    def resolve_hosts(root, _info):
        hosts = get_text_from_element(root, 'hosts')
        return csv_to_list(hosts)

    @staticmethod
    def resolve_port(root, _info):
        return get_text_from_element(root, 'port')

    @staticmethod
    def resolve_severity(root, _info):
        return get_text_from_element(root, 'severity')

    @staticmethod
    def resolve_threat(root, _info):
        return get_text_from_element(root, 'threat')
