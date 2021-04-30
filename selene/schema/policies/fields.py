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

from selene.schema.utils import (
    get_text_from_element,
    get_int_from_element,
    get_boolean_from_element,
)

from selene.schema.entity import EntityObjectType

from selene.schema.nvts.fields import NvtPreference
from selene.schema.scan_configs.fields import ScannerPreference


class PolicyFamily(graphene.ObjectType):
    """Policy family of a policy."""

    name = graphene.String()
    nvt_count = graphene.Int()
    max_nvt_count = graphene.Int()
    growing = graphene.Boolean()

    @staticmethod
    def resolve_name(root, _info):
        return get_text_from_element(root, 'name')

    @staticmethod
    def resolve_nvt_count(root, _info):
        return get_int_from_element(root, 'nvt_count')

    @staticmethod
    def resolve_max_nvt_count(root, _info):
        return get_int_from_element(root, 'max_nvt_count')

    @staticmethod
    def resolve_growing(root, _info):
        return get_boolean_from_element(root, 'growing')


class PolicyAudit(graphene.ObjectType):
    """ "Audit which is using the policy."""

    audit_id = graphene.String(name='id')
    name = graphene.String()

    @staticmethod
    def resolve_audit_id(root, _info):
        return root.get('id')

    @staticmethod
    def resolve_name(root, _info):
        return get_text_from_element(root, 'name')


class PolicyNvtSelector(graphene.ObjectType):
    """Nvt selector of a policy"""

    name = graphene.String()
    include = graphene.Boolean()
    selector_type = graphene.Int(name='type')
    family_or_nvt = graphene.String()

    @staticmethod
    def resolve_name(root, _info):
        return get_text_from_element(root, 'name')

    @staticmethod
    def resolve_include(root, _info):
        return get_boolean_from_element(root, 'include')

    @staticmethod
    def resolve_selector_type(root, _info):
        return get_int_from_element(root, 'type')

    @staticmethod
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

    families = graphene.List(
        PolicyFamily, description='List of NVT Families in this Policy'
    )
    nvt_preferences = graphene.List(
        NvtPreference, description='List of NVT Preferences for this Policy'
    )
    scanner_preferences = graphene.List(
        ScannerPreference,
        description='List of Scanner Preferences for this Policy',
    )
    audits = graphene.List(
        PolicyAudit, description='List of Audits using this Policy'
    )
    nvt_selectors = graphene.List(PolicyNvtSelector)

    @staticmethod
    def resolve_policy_type(root, _info):
        return get_text_from_element(root, 'type')

    @staticmethod
    def resolve_trash(root, _info):
        return get_int_from_element(root, 'trash')

    @staticmethod
    def resolve_family_count(root, _info):
        return get_int_from_element(root, 'family_count')

    @staticmethod
    def resolve_family_growing(root, _info):
        family_count = root.find('family_count')
        return get_int_from_element(family_count, 'growing')

    @staticmethod
    def resolve_nvt_count(root, _info):
        return get_int_from_element(root, 'nvt_count')

    @staticmethod
    def resolve_nvt_growing(root, _info):
        nvt_count = root.find('nvt_count')
        return get_int_from_element(nvt_count, 'growing')

    @staticmethod
    def resolve_usage_type(root, _info):
        return get_text_from_element(root, 'usage_type')

    @staticmethod
    def resolve_max_nvt_count(root, _info):
        return get_int_from_element(root, 'max_nvt_count')

    @staticmethod
    def resolve_known_nvt_count(root, _info):
        return get_int_from_element(root, 'known_nvt_count')

    @staticmethod
    def resolve_predefined(root, _info):
        return get_boolean_from_element(root, 'predefined')

    @staticmethod
    def resolve_families(root, _info):
        families = root.find('families')
        if families is None:
            return None
        return families.findall('family')

    @staticmethod
    def resolve_nvt_preferences(root, _info):
        preferences = root.find('preferences')
        if preferences is not None:
            preferences = preferences.findall('preference')
            if len(preferences) > 0:
                # Works for now.
                return [
                    preference
                    for preference in preferences
                    if preference.find('nvt').get('oid') != ''
                ]
        return None

    @staticmethod
    def resolve_scanner_preferences(root, _info):
        preferences = root.find('preferences')
        if preferences is not None:
            preferences = preferences.findall('preference')
            if len(preferences) > 0:
                return [
                    preference
                    for preference in preferences
                    if preference.find('nvt').get('oid') == ''
                ]
        return None

    @staticmethod
    def resolve_audits(root, _info):
        audits = root.find('tasks')
        if audits is None:
            return None
        return audits.findall('task')

    @staticmethod
    def resolve_nvt_selectors(root, _info):
        selectors = root.find('nvt_selectors')
        if selectors is None:
            return None
        return selectors.findall('nvt_selector')
