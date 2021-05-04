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

import graphene

from graphql import ResolveInfo

from gvm.protocols.next import InfoType as GvmInfoType

from selene.schema.base import SingleObjectQuery

from selene.schema.dfn_cert_advisories.fields import DFNCertAdvisory

from selene.schema.parser import FilterString

from selene.schema.relay import (
    EntityConnectionField,
    Entities,
    get_filter_string_for_pagination,
)

from selene.schema.utils import get_gmp, require_authentication, XmlElement


class GetDFNCertAdvisory(SingleObjectQuery):
    """Gets a single DFNCertAdvisory information.

    Example:

        query {
            dfnCertAdvisory(id: "DFN-CERT-2008-0644") {
                id
                name
                updateTime
                title
                nvdId
                maxCvss
                cveRefs
                status
            }
        }

    Response:

        {
            "data": {
                "dfnCertAdvisory": {
                    "id": "DFN-CERT-2008-0644",
                    "name": "DFN-CERT-2008-0644"
                    "title": "Vendor product etc"
                    "nvdId": "123456"
                    "maxCvss": 5.6
                    "cveRefs": 1
                    "status": "FINAL"
                }
            }
        }

    """

    object_type = DFNCertAdvisory
    kwargs = {
        'dfn_cert_advisory_id': graphene.String(
            required=True, name='id', description="ID of the DFN Cert advisory"
        ),
    }

    @staticmethod
    @require_authentication
    def resolve(_root, info, dfn_cert_advisory_id: str):
        gmp = get_gmp(info)

        xml = gmp.get_info(
            str(dfn_cert_advisory_id), info_type=GvmInfoType.DFN_CERT_ADV
        )
        return xml.find('info')


class GetDFNCertAdvisories(EntityConnectionField):
    """Gets a list of DFNCertAdvisory information with pagination

    Args:
        filter_string (str, optional): Optional filter string to be
            used with query.

    Example:

        .. code-block::

            query {
                dfnCertAdvisorys (filterString: "name~Foo rows=2") {
                    nodes {
                        id
                        name
                    }
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "dfnCertAdvisorys": {
                        "nodes": [
                            {
                                "id": "DFN-CERT-2008-0644",
                                "name": "Foo"
                            },
                            {
                                "id": "DFN-CERT-2008-0645",
                                "name": "Foo Bar"
                            },
                        ]
                    }
                }
            }

    """

    entity_type = DFNCertAdvisory

    @staticmethod
    @require_authentication
    def resolve_entities(  # pylint: disable=arguments-differ
        _root,
        info: ResolveInfo,
        filter_string: FilterString = None,
        details: bool = True,
        after: str = None,
        before: str = None,
        first: int = None,
        last: int = None,
    ) -> Entities:
        gmp = get_gmp(info)

        filter_string = get_filter_string_for_pagination(
            filter_string, first=first, last=last, after=after, before=before
        )

        xml: XmlElement = gmp.get_info_list(
            filter=filter_string.filter_string,
            info_type=GvmInfoType.DFN_CERT_ADV,
            details=details,
        )

        requested = None
        dfn_cert_advisory_elements = []
        info_elements = xml.findall('info')
        for element in info_elements:
            if element.get('id'):
                dfn_cert_advisory_elements.append(element)
            else:
                requested = element
        counts = xml.find('info_count')

        return Entities(dfn_cert_advisory_elements, counts, requested)
