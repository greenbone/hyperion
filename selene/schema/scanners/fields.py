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

import graphene

from gvm.protocols.next import ScannerType as GvmScannerType

from selene.schema.resolver import find_resolver, text_resolver

from selene.schema.utils import (
    get_boolean_from_element,
    get_datetime_from_element,
    get_text_from_element,
)

from selene.schema.base import BaseObjectType
from selene.schema.entity import EntityObjectType

from selene.schema.scan_configs.fields import ScanConfig


class Param(graphene.ObjectType):
    class Meta:
        default_resolver = text_resolver

    id = graphene.String()
    name = graphene.String()
    default = graphene.String()
    description = graphene.String()
    type = graphene.String()

    mandatory = graphene.Boolean()

    @staticmethod
    def resolve_mandatory(root, _info):
        return get_boolean_from_element(root, 'mandatory')


class InfoType(graphene.ObjectType):
    class Meta:
        default_resolver = text_resolver

    name = graphene.String()
    version = graphene.String()


class ScannerInfo(graphene.ObjectType):
    class Meta:
        default_resolver = find_resolver

    description = graphene.String()

    scanner = graphene.Field(InfoType)
    daemon = graphene.Field(InfoType)
    protocol = graphene.Field(InfoType)

    params = graphene.List(Param)

    @staticmethod
    def resolve_description(root, _info):
        return get_text_from_element(root, 'description')

    @staticmethod
    def resolve_params(root, _info):
        params = root.find('params')
        if len(params) == 0:
            return None
        return params.findall('param')


class CaPubInfo(graphene.ObjectType):
    class Meta:
        default_resolver = text_resolver

    time_status = graphene.String()
    md5_fingerprint = graphene.String()
    issuer = graphene.String()

    activation_time = graphene.DateTime()
    expiration_time = graphene.DateTime()

    @staticmethod
    def resolve_activation_time(root, _info):
        return get_datetime_from_element(root, 'activation_time')

    @staticmethod
    def resolve_expiration_time(root, _info):
        return get_datetime_from_element(root, 'expiration_time')


class CaPub(graphene.ObjectType):

    certificate = graphene.String()
    info = graphene.Field(CaPubInfo)

    @staticmethod
    def resolve_certificate(root, _info):
        return root.get("certificate")

    @staticmethod
    def resolve_info(root, _info):
        return root.get("info")


class ScannerTask(BaseObjectType):
    pass


class ScannerCredential(BaseObjectType):
    pass


class ScannerType(graphene.Enum):
    class Meta:
        enum = GvmScannerType


class Scanner(EntityObjectType):

    host = graphene.String()
    port = graphene.String()

    configs = graphene.List(ScanConfig)
    tasks = graphene.List(ScannerTask)

    credential = graphene.Field(ScannerCredential)

    ca_pub = graphene.Field(CaPub)
    ca_pub_info = graphene.Field(CaPubInfo)
    info = graphene.Field(ScannerInfo)

    type = graphene.Field(
        ScannerType, name="type", description="Type of the scanner"
    )

    @staticmethod
    def resolve_host(root, _info):
        return get_text_from_element(root, 'host')

    @staticmethod
    def resolve_port(root, _info):
        return get_text_from_element(root, 'port')

    @staticmethod
    def resolve_configs(root, _info):
        configs = root.find('configs')
        if len(configs) == 0:
            return None
        return configs.findall('config')

    @staticmethod
    def resolve_tasks(root, _info):
        tasks = root.find('tasks')
        if len(tasks) == 0:
            return None
        return tasks.findall('task')

    @staticmethod
    def resolve_ca_pub(parent, _info):
        return {
            "certificate": get_text_from_element(parent, 'ca_pub'),
            "info": parent.find("ca_pub_info"),
        }

    @staticmethod
    def resolve_info(root, _info):
        return root.find('info')

    @staticmethod
    def resolve_credential(root, _info):
        return root.find('credential')

    @staticmethod
    def resolve_type(root, _info):
        return get_text_from_element(root, 'type')
