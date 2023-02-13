import os

import discord
from discord import app_commands
from discord.ext import commands

from typing import *
from utils import *

bot = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all())


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

    await bot.change_presence(activity=discord.Game("m!help"))

    print("Bot is online.")


@bot.event
async def on_guild_join(guild):
    data = read("guilds")

    data[str(guild.id)] = {"prefix": "b!"}

    write("guilds", data)


@bot.event
async def on_guild_remove(guild):
    data = read("guilds")

    data.pop(str(guild.id))

    write("guilds", data)


@bot.event
async def on_message(message):
    await bot.process_commands(message)


@bot.event
async def on_member_join(member: discord.Member):
    channel = member.guild.system_channel or member.guild.text_channels[0]
    await channel.send(f"Hello {member.mention}, welcome to `{member.guild.name}`!")


@bot.event
async def on_member_remove(member: discord.Member):
    channel = member.guild.system_channel or member.guild.text_channels[0]
    await channel.send(f"Goodbye {member.mention}...")


@bot.tree.command()
async def prefix(interaction: discord.Interaction, prefix: str):
    data = read("guilds")

    data[str(interaction.guild_id)]["prefix"] = prefix

    write("guilds", data)

    await interaction.response.send_message(f"Successfully changed server prefix to `{prefix}`.", ephemeral=True)


@bot.tree.command(name="ping", description="Get the bot's latency.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! `{round(bot.latency * 1000)}` ms")


@bot.tree.command(name="clear", description="Clears messages from the channel with a specified limit.")
async def clear(interaction: discord.Interaction, limit: Optional[int]=None):
    async def interaction_check(i):
        return True
        
    view = View(timeout=60, interaction_check=interaction_check)

    async def confirm_callback(i: discord.Interaction):
        confirm_button.disabled = True
        cancel_button.disabled = True
        await i.response.defer()
        messages = await i.channel.purge(limit=limit)
        await interaction.edit_original_response(content=f"Successfully cleared `{len(messages)}` message(s).", view=view)


    async def cancel_callback(i: discord.Interaction):
        confirm_button.disabled = True
        cancel_button.disabled = True
        await i.response.defer()
        await interaction.edit_original_response(view=view)

    confirm_button = Button(label="Yes", style=discord.ButtonStyle.red, callback=confirm_callback)
    cancel_button = Button(label="Cancel", style=discord.ButtonStyle.gray, callback=cancel_callback)
    
    view.add_item(confirm_button)
    view.add_item(cancel_button)
    await interaction.response.send_message(f"Are you sure you would like to clear messages with a limit of `{limit}`?", view=view, ephemeral=True)

@bot.tree.command()
async def kick(interaction: discord.Interaction, member: discord.Member, *, reason: str=None):
    await member.kick(reason=reason)
    await interaction.response.send_message(f"Successfully kicked {member.mention} with reason `{reason}`.", ephemeral=True)

@bot.tree.command()
async def ban(interaction: discord.Interaction, member: discord.Member, *, reason: str=None):
    await member.ban(reason=reason, delete_message_days=0)
    await interaction.response.send_message(f"Successfully banned {member.mention} with reason `{reason}`.", ephemeral=True)

@bot.tree.command()
async def warn(interaction: discord.Interaction, member: discord.Member):
    await member.kick(reason=reason)
    await interaction.response.send_message(f"Successfully kicked {member.mention} with reason `{reason}`.", ephemeral=True)

bot.run(os.environ["TOKEN"])
