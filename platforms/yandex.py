import re
import requests

regex = r'https://music.yandex.ru/album/(\d+)/track/(\d+)'


def get_info_by_url(url: str) -> str:
    match_ids = re.match(regex, url)
    body = {'with-positions': 'True', 'track-ids': f"{match_ids.group(2)}:{match_ids.group(1)}"}
    info = requests.post('https://api.music.yandex.net/tracks', data=body)
    info = info.json()['result'][0]
    return f"{info['title']} {info['artists'][0]['name']}"


def get_track_by_name(query: str) -> str:
    params=[
        ('text', query), ('nocorrect', False),
        ('type', 'all'), ('page', 0),
        ('playlist-in-best', True)
    ]
    search_result = requests.get('https://api.music.yandex.net/search', params=params)
    search_result = search_result.json()
    best = search_result['result']['best']
    if best and best['type'] == "track":
        albumID = best['result']['albums'][0]['id']
        trackID = best['result']['id']
        return f'https://music.yandex.ru/album/{albumID}/track/{trackID}'
    else:
        return "Трек не был найден..."
