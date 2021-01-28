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

from typing import Dict, Tuple

from graphene_django.views import GraphQLView
from graphql.error import GraphQLError

from django.conf import settings
from django.http import HttpResponse

from gvm.connections import UnixSocketConnection
from gvm.errors import GvmError, GvmResponseError, GvmClientError
from gvm.protocols.gmp import Gmp
from gvm.transforms import EtreeCheckCommandTransform

from selene.errors import SeleneError, AuthenticationRequired
from selene.schema import schema

DEFAULT_SETTINGS = {'GMP_SOCKET_PATH': '/var/run/gvmd.sock'}


class HttpResponeAuthenticationRequired(HttpResponse):
    status_code = 401


class SeleneView(GraphQLView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.settings = getattr(settings, 'SELENE', DEFAULT_SETTINGS)
        self.transform = EtreeCheckCommandTransform()

    def get_response(
        self, request, data, show_graphiql=False
    ) -> Tuple[str, int]:
        try:

            connection = UnixSocketConnection(
                path=self.settings['GMP_SOCKET_PATH']
            )

            with Gmp(connection=connection, transform=self.transform) as gmp:
                request.gmp = gmp

                if request.session.get('username'):
                    username = request.session['username']
                    password = request.session['password']
                    try:
                        gmp.authenticate(username, password)
                    except GvmResponseError as e:
                        result = self.get_error_result(
                            request, e, show_graphiql
                        )
                        return result, 403

                return super().get_response(request, data, show_graphiql)

        except GvmClientError as e:
            # not sure if the session should get flushed
            request.session.flush()

            result = self.get_error_result(request, e, pretty=show_graphiql)
            return result, 400
        except (ConnectionError, GvmError) as e:
            result = self.get_error_result(request, e, pretty=show_graphiql)
            return result, 500
        except AuthenticationRequired as e:
            # remove session information
            request.session.flush()

            result = self.get_error_result(request, e, pretty=show_graphiql)
            return result, e.httpStatusCode
        except SeleneError as e:
            result = self.get_error_result(request, e, pretty=show_graphiql)
            return result, e.httpStatusCode

    def get_error_result(
        self, request, error: Exception, pretty: bool = True
    ) -> Dict[str, str]:
        error_dict = {'message': str(error)}
        response = {'errors': [error_dict]}

        if isinstance(error, SeleneError):
            extension = {'errorCode': str(error.errorCode)}
            error_dict['extension'] = extension

        result = self.json_encode(request, response, pretty=pretty)
        return result

    @classmethod
    def format_error(  # pylint: disable=arguments-differ
        cls, graphql_error: GraphQLError
    ) -> Dict[str, str]:

        if getattr(graphql_error, 'original_error', None):
            # this is a hack to allow own http status response codes
            error = graphql_error.original_error
            if isinstance(error, SeleneError):
                raise error from graphql_error

        return super().format_error(graphql_error)


def main():
    return SeleneView.as_view(graphiql=True, schema=schema)
