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

from selene.schema.utils import require_authentication, get_gmp

from selene.schema.entities import (
    create_export_by_ids_mutation,
    create_export_by_filter_mutation,
    create_delete_by_ids_mutation,
    create_delete_by_filter_mutation,
)


class CreateScheduleInput(graphene.InputObjectType):
    """Input object for createSchedule.

    Args:
        name: Name of the new schedule
        icalendar: `iCalendar`_ (RFC 5545) based data.
        timezone: Timezone to use for the icalender events e.g
            Europe/Berlin. If the datetime values in the icalendar data are
            missing timezone information this timezone gets applied.
            Otherwise the datetime values from the icalendar data are
            displayed in this timezone
        comment: Comment on schedule.
    """

    name = graphene.String(
        required=True, description="Name of the new schedule"
    )
    icalendar = graphene.String(
        required=True, description="`iCalendar`_ (RFC 5545) based data"
    )
    timezone = graphene.String(
        required=True,
        description=(
            "Timezone to use for the icalender events e.g"
            "Europe/Berlin. If the datetime values in the icalendar data are"
            "missing timezone information this timezone gets applied."
            "Otherwise the datetime values from the icalendar data are"
            "displayed in this timezone"
        ),
    )
    comment = graphene.String(description="Comment on schedule")


class CreateSchedule(graphene.Mutation):
    class Arguments:
        input_object = CreateScheduleInput(required=True, name='input')

    schedule_id = graphene.UUID(name='id')

    @staticmethod
    @require_authentication
    def mutate(_root, info, input_object):
        gmp = get_gmp(info)

        resp = gmp.create_schedule(
            name=input_object.name,
            icalendar=input_object.icalendar,
            timezone=input_object.timezone,
            comment=input_object.comment,
        )

        return CreateSchedule(schedule_id=resp.get('id'))


class ModifyScheduleInput(graphene.InputObjectType):
    """Input object for modifySchedule.

    Args:
        schedule_id: UUID of the schedule to be modified
        name: Name of the new schedule
        icalendar: `iCalendar`_ (RFC 5545) based data.
        timezone: Timezone to use for the icalender events e.g
            Europe/Berlin. If the datetime values in the icalendar data are
            missing timezone information this timezone gets applied.
            Otherwise the datetime values from the icalendar data are
            displayed in this timezone
        comment: Comment on schedule.
    """

    schedule_id = graphene.UUID(
        name='id',
        required=True,
        description='UUID of the schedule to be modified',
    )
    name = graphene.String(description="Name of the new schedule")
    icalendar = graphene.String(
        description="`iCalendar`_ (RFC 5545) based data"
    )
    timezone = graphene.String(
        description=(
            "Timezone to use for the icalender events e.g"
            "Europe/Berlin. If the datetime values in the icalendar data are"
            "missing timezone information this timezone gets applied."
            "Otherwise the datetime values from the icalendar data are"
            "displayed in this timezone"
        )
    )
    comment = graphene.String(description="Comment on schedule")


class ModifySchedule(graphene.Mutation):
    class Arguments:
        input_object = ModifyScheduleInput(required=True, name='input')

    ok = graphene.Boolean()

    @staticmethod
    @require_authentication
    def mutate(_root, info, input_object):
        gmp = get_gmp(info)

        gmp.modify_schedule(
            str(input_object.schedule_id),
            name=input_object.name,
            icalendar=input_object.icalendar,
            timezone=input_object.timezone,
            comment=input_object.comment,
        )

        return ModifySchedule(ok=True)


class CloneSchedule(graphene.Mutation):
    """Clone a schedule

    Args:
        id (UUID): UUID of schedule to clone.

    Example:

        .. code-block::

            mutation {
                cloneSchedule(
                    id: "b992601e-e0df-4078-b4b1-39e04f92f4cc",
                ) {
                    id
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "cloneSchedule": {
                    "id": "a569f3df-0f8d-4001-aeef-08cdee0cdf49"
                    }
                }
            }
    """

    class Arguments:
        schedule_id = graphene.UUID(required=True, name='id')

    # it is really awkward to reuse the same variable
    # name here, but it seems working ...?!
    schedule_id = graphene.UUID(name='id')

    @staticmethod
    @require_authentication
    def mutate(_root, info, schedule_id):
        gmp = get_gmp(info)
        elem = gmp.clone_schedule(str(schedule_id))
        return CloneSchedule(schedule_id=elem.get('id'))


# Explicit classes needed, else we get error
# 'AssertionError: Found different types with the same name in the
#   schema: DeleteByIds, DeleteByIds.'


DeleteByIdsClass = create_delete_by_ids_mutation(entity_name='schedule')


class DeleteSchedulesByIds(DeleteByIdsClass):
    """Deletes a list of schedules

    Args:
        ids (List(UUID)): List of UUIDs of schedules to delete.
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.

    Returns:
        ok (Boolean)

    Example

        mutation {
            deleteScheduleByIds(
                ids: ["5f8e7b31-35ea-4b43-9797-6d77f058906b"],
                ultimate: false)
            {
                ok
            }
        }

        Response
        {
            "data": {
                "deleteScheduleByIds": {
                    "ok": true
                }
            }
        }
    """


DeleteByFilterClass = create_delete_by_filter_mutation(entity_name='schedule')


class DeleteSchedulesByFilter(DeleteByFilterClass):
    """Deletes a filtered list of schedules

    Args:
        filterString (str): Filter string for schedule list to delete.
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.

    Returns:
        ok (Boolean)

    Example

        mutation {
            deleteScheduleByFilter(
                filterString:"name~Clone",
                ultimate: false)
            {
                ok
            }
        }

        Response
        {
            "data": {
                "deleteScheduleByFilter": {
                    "ok": true
                }
            }
        }
    """


# Explicit classes needed, else we get error
# 'AssertionError: Found different types with the same name in the
#   schema: ExportByIds, ExportByIds.'

ExportByIdsClass = create_export_by_ids_mutation(entity_name='schedule')


class ExportSchedulesByIds(ExportByIdsClass):
    pass


ExportByFilterClass = create_export_by_filter_mutation(entity_name='schedule')


class ExportSchedulesByFilter(ExportByFilterClass):
    pass
