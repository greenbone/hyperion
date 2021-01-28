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

# pylint: disable=no-self-argument, no-member

import graphene

from gvm.protocols.latest import EntityType as GvmEntityType

from selene.schema.resolver import text_resolver

from selene.schema.base import BaseObjectType


class EntityType(graphene.Enum):
    class Meta:
        enum = GvmEntityType


class ResourceAction(graphene.Enum):
    ADD = 'add'
    SET = 'set'
    REMOVE = 'remove'


class Tag(BaseObjectType):
    class Meta:
        default_resolver = text_resolver

    value = graphene.String()
    comment = graphene.String()
