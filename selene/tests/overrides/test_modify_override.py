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

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class OverrideTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            mutation {
                modifyOverride (input: {
                                    id: "e1438fb2-ab2c-4f4a-ad6b-de97005256e8"
                                    newSeverity: 5.0,
                                    text: "Test Override"}) {
                    ok
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_modify_override(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'modify_override',
            '''
            <modify_override_response status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            mutation {
                modifyOverride (input: {
                                    id: "e1438fb2-ab2c-4f4a-ad6b-de97005256e8",
                                    daysActive: 2,
                                    hosts: ["127.0.0.1"],
                                    newSeverity: 5.0,
                                    port: "general/tcp",
                                    resultId:
                                      "74555f56-6d00-47c2-b229-54bdf8c3fe9e",
                                    severity: 0.0,
                                    taskId:
                                      "c05a764c-bea6-4555-b24e-fbd9c741501c",
                                    text: "Test Override"}) {
                    ok
                }
            }
            '''
        )

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_override.assert_called_with(
            "e1438fb2-ab2c-4f4a-ad6b-de97005256e8",
            "Test Override",
            days_active=2,
            hosts=["127.0.0.1"],
            port="general/tcp",
            result_id="74555f56-6d00-47c2-b229-54bdf8c3fe9e",
            severity=0.0,
            new_severity=5.0,
            task_id="c05a764c-bea6-4555-b24e-fbd9c741501c",
        )

    def test_modify_override_minimal(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'modify_override',
            '''
            <modify_override_response status="200" status_text="OK"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            mutation {
                modifyOverride (input: {
                    id: "e1438fb2-ab2c-4f4a-ad6b-de97005256e8",
                    text: "Test Override",
                    newSeverity: 5.0
                }) {
                    ok
                }
            }
            '''
        )

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.modify_override.assert_called_with(
            "e1438fb2-ab2c-4f4a-ad6b-de97005256e8",
            "Test Override",
            days_active=None,
            hosts=None,
            new_severity=5.0,
            port=None,
            result_id=None,
            severity=None,
            task_id=None,
        )
