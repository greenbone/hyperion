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

from graphql.language import ast

from selene.schema.resolver import text_resolver
from selene.schema.base import BaseObjectType
from selene.schema.parser import check_severity
from selene.schema.utils import get_text_from_element


class SeverityType(graphene.Scalar):
    """
    A scalar type representing a severity between 0 and 10

    Additionally the following values are defined:

     -1.0: False positive severity constant
     -2.0: Debug message severity constant
     -3.0: Error message severity constant
    -98.0: Constant for undefined severity (for ranges)
    -99.0: Constant for missing or invalid severity
    """

    @staticmethod
    def serialize(severity):
        return check_severity(severity)

    @staticmethod
    def parse_literal(node):
        # isinstance can only take two arguments
        if isinstance(node, (ast.FloatValue, ast.IntValue)):
            return check_severity(node.value)

    @staticmethod
    def parse_value(value):
        return check_severity(value)


class SeverityRange(graphene.ObjectType):
    """
    SeverityRange object type. Is part of the SeverityClass object.
    """

    class Meta:
        default_resolver = text_resolver

    name = graphene.String()
    minv = SeverityType(name="min")
    maxv = SeverityType(name="max")

    @staticmethod
    def resolve_minv(root, _info):
        return get_text_from_element(root, 'min')

    @staticmethod
    def resolve_maxv(root, _info):
        return get_text_from_element(root, 'max')


class SeverityClass(BaseObjectType):
    """
    SeverityClass object type. Is part of the Report object.
    """

    class Meta:
        default_resolver = text_resolver

    full_name = graphene.String()
    severity_ranges = graphene.List(SeverityRange)

    @staticmethod
    def resolve_severity_ranges(root, _info):
        return root.findall('severity_range')
