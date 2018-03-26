import os
import asyncio
import discord

# To add a command, simply create a function 'async def on_COMMAND(bot, message, arguments)'
# 'bot' is the original bot object
# 'message' is the original message object
# 'arguments' is an array containing all the command arguments

PATH_SONGS = "resources/songs"
JSON_MEMORY_KEY_CHANNEL = "channel"
MESSAGE_PLAY = "Mes moustaches frémissent ! En avant pour {}, volume {} !"
MESSAGE_STOP = "Vous souhaitez un peu de silence, miaou ?"
MESSAGE_INVALID_SONG = "J'ai une grosse bibliothèque, mais je ne trouve pas votre chanson, miaître..."
MESSAGE_NO_SONG = "Vous devez prrréciser une musique, mon chaton."
MESSAGE_NO_CHANNEL = "Vous devez rejoindre un chat-nal vocal d'abord !"
MESSAGE_MEMORY_CHANNEL_SUCCESSFUL = "Ce canal sera miaoutilisé pour mes futures envolées artistiques !"
MESSAGE_MEMORY_CHANNEL_FAILURE = "Ce chat-nal est déjà mon lieu de travail !"

async def on_channel(bot, message, arguments):
    channel = message.channel
    if channel != None:
        if await bot.getmem(JSON_MEMORY_KEY_CHANNEL) != channel.id:
            await bot.setmem(JSON_MEMORY_KEY_CHANNEL, channel.id)
            await bot.speak(MESSAGE_MEMORY_CHANNEL_SUCCESSFUL);
        else:
            await bot.speak(MESSAGE_MEMORY_CHANNEL_FAILURE);

async def on_play(bot, message, arguments):
    channel = message.author.voice.voice_channel
    if channel != None:
        if len(arguments) > 0:
            song_title = arguments[0]
            voice = await get_voice(bot, channel)
            if voice != None and not is_playing(bot):
                song_path = bot.get_path(PATH_SONGS + "/" + song_title)
                song_volume = int(arguments[1]) if len(arguments) > 1 else 2
                song_volume = song_volume if song_volume <= 100 else 100
                if os.path.isfile(song_path):
                    bot.player = voice.create_ffmpeg_player(song_path, options="-af volume=" + str(song_volume / 100))
                    bot.player.start()
                    await bot.speak(MESSAGE_PLAY.format(song_title, song_volume));
                else:
                    await bot.speak(MESSAGE_INVALID_SONG);
        else:
            await bot.speak(MESSAGE_NO_SONG);
    else:
        await bot.speak(MESSAGE_NO_CHANNEL);


async def on_stop(bot, message, arguments):
    if is_playing(bot):
        bot.player.stop()
        await bot.speak(MESSAGE_STOP);

def is_playing(bot):
    return hasattr(bot, "player") and bot.player != None and bot.player.is_playing()

async def get_voice(bot, channel):
    voice = None
    if channel != None:
        for voice_client in bot.client.voice_clients:
            if voice_client.channel == channel:
                voice = voice_client
        if voice == None:
            voice = await bot.client.join_voice_channel(channel)
    return voice;
