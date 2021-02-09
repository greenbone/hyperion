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

from uuid import uuid4

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class ExportAuditsByFilterTestCase(SeleneTestCase):
    def setUp(self):
        self.id1 = uuid4()
        self.id2 = uuid4()

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            f'''
            mutation {{
                exportAuditsByIds(ids: ["{self.id1}", "{self.id2}"]) {{
                   exportedEntities
                }}
            }}
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_export_audits_by_ids(self, mock_gmp: GmpMockFactory):
        self.login('foo', 'bar')

        mock_xml = (
            '<get_tasks_response status="200" status_text="OK">'
            f'<apply_overrides>0</apply_overrides><task id="{self.id1}">'
            f'<name>Foo Clone 1</name></task><task id="{self.id2}">'
            '<name>Foo Clone 2</name></task></get_tasks_response>'
        )

        mock_gmp.mock_response('get_audits', bytes(mock_xml, 'utf-8'))

        response = self.query(
            f'''
            mutation {{
                exportAuditsByIds(ids: ["{self.id1}", "{self.id2}"]) {{
                   exportedEntities
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        xml = json['data']['exportAuditsByIds']['exportedEntities']

        self.assertEqual(mock_xml, xml)
        mock_gmp.gmp_protocol.get_audits.assert_called_with(
            filter=f'uuid={self.id1} uuid={self.id2} ', details=True
        )

    def test_export_empty_ids_array(self, mock_gmp: GmpMockFactory):
        self.login('foo', 'bar')

        mock_xml = (
            "<get_tasks_response status=\"200\" status_text=\"OK\">"
            "<apply_overrides>0</apply_overrides><filters id=\"\">"
            "<term>uuid= first=1 rows=10 sort=name</term>"
            "<keywords><keyword><column>uuid</column><relation>=</relation>"
            "<value /></keyword></keywords></filters></get_tasks_response>"
        )

        mock_gmp.mock_response('get_audits', bytes(mock_xml, 'utf-8'))

        response = self.query(
            '''
            mutation {
                exportAuditsByIds(ids: []) {
                   exportedEntities
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        xml = json['data']['exportAuditsByIds']['exportedEntities']

        self.assertEqual(mock_xml, xml)

        mock_gmp.gmp_protocol.get_audits.assert_called_with(
            filter='', details=True
        )
