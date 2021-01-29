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

from uuid import UUID

from graphql import ResolveInfo

import graphene

from selene.schema.parser import FilterString

from selene.schema.relay import (
    EntityConnectionField,
    Entities,
    get_filter_string_for_pagination,
)

from selene.schema.utils import (
    require_authentication,
    get_gmp,
    XmlElement,
)

from selene.schema.scan_configs.fields import ScanConfig


class GetScanConfig(graphene.Field):
    """Gets a single scan config.

    Args:
        id (UUID): UUID of the scan config being queried

    Example:

        .. code-block::

            query {
                scanConfig (id: "3232d608-e5bb-415e-99aa-019f16eede8d") {
                    name
                    type
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "scan_config": {
                        "name": "Full and fast",
                        "type": 0,
                    }
                }
            }

    """

    def __init__(self):
        super().__init__(
            ScanConfig,
            config_id=graphene.UUID(required=True, name='id'),
            resolver=self.resolve,
        )

    @staticmethod
    @require_authentication
    def resolve(_root, info, config_id: UUID):
        # Elements available in gmp but not currently resolved:
        # - <growing> subelement of <family_count>
        # - <growing> subelement of <nvt_count>
        # - <scanner> element
        # - <permissions> subelement of <task>
        # - Not needed for single scan config: <filters>, <sort>, <configs>,
        #   <config_count>
        gmp = get_gmp(info)

        xml = gmp.get_config(str(config_id), tasks=True)
        return xml.find('config')


class GetScanConfigs(EntityConnectionField):
    """Gets a list of scan configs with pagination

    Args:
        filter_string (str, optional): Optional filter string to be
            used with query.

    Example:

        .. code-block::

            query {
                scanConfigs(filterString: "full and fast"){
                    nodes{
                        name
                        id
                        type
                    }
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "scanConfigs": {
                        "nodes": [
                            {
                                "name": "Full and fast",
                                "id": "daba56c8-73ec-11df-a475-002264764cea",
                                "type": 0
                            },
                            {
                                "name": "Full and fast ultimate",
                                "id": "698f691e-7489-11df-9d8c-002264764cea",
                                "type": 0
                            },
                        ]
                    }
                }
            }

    """

    entity_type = ScanConfig

    @staticmethod
    @require_authentication
    def resolve_entities(  # pylint: disable=arguments-differ
        _root,
        info: ResolveInfo,
        filter_string: FilterString = None,
        after: str = None,
        before: str = None,
        first: int = None,
        last: int = None,
    ) -> Entities:
        gmp = get_gmp(info)

        filter_string = get_filter_string_for_pagination(
            filter_string, first=first, last=last, after=after, before=before
        )

        xml: XmlElement = gmp.get_configs(
            filter=filter_string.filter_string, details=False
        )

        scan_config_elements = xml.findall('config')
        counts = xml.find('config_count')
        requested = xml.find('configs')

        return Entities(scan_config_elements, counts, requested)
