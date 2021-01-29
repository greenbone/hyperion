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

import json

import xml.etree.ElementTree as ET

from unittest.mock import create_autospec, patch, MagicMock

from django.http import HttpResponse
from django.test import TestCase

from gvm.errors import GvmResponseError

from gvm.protocols.gmpv214 import Gmp


from selene.schema import schema


class GmpMockFactory:
    def __init__(self, *args, **kwargs):  # pylint: disable=unused-argument
        gmp_protocol_mock = create_autospec(Gmp)

        self.gmp_protocol = gmp_protocol_mock
        self.gmp = MagicMock()
        self.gmp.__enter__.return_value = gmp_protocol_mock

    def __call__(self, *args, **kwargs):
        return self.gmp

    def fail_authentication(self):
        self.gmp_protocol.authenticate = MagicMock(
            side_effect=GvmResponseError(
                status='401', message='Authentication failed'
            )
        )

    def mock_response(self, request_name: str, content: str):
        func = getattr(self.gmp_protocol, request_name)
        func.return_value = ET.fromstring(content)

    def assert_authenticated_with(self, username: str, password: str):
        self.gmp_protocol.authenticate.assert_called_with(username, password)


class SeleneTestCase(TestCase):
    GRAPHQL_SCHEMA = schema
    GRAPHQL_URL = "/graphql/"

    def login(self, username: str, password: str):
        session = self.client.session

        session['username'] = username
        session['password'] = password
        session.save()

    def query(
        self,
        query: str,
        op_name: str = None,
        input_data: dict = None,
        variables: dict = None,
        headers: dict = None,
    ):
        """
        Args:
            query (string)    - GraphQL query to run
            op_name (string)  - If the query is a mutation or named query, you
                                must supply the op_name. For anon queries
                                ("{ ... }"), should be None (default).
            input_data (dict) - If provided, the $input variable in GraphQL
                                will be set to this value. If both
                                ``input_data`` and ``variables``, are provided,
                                the ``input`` field in the ``variables``
                                dict will be overwritten with this value.
            variables (dict)  - If provided, the "variables" field in GraphQL
                                will be set to this value.
            headers (dict)    - If provided, the headers in POST request to
                                GRAPHQL_URL will be set to this value.

        Returns:
            Response object from client
        """
        body = {"query": query}
        if op_name:
            body["operation_name"] = op_name
        if variables:
            body["variables"] = variables
        if input_data:
            if variables in body:
                body["variables"]["input"] = input_data
            else:
                body["variables"] = {"input": input_data}
        if headers:
            resp = self.client.post(
                self.GRAPHQL_URL,
                json.dumps(body),
                content_type="application/json",
                **headers,
            )
        else:
            resp = self.client.post(
                self.GRAPHQL_URL,
                json.dumps(body),
                content_type="application/json",
            )
        return resp

    def assertResponseNoErrors(
        self, response: HttpResponse
    ):  # pylint: disable=invalid-name
        content = response.json()
        errors = content.get('errors')

        self.assertIsNone(errors, 'Response has errors')

    def assertResponseHasErrors(
        self, response: HttpResponse
    ):  # pylint: disable=invalid-name
        """
        Assert that the call was failing. Take care: Even with errors, GraphQL
        may return status 200!
        """
        content = response.json()
        errors = content.get('errors')

        self.assertIsNotNone(errors, 'Response has no errors')

    def assertResponseHasErrorMessage(
        self, response: HttpResponse, expected: str, msg: str = None
    ):  # pylint: disable=invalid-name
        content = response.json()
        errors = content.get('errors')

        self.assertIsNotNone(errors, 'Response has no errors')

        messages = [error.get('message') for error in errors]

        self.assertIn(expected, messages, msg)

    def assertResponseStatusCode(
        self,
        response: HttpResponse,
        expected: int,
        msg: str = 'Response status code does not match',
    ):  # pylint: disable=invalid-name
        self.assertEqual(response.status_code, expected, msg)

    def assertResponseAuthenticationRequired(
        self, response: HttpResponse
    ):  # pylint: disable=invalid-name
        self.assertResponseStatusCode(response, 401)
        self.assertResponseHasErrorMessage(response, 'Not Authorized')
