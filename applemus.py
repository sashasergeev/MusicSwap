import re
import requests
from bs4 import BeautifulSoup

""" 
    Because of Apple Music Api requires Apple Developer Account,
    which i don't have, so bot won't output link.
"""

regex = r'music.apple.com/(\S+)'

def get_info_by_url(url: str) -> str:
    url = re.sub('com/\w+/', 'com/en/', url)
    req = requests.get(url).text
    data = BeautifulSoup(req, 'html.parser')
    return data.title.text[:-15].replace("by", " ")
