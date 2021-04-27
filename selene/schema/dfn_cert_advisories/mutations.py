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

# pylint: disable=no-self-argument, no-member

from gvm.protocols.next import InfoType as GvmInfoType
from selene.schema.entities import (
    create_export_secinfos_by_ids_mutation,
    create_export_by_filter_mutation,
)


# Explicit classes needed, else we get error
# 'AssertionError: Found different types with the same name in the
#   schema: ExportByIds, ExportByIds.'

ExportByIdsClass = create_export_secinfos_by_ids_mutation(
    info_type=GvmInfoType.DFN_CERT_ADV
)


class ExportDFNCertAdvisoriesByIds(ExportByIdsClass):
    pass


ExportByFilterClass = create_export_by_filter_mutation(
    entity_name='info',
    entities_name='info_list',
    with_details=True,
    info_type=GvmInfoType.DFN_CERT_ADV,
)


class ExportDFNCertAdvisoriesByFilter(ExportByFilterClass):
    pass
