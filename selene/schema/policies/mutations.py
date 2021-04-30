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

from selene.schema.scan_configs.mutations import NvtFamilyInput


class DeletePolicy(graphene.Mutation):
    """Deletes a policy

    Args:
        id (UUID): UUID of policy to delete.

    Returns:
        ok (Boolean)

    Example

        mutation {
            deletePolicy(id: "5f8e7b31-35ea-4b43-9797-6d77f058906b",
                         ultimate: false)
            {
                ok
            }
        }

        Response
        {
            "data": {
                "deletePolicy": {
                    "ok": true
                }
            }
        }
    """

    class Arguments:
        policy_id = graphene.UUID(required=True, name='id')
        ultimate = graphene.Boolean(required=False)

    ok = graphene.Boolean()

    @staticmethod
    @require_authentication
    def mutate(_root, info, policy_id, ultimate):
        gmp = get_gmp(info)
        gmp.delete_policy(str(policy_id), ultimate=ultimate)
        return DeletePolicy(ok=True)


# Explicit classes needed, else we get error
# 'AssertionError: Found different types with the same name in the
#   schema: DeleteByIds, DeleteByIds.'


DeleteByIdsClass = create_delete_by_ids_mutation(
    'policy', entities_name='policies', gmp_entity_response='config'
)


class DeletePoliciesByIds(DeleteByIdsClass):
    """Deletes a list of policys

    Args:
        ids (List(UUID)): List of UUIDs of policys to delete.
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.

    Returns:
        ok (Boolean)

    Example

        mutation {
            deletePoliciesByIds(
                ids: ["5f8e7b31-35ea-4b43-9797-6d77f058906b"],
                ultimate: false)
            {
                ok
            }
        }

        Response
        {
            "data": {
                "deletePoliciesByIds": {
                    "ok": true
                }
            }
        }
    """


DeleteByFilterClass = create_delete_by_filter_mutation(
    'policy', entities_name='policies', gmp_entity_response='config'
)


class DeletePoliciesByFilter(DeleteByFilterClass):
    """Deletes a filtered list of policys

    Args:
        filterString (str): Filter string for policy list to delete.
        ultimate (bool, optional): Whether to remove entirely, or to the
            trashcan.

    Returns:
        ok (Boolean)

    Example

        mutation {
            deletePolicyByFilter(
                filterString:"name~Clone",
                ultimate: false)
            {
                ok
            }
        }

        Response
        {
            "data": {
                "deletePolicyByFilter": {
                    "ok": true
                }
            }
        }
    """


class ClonePolicy(graphene.Mutation):
    """Clone a policy

    Args:
        id (UUID): UUID of policy to clone.

    Example:

        .. code-block::

            mutation {
                clonePolicy(
                    id: "b992601e-e0df-4078-b4b1-39e04f92f4cc",
                ) {
                    id
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "clonePolicy": {
                    "id": "a569f3df-0f8d-4001-aeef-08cdee0cdf49"
                    }
                }
            }
    """

    class Arguments:
        policy_id = graphene.UUID(required=True, name='id')

    policy_id = graphene.UUID(name='id')

    @staticmethod
    @require_authentication
    def mutate(_root, info, policy_id):
        gmp = get_gmp(info)
        elem = gmp.clone_policy(str(policy_id))
        return ClonePolicy(policy_id=elem.get('id'))


# Explicit classes needed, else we get error
# 'AssertionError: Found different types with the same name in the
#   schema: ExportByIds, ExportByIds.'

ExportByIdsClass = create_export_by_ids_mutation(
    'policy', with_details=True, entities_name='policies'
)


class ExportPoliciesByIds(ExportByIdsClass):
    pass


ExportByFilterClass = create_export_by_filter_mutation(
    'policy', with_details=True, entities_name='policies'
)


class ExportPoliciesByFilter(ExportByFilterClass):
    pass


