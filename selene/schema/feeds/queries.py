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

from selene.schema.base import ListQuery, SingleObjectQuery
from selene.schema.feeds.fields import Feed, FeedType
from selene.schema.utils import get_gmp, require_authentication, XmlElement


class GetFeed(SingleObjectQuery):
    """Get a single feed

    Example:

        query {
            feed (feedType: NVT) {
                name
                version
                description
                type
                currentlySyncing
            }
        }

    Response:

    {
        "data": {
            "feed": {
                "name": "Greenbone Security Feed",
                "version": "202010220502",
                "description": "This script synchronizes [...]",
                "type": "NVT",
                "currentlySyncing": True,
            }
        }
    }


    """

    object_type = Feed
    kwargs = {
        'feed_type': FeedType(required=True, description="Requested Feed type")
    }

    @staticmethod
    @require_authentication
    def resolve(_root, info, feed_type: str):
        gmp = get_gmp(info)

        gmp_feed_type = FeedType.get(feed_type)

        xml = gmp.get_feed(gmp_feed_type)
        return xml.find('feed')


class GetFeeds(ListQuery):
    """Gets a list of all feeds

    Example:

        query {
            feeds {
                type
                name
                version
            }
        }

    Response:


        {
            "data": {
                "feeds": [
                    {
                        "type": "NVT",
                        "name": "Greenbone Security Feed",
                        "version": "202010220502"
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

    object_type = Feed

    @staticmethod
    @require_authentication
    def resolve(_root, info):
        gmp = get_gmp(info)

        xml: XmlElement = gmp.get_feeds()

        return xml.findall('feed')
