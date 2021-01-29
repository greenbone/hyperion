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

from uuid import UUID
import graphene

from graphql import ResolveInfo
from selene.schema.parser import FilterString

from selene.schema.utils import get_gmp, require_authentication, XmlElement
from selene.schema.users.fields import User

from selene.schema.relay import (
    EntityConnectionField,
    Entities,
    get_filter_string_for_pagination,
)


class GetUser(graphene.Field):
    """Request a single user."""

    def __init__(self):
        super().__init__(
            User,
            user_id=graphene.UUID(required=True, name='id'),
            resolver=self.resolve,
        )

    @staticmethod
    @require_authentication
    def resolve(_root, info, user_id: UUID):
        gmp = get_gmp(info)

        xml = gmp.get_user(str(user_id))
        return xml.find('user')


class GetUsers(EntityConnectionField):
    """Request a list of users."""

    entity_type = User

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

        xml: XmlElement = gmp.get_users(filter=filter_string.filter_string)

        user_elements = xml.findall('user')
        counts = xml.find('user_count')
        requested = xml.find('user')

        return Entities(user_elements, counts, requested)
