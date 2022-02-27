import re
from typing import Optional

import aiohttp
from messages import NOT_FOUND as NOT_FOUND_MSG


class Yandex:
    """ BOTS ACCESS TO YANDEX API """
    regex = r'https://music.yandex.ru/album/(\d+)/track/(\d+)'

    async def _request(self,
                        section: str,
                        params: Optional[list] = [],
                        body: Optional[dict] = {},
                        method: str = 'get'):
        async with aiohttp.ClientSession() as session:
            url = f'https://api.music.yandex.net/{section}'
            if method == 'get':
                async with session.get(url, params=params) as resp:
                    return await resp.json()
            elif method == 'post':
                async with session.post(url, data=body) as resp:
                    return await resp.json()

    @classmethod
    async def get_info_by_url(self, url: str) -> str:
        match_ids = re.match(self.regex, url)
        body = {'with-positions': 'True', 
                'track-ids': f"{match_ids.group(2)}:{match_ids.group(1)}"}
        try: 
            info = await self._request(self,
                                        section='tracks',
                                        body=body,
                                        method='post')
            info = info['result'][0]
            return f"{info['title']} {info['artists'][0]['name']}"
        except: return NOT_FOUND_MSG

    @classmethod
    async def get_track_by_name(self, query: str) -> str:
        params = [
            ('text', query), ('nocorrect', 'False'),
            ('type', 'all'), ('page', 0),
            ('playlist-in-best', 'True')
        ]
        data = await self._request(self, section='search', params=params)
        data = data['result']['best']
        if data and data['type'] == 'track':
            albumID = data['result']['albums'][0]['id']
            trackID = data['result']['id']        
            return f'https://music.yandex.ru/album/{albumID}/track/{trackID}'
        else: return NOT_FOUND_MSG
