# -*- coding: utf-8 -*-
# Copyright (C) 2019-2021 Greenbone Networks GmbH
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

from graphql import ResolveInfo
from gvm.protocols.latest import InfoType as GvmInfoType

from selene.schema.nvts.fields import (
    ScanConfigNVT,
    NvtFamily,
    NvtPreference,
    NVT,
)

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


class GetScanConfigNvt(graphene.Field):
    """Gets a single ScanConfig NVT.

    Args:
        oid (str): OID of the NVT to get

    Example:

        .. code-block::

            query {
                nvt (oid:"1.3.6.1.4.1.25623.1.0.999999") {
                oid
                creationTime
                modificationTime
                category
                summary
                family
                cvssBase
                qod {
                    value
                    type
                }
                severities {
                    score
                    severitiesList {
                        date
                        origin
                        score
                        type
                        value
                    }
                }
                refs{
                    warning
                    refList{
                        id
                        type
                    }
                }
                tags
                preferenceCount
                timeout
                defaultTimeout
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "nvt": {
                        "name": "Some name of a NVT",
                        .....
                        .....
                    }
                }
            }

    """

    def __init__(self):
        super().__init__(
            ScanConfigNVT,
            oid=graphene.String(required=True),
            resolver=self.resolve,
        )

    @staticmethod
    @require_authentication
    def resolve(_root, info, oid):
        gmp = get_gmp(info)

        xml = gmp.get_nvt(oid)
        return xml.find('nvt')


class GetScanConfigNvts(graphene.List):
    """Gets multiple ScanConfig NVTs.

    Args:
        details (bool, optional): Whether to include full details
        preferences (bool, optional): Whether to include nvt preferences
        preference_count (bool, optional): Whether to include preference count
        timeout (bool, optional): Whether to include the special timeout
            preference
        config_id (str, optional): UUID of scan config to which to limit the
            NVT listing
        preferences_config_id (str, optional): UUID of scan config to use for
            preference values
        family (str, optional): Family to which to limit NVT listing
        sort_order (str, optional): Sort order
        sort_field (str, optional): Sort field
    """

    def __init__(self):
        super().__init__(
            ScanConfigNVT,
            resolver=self.resolve,
            details=graphene.Boolean(),
            preferences=graphene.Boolean(),
            preference_count=graphene.Boolean(),
            timeout=graphene.Boolean(),
            config_id=graphene.String(),
            preferences_config_id=graphene.String(),
            family=graphene.String(),
            sort_order=graphene.String(),
            sort_field=graphene.String(),
        )

    @staticmethod
    @require_authentication
    def resolve(
        _root,
        info,
        details: bool = None,
        preferences: bool = None,
        preference_count: bool = None,
        timeout: bool = None,
        config_id: str = None,
        preferences_config_id: str = None,
        family: str = None,
        sort_order: str = None,
        sort_field: str = None,
    ):
        gmp = get_gmp(info)

        xml = gmp.get_nvts(
            details=details,
            preferences=preferences,
            preference_count=preference_count,
            timeout=timeout,
            config_id=config_id,
            preferences_config_id=preferences_config_id,
            family=family,
            sort_order=sort_order,
            sort_field=sort_field,
        )
        return xml.findall('nvt')


class GetNvtFamilies(graphene.List):
    """Get list of nvt families
        Args:
            sort_order (str, optional): "descending" denotes descending order,
                anything else means ascending.

    Example:

        .. code-block::

            query {
                task (taskId: "f5c40267-71ab-4cd7-b14b-3599a84522e8") {
                    name
                    comment
                }
            }

            query {
                nvtFamilies(sortOrder:"descending"){
                    name
                    maxNvtCount
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "nvtFamilies": [
                    {
                        "name": "Windows : Microsoft Bulletins",
                        "maxNvtCount": 3031
                    }
                    ]
                }
            }

    """

    def __init__(self):
        super().__init__(
            NvtFamily,
            sort_order=graphene.String(),
            resolver=self.resolve,
        )

    @staticmethod
    @require_authentication
    def resolve(_root, info, sort_order=None):

        gmp = get_gmp(info)
        xml = gmp.get_nvt_families(sort_order=sort_order)

        families = xml.find('families')
        if families is None:
            return []
        return families.findall('family')


