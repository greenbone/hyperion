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

# pylint: disable=no-self-argument, no-member, not-an-iterable

import graphene

from selene.schema.entity import EntityObjectType
from selene.schema.severity import SeverityType
from selene.schema.parser import parse_datetime
from selene.schema.utils import (
    get_boolean_from_element,
    get_int_from_element,
    get_text_from_element,
    get_text,
)


class HistoryStatusChange(graphene.ObjectType):
    status = graphene.String()
    date = graphene.String()

    def resolve_status(root, _info):
        return get_text(root)

    def resolve_date(root, _info):
        return parse_datetime(root.get('date'))


class OvalDefinitionHistory(graphene.ObjectType):
    status = graphene.String()
    date = graphene.DateTime()
    contributor = graphene.String()
    organization = graphene.String()
    status_changes = graphene.List(HistoryStatusChange)

    def resolve_status(root, _info):
        return get_text_from_element(root, '{*}status')

    def resolve_date(root, _info):
        submitted = root.find('{*}dates/{*}submitted')
        if submitted is not None:
            return parse_datetime(submitted.get('date'))
        return None

    def resolve_contributor(root, _info):
        submitted = root.find('{*}dates/{*}submitted')
        if submitted is not None:
            return get_text_from_element(submitted, '{*}contributor')

    def resolve_organization(root, _info):
        contributor = root.find('{*}dates/{*}submitted/{*}contributor')
        if contributor is not None:
            return contributor.get('organization')
        return None

    def resolve_status_changes(root, _info):
        dates = root.find('{*}dates')
        if dates is not None:
            status_changes = dates.findall('{*}status_change')
            if len(status_changes) != 0:
                return status_changes
        return None


class OvalDefinitionCriteria(graphene.ObjectType):
    """ Recursive Criteria definition for OvalDefinitions ... """

    operator = graphene.String()
    comment = graphene.String()
    extend_definition = graphene.String()
    criterion = graphene.String()
    criteria = graphene.List(lambda: OvalDefinitionCriteria)

    def resolve_operator(root, _info):
        return root.get('operator')

    def resolve_comment(root, _info):
        return root.get('comment')

    def resolve_extend_definition(root, _info):
        extend_definition = root.find('{*}extend_definition')
        if extend_definition is not None:
            return extend_definition.get('comment')
        return None

    def resolve_criterion(root, _info):
        criterion = root.find('{*}criterion')
        if criterion is not None:
            return criterion.get('comment')
        return None

    def resolve_criteria(root, _info):
        criteria = root.findall('{*}criteria')
        if len(criteria) != 0:
            return criteria
        return None


class OvalDefinitionRefs(graphene.ObjectType):
    source = graphene.String(description='source type of this reference')
    ref_id = graphene.String(name='id', description='ID of this reference')
    url = graphene.String(description='URL of this reference')

    def resolve_source(root, _info):
        return root.get('source')

    def resolve_ref_id(root, _info):
        return root.get('ref_id')

    def resolve_url(root, _info):
        return root.get('ref_url')


class OvalDefinitionAffectedFamily(graphene.ObjectType):
    family = graphene.String()
    platforms = graphene.List(graphene.String)
    products = graphene.List(graphene.String)

    def resolve_family(root, _info):
        return root.get('family')

    def resolve_platforms(root, _info):
        platforms = root.findall('{*}platform')
        if len(platforms) != 0:
            return [platform.text for platform in platforms]
        return None

    def resolve_products(root, _info):
        products = root.findall('{*}product')
        if len(products) != 0:
            return [product.text for product in products]
        return None


class OvalDefinition(EntityObjectType):
    uuid = graphene.String(name='id')
    cve_refs = graphene.Int()
    deprecated = graphene.Boolean()
    description = graphene.String()
    file_path = graphene.String(name='file')
    info_class = graphene.String(name='class')
    affected_family = graphene.Field(OvalDefinitionAffectedFamily)
    references = graphene.List(OvalDefinitionRefs)
    history = graphene.Field(OvalDefinitionHistory)
    criteria = graphene.Field(OvalDefinitionCriteria)
    raw_data = graphene.String()
    score = graphene.Field(SeverityType)
    status = graphene.String()
    title = graphene.String()
    version = graphene.Int()

    def resolve_uuid(root, _info):
        return root.get('id')

    def resolve_cve_refs(root, _info):
        ovaldef = root.find('ovaldef')
        if ovaldef is not None:
            return get_int_from_element(ovaldef, 'cve_refs')
        return None

    def resolve_deprecated(root, _info):
        ovaldef = root.find('ovaldef')
        if ovaldef is not None:
            return get_boolean_from_element(ovaldef, 'deprecated')
        return None

    def resolve_description(root, _info):
        ovaldef = root.find('ovaldef')
        if ovaldef is not None:
            return get_text_from_element(ovaldef, 'description')
        return None

    def resolve_file_path(root, _info):
        ovaldef = root.find('ovaldef')
        if ovaldef is not None:
            return get_text_from_element(ovaldef, 'file')
        return None

    def resolve_info_class(root, _info):
        ovaldef = root.find('ovaldef')
        if ovaldef is not None:
            return get_text_from_element(ovaldef, 'class')
        return None

    def resolve_affected_family(root, _info):
        affected = root.find(
            'ovaldef/raw_data/{*}definition/{*}metadata/{*}affected'
        )
        if affected is not None:
            return affected
        return None

    def resolve_history(root, _info):
        history = root.find(
            'ovaldef/raw_data/{*}definition/{*}metadata/{*}oval_repository'
        )
        if history is not None:
            return history
        return None

    def resolve_criteria(root, _info):
        criteria = root.find('ovaldef/raw_data/{*}definition/{*}criteria')
        if criteria is not None:
            return criteria
        return None

    def resolve_references(root, _info):
        metadata = root.find('ovaldef/raw_data/{*}definition/{*}metadata')
        if metadata is not None:
            references = metadata.findall('{*}reference')
            if len(references) != 0:
                return references
        return None

    def resolve_score(root, _info):
        ovaldef = root.find('ovaldef')
        if ovaldef is not None:
            return get_text_from_element(ovaldef, 'score')
        return None

    def resolve_status(root, _info):
        ovaldef = root.find('ovaldef')
        if ovaldef is not None:
            return get_text_from_element(ovaldef, 'status')
        return None

    def resolve_title(root, _info):
        ovaldef = root.find('ovaldef')
        if ovaldef is not None:
            return get_text_from_element(ovaldef, 'title')
        return None

    def resolve_version(root, _info):
        ovaldef = root.find('ovaldef')
        if ovaldef is not None:
            return get_int_from_element(ovaldef, 'version')
        return None
