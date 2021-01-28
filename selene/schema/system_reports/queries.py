# -*- coding: utf-8 -*-
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

from selene.schema.system_reports.fields import SystemReport
from selene.schema.utils import (
    require_authentication,
    get_gmp,
)


class GetSystemReport(graphene.Field):
    """Gets a single system (performance) report.

    Args:
        name (str): Name of the system report to get.

        sensor_id (str, optional): Optional scanner ID of a sensor to collect
            the data from.

        duration: (int, optional): Optional number of seconds the report should
            cover.

        start_time (datetime, optional): Optional date and time the report
            should start.

        end_time (datetime, optional): Optional date and time the report
            should end.

    Example:

        .. code-block::
        query {
        systemReport(name: "load",
                     startTime: "2020-11-18T15:00:00Z",
                     duration: 600) {
                name
                title
                report {
                    format
                    startTime
                    endTime
                    duration
                    content
                }
            }
        }

        Response:

        .. code-block::
        {
            "data": {
                "systemReport": {
                    "name": "load",
                    "title": "System Load",
                    "report": {
                        "format": "png",
                        "startTime": "2020-11-18T15:00:00+00:00",
                        "endTime": null,
                        "duration": 600,
                        "content": "iVBORw0KGgoAAAA..."
                }
            }
        }

    """

    def __init__(self):
        super().__init__(
            SystemReport,
            name=graphene.String(
                required=True,
                description='Name of the system report to get.',
            ),
            sensor_id=graphene.UUID(
                description='Optional scanner ID of a sensor to collect'
                ' the data from.'
            ),
            duration=graphene.Int(
                description='Optional number of seconds the report should'
                ' cover.'
            ),
            start_time=graphene.DateTime(
                description='Optional date and time the report should start.'
            ),
            end_time=graphene.DateTime(
                description='Optional date and time the report should end.'
            ),
            resolver=self.resolve,
            description='Gets a single system (performance) report.',
        )

    @staticmethod
    @require_authentication
    def resolve(
        _root,
        info,
        name: graphene.String,
        sensor_id: graphene.UUID = None,
        duration: graphene.Int = None,
        start_time: graphene.DateTime = None,
        end_time: graphene.DateTime = None,
    ):
        gmp = get_gmp(info)

        sensor_id_str = str(sensor_id) if sensor_id else None
        xml = gmp.get_system_reports(
            name=name,
            slave_id=sensor_id_str,
            duration=duration,
            start_time=start_time,
            end_time=end_time,
        )
        return xml.find('system_report')


class GetSystemReports(graphene.List):
    """Gets a list of system (performance) report names and titles.

    Args:
        sensor_id (str, optional): Optional scanner ID of a sensor to collect
            the data from.

    Example:

        .. code-block::

        query {
            systemReports (sensorId: "08b69003-5fc2-4037-a479-93b440211c73") {
                name
                title
            }
        }

        Response:

        .. code-block::

        {
            "data": {
                "systemReports": [
                    {
                        "name": "proc",
                        "title": "Processes"
                    },
                    {
                        "name": "load",
                        "title": "System Load"
                    },
                    {
                        "name": "cpu-0",
                        "title": "CPU Usage: cpu-0"
                    },
                    {
                        "name": "mem",
                        "title": "Memory Usage"
                    }
                ]
            }
        }
    """

    def __init__(
        self,
    ):
        super().__init__(
            SystemReport,
            sensor_id=graphene.UUID(
                description='Optional scanner ID of a sensor to collect'
                ' the data from.'
            ),
            resolver=self.resolve,
            description='Gets a list of system (performance) report names'
            ' and titles.',
        )

    @staticmethod
    @require_authentication
    def resolve(_root, info, sensor_id: graphene.UUID = None):
        gmp = get_gmp(info)

        sensor_id_str = str(sensor_id) if sensor_id is not None else None
        xml = gmp.get_system_reports(brief=True, slave_id=sensor_id_str)
        return xml.findall('system_report')
