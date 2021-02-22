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

from selene.schema.entity import EntityObjectType
from selene.schema.severity import SeverityType
from selene.schema.utils import (
    get_datetime_from_element,
    get_int_from_element,
    get_text_from_element,
)


class CveRef(graphene.ObjectType):
    uuid = graphene.String(name='id', description="ID of referenced CVE")
    severity = graphene.Field(
        SeverityType, description="Severity of referenced CVE"
    )

    def resolve_uuid(root, _info):
        return root.get('id')

    def resolve_severity(root, _info):
        return get_text_from_element(root, '{*}cvss/{*}base_metrics/{*}score')


class CPE(EntityObjectType):
    uuid = graphene.String(name='id', description="URI of this CPE")
    update_time = graphene.DateTime(description="Last updated timestamp")
    title = graphene.String(description="Short description/name of this CPE")
    nvd_id = graphene.String(
        description=(
            "Corresponding ID in the national" " vulnerability database (NVD)"
        )
    )
    score = graphene.Int(description="Maximum score from referenced CVEs")
    cve_ref_count = graphene.Int(description="Number of CVE references")
    cve_refs = graphene.List(CveRef, description="CVE references list")
    status = graphene.String(description="Latest CPE status")

    def resolve_uuid(root, _info):
        return root.get('id')

    def resolve_update_time(root, _info):
        return get_datetime_from_element(root, 'update_time')

    def resolve_title(root, _info):
        cpe = root.find('cpe')
        if cpe is not None:
            return get_text_from_element(cpe, 'title')
        return None

    def resolve_nvd_id(root, _info):
        cpe = root.find('cpe')
        if cpe is not None:
            return get_text_from_element(cpe, 'nvd_id')
        return None

    def resolve_score(root, _info):
        cpe = root.find('cpe')
        if cpe is not None:
            return get_text_from_element(cpe, 'score')
        return None

    def resolve_cve_ref_count(root, _info):
        cpe = root.find('cpe')
        if cpe is not None:
            return get_int_from_element(cpe, 'cve_refs')
        return None

    def resolve_cve_refs(root, _info):
        cves = root.find('cpe/cves')
        if cves is not None:
            cves = cves.findall('cve/{*}entry')
            if len(cves) > 0:
                return cves
        return None

    def resolve_status(root, _info):
        cpe = root.find('cpe')
        if cpe is not None:
            return get_text_from_element(cpe, 'status')
        return None
