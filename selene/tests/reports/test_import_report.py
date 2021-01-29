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
class ImportReportTestCase(SeleneTestCase):
    def setUp(self):
        self.qu = f'''
            mutation {{
                importReport(
                    report: "<report id=&quot;f0fdf522-276d-4893-9274-fb8699dc2270&quot;/>",
                    taskId: "{uuid4()}",
                    inAssets: "False"
                ) {{
                    id
                }}
            }}
        '''

    def test_report_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(self.qu)

        self.assertResponseAuthenticationRequired(response)

    def test_import_report(self, mock_gmp: GmpMockFactory):
        report_id = "f0fdf522-276d-4893-9274-fb8699dc2270"
        mock_gmp.mock_response(
            'import_report', f'<create_report_response id="{report_id}"/>'
        )

        self.login('foo', 'bar')

        response = self.query(self.qu)

        json = response.json()

        self.assertResponseNoErrors(response)

        received_report_id = json['data']['importReport']['id']

        self.assertEqual(report_id, received_report_id)
