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

from selene.schema.parser import parse_datetime

from selene.schema.utils import get_text_from_element


class InnerSystemReport(graphene.ObjectType):
    """
    Object class representing a system (performance) report file,
    consisting of the file format / extension, time information and the
    file content as a Base64 string.
    """

    system_report_format = graphene.String(
        name='format', description='Format / extension of the report file.'
    )
    start_time = graphene.DateTime(
        description='Date and time the system report starts at, if specified.'
    )
    end_time = graphene.DateTime(
        description='Date and time the system report ends at, if specified.'
    )
    duration = graphene.Int(
        description='The duration of the system reports in seconds, if it is'
        ' not constrained by start and end time.'
    )
    content = graphene.String(description='The Base64 encoded file content.')

    @staticmethod
    def resolve_system_report_format(root, _info):
        return root.attrib['format']

    @staticmethod
    def resolve_start_time(root, _info):
        if root.attrib['start_time']:
            return parse_datetime(root.attrib['start_time'])
        else:
            return None

    @staticmethod
    def resolve_end_time(root, _info):
        if root.attrib['end_time']:
            return parse_datetime(root.attrib['end_time'])
        else:
            return None

    @staticmethod
    def resolve_duration(root, _info):
        if root.attrib['duration']:
            return root.attrib['duration']
        else:
            return None

    @staticmethod
    def resolve_content(root, _info):
        return root.text


class SystemReport(graphene.ObjectType):
    """
    Object class containing a the name, title and optionally the content of a
    system (performance) report.
    """

    name = graphene.String(
        description='Name of the system report, also used as an identifier.'
    )
    title = graphene.String(
        description='Longer, more human-readable title of the system report.'
    )
    report = graphene.Field(
        InnerSystemReport,
        description='Object representing the system report file.',
    )

    @staticmethod
    def resolve_name(root, _info):
        return get_text_from_element(root, 'name')

    @staticmethod
    def resolve_title(root, _info):
        return get_text_from_element(root, 'title')

    @staticmethod
    def resolve_report(root, _info):
        return root.find('report')
