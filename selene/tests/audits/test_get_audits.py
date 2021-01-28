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

from selene.schema.audits.queries import GetAudits


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class AuditsTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                audits {
                    nodes {
                        id
                        name
                    }
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_audits(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_audits',
            '''
            <get_tasks_response>
                <task id="15085a9a-3d24-11ea-944a-6f78adc016ea">
                    <name>a</name>
                </task>
                <task id="230f47a2-3d24-11ea-bd0b-db49f50db5ae">
                    <name>b</name>
                </task>
            </get_tasks_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                audits {
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

        audits = json['data']['audits']['nodes']

        self.assertEqual(len(audits), 2)

        audit1 = audits[0]
        audit2 = audits[1]

        self.assertEqual(audit1['name'], 'a')
        self.assertEqual(audit1['id'], '15085a9a-3d24-11ea-944a-6f78adc016ea')
        self.assertEqual(audit2['name'], 'b')
        self.assertEqual(audit2['id'], '230f47a2-3d24-11ea-bd0b-db49f50db5ae')

    def test_get_filtered_audits(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'get_audits',
            '''
            <get_tasks_response>
                <task id="f650a1c0-3d23-11ea-8540-e790e17c1b00">
                    <name>a</name>
                </task>
                <task id="0778ac90-3d24-11ea-b722-fff755412c48">
                    <name>b</name>
                </task>
            </get_tasks_response>
            ''',
        )

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                audits (
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

        audits = json['data']['audits']['nodes']

        self.assertEqual(len(audits), 2)

        audit1 = audits[0]
        audit2 = audits[1]

        self.assertEqual(audit1['name'], 'a')
        self.assertEqual(audit1['id'], 'f650a1c0-3d23-11ea-8540-e790e17c1b00')
        self.assertEqual(audit2['name'], 'b')
        self.assertEqual(audit2['id'], '0778ac90-3d24-11ea-b722-fff755412c48')


class AuditsPaginationTestCase(SeleneTestCase):
    gmp_name = 'task'
    selene_name = 'audit'
    gmp_cmd = 'get_audits'
    test_pagination_with_after_and_first = make_test_after_first(
        gmp_name=gmp_name,
        selene_name=selene_name,
        gmp_cmd=gmp_cmd,
        details=True,
    )
    test_counts = make_test_counts(
        gmp_name=gmp_name, selene_name=selene_name, gmp_cmd=gmp_cmd
    )
    test_page_info = make_test_page_info(
        gmp_name=gmp_name,
        selene_name=selene_name,
        gmp_cmd=gmp_cmd,
        query=GetAudits,
    )
    test_edges = make_test_edges(
        gmp_name=gmp_name, selene_name=selene_name, gmp_cmd=gmp_cmd
    )
    test_pagination_with_before_and_last = make_test_before_last(
        gmp_name=gmp_name,
        selene_name=selene_name,
        gmp_cmd=gmp_cmd,
        details=True,
    )
    test_after_first_before_last = make_test_after_first_before_last(
        gmp_name=gmp_name,
        selene_name=selene_name,
        gmp_cmd=gmp_cmd,
        details=True,
    )


class AuditGetEntitiesTestCase(SeleneTestCase):
    gmp_name = 'task'
    selene_name = 'audit'
    gmp_cmd = 'get_audits'
    test_get_entities = make_test_get_entities(
        gmp_name=gmp_name,
        selene_name=selene_name,
        gmp_cmd=gmp_cmd,
        details=True,
    )
