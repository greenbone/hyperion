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
class CapabilitiesTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                capabilities
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_capabilities(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'help',
            '''
            <help_response status="200" status_text="OK">
                <schema format="XML" extension="xml" content_type="text/xml">
                    <command>
                        <name>AUTHENTICATE</name>
                        <summary>Authenticate with the manager.</summary>
                    </command>
                    <command>
                        <name>COMMANDS</name>
                        <summary>Run a list of commands.</summary>
                    </command>
                    <command>
                        <name>CREATE_AGENT</name>
                        <summary>Create an agent.</summary>
                    </command>
                </schema>
            </help_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                capabilities
            }
            '''
        )

        json = response.json()

        caps = json['data']['capabilities']

        self.assertEqual(type(caps), list)
        self.assertEqual(len(caps), 3)

        self.assertEqual(caps[0], 'AUTHENTICATE')
        self.assertEqual(caps[1], 'COMMANDS')
        self.assertEqual(caps[2], 'CREATE_AGENT')
