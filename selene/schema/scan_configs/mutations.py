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

# pylint: disable=no-self-argument, no-member


import graphene

from selene.schema.utils import (
    require_authentication,
    get_gmp,
)

from selene.schema.entities import (
    create_export_by_ids_mutation,
    create_export_by_filter_mutation,
    create_delete_by_ids_mutation,
    create_delete_by_filter_mutation,
)


class DeleteScanConfig(graphene.Mutation):
    """Deletes a scan config

    Args:
        id (UUID): UUID of scan config to delete.

    Returns:
        ok (Boolean)

    Example

        mutation {
            deleteScanConfig(id: "5f8e7b31-35ea-4b43-9797-6d77f058906b",
                         ultimate: false)
            {
                ok
            }
        }

        Response
        {
            "data": {
                "deleteScanConfig": {
                    "ok": true
                }
            }
        }
    """

    class Arguments:
        config_id = graphene.UUID(required=True, name='id')
        ultimate = graphene.Boolean(required=False)

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, config_id, ultimate):
        gmp = get_gmp(info)
        gmp.delete_config(str(config_id), ultimate=ultimate)
        return DeleteScanConfig(ok=True)


# Explicit classes needed, else we get error
# 'AssertionError: Found different types with the same name in the
#   schema: DeleteByIds, DeleteByIds.'


DeleteByIdsClass = create_delete_by_ids_mutation(entity_name='config')


class DeleteScanConfigsByIds(DeleteByIdsClass):
    """Deletes a list of scan configs

    Args:
        ids (List(UUID)): List of UUIDs of scan configs to delete.
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.

    Returns:
        ok (Boolean)

    Example

        mutation {
            deleteScanConfigByIds(
                ids: ["5f8e7b31-35ea-4b43-9797-6d77f058906b"],
                ultimate: false)
            {
                ok
            }
        }

        Response
        {
            "data": {
                "deleteScanConfigByIds": {
                    "ok": true
                }
            }
        }
    """


DeleteByFilterClass = create_delete_by_filter_mutation(entity_name='config')


class DeleteScanConfigsByFilter(DeleteByFilterClass):
    """Deletes a filtered list of scan configs

    Args:
        filterString (str): Filter string for scan config list to delete.
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.

    Returns:
        ok (Boolean)

    Example

        mutation {
            deleteScanConfigByFilter(
                filterString:"name~Clone",
                ultimate: false)
            {
                ok
            }
        }

        Response
        {
            "data": {
                "deleteScanConfigByFilter": {
                    "ok": true
                }
            }
        }
    """


class CloneScanConfig(graphene.Mutation):
    """Clone a scan config

    Args:
        id (UUID): UUID of scan config to clone.

    Example:

        .. code-block::

            mutation {
                cloneScanConfig(
                    id: "b992601e-e0df-4078-b4b1-39e04f92f4cc",
                ) {
                    id
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "cloneScanConfig": {
                    "id": "a569f3df-0f8d-4001-aeef-08cdee0cdf49"
                    }
                }
            }
    """

    class Arguments:
        config_id = graphene.UUID(required=True, name='id')

    config_id = graphene.UUID(name='id')

    @require_authentication
    def mutate(root, info, config_id):
        gmp = get_gmp(info)
        elem = gmp.clone_config(str(config_id))
        return CloneScanConfig(config_id=elem.get('id'))


# Explicit classes needed, else we get error
# 'AssertionError: Found different types with the same name in the
#   schema: ExportByIds, ExportByIds.'

ExportByIdsClass = create_export_by_ids_mutation(
    entity_name='config', with_details=True
)


class ExportScanConfigsByIds(ExportByIdsClass):
    pass


ExportByFilterClass = create_export_by_filter_mutation(
    entity_name='config', with_details=True
)


class ExportScanConfigsByFilter(ExportByFilterClass):
    pass


