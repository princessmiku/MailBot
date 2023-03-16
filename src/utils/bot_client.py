# Copyright (c) 2023 Miku
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from configparser import ConfigParser
from typing import Any

import discord
from discord import Intents, Client, Game, Interaction, InteractionType
from discord.app_commands import CommandTree

from utils.argument_splitter import get_args_guild_mail
from utils.mail_handler import handle_guild_msg


class BotClient(Client):
    config = ConfigParser(); config.read("./config/bot.ini")
    owner = config.getint("DISCORD", "bot_owner")
    update_slash = False

    def __init__(self, *, intents: Intents, **options: Any):
        super().__init__(intents=intents, **options)
        self.tree = CommandTree(self)
        self.bot_guild = discord.Object(id=self.config.getint("DISCORD", "bot_guild"))

    async def on_ready(self):
        print(self.bot_guild)
        print("I'm online")
        await self.change_presence(activity=Game(name=self.config["DISCORD"]["bot_status"]))

    async def on_interaction(self, interaction: Interaction):
        if interaction.type == InteractionType.component:
            if interaction.data["custom_id"].startswith("guild_mail"):
                print(interaction.data["custom_id"])
                channel_id, anonym = get_args_guild_mail(interaction.data["custom_id"])
                await handle_guild_msg(interaction, channel_id, anonym)

    async def setup_hook(self) -> None:
        self.tree.copy_global_to(guild=self.bot_guild)
        if self.update_slash:
            #await self.tree.sync(guild=self.bot_guild)
            await self.tree.sync()


client = BotClient(intents=Intents.default())
