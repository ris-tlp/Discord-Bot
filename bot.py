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
bot.remove_command("help")

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

@bot.command(pass_context = True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(colour=discord.Colour.purple())
    embed.set_author(name='Help')
    embed.add_field(name = 'Prefixes', value = '! . ?', inline = False)
    embed.add_field(name = 'ping', value = 'Returns pong', inline = True)
    embed.add_field(name = 'kick (user)', value = 'Kicks a user', inline = True)
    embed.add_field(name = 'ban (user)', value = 'Bans a user', inline = True)
    embed.add_field(name = '8ball (question)', value = 'Magically answers a yes or no question', inline = False)
    embed.add_field(name = 'join', value = 'Bot joins the voice channel you are in', inline = True)
    embed.add_field(name = 'play (url)', value = 'Plays audio from specified YouTube link', inline = True)
    embed.add_field(name = 'pause', value = 'Pauses audio being played', inline = True)
    embed.add_field(name = 'resume', value = 'Resumes audio', inline = True)
    embed.add_field(name = 'stop', value = 'Stops audio being played', inline = True)
    embed.add_field(name = 'leave', value = 'Bot leaves voice channel', inline = True)

    await bot.send_message(author, embed = embed)

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
        print("I need to be in a voice channel to do this!")

@bot.command(pass_context = True)
async def play(ctx, url):
    server = ctx.message.server
    voice_client = bot.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after = lambda: check_queue(server.id))
    if voice_client:
        players[server.id] = player
        player.start()
    else:
        await bot.say("I need to be in a voice channel to do this!")

@bot.command(pass_context = True)
async def pause(ctx):
    voice_client = setServer(ctx)
    if voice_client:
        id = ctx.message.server.id
        players[id].pause()
    else:
        await bot.say("I need to be in the voice channel to do this!")

@bot.command(pass_context = True)
async def stop(ctx):
    voice_client = setServer(ctx)
    if voice_client:
        id = ctx.message.server.id
        players[id].stop()
    else:
        await bot.say("I need to be in a voice channel to do this!")

@bot.command(pass_context = True)
async def resume(ctx):
    voice_client = setServer(ctx)
    if voice_client:
        id = ctx.message.server.id
        players[id].resume()
    else:
        await bot.say("I need to be in a voice channel to do this!")

@bot.command(pass_context = True)
async def queue(ctx, url):
    server = ctx.message.server
    voice_client = bot.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after = lambda: check_queue(server.id))

    if voice_client:
        if server.id in queues:
            queues[server.id].append(player)
        else:
            queues[server.id] = [player]
    else:
        await bot.say("I need to be in a voice channel to do this!")

def check_queue(id):
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        player.start()

def setServer(ctx):
    server = ctx.message.server
    voice_client = bot.voice_client_in(server)
    return voice_client
##################################


@bot.command(pass_context = True)
async def close(ctx):
    await bot.logout()

bot.run(TOKEN)