class ImportScanConfig(graphene.Mutation):
    """Import a scan config

    Args:
        config (str) : Scan Config XML as string to import. This XML must
            contain a <get_configs_response> root element.

    Example:

        .. code-block::

            mutation {
                importScanConfig(
                    config: "<get_configs_response status=\"200\".......",
                ) {
                    id
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "importScanConfig": {
                        "id": "f7213438-ca44-4dc0-93d7-24bc20c4cf94"
                    }
                }
            }
    """

    class Arguments:
        config = graphene.String()

    config_id = graphene.UUID(name='id')

    @require_authentication
    def mutate(root, info, config):
        gmp = get_gmp(info)
        elem = gmp.import_config(config=config)

        return ImportScanConfig(config_id=elem.get('id'))


class CreateScanConfigInput(graphene.InputObjectType):
    """Input Object for CreateScanConfig
    Args:
        config_id (UUID): UUID of scan config to clone.
        name (str): Name of the new scan config
        comment (str): A comment on the config
    """

    config_id = graphene.UUID(
        required=True, description="UUID of scan config to clone."
    )
    name = graphene.String(
        required=True, description="Name of the new scan config."
    )
    comment = graphene.String(description="A comment on the config.")


class CreateScanConfig(graphene.Mutation):
    """Create a scan config.

    Args:
        Input (CreateScanConfigInput): input object for CreateScanConfig

    Example:

        .. code-block::

            mutation {
                createScanConfig( input" {
                    configId: "085569ce-73ed-11df-83c3-002264764cea",
                    name: "Name of new config",
                    comment: "Comment on the config"}
                ) {
                    id
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "createScanConfig": {
                        "id": "a569f3df-0f8d-4001-aeef-08cdee0cdf49"
                    }
                }
            }
    """

    class Arguments:
        input_object = CreateScanConfigInput(required=True, name='input')

    id_of_created_config = graphene.String(name='id')

    @require_authentication
    def mutate(root, info, input_object):
        gmp = get_gmp(info)
        config_id = (
            str(input_object.config_id)
            if input_object.config_id is not None
            else None
        )
        name = input_object.name if input_object.name is not None else None
        comment = (
            input_object.comment if input_object.comment is not None else None
        )

        elem = gmp.create_config(
            config_id=config_id, name=name, comment=comment
        )

        return CreateScanConfig(id_of_created_config=elem.get('id'))


class CreateScanConfigFromOspScannerInput(graphene.InputObjectType):
    """Input Object for CreateScanConfigFromOspScanner

    Args:
        scanner_id (UUID): UUID of an OSP scanner to get config data from
        name (str): Name of the new scan config
        comment (str): A comment on the config
    """

    scanner_id = graphene.UUID(
        required=True, description="UUID of an OSP scanner."
    )
    name = graphene.String(
        required=True, description="Name of the new scan config."
    )
    comment = graphene.String(description="A comment on the config.")


class CreateScanConfigFromOspScanner(graphene.Mutation):
    """Create a scan config from an osp scanner.

    Args:
        Input (CreateScanConfigFromOspScannerInput): input object for
            CreateScanConfigFromOspScanner

    Example:

        .. code-block::

            mutation {
                createScanConfigFromOspScanner( input" {
                    scannerId: "085569ce-73ed-11df-83c3-002264764cea",
                    name: "Name of new config",
                    comment: "Comment on the config"}
                ) {
                    id
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "createScanConfigFromOspScanner": {
                        "id": "a569f3df-0f8d-4001-aeef-08cdee0cdf49"
                    }
                }
            }
    """

    class Arguments:
        input_object = CreateScanConfigFromOspScannerInput(
            required=True, name='input'
        )

    id_of_created_config = graphene.String(name='id')

    @require_authentication
    def mutate(root, info, input_object):
        gmp = get_gmp(info)
        scanner_id = (
            str(input_object.scanner_id)
            if input_object.scanner_id is not None
            else None
        )
        name = input_object.name if input_object.name is not None else None
        comment = (
            input_object.comment if input_object.comment is not None else None
        )

        elem = gmp.create_config_from_osp_scanner(
            scanner_id=scanner_id, name=name, comment=comment
        )

        return CreateScanConfigFromOspScanner(
            id_of_created_config=elem.get('id')
        )