class GetPreference(graphene.Field):
    """Get a single preference by name.

    name (str): Name of the preference. Has format type:name.
    nvt_oid (str, optional): OID of nvt.
    config_id (UUID, optional): UUID of scan config of which to show
        preference values.

    Example:

        .. code-block::

            query {
                preference (name: "<type>:Some name") {
                    name
                    value
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "preference": {
                        "name": "Some name",
                        "value": "yes,
                    }
                }
            }

    """

    def __init__(self):
        super().__init__(
            NvtPreference,
            name=graphene.String(required=True),
            nvt_oid=graphene.String(),
            config_id=graphene.UUID(),
            resolver=self.resolve,
        )

    @staticmethod
    @require_authentication
    def resolve(
        _root, info, name: str, nvt_oid: str = None, config_id: str = None
    ):
        gmp = get_gmp(info)

        if config_id is not None:
            config_id = str(config_id)

        xml = gmp.get_preference(
            name=name, nvt_oid=nvt_oid, config_id=config_id
        )
        return xml.find('preference')


class GetPreferences(graphene.List):
    """Request a list of preferences

    When the command includes a config_id attribute, the preference element
    includes the preference name, type and value, and the NVT to which the
    preference applies. Otherwise, the preference element includes just the
    name and value, with the NVT and type built into the name.

    nvt_oid (str, optional): OID of nvt.
    config_id (UUID, optional): UUID of a scan config of which to show
        preference values.


    Example:

        .. code-block::

            query {
                preferences (
                    nvtOid:"Some NVT OID",
                    configId: "daba56c8-73ec-11df-a475-002264764cea"
                ) {
                    name
                    value
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                "preferences": [
                    {
                        "name": "Some name 1",
                        "value": "Some value 1"
                    },
                    {
                        "name": "Some name 2",
                        "value": "Some value 2"
                    }
                ]
                }
            }

    """

    def __init__(self):
        super().__init__(
            NvtPreference,
            resolver=self.resolve,
            nvt_oid=graphene.String(),
            config_id=graphene.UUID(),
        )

    @staticmethod
    @require_authentication
    def resolve(
        _root,
        info,
        nvt_oid: str = None,
        config_id: str = None,
    ):
        gmp = get_gmp(info)

        if config_id is not None:
            config_id = str(config_id)

        xml = gmp.get_preferences(nvt_oid=nvt_oid, config_id=config_id)

        return xml.findall('preference')


class GetNVT(graphene.Field):
    """Gets a single NVT information.

    Args:
        id (str): ID of the NVT information being queried

    Example:

        .. code-block::

            query {
                nvt (id: "1.3.6.1.4.1.25623.1.0.123456"){
                        id
                        name
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "nvt": {
                        "id": "1.3.6.1.4.1.25623.1.0.123456",
                        "name": "foo"
                    }
                }
            }

    """

    def __init__(self):
        super().__init__(
            NVT,
            nvt_id=graphene.String(required=True, name='id'),
            resolver=self.resolve,
        )

    @staticmethod
    @require_authentication
    def resolve(_root, info, nvt_id: str):
        gmp = get_gmp(info)

        xml = gmp.get_info(str(nvt_id), info_type=GvmInfoType.NVT)
        return xml.find('info')


class GetNVTs(EntityConnectionField):
    """Gets a list of NVT information with pagination

    Args:
        filter_string (str, optional): Optional filter string to be
            used with query.

    Example:

        .. code-block::

            query {
                nvts (filterString: "name~Foo rows=2") {
                    nodes {
                        oid
                        name
                    }
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "nvts": {
                        "nodes": [
                            {
                                "oid": "NVT-2020-12345",
                                "name": "Foo"
                            },
                            {
                                "oid": "NVT-2020-12346",
                                "name": "Foo Bar"
                            },
                        ]
                    }
                }
            }

    """

    entity_type = NVT

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

        xml: XmlElement = gmp.get_info_list(
            filter=filter_string.filter_string,
            info_type=GvmInfoType.NVT,
        )

        requested = None
        nvt_elements = []
        info_elements = xml.findall('info')
        for element in info_elements:
            if element.get('id'):
                nvt_elements.append(element)
            else:
                requested = element
        counts = xml.find('info_count')

        return Entities(nvt_elements, counts, requested)
