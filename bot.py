import discord
from discord.ext import commands

prefix = (".", "!")
TOKEN = ''

bot = commands.Bot(command_prefix = prefix)

@bot.event
async def on_ready():
    print("Bot running.")

@bot.command(pass_context = True)
async def ping(ctx):
    await bot.say("pong!") #test

bot.run(TOKEN)
