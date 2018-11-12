
# Copyright (c) 2018, Yaroslav Zotov, https://github.com/qiray/
# All rights reserved.

# This file is part of MarkovTextGenerator.

# MarkovTextGenerator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# MarkovTextGenerator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with MarkovTextGenerator.  If not, see <https://www.gnu.org/licenses/>.

import tweepy
import secrets

def get_api(cfg):
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)

def tweet(text, favorite):
    # Fill in the values noted in previous step here
    cfg = secrets.cfg
    api = get_api(cfg)
    status = api.update_status(status=text)
    if favorite and status.id:
        status = api.create_favorite(status.id)
    print(status)
