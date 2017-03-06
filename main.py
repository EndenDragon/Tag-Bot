from config import config
import discord
import asyncio
import random
import string

client = discord.Client()
taggedUsersDict = {}

async def initiateTaggingSequence(member, guild):
    taggedUsersDict[guild] = member
    if member == client.user:
        member_name = client.user.name
    elif member.nick == None:
        member_name = member.name + "#" + member.discriminator
    else:
        member_name = member.nick
    await client.change_nickname(guild.get_member(client.user.id), "%{} is it!".format(member_name))

async def cleanupServers(servers):
    for guild in servers:
        try:
            await client.change_nickname(guild.get_member(client.user.id), None)
        except:
            pass
        if guild in taggedUsersDict:
            del taggedUsersDict[guild]

@client.event
async def on_ready():
    print('------')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print(str(len(client.servers)) + ' connected servers')
    print('------')
    print('Tag, you\'re it!')
    print('------')

@client.event
async def on_server_remove(server):
    serv = [server]
    await cleanupServers(serv)

@client.event
async def on_server_join(server):
    has_tag_channel = False
    channel = None
    for chan in server.channels:
        if chan.name in ["tag", "tagbot", "tag-bot", "tag_bot"]:
            has_tag_channel = True
            channel = chan
    if not has_tag_channel:
        channel = await client.create_channel(server, "tag")
    await client.send_message(channel, "Hello! I am the one, and only Tag Bot. Mention a user in this channel to start a never-ending game of tag!")

@client.event
async def on_message(message):
    if not message.channel.is_private and message.channel.name.lower() in ["tag", "tagbot", "tag-bot", "tag_bot"]: # check channel
        if len(message.mentions) == 1 and message.mentions[0] != message.author:
            if not message.mentions[0].bot:
                await initiateTaggingSequence(message.mentions[0], message.server)
            elif message.mentions[0] == client.user:
                messages = [
                    "Tag! {}",
                    "{}",
                    "Not so fast! {}",
                    "{} tag!!",
                    "{0} {0} {0} {0}!",
                    "{} TAG!!!!!",
                    "{}, you're it!",
                    "{} make me >:V",
                    "HAH {}",
                    "pahlease {}, this was easy",
                    ">:V {}",
                    "no~ {}",
                    "nnnope {}",
                    "eeyup {}",
                    "yo {}, what's shaken?",
                ]
                await initiateTaggingSequence(message.mentions[0], message.server)
                await client.send_typing(message.channel)
                await asyncio.sleep(random.randrange(0,2))
                await initiateTaggingSequence(message.author, message.server)
                await client.send_message(message.channel, random.choice(messages).format(message.author.mention))
        elif set(message.content.lower().translate(str.maketrans('', '', string.punctuation)).split()) <= set(["whos", "who", "is", "it", "whois", "whoisit", "isit"]):
            await client.send_typing(message.channel)
            if message.server in taggedUsersDict:
                await client.send_message(message.channel, "{} is it!".format(taggedUsersDict[message.server].mention))
            else:
                await client.send_message(message.channel, "No one is it! ...yet. :P")

async def playing_background_loop():
    await client.wait_until_ready()
    while not client.is_closed:
        messages = [
            "@mention a user in #tag channel!",
            "Ask me, who's it?",
            "Boop",
            "You're it!",
            "Tag, you're it!",
            "Tag!",
            ":O Quick! Tag your friend!",
            "Who's it?",
            "The power of @",
            "https://github.com/EndenDragon/Tag-Bot",
            "a game of Tag",
            "a never-ending game of Tag!",
        ]
        await client.change_presence(game=discord.Game(name=random.choice(messages)))
        await asyncio.sleep(120)

async def reset_nicknames_task():
    await client.wait_until_ready()
    await cleanupServers(client.servers)

client.loop.create_task(playing_background_loop())
client.loop.create_task(reset_nicknames_task())
client.run(config['DISCORD_BOT_TOKEN'])
