import sys
import os
import random
import time
import asyncio
import importlib
import json
import discord
from colorama import init as colorama

PATH_SRC = "/src"
PATH_MEMORY_FILE = "/memory.json"
JSON_MEMORY_KEY_CHANNEL = "channel"
MESSAGE_UNDEFINED_BEHAVIOUR = "Behaviour {} was not found."
MESSAGE_MEMORY_READ_SUCCESSFUL = "Successfully accessed memory key {} of value {}."
MESSAGE_MEMORY_WRITE_SUCCESSFUL = "Successfully accessed memory key {} of new value {}."

colorama()

class Bot:

    client = discord.Client()
    behaviour_name = ""
    behaviour_lib = None
    behaviour_memory = ""

    def __init__(self, name, token):
        self.set_behaviour(name)
        if(self.behaviour_lib != None):
            self.set_events()
            self.client.run(token)
            self.client.close();

    def set_behaviour(self, name):
        self.behaviour_name = name
        self.behaviour_lib = None
        try:
            self.behaviour_lib = importlib.import_module(name)
        except ModuleNotFoundError:
            self.log_error(MESSAGE_UNDEFINED_BEHAVIOUR, name)
        self.behaviour_memory = self.get_path(PATH_SRC + "/" + self.behaviour_name + PATH_MEMORY_FILE)
        if not os.path.isfile(self.behaviour_memory):
            with open(self.behaviour_memory, "w+") as file:
                json.dump({}, file)

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
                    if hasattr(bot, command):
                        await getattr(bot, command)(bot, message, arguments)
                    elif bot.behaviour_lib != None and hasattr(bot.behaviour_lib, command):
                        await getattr(bot.behaviour_lib, command)(bot, message, arguments)

    def get_path(self, file):
        return os.path.split(os.path.abspath(os.path.realpath(sys.argv[0])))[0] + "/" + file

    def log(self, message, *args):
        print("[{}] {}".format(time.strftime("%y/%m/%d-%H:%M:%S"), str(message).format(*args)))

    def log_ok(self, message, *args):
        self.log("\033[92m" + message + "\033[0m", *args)

    def log_error(self, message, *args):
        self.log("\033[91m" + message + "\033[0m", *args)

    async def speak(self, texts, channel = None):
        text = "";
        if type(texts) == type(""):
            text = texts
        elif type(texts) == type([]) and len(texts) > 0:
            text = random.choice(texts)
        if channel == None:
            channel_id = await self.getmem(JSON_MEMORY_KEY_CHANNEL)
            if channel_id != None:
                channel = self.client.get_channel(channel_id)
        await self.client.send_message(channel, text)

    async def setmem(self, key, value):
        with open(self.behaviour_memory, "r+") as file:
            memory = json.load(file)
            memory[key] = value
            file.seek(0)
            file.truncate()
            json.dump(memory, file)
            self.log_ok(MESSAGE_MEMORY_WRITE_SUCCESSFUL, key, value)

    async def getmem(self, key):
        value = None
        with open(self.behaviour_memory, "r") as file:
            memory = json.load(file)
            if key in memory:
                value = memory[key]
            self.log_ok(MESSAGE_MEMORY_READ_SUCCESSFUL, key, value)
        return value
