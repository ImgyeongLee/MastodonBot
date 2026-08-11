#!/usr/bin/python3
from mastodon import Mastodon

import config

mastodon = Mastodon(
    client_id=config.MASTODON_CLIENT_ID,
    client_secret=config.MASTODON_CLIENT_SECRET,
    access_token=config.MASTODON_ACCESS_TOKEN,
    api_base_url=config.MASTODON_API_BASE_URL,
)
