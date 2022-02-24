import aiohttp
import requests
import vk_api
from decouple import config

# VK AUTH
token = config('VK_AUTH_TOKEN')
vk = vk_api.VkApi(token=token)

# VK AUDIO API
token_audio = config('VK_AUTH_TOKEN_KATE')
user_agent = config('VK_AUTH_AGENT')
headers = {'User-Agent': user_agent}
sess = requests.session()
sess.headers.update({'User-Agent': user_agent})


def write_msg(user_id: int, random_id: int, message: str, song_id: str = None) -> None:
    if song_id is None:
        vk.method('messages.send', {'user_id': user_id,
                                    'random_id': random_id,
                                    'message': message})
    else:
        vk.method('messages.send', {'user_id': user_id,
                                    'random_id': random_id,
                                    'message': message,
                                    'attachment': f'audio{song_id}'})


async def get_track_id(searchTrack: str) -> str:
    params = [('access_token', token_audio),
            ('q', searchTrack),
            ('count', 1),
            ('v', '5.95')]
    async with aiohttp.ClientSession() as session:
        url = 'https://api.vk.com/method/audio.search'
        async with session.get(url, headers=headers, params=params) as resp:
            data = (await resp.json())['response']['items'][0]
            return f"{data['owner_id']}_{data['id']}"


async def get_audio_by_id(song_id: str) -> str:
    params=[('access_token', token_audio),
                ('audios', song_id),
                ('v', '5.95')]
    async with aiohttp.ClientSession() as session:
        url = 'https://api.vk.com/method/audio.getById'
        async with session.get(url, params=params, headers=headers) as resp:
            data = (await resp.json())['response'][0]
            artist = data['artist']
            title = data['title']
            return f"{artist} {title}"
