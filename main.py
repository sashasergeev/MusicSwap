import asyncio

from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkEventType, VkLongPoll
from vk_api.utils import get_random_id

from platforms import applemus, spotify, vk, yandex
import messages

# INIT BOT
longpoll = VkLongPoll(vk.vk)


# BOT INIT DIALOG
def init_bot(user_id: int) -> None:
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button("Информация",color=VkKeyboardColor.PRIMARY)
    vk.vk.method('messages.send', {'user_id': user_id,
                                    'random_id': get_random_id(),
                                    'message': messages.WELCOME,
                                    'keyboard': keyboard.get_keyboard()})


def send_msg(user_id: int, message: str) -> None:
    vk.write_msg(user_id, get_random_id(), message)


async def attached_to_links(event: VkEventType.MESSAGE_NEW) -> None:
    # VK ATTECHED AUDIO -> OTHER PLATFORMS
    audio_id = event.attachments.get('attach1')
    query = await vk.get_audio_by_id(audio_id)
    spotify_link, yandex_link = await asyncio.gather(spotify.get_track_by_name(query),
                                                    yandex.get_track_by_name(query))
    message = f'Spotify\n{spotify_link}\nYandex Music\n{yandex_link}\nApple Music: В данный момент, сервис недоступен.'
    vk.write_msg(event.user_id, event.message_id - 1000,
                                                message)


async def links_to_attached(event: VkEventType.MESSAGE_NEW, url: str) -> None:
    # LINK FROM OTHER PLATFORMS TO VK AUDIO CASE
    if "spotify" in url: track_info = await spotify.get_info_by_url(url)
    elif "apple" in url: track_info = await applemus.get_info_by_url(url)
    elif "yandex" in url: track_info = await yandex.get_info_by_url(url)

    if not track_info or track_info == messages.NOT_FOUND:
        return send_msg(event.user_id, messages.ERROR)

    track_id_vk = await vk.get_track_id(track_info)
    vk.write_msg(event.user_id, event.message_id - 1000,
                    "Приятного прослушивания!", track_id_vk)


async def main():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            ## TYPING STATUS IN THE DIALOG 
            vk.vk.method('messages.setActivity', {'type':'typing', 'peer_id':int(event.user_id)})
            
            ## INIT DIALOG WITH USER - ADD INFO BTN
            if event.text == "/start":
                init_bot(event.user_id)
                continue # QUIT
            elif event.text == "Информация":
                send_msg(event.user_id, messages.INFO)
                continue # QUIT

            # GET LINK OR ATTACHED AUDIO ID 
            is_audio_attached = event.attachments.get('attach1_type') == "audio"
            url = event.text or event.attachments.get('attach1_url')
            
            # WHEN THERE'S NOTHING TO CONVERT
            if not url and not is_audio_attached:
                send_msg(event.user_id, messages.ERROR)
                continue # QUIT

            # VK AUDIO -> PLATFOWM LINKS
            elif is_audio_attached: await attached_to_links(event)
            # PLATFORM LINKS -> VK AUDIO
            elif url: await links_to_attached(event, url)
            

if __name__ == "__main__": asyncio.run(main())
