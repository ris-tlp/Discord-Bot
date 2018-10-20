import discord
from discord import opus
from discord.ext import commands
import random
import nacl
import youtube_dl
import asyncio

prefix = (".", "!")
TOKEN = ''

players = {}
queues = {}
bot = commands.Bot(command_prefix = prefix)

@bot.event
async def on_ready():
    await bot.change_presence(game = discord.Game(name = "with itself"))
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

#################FOR THE MUSIC#################

@bot.command(pass_context = True)
async def join(ctx):
    channel  = ctx.message.author.voice.voice_channel
    await bot.join_voice_channel(channel)

@bot.command(name = "leave",
                pass_context = True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = bot.voice_client_in(server)
    if voice_client:
        await voice_client.disconnect()
        print("Bot left the voice channel")
    else:
        print("Bot was not in channel")

@bot.command(pass_context = True)
async def play(ctx, url):
    server = ctx.message.server
    voice_client = bot.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after = lambda: check_queue(server.id))
    players[server.id] = player
    player.start()

@bot.command(pass_context = True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()

@bot.command(pass_context = True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()

@bot.command(pass_context = True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()

@bot.command(pass_context = True)
async def queue(ctx, url):
    server = ctx.message.server
    voice_client = bot.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after = lambda: check_queue(server.id))

    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]

def check_queue(id):
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        player.start()

##################################

@bot.command(pass_context = True)
async def bye(ctx):
    await bot.logout()

bot.run(TOKEN)