class ModifyScanConfigSetNameInput(graphene.InputObjectType):
    """Input object for ModifyScanConfigSetName
    Args:
        config_id (UUID): UUID of scan config to modify.
        name (str): New name for the config.
    """

    config_id = graphene.UUID(
        required=True, description="ID of scan config to modify.", name='id'
    )
    name = graphene.String(required=True, description="Name of a scan config.")


class ModifyScanConfigSetName(graphene.Mutation):
    """Modify the name of a scan config
    Args:
        input (ModifyScanConfigSetNameInput): Input object for
            ModifyScanConfigSetName.

    Example:

        .. code-block::

            mutation {
                modifyScanConfigSetName(input:{
                    id: "24f0ebae-fe78-4088-bc01-96bfb2eebe83",
                    name:"some_name"})
                {
                    ok
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "modifyScanConfigSetName": {
                        "ok": true
                    }
                }
            }
    """

    class Arguments:
        input_object = ModifyScanConfigSetNameInput(required=True, name='input')

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, input_object):
        config_id = (
            str(input_object.config_id)
            if input_object.config_id is not None
            else None
        )
        name = input_object.name if input_object.name is not None else None

        gmp = get_gmp(info)
        gmp.modify_config_set_name(config_id=config_id, name=name)

        return ModifyScanConfigSetName(ok=True)


class ModifyScanConfigSetCommentInput(graphene.InputObjectType):
    """Input object for ModifyScanConfigSetComment
    Args:
        config_id (UUID): UUID of scan config to modify.
        comment (str, optional): Comment to set on a config. Default: ‘’
    """

    config_id = graphene.UUID(
        required=True, description="ID of scan config to modify.", name='id'
    )
    comment = graphene.String(description="Comment of a scan config.")


class ModifyScanConfigSetComment(graphene.Mutation):
    """Modify comment of a scan config
    Args:
        input (ModifyScanConfigSetCommentInput): Input object for
            ModifyScanConfigSetComment.

    Example:

        .. code-block::

            mutation {
                modifyScanConfigSetComment(input:{
                    id: "24f0ebae-fe78-4088-bc01-96bfb2eebe83",
                    comment:"New 001"})
                {
                    ok
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "modifyScanConfigSetComment": {
                        "ok": true
                    }
                }
            }
    """

    class Arguments:
        input_object = ModifyScanConfigSetCommentInput(
            required=True, name='input'
        )

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, input_object):
        config_id = (
            str(input_object.config_id)
            if input_object.config_id is not None
            else None
        )
        comment = (
            input_object.comment if input_object.comment is not None else None
        )

        gmp = get_gmp(info)
        gmp.modify_config_set_comment(config_id=config_id, comment=comment)

        return ModifyScanConfigSetComment(ok=True)


class NvtFamilyInput(graphene.InputObjectType):
    """Input object for NVT families
    Args:
        name (str): Name of the NVT family to select.
        growing (bool): Whether new NVTs should be added to the
            NVT family automatically.
        all (bool): Whether to include all NVTs in this family.
    """

    name = graphene.String(
        required=True,
        description="Name of the NVT family to select",
    )
    growing = graphene.Boolean(
        required=True,
        description=(
            'Whether new NVTs should be added to the '
            'NVT family automatically.'
        ),
    )

    include_all = graphene.Boolean(
        name='all',
        required=True,
        description='Whether to include all NVTs in this family',
    )


class ModifyScanConfigSetFamilySelectionInput(graphene.InputObjectType):
    """Input object for ModifyScanConfigSetFamilySelection
    Args:
        config_id (UUID): UUID of scan config to modify.
        families (List[NvtFamilyInput], optional): A list of NVT family objects.
        auto_add_new_families (bool, optional): Whether new families should
            be added to the scan config automatically. Default: True.
    """

    config_id = graphene.UUID(
        required=True, description="ID of scan config to modify.", name='id'
    )
    families = graphene.List(
        NvtFamilyInput, description=" A list of NVT family objects."
    )
    auto_add_new_families = graphene.Boolean(
        description="Whether new families should be added to the scan "
        "config automatically."
    )


