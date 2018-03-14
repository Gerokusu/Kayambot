import datetime
import discord
import asyncio
import kayambot
import scraper

MESSAGE_UNDEFINED_MONSTER = [
    "Je ne trouve pas le mon-monstre que vous spécifiez.",
    "Vous êtes sûr qu'un mon-monstre possède ce nom, oga ?",
    "Je ne me rappelle pas avoir déjà vu ce mon-monstre quelquepart."
]

# To add a command, simply create a function 'async def on_COMMAND(client, message, arguments)'
# 'client' is the original client object
# 'message' is the original message object
# 'arguments' is an array containing all the command arguments

async def on_monster(client, message, arguments):
    if len(arguments) > 0:
        parser = await scraper.get_site(scraper.URL_MONSTER + arguments[0])
        if parser != None:
            monster_name = await scraper.get_text(parser, "h3[itemprop='name']")
            monster_hp = await scraper.get_text(parser, ".card .card-block .lead", 0) + "PV";

            embed = discord.Embed(title="", description=monster_hp, colour=discord.Colour(0x0B3372))
            embed.set_author(name=monster_name, url="http://mhgen.kiranico.com/fr/monstre/lagiacrus", icon_url="https://grox2006.github.io/Kayambot/resources/images/thumbnails/icon_monster.png")
            embed.set_thumbnail(url="https://grox2006.github.io/Kayambot/resources/images/thumbnails/monster_lagiacrus.png")
            await client.send_message(message.channel, "", embed=embed);
        else:
            await kayambot.speak(message.channel, MESSAGE_UNDEFINED_MONSTER)
