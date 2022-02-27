import re

from asyncspotify import Client, ClientCredentialsFlow
from decouple import config

from messages import NOT_FOUND as NOT_FOUND_MSG 


class Spotify:
    # SPOTIFY AUTH
    spot_client_id: str = config('SPOTIFY_CLIENT_ID')
    spot_client_secret: str = config('SPOTIFY_CLIENT_SECRET')
    auth = ClientCredentialsFlow(
    client_id=spot_client_id,
    client_secret=spot_client_secret,
    )

    regex = r'spotify.com/track/(\S+)'

    @classmethod
    async def get_info_by_url(self, url: str) -> str:
        song_id = re.search(self.regex, url).group(1)
        async with Client(self.auth) as sp:
            track = await sp.get_track(song_id)
            if track: return f"{track.artists[0].name} {track.name}"
            else: return NOT_FOUND_MSG

    @classmethod
    async def get_track_by_name(self, name: str) -> str:
        async with Client(self.auth) as sp:
            item = await sp.search_track(q=name)
            if item: return f"https://open.spotify.com/track/{item.id}"
            else: return NOT_FOUND_MSG
