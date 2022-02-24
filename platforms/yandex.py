import re

import aiohttp

from messages import NOT_FOUND as NOT_FOUND_MSG 

regex = r'https://music.yandex.ru/album/(\d+)/track/(\d+)'


async def get_info_by_url(url: str) -> str:
    match_ids = re.match(regex, url)
    body = {'with-positions': 'True', 'track-ids': f"{match_ids.group(2)}:{match_ids.group(1)}"}
    async with aiohttp.ClientSession() as session:
        url = 'https://api.music.yandex.net/tracks'
        async with session.post(url, data=body) as resp:
            try:
                info = (await resp.json())['result'][0]
                return f"{info['title']} {info['artists'][0]['name']}"
            except: return NOT_FOUND_MSG


async def get_track_by_name(query: str) -> str:
    params = [
        ('text', query), ('nocorrect', 'False'),
        ('type', 'all'), ('page', 0),
        ('playlist-in-best', 'True')
    ]
    async with aiohttp.ClientSession() as session:
        url = 'https://api.music.yandex.net/search'
        async with session.get(url, params=params) as resp:
            data = (await resp.json())['result']['best']
            if data and data['type'] == 'track':
                albumID = data['result']['albums'][0]['id']
                trackID = data['result']['id']        
                return f'https://music.yandex.ru/album/{albumID}/track/{trackID}'
            else: return NOT_FOUND_MSG