class ImportPolicy(graphene.Mutation):
    """Import a policy

    Args:
        policy (str) : Policy XML as string to import. This XML must
            contain a <get_configs_response> root element.

    Example:

        .. code-block::

            mutation {
                importPolicy(
                    policy: "<get_configs_response status=\"200\".......",
                ) {
                    id
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "importPolicy": {
                        "id": "f7213438-ca44-4dc0-93d7-24bc20c4cf94"
                    }
                }
            }
    """

    class Arguments:
        policy = graphene.String()

    policy_id = graphene.UUID(name='id')

    @staticmethod
    @require_authentication
    def mutate(_root, info, policy):
        gmp = get_gmp(info)
        elem = gmp.import_config(config=policy)

        return ImportPolicy(policy_id=elem.get('id'))


class CreatePolicyInput(graphene.InputObjectType):
    """Input Object for CreatePolicy
    Args:
        policy_id (UUID): UUID of policy to clone.
        name (str): Name of the new policy
        comment (str): A comment on the policy
    """

    policy_id = graphene.UUID(
        required=True, description="UUID of policy to clone."
    )
    name = graphene.String(required=True, description="Name of the new policy.")
    comment = graphene.String(description="A comment on the policy.")


class CreatePolicy(graphene.Mutation):
    """Create a policy.

    Args:
        Input (CreatePolicyInput): input object for CreatePolicy

    Example:

        .. code-block::

            mutation {
                createPolicy( input" {
                    policyId: "085569ce-73ed-11df-83c3-002264764cea",
                    name: "Name of new policy",
                    comment: "Comment on the policy"}
                ) {
                    id
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "createPolicy": {
                        "id": "a569f3df-0f8d-4001-aeef-08cdee0cdf49"
                    }
                }
            }
    """

    class Arguments:
        input_object = CreatePolicyInput(required=True, name='input')

    id_of_created_policy = graphene.String(name='id')

    @staticmethod
    @require_authentication
    def mutate(_root, info, input_object):
        gmp = get_gmp(info)
        policy_id = (
            str(input_object.policy_id)
            if input_object.policy_id is not None
            else None
        )
        name = input_object.name if input_object.name is not None else None
        comment = (
            input_object.comment if input_object.comment is not None else None
        )

        elem = gmp.create_policy(
            policy_id=policy_id, name=name, comment=comment
        )

        return CreatePolicy(id_of_created_policy=elem.get('id'))


class ModifyPolicySetNameInput(graphene.InputObjectType):
    """Input object for ModifyPolicySetName
    Args:
        policy_id (UUID): UUID of policy to modify.
        name (str): New name for the policy.
    """

    policy_id = graphene.UUID(
        required=True, description="ID of policy to modify.", name='id'
    )
    name = graphene.String(required=True, description="Name of a policy.")


class ModifyPolicySetName(graphene.Mutation):
    """Modify the name of a policy
    Args:
        input (ModifyPolicySetNameInput): Input object for
            ModifyPolicySetName.

    Example:

        .. code-block::

            mutation {
                modifyPolicySetName(input:{
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
                    "modifyPolicySetName": {
                        "ok": true
                    }
                }
            }
    """

    class Arguments:
        input_object = ModifyPolicySetNameInput(required=True, name='input')

    ok = graphene.Boolean()

    @staticmethod
    @require_authentication
    def mutate(_root, info, input_object):
        policy_id = (
            str(input_object.policy_id)
            if input_object.policy_id is not None
            else None
        )
        name = input_object.name if input_object.name is not None else None

        gmp = get_gmp(info)
        gmp.modify_policy_set_name(policy_id=policy_id, name=name)

        return ModifyPolicySetName(ok=True)


class ModifyPolicySetCommentInput(graphene.InputObjectType):
    """Input object for ModifyPolicySetComment
    Args:
        policy_id (UUID): UUID of policy to modify.
        comment (str, optional): Comment to set on a policy. Default: ‘’
    """

    policy_id = graphene.UUID(
        required=True, description="ID of policy to modify.", name='id'
    )
    comment = graphene.String(description="Comment of a policy.")


