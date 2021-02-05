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

from pathlib import Path
from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory

# from selene.tests.entity import make_test_get_entity

CWD = Path(__file__).absolute().parent


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class OverrideTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                override(id: "08b69003-5fc2-4037-a479-93b440211c73") {
                    id
                    text
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_query_name_in_override(self, _mock_gmp: GmpMockFactory):

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                override(id: "08b69003-5fc2-4037-a479-93b440211c73") {
                    id
                    name
                }
            }
            '''
        )

        self.assertResponseHasErrorMessage(
            response, 'Cannot query field "name" on type "Override".'
        )

    def test_get_override(self, mock_gmp: GmpMockFactory):
        override_xml_path = CWD / 'example-override.xml'
        override_xml_str = override_xml_path.read_text()

        mock_gmp.mock_response('get_override', override_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                override(id: "08b69003-5fc2-4037-a479-93b440211c73") {
                    id
                    text
                    owner
                    creationTime
                    modificationTime
                    writable
                    inUse
                    active
                    orphan
                    hosts
                    severity
                    newSeverity
                    endTime
                    nvt {
                        id
                        name
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        override = json['data']['override']

        self.assertEqual(override['id'], '5221d57f-3e62-4114-8e19-135a79b6b102')
        self.assertEqual(override['text'], 'sdr')
        self.assertEqual(override['owner'], 'admin')
        self.assertEqual(override['endTime'], '2021-03-07T13:32:36+01:00')
        self.assertEqual(override['writable'], True)
        self.assertEqual(override['inUse'], False)
        self.assertEqual(override['active'], True)
        self.assertEqual(override['orphan'], False)
        self.assertListEqual(override['hosts'], ['127.0.01.1'])
        self.assertEqual(override['severity'], None)
        self.assertEqual(override['newSeverity'], -1)

    def test_get_override_with_no_hosts(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_override',
            '''
            <get_override_response>
                <override id="08b69003-5fc2-4037-a479-93b440211c73">
                    <text>Han shot first</text>
                    <owner><name>Han</name></owner>
                    <creation_time>2020-06-30T09:16:25Z</creation_time>
                    <modification_time>2020-07-30T09:16:25Z</modification_time>
                    <writable>1</writable>
                    <in_use>1</in_use>
                    <active>1</active>
                    <orphan>0</orphan>
                    <nvt><name>Greedo</name></nvt>
                    <severity>5.5</severity>
                    <new_severity>10</new_severity>
                </override>
            </get_override_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                override(id: "08b69003-5fc2-4037-a479-93b440211c73") {
                    hosts
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        override = json['data']['override']

        self.assertListEqual(override['hosts'], [])


class OverrideGetEntityTestCase(SeleneTestCase):
    gmp_name = 'override'
    # test_get_entity = make_test_get_entity(
    #     gmp_name,
    # )
