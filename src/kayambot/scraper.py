import urllib.request
from bs4 import BeautifulSoup

LOG_CONNECTION_SUCCESS = "Successfully connected to {}"
LOG_CONNECTION_FAILURE = "Could not connect to {}"
LOG_DIV_FOUND = "Successfully found div '{}' at index {} : '{}'"
LOG_DIV_NOTFOUND = "Could not find div '{}' at index {}"

URL_MONSTER = "http://mhgen.kiranico.com/fr/monstre/{}"
URL_MONSTER_ICON = "https://grox2006.github.io/Kayambot/resources/images/thumbnails/monster_{}.png"
URL_MONSTER_ICON_CONSTANT = "https://grox2006.github.io/Kayambot/resources/images/thumbnails/icon_monster.png"
URL_HEADER = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'fr-FR,en;q=0.8',
    'Connection': 'keep-alive'
}

async def get_site(bot, url):
    parser = None
    try:
        parser = BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url, headers=URL_HEADER)).read(), "lxml")
        bot.log_ok(LOG_CONNECTION_SUCCESS, url)
    except Exception:
        bot.log_error(LOG_CONNECTION_FAILURE, url)
    return parser;

async def get_text(bot, parser, selector, index = 0):
    result = ""
    response = parser.select(selector)
    if len(response) > index:
        result = response[index].getText()
        bot.log_ok(LOG_DIV_FOUND, selector, index, response[index])
    else:
        bot.log_error(LOG_DIV_NOTFOUND, selector, index)
    return result
