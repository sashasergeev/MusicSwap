import re
from decouple import config
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# SPOTIFY AUTH
spot_client_id: str = config('SPOTIFY_CLIENT_ID')
spot_client_secret: str = config('SPOTIFY_CLIENT_SECRET')
auth_manager = SpotifyClientCredentials(spot_client_id, spot_client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

regex = r'spotify.com/track/(\S+)'


def extract_id_from_url(url: str) -> str:
    song_id = re.search(regex, url).group(1)
    return song_id


def track_by_id(song_id:str) -> str:
    """ this function takes song id and outputs artist name and track title """
    track = sp.track(song_id)
    return f"{track['artists'][0]['name']} {track['name']}"


def get_track_by_id(url: str) -> str:
    song_id = extract_id_from_url(url)
    return track_by_id(song_id)


def get_track_by_name(name: str) -> str:
    try:
        item = sp.search(name, 1)
        return item['tracks']['items'][0]['external_urls']['spotify']
    except IndexError: # error when audio wasn't found
        return "Трек не был найден..."
