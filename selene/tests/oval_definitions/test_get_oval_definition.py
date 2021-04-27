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

# pylint: disable=line-too-long

from pathlib import Path

from unittest.mock import patch

from gvm.protocols.next import InfoType as GvmInfoType

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

    def test_get_oval_definition_sub_field_none_cases(
        self, mock_gmp: GmpMockFactory
    ):
        oval_definition_id = 'foooo'
        mock_gmp.mock_response(
            'get_info',
            f'''
            <get_info_response>
                <info id="{oval_definition_id}">
                    <name>foo</name>
                    <ovaldef>
                        <raw_data>
                            <definition xmlns="http://oval.mitre.org/XMLSchema/oval-definitions-5"
                            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                            xmlns:oval="http://oval.mitre.org/XMLSchema/oval-common-5"
                            xmlns:oval-def="http://oval.mitre.org/XMLSchema/oval-definitions-5" id="oval:org.mitre.oval:def:29480" version="2" class="vulnerability">
                            <metadata>
                                <title>Adobe Reader and Acrobat 7.0.8 and earlier allows user-assisted remote attackers to execute code (CVE-2006-5857)</title>
                                <affected/>
                                <reference source="CVE" ref_id="CVE-2006-5857" ref_url="http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2006-5857"></reference>
                                <description>Adobe Reader and Acrobat 7.0.8 and earlier allows user-assisted remote attackers to execute code via a crafted PDF file that triggers memory corruption and overwrites a subroutine pointer during rendering.</description>
                                <oval_repository><dates/></oval_repository>
                            </metadata>
                            </definition>
                        </raw_data>
                    </ovaldef>
                </info>
            </get_info_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            query {{
                ovalDefinition(id: "{oval_definition_id}") {{
                    id
                    name
                    cveRefs
                    affectedFamily {{
                        family
                        platforms
                        products
                    }}
                    history {{
                        status
                        date
                        contributor
                        organization
                        statusChanges {{
                            status
                            date
                        }}
                    }}
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        oval_definition = json['data']['ovalDefinition']

        self.assertEqual(oval_definition['id'], oval_definition_id)
        self.assertEqual(oval_definition['name'], 'foo')
        self.assertIsNone(oval_definition['affectedFamily']['platforms'])
        self.assertIsNone(oval_definition['affectedFamily']['products'])
        self.assertIsNone(oval_definition['history']['date'])
        self.assertIsNone(oval_definition['history']['contributor'])
        self.assertIsNone(oval_definition['history']['organization'])
        self.assertIsNone(oval_definition['history']['statusChanges'])

        mock_gmp.gmp_protocol.get_info.assert_called_with(
            oval_definition_id, info_type=GvmInfoType.OVALDEF
        )

    def test_get_oval_definition_none_cases(self, mock_gmp: GmpMockFactory):
        oval_definition_id = 'foooo'
        mock_gmp.mock_response(
            'get_info',
            f'''
            <get_info_response>
                <info id="{oval_definition_id}">
                    <name>foo</name>
                </info>
            </get_info_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            f'''
            query {{
                ovalDefinition(id: "{oval_definition_id}") {{
                    id
                    name
                    cveRefs
                    references {{
                        source
                    }}
                    deprecated
                    description
                    file
                    class
                    affectedFamily {{
                        family
                    }}
                    history {{
                        status
                    }}
                    criteria {{
                        operator
                    }}
                    score
                    status
                    title
                    version
                }}
            }}
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        oval_definition = json['data']['ovalDefinition']

        self.assertEqual(oval_definition['id'], oval_definition_id)
        self.assertEqual(oval_definition['name'], 'foo')
        self.assertIsNone(oval_definition['cveRefs'])
        self.assertIsNone(oval_definition['references'])
        self.assertIsNone(oval_definition['deprecated'])
        self.assertIsNone(oval_definition['description'])
        self.assertIsNone(oval_definition['file'])
        self.assertIsNone(oval_definition['class'])
        self.assertIsNone(oval_definition['affectedFamily'])
        self.assertIsNone(oval_definition['history'])
        self.assertIsNone(oval_definition['criteria'])
        self.assertIsNone(oval_definition['score'])
        self.assertIsNone(oval_definition['status'])
        self.assertIsNone(oval_definition['title'])
        self.assertIsNone(oval_definition['version'])

        mock_gmp.gmp_protocol.get_info.assert_called_with(
            oval_definition_id, info_type=GvmInfoType.OVALDEF
        )

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
                    references {
                        source
                        id
                        url
                    }
                    deprecated
                    description
                    file
                    cveRefs
                    class
                    affectedFamily {
                        family
                        platforms
                        products
                    }
                    history {
                        status
                        date
                        contributor
                        organization
                        statusChanges {
                            status
                            date
                        }
                    }
                    criteria {
                        operator
                        comment
                        extendDefinition
                        criterion
                        criteria {
                            operator
                            comment
                            extendDefinition
                            criterion
                            criteria {
                                operator
                            }
                        }
                    }
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
            oval_definition['name'], 'oval:org.mitre.oval:def:29480'
        )
        self.assertEqual(
            oval_definition['id'],
            'oval:org.mitre.oval:def:29480_/oval/5.10/org.mitre.oval/v/family/windows.xml',
        )
        self.assertEqual(
            oval_definition['title'],
            'Adobe Reader and Acrobat 7.0.8 and earlier allows user-assisted remote attackers to execute code (CVE-2006-5857)',
        )
        self.assertEqual(oval_definition['description'], 'short text')
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

        self.assertIsNotNone(oval_definition['affectedFamily'])

        family = oval_definition['affectedFamily']
        self.assertEqual(family['family'], 'windows')
        self.assertEqual(
            family['platforms'],
            [
                'Microsoft Windows 2000',
                'Microsoft Windows 7',
                'Microsoft Windows Server 2003',
                'Microsoft Windows Server 2008',
                'Microsoft Windows Vista',
                'Microsoft Windows XP',
                'Microsoft Windows Server 2008 R2',
                'Microsoft Windows 8',
                'Microsoft Windows Server 2012',
                'Microsoft Windows 8.1',
                'Microsoft Windows Server 2012 R2',
            ],
        )
        self.assertEqual(family['products'], ['Adobe Acrobat', 'Adobe Reader'])

        self.assertIsNotNone(oval_definition['history'])
        history = oval_definition['history']
        self.assertEqual(history['status'], 'INTERIM')
        self.assertEqual(history['date'], '2015-07-30T08:31:03')
        self.assertEqual(history['contributor'], 'Mr. Foo')
        self.assertEqual(history['organization'], 'foo inc')

        self.assertIsNotNone(history['statusChanges'])

        status_changes = history['statusChanges']
        self.assertEqual(
            status_changes[0]['date'], '2015-07-31 12:47:21.289000-04:00'
        )
        self.assertEqual(status_changes[0]['status'], 'DRAFT')

        self.assertIsNotNone(oval_definition['criteria'])

        criteria = oval_definition['criteria']
        self.assertEqual(criteria['operator'], 'OR')
        self.assertIsNone(criteria['comment'])
        self.assertIsNone(criteria['criterion'])
        self.assertIsNone(criteria['extendDefinition'])

        self.assertIsNotNone(criteria['criteria'])

        level_2_criteria = criteria['criteria']
        self.assertEqual(level_2_criteria[0]['operator'], 'AND')
        self.assertEqual(
            level_2_criteria[0]['comment'], 'Check version of Acrobat'
        )
        self.assertEqual(
            level_2_criteria[0]['criterion'],
            'Check if the version of Adobe Acrobat is less than 7.0.8',
        )
        self.assertEqual(
            level_2_criteria[0]['extendDefinition'],
            'Adobe Acrobat is installed',
        )

        self.assertIsNone(level_2_criteria[0]['criteria'])

        self.assertIsNotNone(oval_definition['references'])

        oval_definition_refs = oval_definition['references']
        self.assertEqual(oval_definition_refs[0]['source'], 'CVE')
        self.assertEqual(oval_definition_refs[0]['id'], 'CVE-2006-5857')
        self.assertEqual(
            oval_definition_refs[0]['url'],
            'http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2006-5857',
        )


class OvalDefinitionGetEntityTestCase(SeleneTestCase):
    gmp_name = 'info'
    selene_name = 'ovalDefinition'
    test_get_entity = make_test_get_entity(
        gmp_name, selene_name=selene_name, info_type=GvmInfoType.OVALDEF
    )