class ModifyPolicySetComment(graphene.Mutation):
    """Modify comment of a policy
    Args:
        input (ModifyPolicySetCommentInput): Input object for
            ModifyPolicySetComment.

    Example:

        .. code-block::

            mutation {
                modifyPolicySetComment(input:{
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
                    "modifyPolicySetComment": {
                        "ok": true
                    }
                }
            }
    """

    class Arguments:
        input_object = ModifyPolicySetCommentInput(required=True, name='input')

    ok = graphene.Boolean()

    @staticmethod
    @require_authentication
    def mutate(_root, info, input_object):
        policy_id = (
            str(input_object.policy_id)
            if input_object.policy_id is not None
            else None
        )
        comment = (
            input_object.comment if input_object.comment is not None else None
        )

        gmp = get_gmp(info)
        gmp.modify_policy_set_comment(policy_id=policy_id, comment=comment)

        return ModifyPolicySetComment(ok=True)


class ModifyPolicySetFamilySelectionInput(graphene.InputObjectType):
    """Input object for ModifyPolicySetFamilySelection
    Args:
        policy_id (UUID): UUID of policy to modify.
        families (List[NvtFamilyInput], optional): A list of NVT family objects.
        auto_add_new_families (bool, optional): Whether new families should
            be added to the policy automatically. Default: True.
    """

    policy_id = graphene.UUID(
        required=True, description="ID of policy to modify.", name='id'
    )
    families = graphene.List(
        NvtFamilyInput, description=" A list of NVT family objects."
    )
    auto_add_new_families = graphene.Boolean(
        description="Whether new families should be added to the policy "
        "config automatically."
    )


