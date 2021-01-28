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

from unittest.mock import patch

from gvm.protocols.latest import get_filter_type_from_string

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class FilterTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            mutation {
                createFilter (
                    input: {
                        name: "lol"
                    }
                ) {
                    id
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_create_filter(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'create_filter',
            '''
            <create_filter_response status="201" status_text="OK,
            resource created" id="e1438fb2-ab2c-4f4a-ad6b-de97005256e8"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            mutation {
                createFilter (
                    input: {
                        term: "foo bar"
                        type: ALERT
                        comment: "moo"
                        name: "phew"
                    }
                ) {
                    id
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        filter_id = json['data']['createFilter']['id']
        self.assertEqual(filter_id, 'e1438fb2-ab2c-4f4a-ad6b-de97005256e8')

        mock_gmp.gmp_protocol.create_filter.assert_called_with(
            name="phew",
            term="foo bar",
            filter_type=get_filter_type_from_string('alert'),
            comment="moo",
        )

    def test_create_filter_minimal(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'create_filter',
            '''
            <create_filter_response status="201" status_text="OK,
            resource created" id="e1438fb2-ab2c-4f4a-ad6b-de97005256e8"/>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            mutation {
                createFilter (
                    input: {
                        name: "lol"
                    }
                ) {
                    id
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        filter_id = json['data']['createFilter']['id']
        self.assertEqual(filter_id, 'e1438fb2-ab2c-4f4a-ad6b-de97005256e8')
        mock_gmp.gmp_protocol.create_filter.assert_called_with(
            name="lol",
            term=None,
            filter_type=None,
            comment=None,
        )
