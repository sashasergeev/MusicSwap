from platforms import vk
from platforms import yandex
from platforms import spotify
from platforms import applemus

from vk_api.longpoll import VkEventType


def attached_to_links(event) -> None:
    # VK ATTECHED AUDIO -> OTHER PLATFORMS
    audio_id = event.attachments.get('attach1')
    query = vk.get_audio_by_id(audio_id)
    spotify_link = spotify.get_track_by_name(query)
    yandex_link = yandex.get_track_by_name(query)

    message = f'''Spotify: {spotify_link}
                Apple Music: Not Available Right Now.
                Yandex Music: {yandex_link}
                '''
    vk.write_msg(event.user_id, event.message_id - 1000,
                                                message)


def links_to_attached(url: str) -> None:
    # LINK FROM OTHER PLATFORMS TO VK AUDIO CASE
    if "spotify" in url: track_info = spotify.get_track_by_id(url)
    elif "apple" in url: track_info = applemus.get_info_by_url(url)
    elif "yandex" in url: track_info = yandex.get_info_by_url(url)
    else: return
    track_id_vk = vk.get_track_id(track_info)
    vk.write_msg(event.user_id, event.message_id - 1000,
                    "Приятного прослушивания!", track_id_vk)


for event in vk.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        is_audio_attached = event.attachments.get('attach1_type') == "audio"
        url = event.text or event.attachments.get('attach1_url')
        # VK AUDIO -> PLATFOWM LINKS
        if is_audio_attached: attached_to_links(event)
        # PLATFORM LINKS -> VK AUDIO
        else: links_to_attached(url)
