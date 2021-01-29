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

# pylint: disable=no-self-argument

import graphene

from selene.schema.utils import get_gmp, require_authentication


class EmptyTrashcan(graphene.Mutation):
    """Empties the trashcan

    Returns:
        ok (Boolean)
    """

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info):
        gmp = get_gmp(info)
        gmp.empty_trashcan()
        return EmptyTrashcan(ok=True)


class RestoreFromTrashcan(graphene.Mutation):
    """Restores an entity from the trashcan

    Returns:
        ok (Boolean)
    """

    class Arguments:
        restore_id = graphene.UUID(
            required=True,
            name='id',
            description='UUID of the entity to restore from the trashcan.',
        )

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, restore_id):
        gmp = get_gmp(info)
        gmp.restore(str(restore_id))
        return EmptyTrashcan(ok=True)
