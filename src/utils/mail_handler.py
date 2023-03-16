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
from discord import Interaction, InteractionResponse, ui, TextStyle, Embed, Color
from discord._types import ClientT

from utils.bot_client import client


class MailModal(ui.Modal):

    mail_content = ui.TextInput(
        label="Content",
        placeholder="Write your mail here",
        style=TextStyle.long
    )

    def __init__(self, channel_id: int, anonym: bool):
        super().__init__()
        self.channel_id = channel_id
        self.anonym = anonym
        if anonym:
            self.title = "Create a anonymous mail"
        else:
            self.title = "Create a mail"

    async def on_submit(self, interaction: Interaction[ClientT], /) -> None:
        channel = await client.fetch_channel(self.channel_id)
        if not channel:
            await interaction.response.send_message(
                embed=Embed(
                    description="The mailbox (channel) cannot be found. Please contact a server admin for the problem.",
                    color=Color.red()
                ),
                ephemeral=True
            )
            return
        if not channel.permissions_for(interaction.guild.me, "send_messages"):
            await interaction.response.send_message(
                embed=Embed(
                    description="I am missing write permissions for sending the mail. Please contact an admin.",
                    color=Color.red()
                ),
                ephemeral=True
            )
            return
        await channel.send(
            embed=Embed(
                description=self.mail_content.value,
                color=Color.teal(),
                title=":envelope_with_arrow: You got Mail"
            ).set_thumbnail(
                url="https://images.emojiterra.com/google/noto-emoji/v2.034/512px/1f4ec.png"
            )
        )


async def handle_guild_msg(interaction: Interaction, channel_id: int, anonym: bool):
    await interaction.response.send_modal(MailModal(channel_id, anonym))
