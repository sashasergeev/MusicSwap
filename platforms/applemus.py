import re

from bs4 import BeautifulSoup
import aiohttp

""" 
    Because of Apple Music Api requires Apple Developer Account,
    which i don't have, bot won't output link.
"""


class Apple:
    """ GETTING DATA FROM APPLE MUSIC """
    regex = r'music.apple.com/(\S+)'

    @classmethod
    async def get_info_by_url(self, url: str) -> str:
        url = re.sub('com/\w+/', 'com/en/', url)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.read()
        data = BeautifulSoup(data, 'html.parser')
        return data.title.text[:-15].replace("by", " ")
