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

from selene.schema.base import BaseObjectType
from selene.schema.utils import (
    get_boolean_from_element,
    get_datetime_from_element,
    get_int_from_element,
    get_text_from_element,
)
from selene.schema.parser import parse_uuid
from selene.schema.severity import SeverityType
from selene.schema.resolver import text_resolver
from selene.schema.entity import EntityObjectType


class HostResultCount(graphene.ObjectType):
    current = graphene.Int(description="Current results for the host")
    high = graphene.Int(
        description="Number of results with high severity for the host"
    )
    medium = graphene.Int(
        description="Number of results with medium severity for the host"
    )
    low = graphene.Int(
        description="Number of results with low severity for the host"
    )
    log = graphene.Int(description="Number of log messages for the host")
    false_positive = graphene.Int(
        description="Number of false positive results for the host"
    )

    def resolve_current(parent, _info):
        return get_int_from_element(parent, 'page')

    def resolve_high(parent, _info):
        return get_int_from_element(parent.find('hole'), 'page')

    def resolve_medium(parent, _info):
        return get_int_from_element(parent.find('warning'), 'page')

    def resolve_low(parent, _info):
        return get_int_from_element(parent.find('info'), 'page')

    def resolve_log(parent, _info):
        return get_int_from_element(parent.find('log'), 'page')

    def resolve_false_positive(parent, _info):
        return get_int_from_element(parent.find('false_positive'), 'page')


class HostResults(graphene.ObjectType):
    """Result object type. Is part of the Host object.
    Includes the result counts.
    """

    counts = graphene.Field(HostResultCount)

    def resolve_counts(root, _info):
        return root


class HostPortCounts(graphene.ObjectType):
    current = graphene.Int(description="Current ports for the host")

    def resolve_current(parent, _info):
        return get_int_from_element(parent, 'page')


class HostPorts(graphene.ObjectType):
    """Port object type. Is part of the Host object.
    Includes the port counts.
    """

    counts = graphene.Field(HostPortCounts)

    def resolve_counts(root, _info):
        return root


class RouteHost(graphene.ObjectType):
    host_id = graphene.String(name='id')
    ip = graphene.String()
    distance = graphene.Int()
    same_source = graphene.Boolean()

    def resolve_host_id(root, _info):
        return parse_uuid(root.get('id'))

    def resolve_ip(root, _info):
        return get_text_from_element(root, 'ip')

    def resolve_distance(root, _info):
        return get_int_from_element(root, 'distance')

    def resolve_same_source(root, _info):
        return get_boolean_from_element(root, 'same_source')


class Route(graphene.ObjectType):
    hosts = graphene.List(RouteHost)

    def resolve_hosts(root, _info):
        hosts = root.findall('host')
        if hosts is not None:
            return hosts
        return None


class DetailSource(BaseObjectType):
    class Meta:
        default_resolver = text_resolver

    type = graphene.String()
    description = graphene.String()


class HostDetail(graphene.ObjectType):
    class Meta:
        default_resolver = text_resolver

    name = graphene.String()
    value = graphene.String()
    source = graphene.Field(DetailSource)
    extra = graphene.String()

    def resolve_source(root, _info):
        return root.find('source')


class HostIdentifier(BaseObjectType):

    value = graphene.String()
    creation_time = graphene.DateTime()
    modification_time = graphene.DateTime()
    source_id = graphene.String()
    source_name = graphene.String()
    source_type = graphene.String()
    source_data = graphene.String()
    source_deleted = graphene.Boolean()
    os_id = graphene.String()
    os_title = graphene.String()

    def resolve_value(root, _info):
        return get_text_from_element(root, 'value')

    def resolve_creation_time(root, _info):
        return get_datetime_from_element(root, 'creation_time')

    def resolve_modification_time(root, _info):
        return get_datetime_from_element(root, 'creation_time')

    def resolve_source_id(root, _info):
        source = root.find('source')
        if source is not None:
            return parse_uuid(source.get('id'))
        return None

    def resolve_source_name(root, _info):
        source = root.find('source')
        if source is not None:
            return get_text_from_element(source, 'name')
        return None

    def resolve_source_type(root, _info):
        source = root.find('source')
        if source is not None:
            return get_text_from_element(source, 'type')
        return None

    def resolve_source_data(root, _info):
        source = root.find('source')
        if source is not None:
            return get_text_from_element(source, 'data')
        return None

    def resolve_source_deleted(root, _info):
        source = root.find('source')
        if source is not None:
            return get_boolean_from_element(source, 'deleted')
        return None

    def resolve_os_id(root, _info):
        os = root.find('os')
        if os is not None:
            return parse_uuid(os.get('id'))
        return None

    def resolve_os_title(root, _info):
        os = root.find('os')
        if os is not None:
            return get_text_from_element(os, 'title')
        return None


class Host(EntityObjectType):
    """Host object type. Is part of the Result object."""

    identifiers = graphene.List(HostIdentifier)
    severity = graphene.Field(SeverityType)
    details = graphene.List(HostDetail)
    routes = graphene.List(Route)

    def resolve_identifiers(root, _info):
        identifiers = root.find('identifiers')
        if identifiers is not None:
            return identifiers.findall('identifier')
        return None

    def resolve_severity(root, _info):
        severity = root.find('host').find('severity')
        return get_text_from_element(severity, 'value')

    def resolve_routes(root, _info):
        routes = root.find('host').find('routes')
        if routes is not None:
            return routes.findall('route')
        return None

    def resolve_details(root, _info):
        details = root.find('host').findall('detail')
        if details is not None:
            return details
        return None


class ReportHost(graphene.ObjectType):
    """Host object type. Is part of the Report object."""

    ip = graphene.String()
    asset_id = graphene.UUID(name="id")
    start = graphene.DateTime(description="Start time of the scan for the host")
    end = graphene.DateTime(description="End Time of the scan for the host")
    ports = graphene.Field(HostPorts)
    results = graphene.Field(HostResults)

    details = graphene.List(HostDetail)

    def resolve_ip(root, _info):
        return get_text_from_element(root, 'ip')

    def resolve_asset_id(root, _info):
        asset = root.find('asset')
        return asset.get('asset_id')

    def resolve_start(root, _info):
        return get_datetime_from_element(root, 'start')

    def resolve_end(root, _info):
        return get_datetime_from_element(root, 'end')

    def resolve_details(root, _info):
        return root.findall('detail')

    def resolve_ports(root, _info):
        return root.find('port_count')

    def resolve_results(root, _info):
        return root.find('result_count')
