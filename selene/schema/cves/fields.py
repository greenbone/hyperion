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

from selene.schema.entity import EntityObjectType
from selene.schema.severity import SeverityType
from selene.schema.utils import (
    get_datetime_from_element,
    get_text_from_element,
)


class CVSSv2Vector(graphene.ObjectType):
    access_vector = graphene.String()
    access_complexity = graphene.String()
    authentication = graphene.String()
    confidentiality = graphene.String()
    integrity = graphene.String()
    availability = graphene.String()
    base_score = graphene.Field(SeverityType)

    def resolve_access_vector(root, _info):
        return get_text_from_element(root, 'vector')

    def resolve_access_complexity(root, _info):
        return get_text_from_element(root, 'complexity')

    def resolve_authentication(root, _info):
        return get_text_from_element(root, 'authentication')

    def resolve_confidentiality(root, _info):
        return get_text_from_element(root, 'confidentiality_impact')

    def resolve_integrity(root, _info):
        return get_text_from_element(root, 'integrity_impact')

    def resolve_availability(root, _info):
        return get_text_from_element(root, 'availability_impact')

    def resolve_base_score(root, _info):
        return get_text_from_element(root, 'cvss')


class CVSSv3Vector(graphene.ObjectType):
    attack_vector = graphene.String()
    attack_complexity = graphene.String()
    privileges_required = graphene.String()
    user_interaction = graphene.String()
    scope = graphene.String()
    confidentiality = graphene.String()
    integrity = graphene.String()
    availability = graphene.String()
    score = graphene.Field(SeverityType)

    def resolve_attack_vector(root, _info):
        return get_text_from_element(root, 'vector')

    def resolve_attack_complexity(root, _info):
        return get_text_from_element(root, 'complexity')

    def resolve_privileges_required(root, _info):
        return get_text_from_element(root, 'privileges_required')

    def resolve_user_interaction(root, _info):
        return get_text_from_element(root, 'user_interaction')

    def resolve_scope(root, _info):
        return get_text_from_element(root, 'scope')

    def resolve_confidentiality(root, _info):
        return get_text_from_element(root, 'confidentiality_impact')

    def resolve_access_integrity(root, _info):
        return get_text_from_element(root, 'integrity_impact')

    def resolve_access_availability(root, _info):
        return get_text_from_element(root, 'availability_impact')

    def resolve_base_score(root, _info):
        return get_text_from_element(root, 'cvss')


class CVE(EntityObjectType):
    uuid = graphene.String(name='id')
    update_time = graphene.DateTime()
    cvss_v2_vector = graphene.Field(CVSSv2Vector)
    cvss_v3_vector = graphene.Field(CVSSv3Vector)
    description = graphene.String()
    products = graphene.List(graphene.String)

    def resolve_uuid(root, _info):
        return root.get('id')

    def resolve_update_time(root, _info):
        return get_datetime_from_element(root, 'update_time')

    def resolve_cvss_v2_vector(root, _info):
        return root.find('cve')

    # this is for the future ...
    def resolve_cvss_v3_vector(root, _info):
        return None

    def resolve_description(root, _info):
        return get_text_from_element(root.find('cve'), 'description')

    def resolve_products(root, _info):
        cve = root.find('cve')
        if cve:
            return get_text_from_element(cve, 'products').rstrip().split(' ')
        return None
