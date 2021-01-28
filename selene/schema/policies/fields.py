# -*- coding: utf-8 -*-
# Copyright (C) 2020 Greenbone Networks GmbH
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

from selene.schema.utils import (
    get_text_from_element,
    get_int_from_element,
    get_boolean_from_element,
)

from selene.schema.entity import EntityObjectType

from selene.schema.nvts.fields import NvtPreference


class PolicyFamily(graphene.ObjectType):
    """Policy family of a policy."""

    name = graphene.String()
    nvt_count = graphene.Int()
    max_nvt_count = graphene.Int()
    growing = graphene.Boolean()

    def resolve_name(root, _info):
        return get_text_from_element(root, 'name')

    def resolve_nvt_count(root, _info):
        return get_int_from_element(root, 'nvt_count')

    def resolve_max_nvt_count(root, _info):
        return get_int_from_element(root, 'max_nvt_count')

    def resolve_growing(root, _info):
        return get_boolean_from_element(root, 'growing')


class PolicyTask(graphene.ObjectType):
    """"Task which is using the policy."""

    task_id = graphene.String(name='id')
    name = graphene.String()

    def resolve_task_id(root, _info):
        return root.get('id')

    def resolve_name(root, _info):
        return get_text_from_element(root, 'name')


class PolicyNvtSelector(graphene.ObjectType):
    """Nvt selector of a policy"""

    name = graphene.String()
    include = graphene.Boolean()
    selector_type = graphene.Int(name='type')
    family_or_nvt = graphene.String()

    def resolve_name(root, _info):
        return get_text_from_element(root, 'name')

    def resolve_include(root, _info):
        return get_boolean_from_element(root, 'include')

    def resolve_selector_type(root, _info):
        return get_int_from_element(root, 'type')

    def resolve_family_or_nvt(root, _info):
        return get_text_from_element(root, 'family_or_nvt')


class Policy(EntityObjectType):
    """Policy object type. Can be used in GetPolicy and GetPolicies
    queries."""

    policy_type = graphene.Int(name='type')
    trash = graphene.Int()
    family_count = graphene.Int()
    family_growing = graphene.Boolean()
    nvt_count = graphene.Int()
    nvt_growing = graphene.Boolean()
    usage_type = graphene.String()
    max_nvt_count = graphene.Int()
    known_nvt_count = graphene.Int()
    predefined = graphene.Boolean()

    families = graphene.List(PolicyFamily)
    preferences = graphene.List(NvtPreference)
    tasks = graphene.List(PolicyTask)
    nvt_selectors = graphene.List(PolicyNvtSelector)

    def resolve_policy_type(root, _info):
        return get_text_from_element(root, 'type')

    def resolve_trash(root, _info):
        return get_int_from_element(root, 'trash')

    def resolve_family_count(root, _info):
        return get_int_from_element(root, 'family_count')

    def resolve_family_growing(root, _info):
        family_count = root.find('family_count')
        return get_int_from_element(family_count, 'growing')

    def resolve_nvt_count(root, _info):
        return get_int_from_element(root, 'nvt_count')

    def resolve_nvt_growing(root, _info):
        nvt_count = root.find('nvt_count')
        return get_int_from_element(nvt_count, 'growing')

    def resolve_usage_type(root, _info):
        return get_text_from_element(root, 'usage_type')

    def resolve_max_nvt_count(root, _info):
        return get_int_from_element(root, 'max_nvt_count')

    def resolve_known_nvt_count(root, _info):
        return get_int_from_element(root, 'known_nvt_count')

    def resolve_predefined(root, _info):
        return get_boolean_from_element(root, 'predefined')

    def resolve_families(root, _info):
        families = root.find('families')
        if families is None:
            return None
        return families.findall('family')

    def resolve_preferences(root, _info):
        preferences = root.find('preferences')
        if preferences is None:
            return None
        return preferences.findall('preference')

    def resolve_tasks(root, _info):
        tasks = root.find('tasks')
        if tasks is None:
            return None
        return tasks.findall('task')

    def resolve_nvt_selectors(root, _info):
        selectors = root.find('nvt_selectors')
        if selectors is None:
            return None
        return selectors.findall('nvt_selector')
