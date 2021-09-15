import discord
from discord.ext import commands
import time
import requests
import ctypes
import ctypes.util

print("ctypes - Find opus:")
a = ctypes.util.find_library('opus')
print(a)

print("Discord - Load Opus:")
b = discord.opus.load_opus(a)
print(b)

print("Discord - Is loaded:")
c = discord.opus.is_loaded()
print(c)

client = commands.Bot(command_prefix = 'trigger ')


@client.event                   # event decorators
async def on_ready():
    print("Bot is ready.")

@client.event
async def on_member_join(member):
    print(member,"has joined the server.")

@client.event
async def on_member_remove(member):
    print(member,"has left the server.")


@client.command()
async def ping(ctx):
    await ctx.send( "Pong! ( "+ str( round(client.latency * 1000)) + "ms )" )

@client.command()
async def play(ctx, arg):
    user = ctx.author

    voice_channel = ctx.author.voice.channel
    channel_name = None

    file = open('vm/vm_list', 'r')
    found = False
    file_location = None
    for x in file:
        x = x.split(' ')
        if arg == x[0]:
            file_location = x[1][0:-1]
            found = True
            break
    file.close()
    if found is False:
        await ctx.channel.send('That vm dosnt exist')
        return

    if voice_channel!= None:
        channel_name = voice_channel.name
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(source=file_location), after=lambda e: print('done', e))
        while True:
            time.sleep(2)
            if vc.is_playing() is False:
                break
        await ctx.voice_client.disconnect()
    else:
        await ctx.channel.send(str(user)[0:-5] + ' , Please join a channel first')

@client.command()
async def save(ctx, arg):
     if not ctx.message.attachments:
         await ctx.channel.send("Add an mp3 file as an attachment")
     else:
         attachment_url = ctx.message.attachments[0].url
         file_request = requests.get(attachment_url)
         with open('vm/' + arg + '.mp3', 'wb') as f:
             f.write(file_request.content)
         file = open('vm/vm_list', 'a')
         file.write(arg + ' vm/' + arg + '.mp3\n')
         file.close()
         await ctx.channel.send("Added!")

client.run(<api key>)
