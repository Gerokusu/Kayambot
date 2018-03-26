import asyncio
import discord
from . import scraper

MESSAGE_UNDEFINED_MONSTER = [
    "Je ne trouve pas le mon-monstre que vous spécifiez.",
    "Vous êtes sûr qu'un mon-monstre possède ce nom, oga ?",
    "Je ne me rappelle pas avoir déjà vu ce mon-monstre quelquepart."
]

# To add a command, simply create a function 'async def on_COMMAND(bot, message, arguments)'
# 'bot' is the original bot object
# 'message' is the original message object
# 'arguments' is an array containing all the command arguments

async def on_monster(bot, message, arguments):
    if len(arguments) > 0:
        monster_id = arguments[0]
        monster_url = scraper.URL_MONSTER.format(monster_id)
        parser = await scraper.get_site(bot, monster_url)
        if parser != None:
            monster_name = await scraper.get_text(bot, parser, "h3[itemprop='name']")
            monster_hp = await scraper.get_text(bot, parser, ".card .card-block .lead", 0) + "PV";
            monster_colour = discord.Colour(0x0B3372);
            monster_icon = scraper.URL_MONSTER_ICON.format(monster_id)

            embed = discord.Embed(title="", description=monster_hp, colour=monster_colour)
            embed.set_author(name=monster_name, url=monster_url, icon_url=scraper.URL_MONSTER_ICON_CONSTANT)
            embed.set_thumbnail(url=monster_icon)
            await bot.client.send_message(message.channel, "", embed=embed);
        else:
            await bot.speak(message.channel, MESSAGE_UNDEFINED_MONSTER)
