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

from selene.schema.utils import (
    get_text,
    get_text_from_element,
    get_int_from_element,
    get_boolean_from_element,
)

from selene.schema.entity import EntityObjectType

from selene.schema.nvts.fields import NvtPreference


class ScannerPreference(graphene.ObjectType):
    """Scanner preference."""

    hr_name = graphene.String(
        description='Human readable name of the preference'
    )
    name = graphene.String(description='Name of the preference')
    preference_id = graphene.Int(
        name='id', description='ID of this preference [1..]'
    )
    preference_type = graphene.String(
        name='type',
        description=(
            'The value type of the preference. '
            'One of ratio, checkbox, entry, password'
        ),
    )
    value = graphene.String(description='Current value for this preference')
    default = graphene.String(description='default value for this preference')
    alternative_values = graphene.List(
        graphene.String,
        description=(
            'alternative value(s) for this preference '
            '(preference type: ratio)'
        ),
    )

    def resolve_hr_name(root, _info):
        return get_text_from_element(root, 'hr_name')

    def resolve_name(root, _info):
        return get_text_from_element(root, 'name')

    def resolve_preference_type(root, _info):
        return get_text_from_element(root, 'type')

    def resolve_value(root, _info):
        return get_text_from_element(root, 'value')

    def resolve_default(root, _info):
        return get_text_from_element(root, 'default')

    def resolve_preference_id(root, _info):
        return get_int_from_element(root, 'id')

    def resolve_alternative_values(root, _info):
        alts = root.findall('alt')
        if alts is not None and len(alts) > 0:
            return [get_text(alt) for alt in alts]
        return None


class ScanConfigFamily(graphene.ObjectType):
    """Scan config family of a scan config."""

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


class ScanConfigTask(graphene.ObjectType):
    """ "Task which is using the scan config."""

    task_id = graphene.String(name='id')
    name = graphene.String()

    def resolve_task_id(root, _info):
        return root.get('id')

    def resolve_name(root, _info):
        return get_text_from_element(root, 'name')


class ScanConfigNvtSelector(graphene.ObjectType):
    """Nvt selector of a scan config"""

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


class ScanConfig(EntityObjectType):
    """Scan config object type. Can be used in GetScanConfig and GetScanConfigs
    queries."""

    scan_config_type = graphene.Int(name='type')
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
        ScanConfigFamily, description='List of NVT Families in this Scan Config'
    )
    nvt_preferences = graphene.List(
        NvtPreference,
        description='List of NVT Preferences for this Scan Config',
    )
    scanner_preferences = graphene.List(
        ScannerPreference,
        description='List of Scanner Preferences for this Scan Config',
    )
    tasks = graphene.List(
        ScanConfigTask, description='List of Tasks using this Scan Config'
    )
    nvt_selectors = graphene.List(ScanConfigNvtSelector)

    def resolve_scan_config_type(root, _info):
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
