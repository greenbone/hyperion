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

from gvm.protocols.next import (
    EntityType as GvmEntityType,
    AggregateStatistic as GvmAggregateStatistic,
    SortOrder as GvmSortOrder,
)

from selene.tests import SeleneTestCase, GmpMockFactory


CWD = Path(__file__).absolute().parent


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class AggregateTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        """
        Test authentication requirement.
        """
        response = self.query(
            '''
            query GetAggregate {
                aggregate(
                    input: {
                        dataType: NVT
                    }
                ) {
                    overall {
                        count
                    }
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_missing_data_type(self, _mock_gmp: GmpMockFactory):
        """
        Test if data type is required
        """
        response = self.query(
            '''
            query GetAggregate {
                aggregate(
                    input: {
                        groupColumn: "solution_type"
                    }
                ) {
                    groups {
                        value
                        count
                    }
                }
            }
            '''
        )

        self.assertResponseHasErrors(response)

    def test_minimal_query(self, mock_gmp: GmpMockFactory):
        """
        Test a minimal query only giving the data type and
        returning only an overall count.
        """
        aggregate_xml_path = CWD / 'example-aggregate-minimal.xml'
        aggregate_xml_str = aggregate_xml_path.read_text()
        mock_gmp.mock_response('get_aggregates', aggregate_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query GetAggregate {
                aggregate(
                    input: {
                        dataType: NVT
                    }
                ) {
                    overall {
                        count
                    }
                    columnInfo {
                        name
                        stat
                        entityType
                        column
                        dataType
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.get_aggregates.assert_called_with(
            resource_type=GvmEntityType.NVT,
            filter=None,
            data_columns=None,
            group_column=None,
            subgroup_column=None,
            text_columns=None,
            sort_criteria=None,
            first_group=None,
            max_groups=None,
            mode=None,
        )

        aggregate = json['data']['aggregate']
        self.assertEqual(aggregate['overall']['count'], 85949)

        column_info = aggregate['columnInfo']
        self.assertEqual(len(column_info), 2)

        self.assertEqual(column_info[0]['name'], 'count')
        self.assertEqual(column_info[0]['stat'], 'COUNT')
        self.assertEqual(column_info[0]['entityType'], 'NVT')
        self.assertIsNone(column_info[0]['column'])
        self.assertEqual(column_info[0]['dataType'], 'integer')

        self.assertEqual(column_info[1]['name'], 'c_count')
        self.assertEqual(column_info[1]['stat'], 'C_COUNT')
        self.assertEqual(column_info[1]['entityType'], 'NVT')
        self.assertIsNone(column_info[1]['column'])
        self.assertEqual(column_info[1]['dataType'], 'integer')

    def test_grouped_query(self, mock_gmp: GmpMockFactory):
        """
        Test a grouped aggregate that also includes a filter,
        data columns and sort criteria.
        """
        aggregate_xml_path = CWD / 'example-aggregate-grouped.xml'
        aggregate_xml_str = aggregate_xml_path.read_text()
        mock_gmp.mock_response('get_aggregates', aggregate_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query GetAggregate {
                aggregate(
                    input: {
                        dataType: NVT
                        filterString: "~openssl"
                        groupColumn: "solution_type"
                        dataColumns: ["severity", "qod"]
                        sortCriteria: [
                            {field: "severity", stat: MEAN, order: DESCENDING}
                        ]
                    }
                ) {
                    groups {
                        value
                        count
                      	cumulativeCount
                        stats {
                            column
                            min
                            max
                            mean
                            sum
                            cumulativeSum
                        }
                    }
                        columnInfo {
                        name
                        stat
                        entityType
                        column
                        dataType
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.get_aggregates.assert_called_with(
            resource_type=GvmEntityType.NVT,
            filter='~openssl',
            data_columns=['severity', 'qod'],
            group_column='solution_type',
            subgroup_column=None,
            text_columns=None,
            sort_criteria=[
                {
                    'field': 'severity',
                    'stat': GvmAggregateStatistic.MEAN,
                    'order': GvmSortOrder.DESCENDING,
                }
            ],
            first_group=None,
            max_groups=None,
            mode=None,
        )

        aggregate = json['data']['aggregate']

        groups = aggregate['groups']
        self.assertEqual(len(groups), 5)
        self.assertEqual(
            groups[0],
            {
                'value': 'VendorFix',
                'count': 1241,
                'cumulativeCount': 1241,
                'stats': [
                    {
                        'column': 'severity',
                        'min': 1.2,
                        'max': 10,
                        'mean': 6.18187,
                        'sum': 7671.67,
                        'cumulativeSum': 7671.67,
                    },
                    {
                        'column': 'qod',
                        'min': 30,
                        'max': 100,
                        'mean': 90.9887,
                        'sum': 112917,
                        'cumulativeSum': 112917,
                    },
                ],
            },
        )

        self.assertEqual(groups[1]['value'], 'Mitigation')
        self.assertEqual(groups[1]['count'], 2)
        self.assertEqual(groups[1]['cumulativeCount'], 1243)
        self.assertEqual(groups[1]['stats'][0]['sum'], 10)
        self.assertEqual(groups[1]['stats'][0]['cumulativeSum'], 7681.67)

        column_info = aggregate['columnInfo']
        self.assertEqual(len(column_info), 13)

        self.assertEqual(column_info[0]['name'], 'value')
        self.assertEqual(column_info[0]['stat'], 'VALUE')
        self.assertEqual(column_info[0]['entityType'], 'NVT')
        self.assertEqual(column_info[0]['column'], 'solution_type')
        self.assertEqual(column_info[0]['dataType'], 'text')

        self.assertEqual(column_info[1]['name'], 'count')
        self.assertEqual(column_info[1]['stat'], 'COUNT')
        self.assertEqual(column_info[1]['entityType'], 'NVT')
        self.assertIsNone(column_info[1]['column'])
        self.assertEqual(column_info[1]['dataType'], 'integer')

        self.assertEqual(column_info[5]['name'], 'severity_mean')
        self.assertEqual(column_info[5]['stat'], 'MEAN')
        self.assertEqual(column_info[5]['entityType'], 'NVT')
        self.assertEqual(column_info[5]['column'], 'severity')
        self.assertEqual(column_info[5]['dataType'], 'cvss')

    def test_subgrouped_query(self, mock_gmp: GmpMockFactory):
        """
        Test an aggregate with groups and subgroups.
        """
        aggregate_xml_path = CWD / 'example-aggregate-subgrouped.xml'
        aggregate_xml_str = aggregate_xml_path.read_text()
        mock_gmp.mock_response('get_aggregates', aggregate_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query GetAggregate {
                aggregate(
                    input: {
                        dataType: NVT
                        filterString: "~openssl"
                        groupColumn: "solution_type"
                        subgroupColumn: "family"
                        dataColumns: ["severity"]
                        sortCriteria: [
                            {field: "severity", stat:MEAN, order:DESCENDING}
                        ]
                    }
                ) {
                    groups {
                        value
                        count
                        stats {
                            column
                            mean
                        }
                        subgroups {
                          value
                          count
                          stats {
                            column
                            mean
                          }
                        }
                    }
                    subgroupValues
                    columnInfo {
                        name
                        stat
                        entityType
                        column
                        dataType
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.get_aggregates.assert_called_with(
            resource_type=GvmEntityType.NVT,
            filter='~openssl',
            data_columns=['severity'],
            group_column='solution_type',
            subgroup_column='family',
            text_columns=None,
            sort_criteria=[
                {
                    'field': 'severity',
                    'stat': GvmAggregateStatistic.MEAN,
                    'order': GvmSortOrder.DESCENDING,
                }
            ],
            first_group=None,
            max_groups=None,
            mode=None,
        )

        aggregate = json['data']['aggregate']

        groups = aggregate['groups']
        self.assertEqual(len(groups), 5)
        # Test second group as it has more than one subgroup
        self.assertEqual(
            groups[1],
            {
                'value': 'WillNotFix',
                'count': 3,
                'stats': [{'column': 'severity', 'mean': 3.8}],
                'subgroups': [
                    {
                        'value': 'General',
                        'count': 1,
                        'stats': [{'column': 'severity', 'mean': 5}],
                    },
                    {
                        'value': 'F5 Local Security Checks',
                        'count': 2,
                        'stats': [{'column': 'severity', 'mean': 3.2}],
                    },
                ],
            },
        )

        self.assertEqual(len(aggregate['subgroupValues']), 32)
        self.assertEqual(
            aggregate['subgroupValues'][:5],
            [
                "Amazon Linux Local Security Checks",
                "Buffer overflow",
                "CISCO",
                "CentOS Local Security Checks",
                "Databases",
            ],
        )

    def test_text_column_query(self, mock_gmp: GmpMockFactory):
        """
        Test an aggregate with text columns and limits (firstGroup, maxGroups).
        """
        aggregate_xml_path = CWD / 'example-aggregate-text-columns.xml'
        aggregate_xml_str = aggregate_xml_path.read_text()
        mock_gmp.mock_response('get_aggregates', aggregate_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query GetAggregate {
                aggregate(
                    input: {
                        dataType: NVT
                        groupColumn: "uuid"
                        textColumns: ["created", "name"]
                        sortCriteria: [
                            {field: "created", stat:TEXT, order:ASCENDING}
                        ]
                      	firstGroup: 10
                        maxGroups: 25
                    }
                ) {
                    groups {
                        value
                        textColumns {
                          column,
                          text
                        }
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.get_aggregates.assert_called_with(
            resource_type=GvmEntityType.NVT,
            filter=None,
            data_columns=None,
            group_column='uuid',
            subgroup_column=None,
            text_columns=['created', 'name'],
            sort_criteria=[
                {
                    'field': 'created',
                    'stat': GvmAggregateStatistic.TEXT,
                    'order': GvmSortOrder.ASCENDING,
                }
            ],
            first_group=10,
            max_groups=25,
            mode=None,
        )

        aggregate = json['data']['aggregate']

        groups = aggregate['groups']
        self.assertEqual(len(groups), 25)

        self.assertEqual(
            groups[0],
            {
                'value': '1.3.6.1.4.1.25623.1.0.14372',
                'textColumns': [
                    {'column': 'created', 'text': '2005-11-03T13:08:04Z'},
                    {
                        'column': 'name',
                        'text': 'wu-ftpd S/KEY authentication overflow',
                    },
                ],
            },
        )

    def test_word_count_query(self, mock_gmp: GmpMockFactory):
        """
        Test an aggregate using the word_counts mode.
        """
        aggregate_xml_path = CWD / 'example-aggregate-word-counts.xml'
        aggregate_xml_str = aggregate_xml_path.read_text()
        mock_gmp.mock_response('get_aggregates', aggregate_xml_str)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query GetAggregate {
                aggregate(
                    input: {
                        dataType: NVT
                        groupColumn: "name"
                        maxGroups: 10
                        sortCriteria: [
                          {stat:COUNT, order: DESCENDING}
                        ]
                        mode: WORD_COUNTS
                    }
                ) {
                    groups {
                        value
                        count
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        mock_gmp.gmp_protocol.get_aggregates.assert_called_with(
            resource_type=GvmEntityType.NVT,
            filter=None,
            data_columns=None,
            group_column='name',
            subgroup_column=None,
            text_columns=None,
            sort_criteria=[
                {
                    'stat': GvmAggregateStatistic.COUNT,
                    'order': GvmSortOrder.DESCENDING,
                }
            ],
            first_group=None,
            max_groups=10,
            mode='word_counts',
        )

        aggregate = json['data']['aggregate']

        groups = aggregate['groups']
        self.assertEqual(len(groups), 10)
        self.assertEqual(
            groups,
            [
                {'value': 'Update', 'count': 31721},
                {'value': 'Security', 'count': 25570},
                {'value': 'Advisory', 'count': 20274},
                {'value': 'Fedora', 'count': 17010},
                {'value': 'Vulnerability', 'count': 13482},
                {'value': 'Vulnerabilities', 'count': 7522},
                {'value': 'Multiple', 'count': 7126},
                {'value': 'Debian', 'count': 6342},
                {'value': 'Linux', 'count': 6056},
                {'value': 'Windows', 'count': 5888},
            ],
        )
