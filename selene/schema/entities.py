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

from xml import etree
from typing import List

import graphene

from selene.schema.utils import get_gmp, require_authentication, XmlElement


class AbstractExportByFilter(graphene.ObjectType):
    class Arguments:
        filter_string = graphene.String(
            description="Filter term for entities to export."
        )

    exported_entities = graphene.String()


def create_export_by_filter_mutation(
    entity_name: str,
    *,
    with_details: bool = None,
    entities_name: str = None,
    **kwargs,
):
    """
    Args:
        entity_name (str): Type of the entity in singular. E.g. 'config'
        with_details (bool, optional): Should entities be returned with details
        entities_name (str, optional): Plural for irregular words
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.
    """

    class ExportByFilter(graphene.Mutation, AbstractExportByFilter):
        @require_authentication
        def mutate(root, info, filter_string: str = None):
            gmp = get_gmp(info)

            get_entities = (
                getattr(gmp, f'get_{entities_name}')
                if entities_name
                else getattr(gmp, f'get_{entity_name}s')
            )

            if with_details:
                # not all get_entities function has details argument
                xml: XmlElement = get_entities(
                    filter=filter_string, details=True, **kwargs
                )
            else:
                xml: XmlElement = get_entities(filter=filter_string, **kwargs)

            serialized_xml = etree.ElementTree.tostring(xml, encoding='unicode')

            return AbstractExportByFilter(exported_entities=serialized_xml)

    return ExportByFilter


class AbstractExportByIds(graphene.ObjectType):
    class Arguments:
        entity_ids = graphene.List(
            graphene.UUID,
            required=True,
            name='ids',
            description="List of UUIDs of entities to export.",
        )

    exported_entities = graphene.String()


def create_export_by_ids_mutation(
    entity_name: str,
    *,
    with_details: bool = None,
    entities_name: List[str] = None,
    **kwargs,
):
    """
    Args:
        entity_name (str): Type of the entity in singular. E.g. 'config'
        with_details (bool, optional): Should entities be returned with details
        entities_name (str, optional): Plural for irregular words
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.
    """

    class ExportByIds(graphene.Mutation, AbstractExportByIds):
        @require_authentication
        def mutate(root, info, entity_ids: str = None):
            gmp = get_gmp(info)

            get_entities = (
                getattr(gmp, f'get_{entities_name}')
                if entities_name
                else getattr(gmp, f'get_{entity_name}s')
            )

            filter_string = ''

            for entity_id in entity_ids:
                filter_string += f'uuid={str(entity_id)} '

            if with_details:
                # not all get_entities function has details argument
                xml: XmlElement = get_entities(
                    filter=filter_string, details=True, **kwargs
                )
            else:
                xml: XmlElement = get_entities(filter=filter_string, **kwargs)
            serialized_xml = etree.ElementTree.tostring(xml, encoding='unicode')

            return AbstractExportByIds(exported_entities=serialized_xml)

    return ExportByIds


class AbstractDeleteByFilter(graphene.ObjectType):
    class Arguments:
        filter_string = graphene.String(
            description="Filter term for entities to delete."
        )
        ultimate = graphene.Boolean()

    ok = graphene.Boolean()


def create_delete_by_filter_mutation(
    entity_name: str,
    *,
    entities_name: str = None,
    gmp_entity_response: str = None,
    **kwargs,
):
    """
    Args:
        entity_name (str): Type of the entity in singular. E.g. 'config'
        entities_name (str, optional): Plural for irregular words
        gmp_entity_response (str, optional): Expected entity name in the gmp
            response.
            E.g.: policy has 'config' and audit has 'task' as entity
            response.
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.
    """

    class DeleteByFilter(graphene.Mutation, AbstractDeleteByFilter):
        @require_authentication
        def mutate(
            root, info, filter_string: str = None, ultimate: bool = None
        ):
            gmp = get_gmp(info)

            # gmp delete function to call later.
            delete_entity = getattr(gmp, f'delete_{entity_name}')
            # gmp get function to call later.
            get_entities = (
                getattr(gmp, f'get_{entities_name}')
                if entities_name
                else getattr(gmp, f'get_{entity_name}s')
            )
            # Get the entities via a filter
            get_entities_xml_response = get_entities(
                filter=filter_string, **kwargs
            )

            xml_entities = get_entities_xml_response.findall(
                gmp_entity_response if gmp_entity_response else entity_name
            )
            for entity in xml_entities:
                entity_id = {f'{entity_name}_id': str(entity.get('id'))}
                if ultimate:
                    delete_entity(ultimate=True, **entity_id)
                else:
                    delete_entity(**entity_id)

            return AbstractDeleteByIds(ok=True)

    return DeleteByFilter


