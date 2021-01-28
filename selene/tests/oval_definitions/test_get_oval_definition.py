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

# pylint: disable=line-too-long

from pathlib import Path

from unittest.mock import patch

from gvm.protocols.latest import InfoType as GvmInfoType

from selene.tests import SeleneTestCase, GmpMockFactory

from selene.tests.entity import make_test_get_entity

CWD = Path(__file__).absolute().parent


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class OvalDefinitionTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                ovalDefinition(id: "oval:org.mitre.oval:def:29480_/oval/5.10/org.mitre.oval/v/family/windows.xml") {
                    id
                    name
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_oval_definition(self, mock_gmp: GmpMockFactory):
        oval_definition_xml_path = CWD / 'example-oval-definition.xml'
        oval_definition_xml_str = oval_definition_xml_path.read_text()

        mock_gmp.mock_response('get_info', oval_definition_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                ovalDefinition(id:
                    "oval:org.mitre.oval:def:29480_/oval/5.10/org.mitre.oval/v/family/windows.xml"
                ) {
                    id
                    name
                    cveRefs
                    deprecated
                    description
                    file
                    class
                    rawData
                    score
                    status
                    title
                    version
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        oval_definition = json['data']['ovalDefinition']

        self.assertEqual(
            oval_definition['name'],
            'oval:org.mitre.oval:def:29480',
        )
        self.assertEqual(
            oval_definition['id'],
            'oval:org.mitre.oval:def:29480_/oval/5.10/org.mitre.oval/v/family/windows.xml',
        )
        self.assertEqual(
            oval_definition['title'],
            'Adobe Reader and Acrobat 7.0.8 and earlier allows user-assisted remote attackers to execute code (CVE-2006-5857)',
        )
        self.assertEqual(
            oval_definition['description'],
            'short text',
        )
        self.assertEqual(oval_definition['score'], 93)
        self.assertEqual(oval_definition['cveRefs'], 1)
        self.assertEqual(oval_definition['deprecated'], False)
        self.assertEqual(
            oval_definition['file'],
            '/oval/5.10/org.mitre.oval/v/family/windows.xml',
        )
        self.assertEqual(oval_definition['class'], 'vulnerability')
        self.assertEqual(oval_definition['status'], 'INTERIM')
        self.assertEqual(oval_definition['version'], 2)

        # tests for the complex rawData will need to be added, when a
        # final design decision about them was made


class OvalDefinitionGetEntityTestCase(SeleneTestCase):
    gmp_name = 'info'
    selene_name = 'ovalDefinition'
    test_get_entity = make_test_get_entity(
        gmp_name,
        selene_name=selene_name,
        info_type=GvmInfoType.OVALDEF,
    )
