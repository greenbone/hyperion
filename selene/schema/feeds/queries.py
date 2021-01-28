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

import graphene

from gvm.protocols.latest import FeedType as GmpFeedType

from selene.schema.feeds.fields import Feed, FeedType
from selene.schema.utils import get_gmp, require_authentication, XmlElement


class GetFeed(graphene.Field):
    """Gets a single feed

    Example:

    .. code-block::
        query {
            feed (feedType: NVT) {
                name
                version
                description
                type
                syncNotAvailable {
                    error
                }
                currentlySyncing {
                    timestamp
                }
            }
        }

    Response:

    .. code-block::

    {
        "data": {
            "feed": {
                "name": "Greenbone Security Feed",
                "version": "202010220502\n",
                "description": "This script synchronizes [...]",
                "type": "NVT",
                "syncNotAvailable": null,
                "currentlySyncing": {
                    "timestamp": "Mon Nov 16 14:32:26 2020"
                }
            }
        }
    }


    """

    def __init__(self):
        super().__init__(
            Feed,
            feed_type=FeedType(required=True),
            resolver=self.resolve,
        )

    @staticmethod
    @require_authentication
    def resolve(_root, info, feed_type: str):
        gmp = get_gmp(info)

        if feed_type == FeedType.CERT:
            gmp_feed_type = GmpFeedType.CERT
        elif feed_type == FeedType.SCAP:
            gmp_feed_type = GmpFeedType.SCAP
        elif feed_type == FeedType.NVT:
            gmp_feed_type = GmpFeedType.NVT

        xml = gmp.get_feed(gmp_feed_type)
        return xml.find('feed')


class GetFeeds(graphene.List):
    """Gets a list of all feeds

    Args:
        filter_string (str, optional): Optional filter string to be
            used with query.

    Example:

        .. code-block::

            query {
                feeds {
                    type
                    name
                    version
                }
            }

        Response:

        .. code-block::

        {
            "data": {
                "feeds": [
                    {
                        "type": "NVT",
                        "name": "Greenbone Security Feed",
                        "version": "202010220502\n"
                    },
                    {
                        "type": "SCAP",
                        "name": "Greenbone Community SCAP Feed",
                        "version": "202011130230"
                    },
                    {
                        "type": "CERT",
                        "name": "Greenbone CERT Feed",
                        "version": "202010220030"
                    },
                    {
                        "type": "GVMD_DATA",
                        "name": "Greenbone gvmd Data Feed",
                        "version": "202010160853"
                    }
                ]
            }
        }

    """

    def __init__(self):
        super().__init__(Feed, resolver=self.resolve)

    @staticmethod
    @require_authentication
    def resolve(_root, info):
        gmp = get_gmp(info)

        xml: XmlElement = gmp.get_feeds()

        return xml.findall('feed')
