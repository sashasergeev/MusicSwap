import aiohttp

from decouple import config
from vkbottle import API


class VK:
    # VK AUTH
    token = config('VK_AUTH_TOKEN')
    api = API(token, True)

    # VK AUDIO API
    token_audio = config('VK_AUTH_TOKEN_KATE')
    user_agent = config('VK_AUTH_AGENT')
    headers = {'User-Agent': user_agent}

    @classmethod
    async def get_track_id(self, searchTrack: str) -> str:
        params = [('access_token', self.token_audio),
                ('q', searchTrack),
                ('count', 1),
                ('v', '5.95')]
        async with aiohttp.ClientSession() as session:
            url = 'https://api.vk.com/method/audio.search'
            async with session.get(url, headers=self.headers, params=params) as resp:
                data = (await resp.json())['response']['items'][0]
                return f"{data['owner_id']}_{data['id']}"


# async def get_audio_by_id(song_id: str) -> str:
#     params=[('access_token', token_audio),
#                 ('audios', song_id),
#                 ('v', '5.95')]
#     async with aiohttp.ClientSession() as session:
#         url = 'https://api.vk.com/method/audio.getById'
#         async with session.get(url, params=params, headers=headers) as resp:
#             data = (await resp.json())['response'][0]
#             artist = data['artist']
#             title = data['title']
#             return f"{artist} {title}"
