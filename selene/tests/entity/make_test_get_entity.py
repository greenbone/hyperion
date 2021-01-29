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

import unittest

from selene.tests import GmpMockFactory

from selene.tests.utils.utils import return_gmp_methods


def compose_mock_response(entity_name):
    xml_response = f'''
        <get_{entity_name}_response>
                <{entity_name} id="08b69003-5fc2-4037-a479-93b440211c73">
                    <owner>
                        <name>admin</name>
                    </owner>
                    <name>foo</name>
                    <comment>bar</comment>
                    <creation_time>2019-07-19T13:33:21Z</creation_time>
                    <modification_time>2019-07-19T13:33:21Z</modification_time>
                    <writable>1</writable>
                    <in_use>1</in_use>
                    <permissions>
                        <permission>
                            <name>Everything</name>
                        </permission>
                    </permissions>
                    <user_tags>
                        <count>2</count>
                        <tag id="480cdbd9-1af2-4be6-a195-163748b80381">
                            <name>test tag 1</name>
                            <value/>
                            <comment/>
                        </tag>
                        <tag id="82a7864f-b9ab-4063-9153-c84e37e5c213">
                            <name>test tag 2</name>
                            <value/>
                            <comment/>
                        </tag>
                    </user_tags>
                </{entity_name}>
            </get_{entity_name}_response>
    '''
    return xml_response


def compose_mock_query(entity_name):
    query = f'''
            query {{
                {entity_name} (
                    id: "08b69003-5fc2-4037-a479-93b440211c73"
                ) {{
                    id
                    name
                    comment
                    owner
                    creationTime
                    modificationTime
                    writable
                    inUse
                    permissions {{
                        name
                    }}
                    userTags {{
                        count
                        tags {{
                            name
                            id
                            value
                            comment
                        }}
                    }}
                }}
            }}
            '''
    return query


def make_test_get_entity(
    gmp_name: str, *, selene_name: str = None, gmp_cmd: str = None, **kwargs
):

    if not selene_name:
        selene_name = gmp_name

    # for special gmp commands like "get_info_list"
    if not gmp_cmd:
        gmp_cmd = 'get_' + gmp_name

    @unittest.mock.patch('selene.views.Gmp', new_callable=GmpMockFactory)
    def test(self, mock_gmp: GmpMockFactory):

        gmp_commands = return_gmp_methods(mock_gmp.gmp_protocol)

        mock_gmp.mock_response(gmp_cmd, compose_mock_response(gmp_name))

        self.login('foo', 'bar')

        response = self.query(compose_mock_query(selene_name))

        json = response.json()

        self.assertResponseNoErrors(response)

        get_entity = gmp_commands[gmp_cmd]

        get_entity.assert_called_with(
            "08b69003-5fc2-4037-a479-93b440211c73", **kwargs
        )

        entity = json['data'][selene_name]

        self.assertEqual(entity['id'], '08b69003-5fc2-4037-a479-93b440211c73')
        self.assertEqual(entity['name'], 'foo')
        self.assertEqual(entity['comment'], "bar")
        self.assertEqual(entity['owner'], 'admin')

        self.assertEqual(entity['creationTime'], '2019-07-19T13:33:21+00:00')
        self.assertEqual(
            entity['modificationTime'], '2019-07-19T13:33:21+00:00'
        )

        self.assertTrue(entity['inUse'])
        self.assertTrue(entity['writable'])

        permissions = entity['permissions']
        self.assertEqual(len(permissions), 1)
        self.assertEqual(permissions[0]['name'], 'Everything')

        user_tags = entity['userTags']

        self.assertEqual(user_tags['count'], 2)

        tags = user_tags['tags']

        self.assertEqual(len(tags), 2)

        tag1 = tags[0]

        self.assertEqual(tag1['name'], 'test tag 1')
        self.assertEqual(tag1['id'], '480cdbd9-1af2-4be6-a195-163748b80381')
        self.assertIsNone(tag1['value'])
        self.assertIsNone(tag1['comment'])

    return test
