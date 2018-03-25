import os
import random
import time
import asyncio
import importlib
import discord
from colorama import init as colorama

MESSAGE_UNDEFINED_BEHAVIOUR = "Behaviour %s was not found."

colorama()

class Bot:

    client = discord.Client()
    behaviour = None

    def __init__(self, name, token):
        self.set_behaviour(name)
        self.set_events()
        self.client.run(token)

    def set_behaviour(self, name):
        self.behaviour = None
        try:
            self.behaviour = importlib.import_module(name)
        except:
            log_error(MESSAGE_UNDEFINED_BEHAVIOUR, name)

    def set_events(self):
        bot = self

        @bot.client.event
        async def on_ready():
            bot.log_ok("Ready !")

        @bot.client.event
        async def on_message(message):
            bot.log("({}#{}) <{}> {}".format(message.channel.server.name, message.channel.name, message.author.name, message.content))
            if message.content.startswith("!"):
                words = message.content[1:].lower().split(" ")
                if len(words) > 0:
                    command = "on_" + words[0]
                    arguments = []
                    if len(words) > 1:
                        arguments.extend(words[1:])
                    if bot.behaviour != None and hasattr(bot.behaviour, command):
                        function = getattr(bot.behaviour, command);
                        await function(bot, message, arguments)

    def log(self, message, *args):
        print("[{}] {}".format(time.strftime("%y/%m/%d-%H:%M:%S"), str(message).format(*args)))

    def log_ok(self, message, *args):
        self.log("\033[92m" + message + "\033[0m", *args)

    def log_error(self, message, *args):
        self.log("\033[91m" + message + "\033[0m", *args)

    async def speak(self, channel, texts):
        text = "";
        if type(texts) == type(""):
            text = texts
        elif type(texts) == type([]) and len(texts) > 0:
            text = random.choice(texts)
        await self.client.send_message(channel, text)
