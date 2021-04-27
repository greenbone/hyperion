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

# pylint: disable=no-self-argument, no-member

import graphene

from selene.schema.base import BaseObjectType
from selene.schema.entity import EntityObjectType
from selene.schema.utils import get_text, get_text_from_element
from selene.schema.resolver import text_resolver, boolean_resolver


class Keyword(graphene.ObjectType):
    class Meta:
        default_resolver = text_resolver

    column = graphene.String()
    relation = graphene.String()
    value = graphene.String()


class FilterAlerts(BaseObjectType):
    pass


class FilterDelta(graphene.ObjectType):
    class Meta:
        default_resolver = boolean_resolver

    states = graphene.String()
    changed = graphene.Boolean()
    gone = graphene.Boolean()
    new = graphene.Boolean()
    same = graphene.Boolean()

    def resolve_states(root, _info):
        return get_text(root)


class Filter(EntityObjectType):
    entity_type = graphene.String(name="type")
    term = graphene.String()
    alerts = graphene.List(FilterAlerts)

    def resolve_entity_type(root, _info):
        return get_text_from_element(root, 'type')

    def resolve_term(root, _info):
        return get_text_from_element(root, 'term')

    def resolve_alerts(root, _info):
        alerts = root.find('alerts')
        if alerts is not None:
            return alerts.findall('alert')
        return None
