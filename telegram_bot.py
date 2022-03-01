import asyncio

from decouple import config
from telebot import types
from telebot.async_telebot import AsyncTeleBot

import messages
from platforms import VK, Apple, Spotify, Yandex

TOKEN = config('TELEGRAM_BOT_TOKEN')
bot = AsyncTeleBot(TOKEN)


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

    spotify_link, yandex_link = await asyncio.gather(Spotify.get_track_by_name(track_info),
                                                    Yandex.get_track_by_name(track_info))
    links = f'Spotify\n{spotify_link}\nYandex Music\n{yandex_link}\nApple Music: В данный момент, сервис недоступен.'
    await bot.reply_to(message, links)


async def main():
    await bot.set_my_commands([
        types.BotCommand("/help", "Информация о боте")
        ])
    await bot.polling()


if __name__ == '__main__':
    asyncio.run(main())
