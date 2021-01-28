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
class ModifyReportFormatTestCase(SeleneTestCase):
    def setUp(self):

        self.report_format_id = str(uuid4())

    def test_report_require_authentication(self, _mock_gmp: GmpMockFactory):
        query = f'''
            mutation {{
                modifyReportFormat(input: {{
                    id: "{self.report_format_id}",
                }}) {{
                    ok
                }}
            }}
        '''
        response = self.query(query)

        self.assertResponseAuthenticationRequired(response)

    def test_modify_report_format(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'modify_report_format',
            f'<modify_report_format_response id="{self.report_format_id}"/>',
        )
        query = f'''
            mutation {{
                modifyReportFormat(input: {{
                    id: "{self.report_format_id}",
                    name: "foo",
                    summary: "SomeFancySummary",
                }}) {{
                    ok
                }}
            }}
        '''
        self.login('foo', 'bar')

        response = self.query(query)

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['modifyReportFormat']['ok']

        self.assertEqual(ok, True)

        mock_gmp.gmp_protocol.modify_report_format.assert_called_with(
            str(self.report_format_id),
            active=None,
            name='foo',
            summary="SomeFancySummary",
            param_name=None,
            param_value=None,
        )
