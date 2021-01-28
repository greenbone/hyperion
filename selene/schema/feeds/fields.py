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

import graphene

from selene.schema.resolver import find_resolver, text_resolver

from selene.schema.utils import get_text_from_element


class FeedType(graphene.Enum):
    CERT = 'cert'
    GVMD_DATA = 'gvmd_data'
    NVT = 'nvt'
    SCAP = 'scap'


class FeedSyncNotAvailable(graphene.ObjectType):
    class Meta:
        default_resolver = text_resolver

    error = graphene.String()


class FeedCurrentlySyncing(graphene.ObjectType):
    class Meta:
        default_resolver = text_resolver

    timestamp = graphene.String()


class Feed(graphene.ObjectType):
    class Meta:
        default_resolver = find_resolver

    feed_type = FeedType(name='type')
    name = graphene.String()
    version = graphene.String()
    description = graphene.String()
    sync_not_available = graphene.Field(FeedSyncNotAvailable)
    currently_syncing = graphene.Field(FeedCurrentlySyncing)

    @staticmethod
    def resolve_name(root, _info):
        return get_text_from_element(root, 'name')

    @staticmethod
    def resolve_version(root, _info):
        return get_text_from_element(root, 'version')

    @staticmethod
    def resolve_description(root, _info):
        return get_text_from_element(root, 'description')

    @staticmethod
    def resolve_feed_type(root, _info):
        text = get_text_from_element(root, 'type').upper()

        if text == 'CERT':
            return FeedType.CERT
        elif text == 'GVMD_DATA':
            return FeedType.GVMD_DATA
        elif text == 'NVT':
            return FeedType.NVT
        elif text == 'SCAP':
            return FeedType.SCAP
