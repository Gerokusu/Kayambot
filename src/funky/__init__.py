import asyncio
import discord

# To add a command, simply create a function 'async def on_COMMAND(bot, message, arguments)'
# 'bot' is the original bot object
# 'message' is the original message object
# 'arguments' is an array containing all the command arguments

MESSAGE_PLAY = "Let's rock, nya !"
MESSAGE_STOP = "Silence is gold, meow !"
MESSAGE_INVALID_SONG = "My disco library is huge but I can't find your song, myaster..."
MESSAGE_NO_SONG = "You must preeecise a song, darling."
MESSAGE_NO_CHANNEL = "You meowst join a voice channel before !"

async def on_play(bot, message, arguments):
    channel = message.author.voice.voice_channel
    if channel != None:
        if len(arguments) > 0:
            voice = await get_voice(bot, channel)
            if voice != None and not is_playing(bot):
                try:
                    await bot.speak(message.channel, MESSAGE_PLAY);
                    bot.player = voice.create_ffmpeg_player("resources/songs/beruna_village.mp3")
                    bot.player.start()
                except Exception:
                    await bot.speak(message.channel, MESSAGE_INVALID_SONG);
        else:
            await bot.speak(message.channel, MESSAGE_NO_SONG);
    else:
        await bot.speak(message.channel, MESSAGE_NO_CHANNEL);


async def on_stop(bot, message, arguments):
    if is_playing(bot):
        bot.player.stop()
        await bot.speak(message.channel, MESSAGE_STOP);

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
