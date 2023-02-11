import os


import discord
from discord import app_commands
from discord.ext import commands


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


   data[str(guild.id)] = {"prefix": "m!"}


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
   await channel.send(f"Hello {member.mention}, welcome to {member.guild.name}!")




@bot.event
async def on_member_remove(member: discord.Member):
   channel = member.guild.system_channel or member.guild.text_channels[0]
   await channel.send(f"Goodbye {member.mention}...")




@bot.tree.command()
async def prefix(interaction: discord.Interaction, prefix: str):
   data = read("guilds")


   data[str(interaction.guild_id)]["prefix"] = prefix


   write("guilds", data)




@bot.tree.command(name="ping", description="Get the bot's latency.")
async def ping(interaction: discord.Interaction):
   await interaction.response.send_message(f"Pong! {round(bot.latency * 1000)}ms")




@bot.tree.command(name="clear", description="Clears a certain number of messages from the channel.")
async def clear(interaction: discord.Interaction, amount: int):
   view = View(timeout=60)


   async def confirm_callback(interaction: discord.Interaction):
       await interaction.channel.purge(limit=amount)


   async def cancel_callback(interaction: discord.Interaction):
       await interaction.response.send_message("")


   view.add_item(
       Button(label="Yes", style=discord.ButtonStyle.red, callback=confirm_callback))
   view.add_item(Button(
       label="Cancel", style=discord.ButtonStyle.gray, callback=cancel_callback))
   await interaction.response.send_message(f"Are you sure you would like to clear {amount} messages?", view=view, ephemeral=True)




@bot.tree.command(name="hello")
async def hello(interaction: discord. Interaction):
   await interaction.response.send_message(f"Hey {interaction.user.mention}! This is a slash command!", ephemeral=True)


bot.run(os.environ["TOKEN"])