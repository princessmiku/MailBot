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
from discord import Interaction

from utils.bot_client import client


@client.tree.command(
    name="help",
    description="Helpful information's for using this bot"
)
async def slash_help(interaction: Interaction):
    await interaction.response.send_message(
        """
**MailBot Help**
Unlimited mailboxes are possible, make sure you follow the discord rules of character limit for the title and description when creating them.

**Setup of the bot**
The setup is very simple. Go to the channel you would like to be in where users can post a message.

Execute the slash command `/mailbox` in the channel. *For this command you need administrator permissions.*

Fill this with the arguments.

The `mail_box_channel` is the channel where the messages are then received that are written via the bot.

With the `sending_method` you specify which kind of information should be sent by the user.
`user` gives you the username and the id
`anonym` gives you the information that the message was sent anonymously.
user and `anonymous` gives the possibility that the user can choose what he prefers.

With `title` you can give the embed a title, this also serves the purpose that when you receive a message you know with which embed it was sent.
With `description` you can add your own description to the embed.

*Note that the bot needs `send_messages` and `embed_links` permissions in both channels*
""",
        ephemeral=True
    )
