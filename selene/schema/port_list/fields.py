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

import graphene
from gvm.protocols.latest import (
    PortRangeType as GvmPortRangeType,
)

from selene.schema.base import BaseObjectType
from selene.schema.entity import EntityObjectType

from selene.schema.parser import parse_uuid

from selene.schema.resolver import find_resolver

from selene.schema.utils import (
    get_text_from_element,
    get_int_from_element,
)


class PortRangeType(graphene.Enum):
    class Meta:
        enum = GvmPortRangeType


class PortRange(graphene.ObjectType):
    uuid = graphene.UUID(name='id')
    start = graphene.Int()
    end = graphene.Int()
    protocol_type = graphene.String()

    def resolve_uuid(root, _info):
        return parse_uuid(root.get('id'))

    def resolve_start(root, _info):
        return get_int_from_element(root, 'start')

    def resolve_end(root, _info):
        return get_int_from_element(root, 'end')

    def resolve_protocol_type(root, _info):
        return get_text_from_element(root, 'type')


class PortCount(graphene.ObjectType):
    count_all = graphene.Int(name='all')  # 'all' is a built-in python method
    tcp = graphene.Int()
    udp = graphene.Int()

    def resolve_count_all(root, _info):
        return get_int_from_element(root, 'all')

    def resolve_tcp(root, _info):
        return get_int_from_element(root, 'tcp')

    def resolve_udp(root, _info):
        return get_int_from_element(root, 'udp')


class PortListTarget(BaseObjectType):
    pass


class PortList(EntityObjectType):
    class Meta:
        default_resolver = find_resolver

    port_ranges = graphene.List(PortRange)
    port_count = graphene.Field(PortCount)
    targets = graphene.List(PortListTarget)

    def resolve_port_ranges(root, _info):
        port_ranges = root.find('port_ranges')
        if len(port_ranges) == 0:
            return None
        return port_ranges.findall('port_range')

    def resolve_targets(root, _info):
        targets = root.find('targets')
        if len(targets) == 0:
            return None
        return targets.findall('target')
