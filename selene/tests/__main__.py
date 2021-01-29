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

import os
import sys

from pathlib import Path

import django

from django.conf import settings
from django.test.utils import get_runner


def main():
    cwd = Path(__file__).absolute().parent
    sys.path.insert(0, str(cwd))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    django.setup()
    test_runner_cls = get_runner(settings)
    test_runner = test_runner_cls()
    failures = test_runner.run_tests(test_labels=None)
    sys.exit(bool(failures))


if __name__ == "__main__":
    main()
