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

import discord
from discord import Interaction, TextChannel, Color
from discord.ui import View, Button

from utils.bot_client import client


class CreateMailButton(Button):

    def __init__(self, button_id: str):
        super().__init__()
        self.custom_id = button_id
        self.label = "Create mail"
        self.emoji = "✉️"


class CreateMail(View):

    def __init__(self, button_id: str):
        super().__init__(timeout=1)
        self.add_item(CreateMailButton(button_id))


@client.tree.command(
    name="mailbox",
    description="Connect a Channel with a mailbox"
)
async def set_ticket_channel(interaction: Interaction, mail_box_channel: TextChannel, anonym: bool = False,
                             description: str = "Create a mail that will be delivered to this guild",
                             title: str = "Mail service"):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "This slash command is only for guild administrator",
            ephemeral=True
        )
        return
    channel: TextChannel = interaction.channel
    if not isinstance(channel, TextChannel):
        await interaction.response.send_message(
            "Unsupported channel type for the mailbox message"
        )
        return
    if not channel.permissions_for(interaction.guild.me).send_messages:
        await interaction.response.send_message(
            "Can't send messages in this channel",
            ephemeral=True
        )
        return
    if not channel.permissions_for(interaction.guild.me).embed_links:
        await interaction.response.send_message(
            "Can't send embeds in this channel",
            ephemeral=True
        )
        return
    if mail_box_channel.guild.id != interaction.guild.id:
        await interaction.response.send_message(
            "The mailbox channel is not on this guild",
            ephemeral=True
        )
        return
    if not mail_box_channel.permissions_for(interaction.guild.me).send_messages:
        await interaction.response.send_message(
            "Can't send messages in the mailbox channel",
            ephemeral=True
        )
        return
    if not mail_box_channel.permissions_for(interaction.guild.me).embed_links:
        await interaction.response.send_message(
            "Can't send embeds in the mailbox channel",
            ephemeral=True
        )
        return
    await channel.send(
        embed=discord.Embed(
            description=description,
            title=title,
            color=Color.teal()
        ).set_footer(
            text="When writing the mail, the reader does NOT know who you are" if anonym else
            "When you write the mail, the reader knows who you are"
        ),
        view=CreateMail(f"guild_mail.{str(mail_box_channel.id)}.{'anonym' if anonym else 'not_anonym'}")
    )
    await interaction.response.send_message(
        "Mailbox successfully created",
        ephemeral=True
    )
