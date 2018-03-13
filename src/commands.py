import datetime
import discord
import asyncio
import kayambot

# To add a command, simply create a function 'async def on_COMMAND(client, message, arguments)'
# 'client' is the original client object
# 'message' is the original message object
# 'arguments' is an array containing all the command arguments

async def on_monster(client, message, arguments):
    if len(arguments) > 0:
        embed = discord.Embed(title="Lagiacrus", description="Roi des mers", colour=discord.Colour(0x0B3372))
        embed.set_author(name="Lagiacrus", url="http://mhgen.kiranico.com/fr/monstre/lagiacrus", icon_url="https://grox2006.github.io/Kayambot/resources/images/thumbnails/icon_monster.png")
        embed.set_thumbnail(url="https://grox2006.github.io/Kayambot/resources/images/thumbnails/monster_lagiacrus.png")
        await client.send_message(message.channel, "", embed=embed);
