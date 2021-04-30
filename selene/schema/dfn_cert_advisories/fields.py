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

from selene.schema.entity import EntityObjectType
from selene.schema.severity import SeverityType
from selene.schema.utils import (
    get_datetime_from_element,
    get_int_from_element,
    get_text_from_element,
)

# the raw-data in the xml for DFN-CERTS contain namespaces
# these make it kind of difficult to resolve the fields
# especially since python 3.7 doesn't support the wildcard
# to ignore namespaces in lxml (element.find('{*}tag'))
# so with 3.7 support this is a workaround only ...


class DFNCertAdvisoryAuthor(graphene.ObjectType):
    name = graphene.String()
    uri = graphene.String()

    @staticmethod
    def resolve_name(root, _info):
        for elem in root:
            if 'name' in elem.tag:
                return elem.text

    @staticmethod
    def resolve_uri(root, _info):
        for elem in root:
            if 'uri' in elem.tag:
                return elem.text


class DFNCertAdvisory(EntityObjectType):
    uuid = graphene.String(name='id')
    update_time = graphene.DateTime()
    title = graphene.String()
    summary = graphene.String()
    max_cvss = graphene.Field(SeverityType)
    score = graphene.Field(SeverityType)
    author = graphene.Field(DFNCertAdvisoryAuthor)
    cve_refs = graphene.Int()
    cves = graphene.List(graphene.String)
    link = graphene.String()

    @staticmethod
    def resolve_uuid(root, _info):
        return root.get('id')

    @staticmethod
    def resolve_update_time(root, _info):
        return get_datetime_from_element(root, 'update_time')

    @staticmethod
    def resolve_title(root, _info):
        dfn_cert_adv = root.find('dfn_cert_adv')
        if dfn_cert_adv is not None:
            return get_text_from_element(dfn_cert_adv, 'title')
        return None

    @staticmethod
    def resolve_summary(root, _info):
        dfn_cert_adv = root.find('dfn_cert_adv')
        if dfn_cert_adv is not None:
            return get_text_from_element(dfn_cert_adv, 'summary').strip()
        return None

    @staticmethod
    def resolve_max_cvss(root, _info):
        dfn_cert_adv = root.find('dfn_cert_adv')
        if dfn_cert_adv is not None:
            return get_text_from_element(dfn_cert_adv, 'max_cvss')
        return None

    @staticmethod
    def resolve_score(root, _info):
        dfn_cert_adv = root.find('dfn_cert_adv')
        if dfn_cert_adv is not None:
            return get_text_from_element(dfn_cert_adv, 'score')
        return None

    @staticmethod
    def resolve_cve_refs(root, _info):
        dfn_cert_adv = root.find('dfn_cert_adv')
        if dfn_cert_adv is not None:
            return get_int_from_element(dfn_cert_adv, 'cve_refs')
        return None

    @staticmethod
    def resolve_cves(root, _info):
        dfn_cert_adv = root.find('dfn_cert_adv/raw_data/{*}entry')
        if dfn_cert_adv is not None:
            cves = dfn_cert_adv.findall('{*}cve')
            if cves is not None:
                return [cve.text for cve in cves]
        return None

    @staticmethod
    def resolve_author(root, _info):
        author = root.find('dfn_cert_adv/raw_data/{*}entry/{*}author')
        if author is not None:
            return author
        return None

    @staticmethod
    def resolve_link(root, _info):
        link = root.find('dfn_cert_adv/raw_data/{*}entry/{*}link')
        if link is not None:
            return link.get('href')
        return None
