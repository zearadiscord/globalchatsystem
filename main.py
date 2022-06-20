import discord
from discord.ext import commands
from discord import interactions
from config.server import keep_alive
import os
import asyncio
import json
import requests


intents = discord.Intents.default()
intents.members = True
intents.guild_reactions = True
intents.guild_messages = True
bot = commands.Bot(command_prefix="aarrm!",intents=intents)
bot.remove_command("help")


@bot.event
async def on_ready():
  print("bot online")
  while True:
    await bot.change_presence(activity=discord.Game(
        name=f"{len(bot.guilds)}の{len(bot.users)}を管理"))
    await asyncio.sleep(5)
    await bot.change_presence(activity=discord.Game(
        name=f"Guild:{len(bot.guilds)}Users:{len(bot.users)}を管理"))
    









class AddButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label=f"追加",
            style=discord.ButtonStyle.primary
        )
    async def callback(self, interaction: discord.Interaction):
        self.channel = await bot.get_channel(int(interaction.channel.id))
        with open("globals.json","r+") as file:
          save = {
            "channel": [
              {
            "channelid": interaction.channel.id,
            "webhook": self.channel.create_webhook(name="zearadiscord-globalchat").url
              }
            ]
          }
        json.dump(save, file, ensure_ascii=False, indent=2)
        await interaction.response.send_message(
                f"{self.channel.name}\n🎉globalchatに追加しました",
                ephemeral=True
            )

@bot.slash_command(name="global-chat-add", description="guild add globalchat")
@commands.has_permissions(manage_channels=True)
async def add_slash(interaction: interactions.Interaction,channel: discord.channel = None):
    if channel:
      view = discord.ui.View(timeout=None)
      view.add_item(AddButton(channel))
      await interaction.send("追加",view=view)
    if not channel:
      view = discord.ui.View(timeout=None)
      view.add_item(AddButton(interaction.channel))
      await interaction.send("追加",view=view)

@bot.slash_command(name="help", description="help")
async def helpcommand(ctx):
  embed = discord.Embed(title="Help",description="/global-chat-add <channel>")
  await ctx.send(embed=embed)


@bot.listen("on_message")
async def globalchat(message):
  with open("globals.json") as file:
    file = json.load(file)
  if not message.channel.id == file["channel"]["channelid"]:
    return
  if message.channel.id == file["channel"]["channelid"]:
    await message.delete()
    for webhook in file["channel"]["webhook"]:
      data = {
        "name": f"{message.author.name}({message.author.id})",
        "avatar_url": message.author.avatar_url,
        "content": message.content
      }
      requests.get(webhook,data=data)



keep_alive()
bot.run(os.getenv("TOKEN"))
