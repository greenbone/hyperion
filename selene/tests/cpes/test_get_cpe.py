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
class CPETestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                cpe(id: "cpe:/a:$0.99_kindle_books_project:$0.99_kindle_books:6::~~~android~~") {
                    id
                    name
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_cpe(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_info',
            '''
            <get_info_response>
                <info id="cpe:/a:$0.99_kindle_books_project:$0.99_kindle_books:6::~~~android~~">
                    <name>foo</name>
                </info>
            </get_info_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                cpe(id:
                    "cpe:/a:$0.99_kindle_books_project:$0.99_kindle_books:6::~~~android~~"
                ) {
                    id
                    name
                    owner
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        cpe = json['data']['cpe']

        self.assertEqual(
            cpe['id'],
            'cpe:/a:$0.99_kindle_books_project:$0.99_kindle_books:6::~~~android~~',
        )
        self.assertEqual(cpe['name'], 'foo')
        self.assertIsNone(cpe['owner'])

    def test_complex_cpe(self, mock_gmp: GmpMockFactory):
        cpe_xml_path = CWD / 'example-cpe.xml'
        cpe_xml_str = cpe_xml_path.read_text()

        mock_gmp.mock_response('get_info', cpe_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                cpe(id:
                    "cpe:/a:$0.99_kindle_books_project:$0.99_kindle_books:6::~~~android~~"
                ) {
                    id
                    name
                    updateTime
                    title
                    nvdId
                    maxCvss
                    cveRefs
                    status
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        cpe = json['data']['cpe']

        self.assertEqual(
            cpe['name'],
            'cpe:/a:$0.99_kindle_books_project:'
            '$0.99_kindle_books:6::~~~android~~',
        )
        self.assertEqual(
            cpe['id'],
            'cpe:/a:$0.99_kindle_books_project:'
            '$0.99_kindle_books:6::~~~android~~',
        )
        self.assertEqual(
            cpe['title'],
            '$0.99 Kindle Books project $0.99 Kindle Books '
            '(aka com.kindle.books.for99) for android 6.0',
        )
        self.assertEqual(cpe['nvdId'], '289692')
        self.assertEqual(cpe['status'], 'FINAL')
        self.assertEqual(cpe['maxCvss'], 5.4)
        self.assertEqual(cpe['cveRefs'], 1)


class CPEGetEntityTestCase(SeleneTestCase):
    gmp_name = 'info'
    selene_name = 'cpe'
    test_get_entity = make_test_get_entity(
        gmp_name,
        selene_name=selene_name,
        info_type=GvmInfoType.CPE,
    )
