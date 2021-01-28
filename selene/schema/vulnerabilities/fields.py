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

# pylint: disable=no-self-argument, no-member

import graphene

from selene.schema.resolver import text_resolver

from selene.schema.severity import SeverityType

from selene.schema.utils import (
    get_datetime_from_element,
    get_int_from_element,
    get_text_from_element,
)


class VulnerabilityResults(graphene.ObjectType):
    count = graphene.Int()
    oldest = graphene.DateTime()
    newest = graphene.DateTime()

    def resolve_count(root, _info):
        return get_int_from_element(root, 'count')

    def resolve_oldest(root, _info):
        return get_datetime_from_element(root, 'oldest')

    def resolve_newest(root, _info):
        return get_datetime_from_element(root, 'newest')


class Vulnerability(graphene.ObjectType):
    class Meta:
        default_resolver = text_resolver

    vuln_id = graphene.String(name="id")
    name = graphene.String()
    vuln_type = graphene.String(name="type")
    creation_time = graphene.DateTime()
    modification_time = graphene.DateTime()
    severity = SeverityType()  # change this to score if implememnted in GVMD
    qod = graphene.Int()
    results = graphene.Field(VulnerabilityResults)
    host_count = graphene.Int()

    def resolve_vuln_id(root, _info):
        return root.get('id')

    def resolve_vuln_type(root, _info):
        return get_text_from_element(root, 'type')

    def resolve_creation_time(root, _info):
        return get_datetime_from_element(root, 'creation_time')

    def resolve_modification_time(root, _info):
        return get_datetime_from_element(root, 'modification_time')

    def resolve_host_count(root, _info):
        hosts = root.find('hosts')
        return get_int_from_element(hosts, 'count')

    def resolve_results(root, _info):
        return root.find('results')

    def resolve_qod(root, _info):
        return get_int_from_element(root, 'qod')
