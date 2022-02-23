from decouple import config
import json
import vk_api
import requests

# VK AUTH
token = config('VK_AUTH_TOKEN')
vk = vk_api.VkApi(token=token)

# VK AUDIO API
token_audio = config('VK_AUTH_TOKEN_KATE')
user_agent = config('VK_AUTH_AGENT')
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


def get_track_id(searchTrack: str) -> str:
    audio = sess.get(
        'https://api.vk.com/method/audio.search',
        params=[('access_token', token_audio),
                ('q', searchTrack),
                ('count', 1),
                ('v', '5.95')]
    )
    data = json.loads(audio.text)['response']['items'][0]
    return f"{data['owner_id']}_{data['id']}"


def get_audio_by_id(song_id: str) -> str:
    audio = sess.get(
        'https://api.vk.com/method/audio.getById',
        params=[('access_token', token_audio),
                ('audios', song_id),
                ('v', '5.95')]
    )
    data = json.loads(audio.text)['response'][0]
    artist = data['artist']
    title = data['title']
    return f"{artist} {title}"
