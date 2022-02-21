import re
from yandex_music import Client

client = Client().init()

regex = r'https://music.yandex.ru/album/(\d+)/track/(\d+)'


def get_info_by_url(url: str) -> str:
    match_ids = re.match(regex, url)
    info = client.tracks(f"{match_ids.group(2)}:{match_ids.group(1)}")[0]
    return f"{info['title']} {info['artists'][0]['name']}"


def get_track_by_name(query: str) -> str:
    search_result = client.search(query)
    best = search_result.best
    if best and best.type == "track":
        return f'https://music.yandex.ru/album/{best.result.albums[0].id}/track/{best.result.id}'
