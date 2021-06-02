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

from datetime import timedelta

import graphene

from django.utils import timezone as django_timezone

from graphql import ResolveInfo

from gvm.errors import GvmResponseError

from selene.errors import AuthenticationFailed

from selene.schema.utils import (
    get_gmp,
    get_request,
    get_subelement,
    get_text_from_element,
    require_authentication,
)

USER_SETTING_LOCALE = "6765549a-934e-11e3-b358-406186ea4fc5"


class CurrentUser(graphene.ObjectType):
    """Login information for the current user"""

    session_timeout = graphene.DateTime(
        description='End of the current session. '
        'None if the user is not logged in'
    )
    username = graphene.String(description='Username of the logged in used')
    is_authenticated = graphene.Boolean(
        description='True if the current user is logged in'
    )

    @staticmethod
    def resolve_session_timeout(_root, info: ResolveInfo):
        request = get_request(info)
        username = request.session.get('username')

        if username is not None:
            return request.session.get_expiry_date()

    @staticmethod
    def resolve_username(_root, info: ResolveInfo):
        request = get_request(info)
        return request.session.get('username')

    @staticmethod
    def resolve_is_authenticated(_root, info: ResolveInfo):
        request = get_request(info)
        username = request.session.get('username')

        if username is not None:
            timeout = request.session.get_expiry_age()
            return timeout > 0
        return False


class LoginMutation(graphene.Mutation):
    """Login a user"""

    class Arguments:
        username = graphene.String(
            required=True, description='Name of the user'
        )
        password = graphene.String(
            required=True, description='Password for the user'
        )

    ok = graphene.Field(graphene.Boolean, description='Will always be true')
    timezone = graphene.Field(
        graphene.String,
        description='Only temporary. Should be converted into a user setting',
    )
    session_timeout = graphene.Field(
        graphene.DateTime, description="Datetime when the session will end."
    )
    locale = graphene.String(description="Current locale of the user")

    @staticmethod
    def mutate(_root, info: ResolveInfo, username: str, password: str):
        request = get_request(info)
        gmp = get_gmp(info)
        try:
            response = gmp.authenticate(username, password)
            request.session['username'] = username
            request.session['password'] = password

            timezone = get_text_from_element(response, 'timezone')

            # get the timeout from now
            timeout = request.session.get_expiry_date()
            # actually store the timeout in the session
            request.session.set_expiry(timeout)

            setting_response = gmp.get_user_setting(USER_SETTING_LOCALE)
            setting_element = get_subelement(setting_response, 'setting')
            setting = get_text_from_element(setting_element, 'value')

            return LoginMutation(
                ok=True,
                timezone=timezone,
                session_timeout=timeout,
                locale=setting,
            )
        except GvmResponseError as e:
            raise AuthenticationFailed(e.message) from None


class LogoutMutation(graphene.Mutation):
    """Logout the current user"""

    ok = graphene.Boolean(description='Always true if no error occurred')

    @staticmethod
    def mutate(_root, info: ResolveInfo):
        request = get_request(info)
        request.session.flush()
        return LogoutMutation(ok=True)


class RenewSessionMutation(graphene.Mutation):
    """
    Renew the session of the current logged in user
    """

    current_user = graphene.Field(
        CurrentUser, description='Session information of the current user'
    )

    @staticmethod
    @require_authentication
    def mutate(_root, info: ResolveInfo):
        request = get_request(info)
        modification = django_timezone.now()
        expiry = request.session.get_session_cookie_age()
        session_timeout = modification + timedelta(seconds=expiry)
        request.session.set_expiry(session_timeout)
        # return True for current_user to activate resolvers of CurrentUser
        return RenewSessionMutation(current_user=True)
