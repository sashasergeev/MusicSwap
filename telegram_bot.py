import asyncio

from decouple import config
from telebot import types
from telebot.async_telebot import AsyncTeleBot

import messages
from platforms import VK, Apple, Spotify, Yandex

TOKEN = config('TELEGRAM_BOT_TOKEN')
bot = AsyncTeleBot(TOKEN)


async def gen_links_btns(spotify: str, yandex: str, vk: str):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(types.InlineKeyboardButton("Spotify", url=spotify),
                types.InlineKeyboardButton("Yandex Music", url=yandex),
                types.InlineKeyboardButton("VK",
                                            url=f"https://vk.com/audio{vk}"),
                types.InlineKeyboardButton("Apple (Недоступно)",
                                                callback_data="unavailable"))
    return markup 


@bot.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await bot.reply_to(message, messages.WELCOME)


@bot.message_handler(commands=['help'])
async def help_handler(message: types.Message):
    await bot.reply_to(message, messages.INFO)


@bot.message_handler(regexp=r'^https://')
async def convert_link(message: types.Message):
    url = message.text
    track_info = None
    if "spotify" in url: track_info = await Spotify.get_info_by_url(url)
    elif "apple" in url: track_info = await Apple.get_info_by_url(url)
    elif "yandex" in url: track_info = await Yandex.get_info_by_url(url)
    if not track_info or track_info == messages.NOT_FOUND:
        return await bot.reply_to(message, messages.ERROR)

    spotify_link, yandex_link, vk_link =  await asyncio.gather(
                            Spotify.get_track_by_name(track_info),
                            Yandex.get_track_by_name(track_info),
                            VK.get_track_id(track_info))

    await bot.reply_to(message, messages.GOOD,
                reply_markup= await gen_links_btns(
                                            spotify_link,
                                            yandex_link,
                                            vk_link))


async def main():
    await bot.set_my_commands([
        types.BotCommand("/help", "Информация о боте")
        ])
    await bot.polling()


if __name__ == '__main__':
    asyncio.run(main())
