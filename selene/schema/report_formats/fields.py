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

import graphene

from selene.schema.entity import EntityObjectType
from selene.schema.utils import (
    get_boolean_from_element,
    get_text_from_element,
    get_datetime_from_element,
)


class ReportFormat(EntityObjectType):
    """ReportFormat object type. Can be used in getReportFormat and
    getReportFormats queries.

    Please query in camelCase e.g. report_format_id => reportFormatId.
    """

    summary = graphene.String()
    description = graphene.String()
    predefined = graphene.Boolean()
    trust = graphene.String()
    trust_time = graphene.DateTime()
    active = graphene.Boolean()
    extension = graphene.String()

    @staticmethod
    def resolve_summary(root, _info):
        return get_text_from_element(root, 'summary')

    @staticmethod
    def resolve_description(root, _info):
        return get_text_from_element(root, 'description')

    @staticmethod
    def resolve_trust(root, _info):
        return get_text_from_element(root, 'trust')

    @staticmethod
    def resolve_trust_time(root, _info):
        trust = root.find('trust')
        return get_datetime_from_element(trust, 'time')

    @staticmethod
    def resolve_predefined(root, _info):
        return get_boolean_from_element(root, 'predefined')

    @staticmethod
    def resolve_active(root, _info):
        return get_boolean_from_element(root, 'active')

    @staticmethod
    def resolve_extension(root, _info):
        return get_text_from_element(root, 'extension')
