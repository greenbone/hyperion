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

# pylint: disable=no-self-argument, no-member, not-an-iterable

from xml import etree

import graphene

from selene.schema.entity import EntityObjectType
from selene.schema.severity import SeverityType
from selene.schema.utils import (
    get_boolean_from_element,
    get_int_from_element,
    get_text_from_element,
)


class OvalDefinition(EntityObjectType):
    uuid = graphene.String(name='id')
    cve_refs = graphene.Int()
    deprecated = graphene.Boolean()
    description = graphene.String()
    file_path = graphene.String(name='file')
    info_class = graphene.String(name='class')
    raw_data = graphene.String()
    score = graphene.Field(SeverityType)
    status = graphene.String()
    title = graphene.String()
    version = graphene.Int()

    def resolve_uuid(root, _info):
        return root.get('id')

    def resolve_cve_refs(root, _info):
        ovaldef = root.find('ovaldef')
        if ovaldef:
            return get_int_from_element(ovaldef, 'cve_refs')
        return None

    def resolve_deprecated(root, _info):
        ovaldef = root.find('ovaldef')
        if ovaldef:
            return get_boolean_from_element(ovaldef, 'deprecated')
        return None

    def resolve_description(root, _info):
        ovaldef = root.find('ovaldef')
        if ovaldef:
            return get_text_from_element(ovaldef, 'description')
        return None

    def resolve_file_path(root, _info):
        ovaldef = root.find('ovaldef')
        if ovaldef:
            return get_text_from_element(ovaldef, 'file')
        return None

    def resolve_info_class(root, _info):
        ovaldef = root.find('ovaldef')
        if ovaldef:
            return get_text_from_element(ovaldef, 'class')
        return None

    def resolve_raw_data(root, _info):
        # dump everything in raw_data into a string. This needs to be parsed
        # properly in GSA. It will include (among others) the information about
        # criteria and affected assets
        criteria = root.find('ovaldef').find('raw_data').find('*')
        if criteria:
            return etree.ElementTree.tostring(criteria, encoding='unicode')
        return None

    def resolve_score(root, _info):
        ovaldef = root.find('ovaldef')
        if ovaldef:
            return get_text_from_element(ovaldef, 'score')
        return None

    def resolve_status(root, _info):
        ovaldef = root.find('ovaldef')
        if ovaldef:
            return get_text_from_element(ovaldef, 'status')
        return None

    def resolve_title(root, _info):
        ovaldef = root.find('ovaldef')
        if ovaldef:
            return get_text_from_element(ovaldef, 'title')
        return None

    def resolve_version(root, _info):
        ovaldef = root.find('ovaldef')
        if ovaldef:
            return get_int_from_element(ovaldef, 'version')
        return None
