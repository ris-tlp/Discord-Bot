import discord
from discord.ext import commands
import random

prefix = (".", "!")
TOKEN = ''

bot = commands.Bot(command_prefix = prefix)

@bot.event
async def on_ready():
    print("Bot running.")

@bot.command(pass_context = True)
async def ping(ctx):
    await bot.say("pong!") # for testing #

@bot.event
async def on_member_join(member):
    channel = member.server.get_channel("") #put channel id
    await bot.send_message(channel, "Welcome to the server, {0}".format(member.mention))

@bot.event
async def on_member_remove(member):
    channel = member.server.get_channel("") #put channel id
    await bot.send_message(channel, "{0} has left the server.".format(member.mention))

@bot.command(pass_context = True)
async def kick(ctx, user: discord.User):
    await bot.kick(user)

@bot.command(pass_context = True)
async def ban(ctx, user: discord.User):
    await bot.ban(user)

@bot.command(pass_context = True, name = '8ball')
async def ball(ctx):
    responses = ["As I see it, yes",
                "Ask again later",
                "Better not tell you now",
                "Don't count on it",
                "It is certain",
                "Most likely",
                "Outlook good",
                "Outlook not so good",
                "Without a doubt",
                "Doubtful"]
    await bot.say(random.choice(responses) + ", " + ctx.message.author.mention)

bot.run(TOKEN)
