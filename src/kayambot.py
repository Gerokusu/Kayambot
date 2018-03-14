import os
import time
import random
import discord
import asyncio
import commands
from colorama import init as colorama

client = discord.Client()
colorama();

def kayambot(token):
    client.run(token)

def log(message, *args):
    print("[{}] {}".format(time.strftime("%y/%m/%d-%H:%M:%S"), str(message).format(*args)))

def log_ok(message, *args):
    log("\033[92m" + message + "\033[0m", *args)

def log_error(message, *args):
    log("\033[91m" + message + "\033[0m", *args)

async def speak(channel, texts):
    text = "";
    if type(texts) == type(""):
        text = texts
    elif type(texts) == type([]) and len(texts) > 0:
        text = random.choice(texts)
    await client.send_message(channel, text)

@client.event
async def on_ready():
    log_ok("Ready !")

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