class AbstractDeleteByIds(graphene.ObjectType):
    """
    Args:
        entity_name (str): Type of the entity in singular. E.g. 'config'
        entities_name (str, optional): Plural for irregular words
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.
    """

    class Arguments:
        entity_ids = graphene.List(
            graphene.UUID,
            required=True,
            name='ids',
            description="List of UUIDs of entities to delete..",
        )
        ultimate = graphene.Boolean()

    ok = graphene.Boolean()


def create_delete_by_ids_mutation(
    entity_name: str,
    entities_name: str = None,
    gmp_entity_response: str = None,
    **kwargs,
):
    """
    Args:
        entity_name (str): Type of the entity in singular. E.g. 'config'
        gmp_entity_response (str, optional): Expected entity name in the gmp
            response.
            E.g.: policy has 'config' and audit has 'task' as entity
            response.

    """

    class DeleteByIds(graphene.Mutation, AbstractDeleteByIds):
        @require_authentication
        def mutate(root, info, entity_ids=None, ultimate=None):
            gmp = get_gmp(info)

            # gmp delete function to call later.
            delete_entity = getattr(gmp, f'delete_{entity_name}')
            # gmp get function to call later.
            get_entities = (
                getattr(gmp, f'get_{entities_name}')
                if entities_name
                else getattr(gmp, f'get_{entity_name}s')
            )

            filter_string = ''
            for entity_id in entity_ids:
                filter_string += f'uuid={str(entity_id)} '
            # Get the entities via a filter. This is needed because we need to
            # be sure that the entities we want to delete really exist. Else
            # we might only delete some of the entities until an error
            # interrupts the deletion process.
            get_entities_xml_response = get_entities(
                filter=filter_string, **kwargs
            )

            xml_entities = get_entities_xml_response.findall(
                gmp_entity_response if gmp_entity_response else entity_name
            )
            found_ids = []
            for entity in xml_entities:
                found_ids.append(entity.get('id'))

            # Entities only get deleted if all entities were found.
            if len(entity_ids) != len(found_ids):
                return AbstractDeleteByIds(ok=False)
            else:
                for entity in entity_ids:
                    # Not all delete functions support the ultimate flag.
                    entity_id = {f'{entity_name}_id': str(entity)}
                    if ultimate:
                        delete_entity(ultimate=True, **entity_id)
                    else:
                        delete_entity(**entity_id)

            return AbstractDeleteByIds(ok=True)

    return DeleteByIds


class AbstractExportSecInfosByIds(graphene.ObjectType):
    class Arguments:
        entity_ids = graphene.List(
            graphene.String,
            required=True,
            name='ids',
            description="List of IDs of secinfo to export.",
        )

    exported_entities = graphene.String()


def create_export_secinfos_by_ids_mutation(
    entity_name: str,
    *,
    with_details: bool = None,
    entities_name: str = None,
    **kwargs,
):
    """
    Args:
        entity_name (str): Type of the entity in singular. E.g. 'config'
        with_details (bool, optional): Should entities be returned with details
        entities_name (str, optional): Plural for irregular words
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.
    """

    class ExportByIds(graphene.Mutation, AbstractExportByIds):
        @require_authentication
        def mutate(root, info, entity_ids: List[str] = None):
            gmp = get_gmp(info)

            get_entities = (
                getattr(gmp, f'get_{entities_name}')
                if entities_name
                else getattr(gmp, f'get_{entity_name}s')
            )

            filter_string = ''

            for entity_id in entity_ids:
                filter_string += f'uuid={str(entity_id)} '

            if with_details:
                # not all get_entities function has details argument
                xml: XmlElement = get_entities(
                    filter=filter_string, details=True, **kwargs
                )
            else:
                xml: XmlElement = get_entities(filter=filter_string, **kwargs)
            serialized_xml = etree.ElementTree.tostring(xml, encoding='unicode')

            return AbstractExportByIds(exported_entities=serialized_xml)

    return ExportByIds
