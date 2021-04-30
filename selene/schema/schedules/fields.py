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

from selene.schema.resolver import find_resolver

from selene.schema.utils import get_text_from_element

from selene.schema.tasks.fields import Task
from selene.schema.entity import EntityObjectType


class Schedule(EntityObjectType):
    class Meta:
        default_resolver = find_resolver

    icalendar = graphene.String()
    tasks = graphene.List(Task)
    timezone = graphene.String()

    @staticmethod
    def resolve_icalendar(root, _info):
        return get_text_from_element(root, 'icalendar')

    @staticmethod
    def resolve_tasks(root, _info):
        tasks = root.find('tasks')
        if len(tasks) == 0:
            return None
        return tasks.findall('task')

    @staticmethod
    def resolve_timezone(root, _info):
        return get_text_from_element(root, 'timezone')