class ModifyPolicySetFamilySelection(graphene.Mutation):
    """Modify family selection of a policy
    Args:
        input (ModifyPolicySetFamilySelectionInput): Input object for
            ModifyPolicySetFamilySelection.

    Example:

        .. code-block::

            mutation {
                modifyPolicySetFamilySelection(input:{
                    id: "24f0ebae-fe78-4088-bc01-96bfb2eebe83",
                    families:[
                        {name: "fam1", growing: true, all: 0},
                        {name: "fam2", growing: false, all: 1}
                    ],
                    autoAddNewFamilies: "true"}),
                {
                    ok
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "modifyPolicySetFamilySelection": {
                        "ok": true
                    }
                }
            }
    """

    class Arguments:
        input_object = ModifyPolicySetFamilySelectionInput(
            required=True, name='input'
        )

    ok = graphene.Boolean()

    @staticmethod
    @require_authentication
    def mutate(_root, info, input_object):
        policy_id = (
            str(input_object.policy_id)
            if input_object.policy_id is not None
            else None
        )
        families = (
            input_object.families if input_object.families is not None else None
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
        gmp.modify_policy_set_family_selection(
            policy_id=policy_id,
            families=families,
            auto_add_new_families=auto_add_new_families,
        )

        return ModifyPolicySetFamilySelection(ok=True)


class ModifyPolicySetNvtPreferenceInput(graphene.InputObjectType):
    """Input object for ModifyPolicySetNvtPreference
    Args:
        policy_id (UUID): UUID of policy to modify.
        name (str): Name for preference to change.
            Name has the format "OID:id:type:name".
        nvt_oid (str): OID of the NVT associated with preference to modify.
        value (str, optional):  New value for the preference.
            None to delete the preference and to use the default instead.
    """

    policy_id = graphene.UUID(
        required=True, description="ID of policy to modify.", name='id'
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


class ModifyPolicySetNvtPreference(graphene.Mutation):
    """Modify NVT preference of a policy
    Args:
        input (ModifyPolicySetNvtPreferenceInput): Input object for
            ModifyPolicySetNvtPreference.

    Example:

        .. code-block::

            mutation {
                modifyPolicySetNvtPreference(input:{
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
                    "modifyPolicySetNvtPreference": {
                        "ok": true
                    }
                }
            }
    """

    class Arguments:
        input_object = ModifyPolicySetNvtPreferenceInput(
            required=True, name='input'
        )

    ok = graphene.Boolean()

    @staticmethod
    @require_authentication
    def mutate(_root, info, input_object):
        policy_id = (
            str(input_object.policy_id)
            if input_object.policy_id is not None
            else None
        )
        name = input_object.name if input_object.name is not None else None
        nvt_oid = (
            input_object.nvt_oid if input_object.nvt_oid is not None else None
        )
        value = input_object.value if input_object.value is not None else None

        gmp = get_gmp(info)
        gmp.modify_policy_set_nvt_preference(
            policy_id=policy_id, name=name, nvt_oid=nvt_oid, value=value
        )

        return ModifyPolicySetNvtPreference(ok=True)


class ModifyPolicySetNvtSelectionInput(graphene.InputObjectType):
    """Input object for ModifyPolicySetNvtSelection
    Args:
        policy_id (UUID): UUID of policy to modify.
        family (str): Name of the NVT family to include NVTs from.
        nvt_oids (List[str]): List of NVTs to select for the family.
    """

    policy_id = graphene.UUID(
        required=True, description="ID of policy to modify.", name='id'
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


class ModifyPolicySetNvtSelection(graphene.Mutation):
    """Modifies the selected nvts of an existing policy.
        The manager updates the given family in the config to include only the
        given NVTs.

    Args:
        input (ModifyPolicySetNvtSelectionInput): Input object for
            ModifyPolicySetNvtSelection.

    Example:

        .. code-block::

            mutation {
                modifyPolicySetNvtSelection(input:{
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
                    "modifyPolicySetNvtSelection": {
                        "ok": true
                    }
                }
            }
    """

    class Arguments:
        input_object = ModifyPolicySetNvtSelectionInput(
            required=True, name='input'
        )

    ok = graphene.Boolean()

    @staticmethod
    @require_authentication
    def mutate(_root, info, input_object):
        policy_id = (
            str(input_object.policy_id)
            if input_object.policy_id is not None
            else None
        )
        family = (
            input_object.family if input_object.family is not None else None
        )
        nvt_oids = (
            input_object.nvt_oids if input_object.nvt_oids is not None else None
        )

        gmp = get_gmp(info)
        gmp.modify_policy_set_nvt_selection(
            policy_id=policy_id, family=family, nvt_oids=nvt_oids
        )

        return ModifyPolicySetNvtSelection(ok=True)


class ModifyPolicySetScannerPreferenceInput(graphene.InputObjectType):
    """Input object for ModifyPolicySetScannerPreference

    Args:
        policy_id (UUID): UUID of policy to modify.
        name (str): Name of the scanner preference to change.
        value (str, optional): New value for the preference.
            None to delete the preference and to use the default instead.
    """

    policy_id = graphene.UUID(
        required=True, description="ID of policy to modify.", name='id'
    )
    name = graphene.String(
        required=True, description="Name of the scanner preference to change."
    )
    value = graphene.String(
        description="New value for the preference."
        "None to delete the preference and to use the default instead."
    )


class ModifyPolicySetScannerPreference(graphene.Mutation):
    """Modifies the scanner preferences of an existing policy

    Args:
        input (ModifyPolicySetScannerPreferenceInput): Input object for
            ModifyPolicySetScannerPreference.

    Example:

        .. code-block::

            mutation {
                modifyPolicySetScannerPreference(input:{
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
        input_object = ModifyPolicySetScannerPreferenceInput(
            required=True, name='input'
        )

    ok = graphene.Boolean()

    @staticmethod
    @require_authentication
    def mutate(_root, info, input_object):
        policy_id = (
            str(input_object.policy_id)
            if input_object.policy_id is not None
            else None
        )
        name = input_object.name if input_object.name is not None else None
        value = input_object.value if input_object.value is not None else None

        gmp = get_gmp(info)
        gmp.modify_policy_set_scanner_preference(
            policy_id=policy_id, name=name, value=value
        )

        return ModifyPolicySetScannerPreference(ok=True)
