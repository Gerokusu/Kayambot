import time
import discord
import asyncio
import commands

client = discord.Client()

def kayambot(token):
    client.run(token)

def log(message):
    print("[{}] {}".format(time.strftime("%y/%m/%d-%H:%M:%S"), message))

@client.event
async def on_ready():
    log("Ready !")

@client.event
async def on_message(message):
    log("({}#{}) <{}> {}".format(message.channel.server.name, message.channel.name, message.author.name, message.content))
    if message.content.startswith("!"):
        words = message.content[1:].lower().split(" ")
        if len(words) > 0:
            command = "on_" + words[0]
            arguments = []
            if len(words) > 1:
                arguments.extend(words[1:])
            if hasattr(commands, command):
                function = getattr(commands, command);
                await function(client, message, arguments)
