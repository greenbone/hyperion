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

import unittest

from selene.tests import GmpMockFactory

from selene.tests.utils.utils import (
    compose_mock_command,
    pluralize_name,
    return_gmp_methods,
)


def compose_mock_response(gmp_name):
    gmp_plural = pluralize_name(gmp_name)
    xml_response = f'''
        <get_{gmp_plural}_response>
                <{gmp_name} id="08b69003-5fc2-4037-a479-93b440211c73">
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
                </{gmp_name}>
                <{gmp_name} id="6b2db524-9fb0-45b8-9b56-d958f84cb546">
                    <owner>
                        <name>admin</name>
                    </owner>
                    <name>lorem</name>
                    <comment>ipsum</comment>
                    <creation_time>2019-07-19T13:33:21Z</creation_time>
                    <modification_time>2019-07-19T13:33:21Z</modification_time>
                    <writable>1</writable>
                    <in_use>0</in_use>
                    <permissions>
                        <permission>
                            <name>{gmp_name}</name>
                        </permission>
                        <permission>
                            <name>{gmp_name}</name>
                        </permission>
                    </permissions>
                </{gmp_name}>
            </get_{gmp_plural}_response>
    '''
    return xml_response


def compose_mock_query(entity_plural):
    query = f'''
            query {{
                {entity_plural} (
                    filterString: "lorem",
                ) {{
                    nodes {{
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
            }}
            '''
    return query


def make_test_get_entities(
    gmp_name: str,
    *,
    selene_name: str = None,
    gmp_cmd: str = None,
    plural_selene_name: str = None,
    **kwargs,
):
    if not selene_name:
        selene_name = gmp_name

    # for special gmp commands like "get_info_list"
    if not gmp_cmd:
        gmp_cmd = compose_mock_command(gmp_name)

    # for special plurals of irregulars like policy
    if not plural_selene_name:
        plural_selene_name = pluralize_name(selene_name)

    @unittest.mock.patch('selene.views.Gmp', new_callable=GmpMockFactory)
    def test(self, mock_gmp: GmpMockFactory):
        # get the gmp_commands
        gmp_commands = return_gmp_methods(mock_gmp.gmp_protocol)

        # create the mock response with the gmp_command and the gmp_name
        mock_gmp.mock_response(gmp_cmd, compose_mock_response(gmp_name))

        self.login('foo', 'bar')

        response = self.query(compose_mock_query(plural_selene_name))

        json = response.json()

        self.assertResponseNoErrors(response)

        get_entities = gmp_commands[gmp_cmd]

        get_entities.assert_called_with(filter='lorem', **kwargs)

        entities = json['data'][plural_selene_name]['nodes']

        self.assertEqual(len(entities), 2)

        entity1 = entities[0]
        entity2 = entities[1]

        # Entity 1

        self.assertEqual(entity1['id'], '08b69003-5fc2-4037-a479-93b440211c73')
        self.assertEqual(entity1['name'], 'foo')
        self.assertEqual(entity1['comment'], "bar")
        self.assertEqual(entity1['owner'], 'admin')

        self.assertEqual(entity1['creationTime'], '2019-07-19T13:33:21+00:00')
        self.assertEqual(
            entity1['modificationTime'], '2019-07-19T13:33:21+00:00'
        )

        self.assertTrue(entity1['inUse'])
        self.assertTrue(entity1['writable'])

        permissions = entity1['permissions']
        self.assertEqual(len(permissions), 1)
        self.assertEqual(permissions[0]['name'], 'Everything')

        user_tags = entity1['userTags']

        self.assertEqual(user_tags['count'], 2)

        tags = user_tags['tags']

        self.assertEqual(len(tags), 2)

        tag1 = tags[0]

        self.assertEqual(tag1['name'], 'test tag 1')
        self.assertEqual(tag1['id'], '480cdbd9-1af2-4be6-a195-163748b80381')
        self.assertIsNone(tag1['value'])
        self.assertIsNone(tag1['comment'])

        # Entity 2

        self.assertEqual(entity2['id'], '6b2db524-9fb0-45b8-9b56-d958f84cb546')
        self.assertEqual(entity2['name'], 'lorem')
        self.assertEqual(entity2['comment'], 'ipsum')
        self.assertEqual(entity2['owner'], 'admin')

        self.assertEqual(entity2['creationTime'], '2019-07-19T13:33:21+00:00')
        self.assertEqual(
            entity2['modificationTime'], '2019-07-19T13:33:21+00:00'
        )

        self.assertFalse(entity2['inUse'])
        self.assertTrue(entity2['writable'])

        permissions = entity2['permissions']
        self.assertEqual(len(permissions), 2)
        self.assertEqual(permissions[0]['name'], gmp_name)

        self.assertIsNone(entity2['userTags'])

    return test
