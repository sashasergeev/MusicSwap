from platforms import vk, yandex, spotify, applemus
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id


# BOT DEFAULT MESSAGES
WELCOME_MSG = ('Добро пожаловать!\n Для конвертирования мызыки с одной'
            ' платформы на другую, предоставьте ссылку или прикрепите аудиозапись.')
ERROR_MSG = ('Пожалуйста, повторите попытку.\Обратите внимание на то,'
            ' что бот не принимает пересланные сообщения как источник аудио.')
INFO_MSG = ('Для конвертирования мызыки с одной платформы на другую, '
            'предоставьте ссылку или прикрепите аудиозапись. На данный момент,'
            ' бот не считывает аудиозапись из пересланного сообщения')


# INIT BOT
longpoll = VkLongPoll(vk.vk)


# BOT INIT DIALOG
def init_bot(user_id: int) -> None:
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button("Информация",color=VkKeyboardColor.PRIMARY)
    vk.vk.method('messages.send', {'user_id': user_id,
                                    'random_id': get_random_id(),
                                    'message': WELCOME_MSG,
                                    'keyboard': keyboard.get_keyboard()})


def send_msg(user_id: int, message: str) -> None:
    vk.write_msg(user_id, get_random_id(), message)


def attached_to_links(event: VkEventType.MESSAGE_NEW) -> None:
    # VK ATTECHED AUDIO -> OTHER PLATFORMS
    audio_id = event.attachments.get('attach1')
    query = vk.get_audio_by_id(audio_id)
    spotify_link = spotify.get_track_by_name(query)
    yandex_link = yandex.get_track_by_name(query)

    message = f'Spotify\n{spotify_link}\nYandex Music\n{yandex_link}\nApple Music: В данный момент, сервис недоступен.'
                
    vk.write_msg(event.user_id, event.message_id - 1000,
                                                message)


def links_to_attached(event: VkEventType.MESSAGE_NEW, url: str) -> None:
    # LINK FROM OTHER PLATFORMS TO VK AUDIO CASE
    if "spotify" in url: track_info = spotify.get_track_by_id(url)
    elif "apple" in url: track_info = applemus.get_info_by_url(url)
    elif "yandex" in url: track_info = yandex.get_info_by_url(url)
    else: return send_msg(event.user_id, ERROR_MSG)
    track_id_vk = vk.get_track_id(track_info)
    vk.write_msg(event.user_id, event.message_id - 1000,
                    "Приятного прослушивания!", track_id_vk)


for event in vk.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        ## TYPING STATUS IN THE DIALOG 
        vk.vk.method('messages.setActivity', {'type':'typing', 'peer_id':int(event.user_id)})
        
        ## INIT DIALOG WITH USER - ADD INFO BTN
        if event.text == "/start":
            init_bot(event.user_id)
            continue # QUIT
        elif event.text == "Информация":
            send_msg(event.user_id, INFO_MSG)
            continue

        # GET LINK OR ATTACHED AUDIO ID 
        is_audio_attached = event.attachments.get('attach1_type') == "audio"
        url = event.text or event.attachments.get('attach1_url')
        
        # WHEN THERE'S NOTHING TO CONVERT
        if not url and not is_audio_attached:
            send_msg(event.user_id, ERROR_MSG)
            continue # QUIT

        # VK AUDIO -> PLATFOWM LINKS
        elif is_audio_attached: attached_to_links(event)
        # PLATFORM LINKS -> VK AUDIO
        elif url: links_to_attached(event, url)
