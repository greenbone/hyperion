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
    get_int_from_element,
    get_text_from_element,
)
from selene.schema.parser import parse_uuid
from selene.schema.severity import SeverityType
from selene.schema.entity import EntityObjectType


class OperatingSystemHost(BaseObjectType):
    severity = graphene.Field(SeverityType)

    def resolve_severity(root, _info):
        severity = root.find('severity')
        return get_text_from_element(severity, 'value')


class OperatingSystemInformation(graphene.ObjectType):

    latest_severity = graphene.Field(SeverityType)
    highest_severity = graphene.Field(SeverityType)
    average_severity = graphene.Field(SeverityType)
    title = graphene.String()
    installs = graphene.Int()
    host_count = graphene.Int()
    hosts = graphene.List(OperatingSystemHost)

    def resolve_latest_severity(root, _info):
        severity = root.find('latest_severity')
        return get_text_from_element(severity, 'value')

    def resolve_highest_severity(root, _info):
        severity = root.find('highest_severity')
        return get_text_from_element(severity, 'value')

    def resolve_average_severity(root, _info):
        severity = root.find('average_severity')
        return get_text_from_element(severity, 'value')

    def resolve_title(root, _info):
        source = root.find('source')
        if source is not None:
            return parse_uuid(source.get('id'))
        return None

    def resolve_installs(root, _info):
        return get_int_from_element(root, 'installs')

    def resolve_host_count(root, _info):
        return get_int_from_element(root, 'hosts')

    def resolve_hosts(root, _info):
        hosts = root.find('hosts').findall('asset')
        if hosts is not None:
            return hosts
        return None


class OperatingSystem(EntityObjectType):
    """OperatingSystem object type. Is part of the Result object."""

    operating_system_information = graphene.Field(OperatingSystemInformation)

    def resolve_operating_system_information(root, _info):
        return root.find('os')
