# :headphones: MusicSwap 
#### [:link: TELEGRAM BOT :link:](https://telegram.me/MusicSwapBot)
#### [:link: VK BOT :link:](https://vk.com/im?sel=-207239765)
**Nowadays, there is a wide market of media platforms on which you can listen music. The problem is that you and your friends can use different platforms which makes music sharement time consuming.
In order to make this process easier and faster this bot was created.**

### How it works
User sends attached track *or* track link to bot and receives links to this track on other platforms.
Bot also works with group chats.

This project contain **2 bots**: one for **VK** and another if for **Telegram**.

## Faced problems :imp:
1. Closed VK Audio api
    
    So, to access audio data, i needed to imitate that api requests is made from kate mobile app, which is done by passing user agent and specific token, which i obtained with [vkaudiotoken library](https://github.com/vodka2/vkaudiotoken-python),
2. Apple Music paid api
  
    I don't retrieve apple music data through api, i instead, scrape data off their site. Bot can accept apple music link and output links from other platforms, but can't generate its link because don't have access to search api.
3. Slowness
    
    At first, this bot was synchronous and in order to take new task from queue it have needed to wait until previous one is fully finished.
    To make application more productive, i implemented asynchronous execution of tasks. 

## Supported platforms :recycle:
- [VK](https://vk.com/)
- [Spotify](https://spotify.com/)
- [Yandex Music](https://music.yandex.com/)
- [Apple Music](https://music.apple.com/)


## Used libraries/tools :electric_plug:
> aiohttp - for making requests   
> python decouple - enviroment variables  
> beautifulsoup4 - scrape data from apple music   
> async spotify - to obtain data about tracks on spotify    
> vkbottle - bot functionality and to obtain data about tracks on vk    
> Docker
