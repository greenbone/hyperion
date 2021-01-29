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

from selene.tests.pagination import (
    make_test_counts,
    make_test_after_first,
    make_test_page_info,
    make_test_edges,
    make_test_before_last,
    make_test_after_first_before_last,
)

from selene.schema.vulnerabilities.queries import GetVulnerabilities


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class VulnerabilitiesTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                vulnerabilities {
                    nodes {
                        id
                        name
                    }
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_vulnerabilities(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_vulnerabilities',
            '''
            <get_vulns_response>
                <vuln id="15085a9a-3d24-11ea-944a-6f78adc016ea">
                    <name>a</name>
                </vuln>
                <vuln id="230f47a2-3d24-11ea-bd0b-db49f50db5ae">
                    <name>b</name>
                </vuln>
            </get_vulns_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                vulnerabilities {
                    nodes {
                        id
                        name
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        vulnerabilities = json['data']['vulnerabilities']['nodes']

        self.assertEqual(len(vulnerabilities), 2)

        vulnerabilitie1 = vulnerabilities[0]
        vulnerabilitie2 = vulnerabilities[1]

        self.assertEqual(vulnerabilitie1['name'], 'a')
        self.assertEqual(
            vulnerabilitie1['id'], '15085a9a-3d24-11ea-944a-6f78adc016ea'
        )
        self.assertEqual(vulnerabilitie2['name'], 'b')
        self.assertEqual(
            vulnerabilitie2['id'], '230f47a2-3d24-11ea-bd0b-db49f50db5ae'
        )

    def test_get_filtered_vulnerabilities(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_vulnerabilities',
            '''
            <get_vulns_response>
                <vuln id="f650a1c0-3d23-11ea-8540-e790e17c1b00">
                    <name>a</name>
                </vuln>
                <vuln id="0778ac90-3d24-11ea-b722-fff755412c48">
                    <name>b</name>
                </vuln>
            </get_vulns_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                vulnerabilities (
                    filterString: "lorem",
                ) {
                    nodes {
                        id
                        name
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        vulnerabilities = json['data']['vulnerabilities']['nodes']

        self.assertEqual(len(vulnerabilities), 2)

        vulnerabilitie1 = vulnerabilities[0]
        vulnerabilitie2 = vulnerabilities[1]

        self.assertEqual(vulnerabilitie1['name'], 'a')
        self.assertEqual(
            vulnerabilitie1['id'], 'f650a1c0-3d23-11ea-8540-e790e17c1b00'
        )
        self.assertEqual(vulnerabilitie2['name'], 'b')
        self.assertEqual(
            vulnerabilitie2['id'], '0778ac90-3d24-11ea-b722-fff755412c48'
        )


class VulnerabilitiesPaginationTestCase(SeleneTestCase):
    gmp_name = 'vuln'
    selene_name = 'vulnerability'
    plural_selene_name = 'vulnerabilities'
    gmp_cmd = 'get_vulnerabilities'
    test_pagination_with_after_and_first = make_test_after_first(
        gmp_name,
        selene_name=selene_name,
        plural_selene_name=plural_selene_name,
        gmp_cmd=gmp_cmd,
    )
    test_counts = make_test_counts(
        gmp_name,
        selene_name=selene_name,
        plural_selene_name=plural_selene_name,
        gmp_cmd=gmp_cmd,
    )
    test_page_info = make_test_page_info(
        gmp_name,
        selene_name=selene_name,
        plural_selene_name=plural_selene_name,
        gmp_cmd=gmp_cmd,
        query=GetVulnerabilities,
    )
    test_edges = make_test_edges(
        gmp_name,
        selene_name=selene_name,
        plural_selene_name=plural_selene_name,
        gmp_cmd=gmp_cmd,
    )
    test_pagination_with_before_and_last = make_test_before_last(
        gmp_name,
        selene_name=selene_name,
        plural_selene_name=plural_selene_name,
        gmp_cmd=gmp_cmd,
    )
    test_after_first_before_last = make_test_after_first_before_last(
        gmp_name,
        selene_name=selene_name,
        plural_selene_name=plural_selene_name,
        gmp_cmd=gmp_cmd,
    )
