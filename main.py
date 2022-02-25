import asyncio

from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, Text, KeyboardButtonColor

from platforms import applemus, spotify, vk, yandex
import messages

# INIT BOT
bot = Bot(api=vk.vk)

KEYBOARD = Keyboard(one_time=False).add(Text("Информация"),color=KeyboardButtonColor.PRIMARY).get_json()


async def links_to_attached(url: str) -> None:
    # LINK FROM OTHER PLATFORMS TO VK AUDIO CASE
    await asyncio.sleep(10)
    if "spotify" in url: track_info = await spotify.get_info_by_url(url)
    elif "apple" in url: track_info = await applemus.get_info_by_url(url)
    elif "yandex" in url: track_info = await yandex.get_info_by_url(url)
    if not track_info or track_info == messages.NOT_FOUND:
        return None
    return await vk.get_track_id(track_info)


@bot.on.message(text="/start")
async def start(message: Message):
    # INIT DIALOG
    await message.answer(messages.WELCOME, keyboard=KEYBOARD)


@bot.on.message(text="Информация")
async def info(message: Message):
    # GET INFORMATION ABOUT BOT
    await message.answer(messages.INFO)


@bot.on.message(attachment="audio")
async def attached_to_links(message: Message):
    # WHEN USER ATTACHES AN VK AUDIO, BOT WILL SEND ITS LINKS FROM SUPPORTED PLATFPRMS
    audio_data = message.attachments[0].dict()
    query = f"{audio_data['audio']['artist']} {audio_data['audio']['title']}"
    spotify_link, yandex_link = await asyncio.gather(spotify.get_track_by_name(query),
                                                    yandex.get_track_by_name(query))
    links = f'Spotify\n{spotify_link}\nYandex Music\n{yandex_link}\nApple Music: В данный момент, сервис недоступен.'
    await message.answer(links)


@bot.on.message(attachment="link")
@bot.on.message(text=r"https://<!>")
async def link_to_attached(message: Message):
    # case when link is in attachment
    try: url = message.attachments[0].dict()['link']['url']
    # case when link is in message text
    except IndexError: url = message.text
    track_id = await links_to_attached(url)
    if track_id:
        await message.answer(messages.GOOD, attachment=f"audio{track_id}")
    else: message.answer(messages.ERROR)
            

bot.run_forever()
