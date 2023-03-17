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
from discord import Interaction, ui, TextStyle, Embed, Color
from discord._types import ClientT


class MailModal(ui.Modal):

    mail_content = ui.TextInput(
        label="Content",
        placeholder="Write your mail here",
        style=TextStyle.long,
        max_length=1500
    )

    def __init__(self, channel_id: int, anonym: bool, embed_title: str = None):
        if anonym:
            self.title = "Create an anonymous mail"
        else:
            self.title = "Create a mail"
        super().__init__()
        self.channel_id = channel_id
        self.anonym = anonym
        self.embed_title = embed_title

    async def on_submit(self, interaction: Interaction[ClientT], /) -> None:
        from utils.bot_client import client
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
        if not channel.permissions_for(interaction.guild.me).send_messages:
            await interaction.response.send_message(
                embed=Embed(
                    description="I am missing write permissions for sending the mail. Please contact an admin.",
                    color=Color.red()
                ).add_field(
                    name="Your mail content",
                    value=self.mail_content.value
                ),
                ephemeral=True
            )
            return
        if not channel.permissions_for(interaction.guild.me).embed_links:
            await interaction.response.send_message(
                embed=Embed(
                    description="I am missing the permissions for embed links for the mail. Please contact an admin.",
                    color=Color.red()
                ).add_field(
                    name="Your mail content",
                    value=self.mail_content.value
                ),
                ephemeral=True
            )
            return
        embed = Embed(
                description=self.mail_content.value,
                color=Color.teal(),
                title=":envelope_with_arrow: You've got a Mail"
            ).set_thumbnail(
                url="https://images.emojiterra.com/google/noto-emoji/v2.034/512px/1f4ec.png"
            )
        if self.anonym:
            embed.set_author(
                name="This is an anonymous message"
            )
        else:
            embed.set_author(
                name=f"This message was written by {interaction.user.name} ({str(interaction.user.id)})",
                icon_url=interaction.user.display_avatar
            )

        if self.embed_title:
            embed.set_footer(text="Mail receive from " + self.embed_title)
        message = await channel.send(
            embed=embed
        )
        await interaction.response.send_message(
            "Your mail was delivered",
            ephemeral=True
        )
