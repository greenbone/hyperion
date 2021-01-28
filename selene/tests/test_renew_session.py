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
class RenewSessionTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            mutation {
                renewSession {
                    currentUser {
                        sessionTimeout
                    }
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_should_increase_timeout(self, _mock_gmp: GmpMockFactory):
        now = datetime.datetime.now()
        expiry = now + datetime.timedelta(seconds=30)

        session = self.client.session
        session.set_expiry(expiry)
        session.save()

        self.login('foo', 'bar')

        response = self.query(
            '''
            mutation {
                renewSession {
                    currentUser {
                        sessionTimeout
                    }
                }
            }
            '''
        )

        self.assertResponseStatusCode(response, 200)

        json = response.json()

        self.assertResponseNoErrors(response)

        timeout = json['data']['renewSession']['currentUser']['sessionTimeout']

        timeout_read = datetime.datetime.strptime(
            timeout, '%Y-%m-%dT%H:%M:%S.%f'
        )
        diff_time = timeout_read - now

        self.assertEqual(diff_time.seconds, settings.SESSION_COOKIE_AGE)

    def test_should_return_current_user(self, _mock_gmp: GmpMockFactory):
        now = datetime.datetime.now()
        expiry = now + datetime.timedelta(seconds=30)

        session = self.client.session
        session.set_expiry(expiry)
        session.save()

        self.login('foo', 'bar')

        response = self.query(
            '''
            mutation {
                renewSession {
                    currentUser {
                        sessionTimeout
                        username,
                        isAuthenticated
                    }
                }
            }
            '''
        )

        self.assertResponseStatusCode(response, 200)

        json = response.json()

        self.assertResponseNoErrors(response)

        current_user = json['data']['renewSession']['currentUser']

        self.assertIsNotNone(current_user['sessionTimeout'])
        self.assertEqual(current_user['username'], 'foo')
        self.assertTrue(current_user['isAuthenticated'])
