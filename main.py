import vk
import spotify

import re
from vk_api.longpoll import VkEventType


for event in vk.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        # print("Attachments: ", event.attachments)
        # print("Raw: ", event.raw)
        url = event.text

        attached_url = event.attachments.get('attach1_url')
        is_audio_attached = event.attachments.get('attach1_type') == "audio"
        if (re.search(spotify.regex, url) or attached_url and
                    re.search(spotify.regex, attached_url)): # SPOTIFY LINK IN MSG OR ATTACHED
            # SPOTIFY LINK -> VK  
            # get track title from spotify
            if not url: url = event.attachments['attach1_url']
            track = spotify.get_track_by_id(url)
            # vk - get track id and send message with attachment
            track_id_vk = vk.get_track_id(track)
            vk.write_msg(event.user_id, event.message_id - 1000,
                            "Приятного прослушивания!", track_id_vk)
        elif is_audio_attached: # VK AUDIO ATTCHED CASE
            # VK ATTECHED AUDIO -> SPOTIFY
            audio_id = event.attachments.get('attach1')
            track_info = vk.get_audio_by_id(audio_id)
            track_spotify_link = spotify.get_track_by_name(track_info)
            vk.write_msg(event.user_id, event.message_id - 1000,
                        track_spotify_link)
        else:
            vk.write_msg(event.user_id, event.message_id - 1000,
                                        "Couldn't find anything...")




                