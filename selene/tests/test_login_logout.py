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

import datetime

from unittest.mock import patch

from django.conf import settings

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class LoginLogoutTestCase(SeleneTestCase):
    def test_login_success(self, mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            mutation {
              login(username: "foo", password: "bar") {
                ok
              }
            }
            '''
        )
        self.assertResponseStatusCode(response, 200)

        mock_gmp.assert_authenticated_with('foo', 'bar')

    def test_login_failure(self, mock_gmp: GmpMockFactory):
        mock_gmp.fail_authentication()

        response = self.query(
            '''
            mutation {
              login(username: "foo", password: "bar") {
                ok
              }
            }
            '''
        )

        mock_gmp.assert_authenticated_with('foo', 'bar')

        self.assertResponseStatusCode(response, 200)
        self.assertResponseHasErrorMessage(response, 'Authentication failed')

    def test_login_success_with_timezone(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'authenticate',
            '''
            <authenticate>
                <timezone>Foo/Bar</timezone>
            </authenticate>
            ''',
        )
        response = self.query(
            '''
            mutation {
              login(username: "foo", password: "bar") {
                ok
                timezone
              }
            }
            '''
        )
        self.assertResponseStatusCode(response, 200)

        mock_gmp.assert_authenticated_with('foo', 'bar')

        json = response.json()

        self.assertResponseNoErrors(response)

        timezone = json['data']['login']['timezone']

        self.assertEqual(timezone, 'Foo/Bar')

    def test_login_success_with_session_timeout(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'authenticate',
            '''
            <authenticate>
            </authenticate>
            ''',
        )

        now = datetime.datetime.now()

        session = self.client.session
        session.set_expiry(300)
        session.save()

        response = self.query(
            '''
            mutation {
              login(username: "foo", password: "bar") {
                ok
                sessionTimeout
              }
            }
            '''
        )
        self.assertResponseStatusCode(response, 200)

        mock_gmp.assert_authenticated_with('foo', 'bar')

        json = response.json()

        self.assertResponseNoErrors(response)

        timeout = json['data']['login']['sessionTimeout']

        timeout_read = datetime.datetime.strptime(
            timeout, '%Y-%m-%dT%H:%M:%S.%f'
        )
        diff_time = timeout_read - now

        self.assertEqual(diff_time.seconds, settings.SESSION_COOKIE_AGE)

    def test_login_success_with_locale(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'authenticate',
            '''
            <authenticate>
                <timezone>Foo/Bar</timezone>
            </authenticate>
            ''',
        )
        mock_gmp.mock_response(
            'get_setting',
            '''
            <get_settings_response>
                <setting>
                    <value>foo</value>
                </setting>
            </get_settings_response>
            ''',
        )
        response = self.query(
            '''
            mutation {
              login(username: "foo", password: "bar") {
                ok
                locale
              }
            }
            '''
        )
        self.assertResponseStatusCode(response, 200)

        mock_gmp.assert_authenticated_with('foo', 'bar')

        json = response.json()

        self.assertResponseNoErrors(response)

        locale = json['data']['login']['locale']

        self.assertEqual(locale, 'foo')

    def test_logout(self, _mock_gmp: GmpMockFactory):
        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                tasks {
                    nodes {
                      id
                    }
                }
            }
            '''
        )

        self.assertResponseStatusCode(response, 200)
        self.assertResponseNoErrors(response)

        response = self.query(
            '''
            mutation {
              logout {
                ok
              }
            }
            '''
        )

        self.assertResponseStatusCode(response, 200)

        response = self.query(
            '''
            query {
                tasks {
                    nodes {
                      id
                    }
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_current_user(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response(
            'authenticate',
            '''
            <authenticate>
            </authenticate>
            ''',
        )

        now = datetime.datetime.now()

        session = self.client.session
        session.set_expiry(300)
        session.save()

        login_response = self.query(
            '''
          mutation {
            login(username: "foo", password: "bar") {
              ok
              sessionTimeout
            }
          }
          '''
        )
        self.assertResponseStatusCode(login_response, 200)

        mock_gmp.assert_authenticated_with('foo', 'bar')

        auth_response = self.query(
            '''
          query {
            currentUser {
              username
              isAuthenticated
              sessionTimeout
            }
          }
          '''
        )

        auth_data = auth_response.json()
        current_user = auth_data['data']['currentUser']

        timeout = current_user['sessionTimeout']

        timeout_read = datetime.datetime.strptime(
            timeout, '%Y-%m-%dT%H:%M:%S.%f'
        )
        diff_time = timeout_read - now

        self.assertEqual(
            diff_time.seconds, datetime.timedelta(minutes=5).seconds
        )

        self.assertEqual(current_user['isAuthenticated'], True)
        self.assertEqual(current_user['username'], 'foo')

        logout_response = self.query(
            '''
          mutation {
            logout {
              ok
            }
          }
          '''
        )
        self.assertResponseStatusCode(logout_response, 200)

        auth_response = self.query(
            '''
          query {
            currentUser {
              username
              isAuthenticated
              sessionTimeout
            }
          }
          '''
        )

        auth_data = auth_response.json()
        current_user = auth_data['data']['currentUser']

        self.assertEqual(current_user['isAuthenticated'], False)
        self.assertIsNone(current_user['username'])
        self.assertIsNone(current_user['sessionTimeout'])