class ModifyScanConfigSetFamilySelection(graphene.Mutation):
    """Modify family selection of a scan config
    Args:
        input (ModifyScanConfigSetFamilySelectionInput): Input object for
            ModifyScanConfigSetFamilySelection.

    Example:

        .. code-block::

            mutation {
                modifyScanConfigSetFamilySelection(input:{
                    id: "24f0ebae-fe78-4088-bc01-96bfb2eebe83",
                    families:[
                        {name: "fam1", growing: true, all: 0},
                        {name: "fam2", growing: false, all: 1}
                    ],
                    autoAddNewFamilies: "true"}
                {
                    ok
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "modifyScanConfigSetFamilySelection": {
                        "ok": true
                    }
                }
            }
    """

    class Arguments:
        input_object = ModifyScanConfigSetFamilySelectionInput(
            required=True, name='input'
        )

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, input_object):
        config_id = (
            str(input_object.config_id)
            if input_object.config_id is not None
            else None
        )

        auto_add_new_families = (
            input_object.auto_add_new_families
            if input_object.auto_add_new_families is not None
            else None
        )

        if not input_object.families:
            families = None
        else:
            families = []
            for family in input_object.families:
                families.append(
                    (family.name, family.growing, family.include_all)
                )

        gmp = get_gmp(info)
        gmp.modify_config_set_family_selection(
            config_id=config_id,
            families=families,
            auto_add_new_families=auto_add_new_families,
        )

        return ModifyScanConfigSetFamilySelection(ok=True)


class ModifyScanConfigSetNvtPreferenceInput(graphene.InputObjectType):
    """Input object for ModifyScanConfigSetNvtPreference
    Args:
        config_id (UUID): UUID of scan config to modify.
        name (str): Name for preference to change.
            Name has the format "OID:id:type:name".
        nvt_oid (str): OID of the NVT associated with preference to modify.
        value (str, optional):  New value for the preference.
            None to delete the preference and to use the default instead.
    """

    config_id = graphene.UUID(
        required=True, description="ID of scan config to modify.", name='id'
    )
    name = graphene.String(
        required=True,
        description="Name for preference to change."
        "Name has the format \"OID:id:type:name\".",
    )
    nvt_oid = graphene.String(
        required=True,
        description="OID of the NVT associated with preference to modify",
    )
    value = graphene.String(
        description="New value for the preference."
        "None to delete the preference and to use the default instead."
    )


class ModifyScanConfigSetNvtPreference(graphene.Mutation):
    """Modify NVT preference of a scan config
    Args:
        input (ModifyScanConfigSetNvtPreferenceInput): Input object for
            ModifyScanConfigSetNvtPreference.

    Example:

        .. code-block::

            mutation {
                modifyScanConfigSetNvtPreference(input:{
                    id: "24f0ebae-fe78-4088-bc01-96bfb2eebe83",
                    name:"<OID>:<id>:<type>:name",
                    nvtOid: "1.3.6.1.4.1.25623.1.0.100315",
                    value: "yes"})
                {
                    ok
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "modifyScanConfigSetNvtPreference": {
                        "ok": true
                    }
                }
            }
    """

    class Arguments:
        input_object = ModifyScanConfigSetNvtPreferenceInput(
            required=True, name='input'
        )

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, input_object):
        config_id = (
            str(input_object.config_id)
            if input_object.config_id is not None
            else None
        )
        name = input_object.name if input_object.name is not None else None
        nvt_oid = (
            input_object.nvt_oid if input_object.nvt_oid is not None else None
        )
        value = input_object.value if input_object.value is not None else None

        gmp = get_gmp(info)
        gmp.modify_config_set_nvt_preference(
            config_id=config_id,
            name=name,
            nvt_oid=nvt_oid,
            value=value,
        )

        return ModifyScanConfigSetNvtPreference(ok=True)


