import json
from typing import *

import discord


def read(file):
    with open(f"database/{file}.json", "r") as f:
        return json.load(f)


def write(file, data):
    with open(f"database/{file}.json", "w") as f:
        json.dump(data, f, indent=4)


def get_prefix(bot, message):
    data = read("guilds")
    return data[str(message.guild.id)]["prefix"]


class View(discord.ui.View):
    def __init__(self, *, timeout: Optional[float] = 180, interaction_check: Optional[Coroutine] = None, on_error: Optional[Coroutine] = None, on_timeout: Optional[Coroutine] = None):
        super().__init__(timeout=timeout)
        self.interaction_check = interaction_check
        self.on_error = on_error
        self.on_timeout = on_timeout


class Button(discord.ui.Button):
    def __init__(self, *, style: discord.ButtonStyle = discord.ButtonStyle.secondary, label: Optional[str] = None, disabled: bool = False, custom_id: Optional[str] = None, url: Optional[str] = None, emoji: Optional[Union[str, discord.Emoji, discord.PartialEmoji]] = None, row: Optional[int] = None, callback: Optional[Coroutine] = None):
        super().__init__(style=style, label=label, disabled=disabled,
                         custom_id=custom_id, url=url, emoji=emoji, row=row)
        self.callback = callback
