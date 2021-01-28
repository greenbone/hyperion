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

from uuid import uuid4

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class ModifyScanConfigSetNameTestCase(SeleneTestCase):
    def setUp(self):
        self.id1 = uuid4()
        self.name = 'some name'

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            f'''
            mutation {{
                modifyScanConfigSetName(input: {{
                    id: "{self.id1}",
                    name: "{self.name}"
                }}) {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_modify_scan_config_set_name(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'modify_config_set_name',
            '''
            <modify_config_response status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyScanConfigSetName(input: {{
                    id: "{self.id1}",
                    name: "{self.name}"
                }}) {{
                    ok
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['modifyScanConfigSetName']['ok']

        self.assertEqual(ok, True)

        mock_gmp.gmp_protocol.modify_config_set_name.assert_called_with(
            config_id=str(self.id1),
            name=self.name,
        )


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class ModifyScanConfigSetCommentTestCase(SeleneTestCase):
    def setUp(self):
        self.id1 = uuid4()
        self.comment1 = 'comment 1'

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            f'''
            mutation {{
                modifyScanConfigSetComment(input: {{
                    id: "{self.id1}",
                    comment: "{self.comment1}"
                }}) {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_modify_scan_config_set_comment(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'modify_config_set_comment',
            '''
            <modify_config_response status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyScanConfigSetComment(input: {{
                    id: "{self.id1}",
                    comment: "{self.comment1}"
                }}) {{
                    ok
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['modifyScanConfigSetComment']['ok']

        self.assertEqual(ok, True)

        mock_gmp.gmp_protocol.modify_config_set_comment.assert_called_with(
            config_id=str(self.id1),
            comment=self.comment1,
        )


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class ModifyScanConfigSetFamilySelectionTestCase(SeleneTestCase):
    def setUp(self):
        self.id1 = uuid4()

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            f'''
            mutation {{
                modifyScanConfigSetFamilySelection(input: {{
                    id: "{self.id1}",
                    families: [
                        {{name: "family1", growing: true, all: false}},
                        {{name: "family2", growing: false, all: true}}
                    ],
                }}) {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_modify_scan_config_set_family_selection(
        self, mock_gmp: GmpMockFactory
    ):
        mock_gmp.mock_response(
            'modify_config_set_family_selection',
            '''
            <modify_config_response status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyScanConfigSetFamilySelection(input: {{
                    id: "{self.id1}",
                    families: [
                        {{name: "family1", growing: true, all: false}},
                        {{name: "family2", growing: false, all: true}}
                    ],
                    autoAddNewFamilies: true,
                }}) {{
                    ok
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['modifyScanConfigSetFamilySelection']['ok']

        self.assertEqual(ok, True)

        # pylint: disable=line-too-long
        mock_gmp.gmp_protocol.modify_config_set_family_selection.assert_called_with(
            config_id=str(self.id1),
            families=[("family1", True, False), ("family2", False, True)],
            auto_add_new_families=True,
        )


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class ModifyScanConfigSetNvtPreferenceTestCase(SeleneTestCase):
    def setUp(self):
        self.id1 = uuid4()
        self.name = "1.3.6.1.4.1.25623.1.0.100315:1:checkbox:Do a TCP ping"

    def test_require_authentication1(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            f'''
            mutation {{
                modifyScanConfigSetNvtPreference(input:{{
                    id: "{self.id1}",
                    name:"Do an ICMP ping",
                    nvtOid: "1.3.6.1.4.1.25623.1.0.100315",
                    value: "yes"}})
                {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_modify_scan_config_set_nvt_prefernce(
        self, mock_gmp: GmpMockFactory
    ):
        mock_gmp.mock_response(
            'modify_config_set_nvt_preference',
            '''
            <modify_config_response status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyScanConfigSetNvtPreference(input:{{
                    id: "{self.id1}",
                    name: "{self.name}",
                    nvtOid: "1.3.6.1.4.1.25623.1.0.100315",
                    value: "yes"}})
                {{
                    ok
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['modifyScanConfigSetNvtPreference']['ok']

        self.assertEqual(ok, True)

        # pylint: disable=line-too-long
        mock_gmp.gmp_protocol.modify_config_set_nvt_preference.assert_called_with(
            config_id=str(self.id1),
            name=self.name,
            nvt_oid="1.3.6.1.4.1.25623.1.0.100315",
            value="yes",
        )


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class ModifyScanConfigSetNvtSelectionTestCase(SeleneTestCase):
    def setUp(self):
        self.id1 = uuid4()
        self.nvt_oid = "1.3.6.1.4.1.25623.1.0.100315"
        self.family = "Some NVT Family"

    def test_require_authentication1(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            f'''
            mutation {{
                modifyScanConfigSetNvtSelection(input:{{
                    id: "{self.id1}",
                    family:"{self.family}",
                    nvtOids: ["{self.nvt_oid}"]}})
                {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_modify_scan_config_set_nvt_selection(
        self, mock_gmp: GmpMockFactory
    ):
        mock_gmp.mock_response(
            'modify_config_set_nvt_selection',
            '''
            <modify_config_response status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyScanConfigSetNvtSelection(input:{{
                    id: "{self.id1}",
                    family:"{self.family}",
                    nvtOids: ["{self.nvt_oid}"]}})
                {{
                    ok
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['modifyScanConfigSetNvtSelection']['ok']

        self.assertEqual(ok, True)

        # pylint: disable=line-too-long
        mock_gmp.gmp_protocol.modify_config_set_nvt_selection.assert_called_with(
            config_id=str(self.id1),
            family=self.family,
            nvt_oids=[self.nvt_oid],
        )


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class ModifyScanConfigSetScannerPreferenceTestCase(SeleneTestCase):
    def setUp(self):
        self.id1 = uuid4()
        self.name = "scanner:scanner:scanner:optimize_test"
        self.value = "1"

    def test_require_authentication1(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            f'''
            mutation {{
                modifyScanConfigSetScannerPreference(input:{{
                    id: "{self.id1}",
                    name:"{self.name}",
                    value: "{self.value}"}})
                {{
                    ok
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_modify_scan_config_set_scanner_prefernce(
        self, mock_gmp: GmpMockFactory
    ):
        mock_gmp.mock_response(
            'modify_config_set_scanner_preference',
            '''
            <modify_config_response status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            mutation {{
                modifyScanConfigSetScannerPreference(input:{{
                    id: "{self.id1}",
                    name:"{self.name}",
                    value: "{self.value}"}})
                {{
                    ok
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['modifyScanConfigSetScannerPreference']['ok']

        self.assertEqual(ok, True)

        # pylint: disable=line-too-long
        mock_gmp.gmp_protocol.modify_config_set_scanner_preference.assert_called_with(
            config_id=str(self.id1),
            name=self.name,
            value=self.value,
        )
