import asyncio

from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Bot, Message

import messages
from platforms import VK, Apple, Spotify, Yandex

# INIT BOT
bot = Bot(api=VK.api)

KEYBOARD = Keyboard(one_time=False).add(Text("Информация"),color=KeyboardButtonColor.PRIMARY).get_json()


async def links_to_attached(url: str) -> None:
    # LINK FROM OTHER PLATFORMS TO VK AUDIO CASE
    track_info = None
    if "spotify" in url: track_info = await Spotify.get_info_by_url(url)
    elif "apple" in url: track_info = await Apple.get_info_by_url(url)
    elif "yandex" in url: track_info = await Yandex.get_info_by_url(url)
    if not track_info or track_info == messages.NOT_FOUND:
        return None
    return await VK.get_track_id(track_info)


@bot.on.message(text="/start")
async def start(message: Message):
    # INIT DIALOG
    await message.answer(messages.WELCOME, keyboard=KEYBOARD)


@bot.on.message(text="Информация")
async def info(message: Message):
    # GET INFORMATION ABOUT BOT
    await message.answer(messages.INFO)


@bot.on.message(attachment="audio")
async def attached_to_links(message: Message, from_id: int = None):
    user_id = from_id or message.from_id
    # WHEN USER ATTACHES AN VK AUDIO, BOT WILL SEND ITS LINKS FROM SUPPORTED PLATFPRMS
    audio_data = message.attachments[0].dict()
    query = f"{audio_data['audio']['artist']} {audio_data['audio']['title']}"
    spotify_link, yandex_link = await asyncio.gather(Spotify.get_track_by_name(query),
                                                    Yandex.get_track_by_name(query))
    links = f'Spotify\n{spotify_link}\nYandex Music\n{yandex_link}\nApple Music: В данный момент, сервис недоступен.'
    await bot.api.messages.send(peer_id=user_id, message=links, random_id=0)



@bot.on.message(attachment="link")
@bot.on.message(text=r"https://<!>")
async def link_to_attached(message: Message, from_id: int = None):
    user_id = from_id or message.from_id
    # case when link is in attachment
    try: url = message.attachments[0].dict()['link']['url']
    # case when link is in message text
    except IndexError: url = message.text
    track_id = await links_to_attached(url)
    if track_id:
        await bot.api.messages.send(peer_id=user_id,
                                    message=messages.GOOD,
                                    attachment=f"audio{track_id}",
                                    random_id = 0)
    else:
        await bot.api.messages.send(peer_id=user_id, message=messages.ERROR, random_id=0)
            

@bot.on.message(func = lambda message: len(message.fwd_messages) > 0)
async def forwarded_messages(message: Message):
    forwarded_message = message.fwd_messages[0]
    user_id = message.from_id
    try: attachments = forwarded_message.attachments[0].dict()
    except IndexError: attachments = {}
    
    if attachments['audio']: 
        await attached_to_links(forwarded_message, user_id)
    else:
        await link_to_attached(forwarded_message, user_id)


bot.run_forever()