class ModifyScanConfigSetNvtSelectionInput(graphene.InputObjectType):
    """Input object for ModifyScanConfigSetNvtSelection
    Args:
        config_id (UUID): UUID of scan config to modify.
        family (str): Name of the NVT family to include NVTs from.
        nvt_oids (List[str]): List of NVTs to select for the family.
    """

    config_id = graphene.UUID(
        required=True, description="ID of scan config to modify.", name='id'
    )
    family = graphene.String(
        required=True,
        description="Name of the NVT family to include NVTs from.",
    )
    nvt_oids = graphene.List(
        graphene.String,
        required=True,
        description="List of NVTs to select for the family.",
    )


class ModifyScanConfigSetNvtSelection(graphene.Mutation):
    """Modifies the selected nvts of an existing scan config.
        The manager updates the given family in the config to include only the
        given NVTs.

    Args:
        input (ModifyScanConfigSetNvtSelectionInput): Input object for
            ModifyScanConfigSetNvtSelection.

    Example:

        .. code-block::

            mutation {
                modifyScanConfigSetNvtSelection(input:{
                    id: "24f0ebae-fe78-4088-bc01-96bfb2eebe83",
                    name:"<OID>:<id>:<type>:name",
                    nvtOids: ["1.3.6.1.4.1.25623.1.0.100315"]
                    })
                {
                    ok
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "modifyScanConfigSetNvtSelection": {
                        "ok": true
                    }
                }
            }
    """

    class Arguments:
        input_object = ModifyScanConfigSetNvtSelectionInput(
            required=True, name='input'
        )

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, input_object):
        config_id = (
            str(input_object.config_id)
            if input_object.config_id is not None
            else None
        )
        family = (
            input_object.family if input_object.family is not None else None
        )
        nvt_oids = (
            input_object.nvt_oids if input_object.nvt_oids is not None else None
        )

        gmp = get_gmp(info)
        gmp.modify_config_set_nvt_selection(
            config_id=config_id, family=family, nvt_oids=nvt_oids
        )

        return ModifyScanConfigSetNvtSelection(ok=True)


class ModifyScanConfigSetScannerPreferenceInput(graphene.InputObjectType):
    """Input object for ModifyScanConfigSetScannerPreference

    Args:
        config_id (UUID): UUID of scan config to modify.
        name (str): Name of the scanner preference to change.
        value (str, optional): New value for the preference.
            None to delete the preference and to use the default instead.
    """

    config_id = graphene.UUID(
        required=True, description="ID of scan config to modify.", name='id'
    )
    name = graphene.String(
        required=True,
        description="Name of the scanner preference to change.",
    )
    value = graphene.String(
        description="New value for the preference."
        "None to delete the preference and to use the default instead."
    )


class ModifyScanConfigSetScannerPreference(graphene.Mutation):
    """Modifies the scanner preferences of an existing scan config

    Args:
        input (ModifyScanConfigSetScannerPreferenceInput): Input object for
            ModifyScanConfigSetScannerPreference.

    Example:

        .. code-block::

            mutation {
                modifyScanConfigSetScannerPreference(input:{
                    id: "24f0ebae-fe78-4088-bc01-96bfb2eebe83",
                    name:"scanner:scanner:scanner:log_whole_attack",
                    value: "1"})
                {
                    ok
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "modifyScanConfigSetScannerPreference": {
                        "ok": true
                    }
                }
            }
    """

    class Arguments:
        input_object = ModifyScanConfigSetScannerPreferenceInput(
            required=True, name='input'
        )

    ok = graphene.Boolean()

    @require_authentication
    def mutate(root, info, input_object):
        config_id = (
            str(input_object.config_id)
            if input_object.config_id is not None
            else None
        )
        name = input_object.name if input_object.name is not None else None
        value = input_object.value if input_object.value is not None else None

        gmp = get_gmp(info)
        gmp.modify_config_set_scanner_preference(
            config_id=config_id,
            name=name,
            value=value,
        )

        return ModifyScanConfigSetScannerPreference(ok=True)
