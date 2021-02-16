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

from gvm.protocols.next import InfoType as GvmInfoType

from selene.tests import SeleneTestCase, GmpMockFactory

from selene.tests.pagination import (
    make_test_counts,
    make_test_after_first,
    make_test_page_info,
    make_test_edges,
    make_test_before_last,
    make_test_after_first_before_last,
)
from selene.tests.entity import make_test_get_entities

from selene.schema.dfn_cert_advisories.queries import GetDFNCertAdvisories


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class DFNCertAdvisoriesTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                dfnCertAdvisories {
                    nodes {
                        id
                        name
                    }
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_dfn_cert_advisories(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_info_list',
            '''
            <get_info_response>
                <info id="DFN-CERT-2008-0644">
                    <name>a</name>
                </info>
                <info id="DFN-CERT-2008-0645">
                    <name>b</name>
                </info>
            </get_info_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                dfnCertAdvisories {
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

        dfn_cert_advisories = json['data']['dfnCertAdvisories']['nodes']

        self.assertEqual(len(dfn_cert_advisories), 2)

        dfn_cert_advisory1 = dfn_cert_advisories[0]
        dfn_cert_advisory2 = dfn_cert_advisories[1]

        self.assertEqual(dfn_cert_advisory1['name'], 'a')
        self.assertEqual(dfn_cert_advisory1['id'], 'DFN-CERT-2008-0644')
        self.assertEqual(dfn_cert_advisory2['name'], 'b')
        self.assertEqual(dfn_cert_advisory2['id'], 'DFN-CERT-2008-0645')

    def test_get_filtered_dfn_cert_advisories(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_info_list',
            '''
            <get_info_response>
                <info id="DFN-CERT-2008-0644">
                    <name>a</name>
                </info>
                <info id="DFN-CERT-2008-0645">
                    <name>b</name>
                </info>
            </get_info_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                dfnCertAdvisories (
                    filterString: "lorem"
                    details: true
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

        dfn_cert_advisories = json['data']['dfnCertAdvisories']['nodes']

        self.assertEqual(len(dfn_cert_advisories), 2)

        dfn_cert_advisory1 = dfn_cert_advisories[0]
        dfn_cert_advisory2 = dfn_cert_advisories[1]

        self.assertEqual(dfn_cert_advisory1['name'], 'a')
        self.assertEqual(dfn_cert_advisory1['id'], 'DFN-CERT-2008-0644')
        self.assertEqual(dfn_cert_advisory2['name'], 'b')
        self.assertEqual(dfn_cert_advisory2['id'], 'DFN-CERT-2008-0645')


class DFNCertAdvisoriesPaginationTestCase(SeleneTestCase):
    entity_name = 'info'
    gmp_cmd = 'get_info_list'
    selene_name = 'dfncertadvisory'
    plural_selene_name = 'dfnCertAdvisories'
    test_pagination_with_after_and_first = make_test_after_first(
        entity_name,
        selene_name=selene_name,
        plural_selene_name=plural_selene_name,
        gmp_cmd=gmp_cmd,
        info_type=GvmInfoType.DFN_CERT_ADV,
        details=True,
    )
    test_counts = make_test_counts(
        entity_name,
        selene_name=selene_name,
        plural_selene_name=plural_selene_name,
        gmp_cmd=gmp_cmd,
        no_plural=True,
    )
    test_page_info = make_test_page_info(
        entity_name,
        selene_name=selene_name,
        gmp_cmd=gmp_cmd,
        plural_selene_name=plural_selene_name,
        query=GetDFNCertAdvisories,
        no_plural=True,
    )
    test_edges = make_test_edges(
        entity_name,
        gmp_cmd=gmp_cmd,
        selene_name=selene_name,
        plural_selene_name=plural_selene_name,
        no_plural=True,
    )
    test_pagination_with_before_and_last = make_test_before_last(
        entity_name,
        selene_name=selene_name,
        plural_selene_name=plural_selene_name,
        gmp_cmd=gmp_cmd,
        info_type=GvmInfoType.DFN_CERT_ADV,
        details=True,
    )
    test_after_first_before_last = make_test_after_first_before_last(
        entity_name,
        selene_name=selene_name,
        plural_selene_name=plural_selene_name,
        gmp_cmd=gmp_cmd,
        info_type=GvmInfoType.DFN_CERT_ADV,
        details=True,
    )


class DFNCertAdvisoriesGetEntitiesTestCase(SeleneTestCase):
    gmp_name = 'info'
    gmp_cmd = 'get_info_list'
    selene_name = 'dfncertadvisory'
    plural_selene_name = 'dfnCertAdvisories'
    test_get_entities = make_test_get_entities(
        gmp_name,
        selene_name=selene_name,
        plural_selene_name=plural_selene_name,
        gmp_cmd=gmp_cmd,
        info_type=GvmInfoType.DFN_CERT_ADV,
        details=True,
    )
