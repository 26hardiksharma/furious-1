import discord
import os
from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter
import json
import asyncio
import random
from discord.raw_models import RawMessageDeleteEvent
import wikipedia
import datetime
import asyncpraw 
from PIL import Image
from io import BytesIO
import datetime
import time
import dbl
import requests
import pyjokes
import aiohttp
from art import *
import pymongo
from pymongo import MongoClient
import motor.motor_asyncio
import dns


TOKEN = 'NzkwNDc4NTAyOTA5ODM3MzMz.X-BMeQ.QMkidb3B5HSVnSZMvIQLDtlxsfU'
dbl_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc5MDQ3ODUwMjkwOTgzNzMzMyIsImJvdCI6dHJ1ZSwiaWF0IjoxNjEyNTI3NTExfQ.lbl6oMuLvlqSGGnhV5y2Z3ZOXU0ldwUTHgXKVYytAD4"
dbl_webhook = "https://discord.com/api/webhooks/814525601175437342/FlvD7x4oaoNQvT9PhsvIRIpwv2Q_-J5muSQ1nP1A3U1RVI4GmTLrMELHZN17MFBr2nkt"
async def getprefix(client,message):
  if not message.guild:
    return commands.when_mentioned_or('F!','f!','^')(client,message)
  try:
    
    data = await client.config.find(message.guild.id)
    if not data or "prefix" not in data:
      return commands.when_mentioned_or('F!','f!','^')(client,message)
    return commands.when_mentioned_or(data["prefix"])(client,message)
  except:
    return commands.when_mentioned_or('f!','F!','^')(client,message)
client = commands.Bot(command_prefix =getprefix,help_command=None,case_insensitive = True,strip_after_prefix = True)


client.dblpy = dbl.DBLClient(client,dbl_token,webhook_path = '/dblwebhook/https://discord.com/api/webhooks/814525601175437342/FlvD7x4oaoNQvT9PhsvIRIpwv2Q_-J5muSQ1nP1A3U1RVI4GmTLrMELHZN17MFBr2nkt',webhook_auth = 'pogchamp',webhook_port = 5000)


intents = discord.Intents.default()
@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"Customizable Karuta Cardping || F!karuta help"))
  print('Connected to bot: {}'.format(client.user.name))
  print('Bot ID: {}'.format(client.user.id))
  client.mongo = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
  client.db = client.mongo['furiousop']
  print('Connected To Collection: furiousop\n\nConnecting With Config')
  client.config = Document(client.db,'stores')
  print('Connected To Config\nConnecting With Warnings')
  client.warndb = Document(client.db,'warnings')
  print('Connection Established')
  print('Connecting With Blacklist')
  client.bls = Document(client.db,'blacklists')
  print('Connected With Blacklist')
  client.economy = Document(client.db,'economy')
  client.nextMeme = await getMeme()
  print('Fetched A Meme!')
  client.nowtime = datetime.datetime.now()
intents.guilds = True
def blcheck():
  async def lol(ctx:commands.Context):
    data = await client.bls.find(ctx.author.id)
    if not data:
      return True
    if not "blacklisted" in data:
      return True
    if data["blacklisted"] == "yes":
      return False
  return commands.check(lol)
@client.command()
@commands.cooldown(1,5,commands.BucketType.user)
@blcheck()
async def kick(ctx,user:discord.Member= None,*,reason = "No Reason Specified"):
  await ctx.message.delete()
  abc = ctx.guild.get_member(client.user.id) 
  if ctx.author.guild_permissions.kick_members:
    if abc.guild_permissions.kick_members:
      if not user:
        return await ctx.send('Please be Sure To Mention A Member Or use Their ID To Kick Them!')
      if ctx.author.id == ctx.guild.owner_id:
        try:
          await user.kick(reason = f"{reason} || Action By {ctx.author}")
          await ctx.send(f'Kicked {user} From {ctx.guild.name} || Reason: {reason}')
        except:
          await ctx.send(f'I Am Unable To Interact With {user}')
          return
        try:
          await member.send(f'You Have Been Kicked From {ctx.guild.name} Because Of {reason}')
        except:
          return
      else:
        if user.top_role>= ctx.author.top_role or user.id == ctx.guild.owner_id:
          return await ctx.send(f'You Dont Have Permission To Interact With {user}!')
        try:
          await user.kick(reason = f"{reason} || Action By {ctx.author}")
          await ctx.send(f'Kicked {user} From {ctx.guild.name} || Reason: {reason}')
        except:
          await ctx.send(f'I Am Unable To Interact With {user}')
          return
        try:
          await user.send(f'You Have Been Kicked From {ctx.guild.name} Because Of {reason}')
        except:
          return
    else:
      await ctx.send(f"I Am Missing The **KICK MEMBERS** Permission Required To Execute This Action")
  else:
    await ctx.send(f"You Are Missing The **KICK MEMBERS** Permission Required To Execute This Action")
@client.command()
@commands.cooldown(1,5,commands.BucketType.user)
@blcheck()
async def ban(ctx,user: discord.Member = None,*,reason = "No Reason Specified"):
  if ctx.author.guild_permissions.ban_members:
    if ctx.guild.me.guild_permissions.ban_members:
      if not user:
        return await ctx.send('Please be Sure To Mention A Member Or use Their ID To Ban Them!')
      if ctx.author.id == ctx.guild.owner_id:
        try:
          await user.ban(reason = f"{reason} || Action By {ctx.author}")
          await ctx.send(f'Banned {user} From {ctx.guild.name} || Reason: {reason}')
        except:
          await ctx.send(f'I Am Unable To Interact With {user}')
          return
        try:
          await member.send(f'You Have Been Banned From {ctx.guild.name} Because Of {reason}')
        except:
          return
      else:
        if user.top_role>= ctx.author.top_role or user.id == ctx.guild.owner_id:
          return await ctx.send(f'You Dont Have Permission To Interact With {user}!')
        try:
          await user.ban(reason = f"{reason} || Action By {ctx.author}")
          await ctx.send(f'Banned {user} From {ctx.guild.name} || Reason: {reason}')
        except:
          await ctx.send(f'I Am Unable To Interact With {user}')
          return
        try:
          await user.send(f'You Have Been Banned From {ctx.guild.name} Because Of {reason}')
        except:
          return
    else:
      await ctx.send(f"I Am Missing The **BAN MEMBERS** Permission Required To Execute This Action")
  else:
    await ctx.send(f"You Are Missing The **BAN MEMBERS** Permission Required To Execute This Action")
@client.command(aliases = ['um'])
@blcheck()
async def unmute(ctx,member : discord.Member):
  if ctx.author.guild_permissions.manage_messages:
    muted_role = discord.utils.get(member.guild.roles, name='Muted')
    if muted_role in member.roles:

      await member.remove_roles(muted_role)
      await ctx.message.delete()
      embed = discord.Embed(title = " 🔈Unmute" , description = f" {member.mention} Has Been Successfully Unmuted" , color = discord.Colour.red())
      await ctx.send(embed=embed)
      memberembed = discord.Embed(title = "🔈 Unmute", description = "You Have Been Unmuted", color = discord.Colour.green())
      memberembed.add_field(name = "Moderator :- ", value = ctx.author.name)
      await member.send(embed = memberembed)
    else:
      embed = discord.Embed(title = "<:error:795629492693368833> Unmute",color = discord.Color.red())
      embed.add_field(name = "Status",value = f"I Cant Unmute {member.mention}, They Are Not Muted")
      await ctx.send(embed=embed)

@client.command(aliases=['user'])
@blcheck()
async def whois(ctx, *,member : discord.Member = None):
  if member == None:
    member = ctx.author
  count = 0
  perms_string = ""
  rc = 0
  role_str = ""
  for role in member.roles[1:]:
    role_str += f"{role.mention} "
    rc += 1
  embed = discord.Embed(title = "User Info" , description = member.mention , colour = 0xE91E63)
  embed.set_thumbnail(url = member.avatar_url)
  embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
  embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
  embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested By {ctx.author.name}")
  embed.add_field(name= "Avatar Link",value = f"[Click Here]({member.avatar_url})")
  for perm, stat in member.guild_permissions:
    if stat is True:
      perms_string += f"**`{str(perm).upper()}`** "
      count += 1
  if rc >= 1:
    if len(role_str) <= 1024:
      embed.add_field(name=f"Roles[{rc}]", value=role_str,inline = False)
    else:
      embed.add_field(name = f"Roles[{rc}]",value = "User Has Too Many Roles!",inline = False)
    embed.add_field(name="Highest Role:", value=member.top_role.mention,inline = False)
  else:
    embed.add_field(name = "Roles",value = "None",inline = False)
  if count >= 1:
    embed.add_field(name = f"Key Permissions",value = f"{perms_string}")
  else:
    embed.add_field(name = "Key Permissions",value = "None")
  await ctx.send(embed=embed)
@client.command(aliases = ['av'])
@blcheck()
async def avatar(ctx,*, member : discord.Member=None):
  member = member or ctx.author
  embed = discord.Embed(title = f" {member.name}'s Avatar",url = member.avatar_url)
  embed.set_image(url = member.avatar_url)
  await ctx.send(embed=embed)
@client.command(aliases = ['clear'])
@commands.cooldown(1,5,commands.BucketType.user)
@blcheck()
async def purge(ctx,amt = None,member : discord.Member = None):
    if ctx.author.guild_permissions.manage_messages:
      if amt == None:
        await ctx.send(f"Please Specify The Number Of Messages To Be Purged")
      try:
        amt = int(amt)
      except:
        await ctx.send("Only Integer Values Can Be Used To Execute A Purge Command.")
      else:
        if member == None:   
          try:
            await ctx.message.delete()
            def kekcheck(m):
              return m.pinned == False
            await ctx.channel.purge(limit = amt,check=kekcheck)

            msg = await ctx.send(f"<a:EO_rtick:798248741429706814> Successfully Purged {amt} Messages")
            await asyncio.sleep(3)
            await msg.delete()
          except commands.BadArgument as e:
            await ctx.send(f"Please Enter Only Integer Value For The Number Of Messages To Be Purged")
        else:
          def check(m):
            return m.author == member and m.pinned == False
          try:
            await ctx.message.delete()
            await ctx.channel.purge(limit = amt,check=check)
            msg = await ctx.send(f"<a:EO_rtick:798248741429706814> Successfully Purged {amt} Messages Of {member}")
            await asyncio.sleep(3)
            await msg.delete()
          except commands.BadArgument as e:
            await ctx.send(f"Please Enter Only Integer Value For The Number Of Messages To Be Purged") 
    else:
      embed = discord.Embed(title = "Purge")
      embed.add_field(name = "Status", value = f" {ctx.author.mention}, You Don't Have The Permission To Execute This Command",inline = False)
      embed.add_field(name = "Missing Permission(s)", value = "Manage Messages",inline = False)
      embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested By {ctx.author.name}")
      await ctx.send(embed=embed)
@blcheck()
@client.command(aliases = ['m'])
async def mute(ctx,member : discord.Member,*,reason = "No reason Specified"):
  if ctx.author.guild_permissions.manage_messages:
    if member.guild_permissions.manage_messages:
      await ctx.message.delete()
      embed = discord.Embed(title = "<:error:795629492693368833> Mute",colour = 0xFF0000)
      embed.add_field(name = "Status",value = f"That User Is A Moderator/Admin. Command Could Not Be Executed!")
      await ctx.send(embed=embed)
    else:
      muted = await client.config.find(ctx.guild.id)
      if not muted or "mrole" not in muted:
        return await ctx.send('A Mute Role Is Not Configured In This Server, Use `F!muterole set <@role>` or `F!muterole setup` To Instantly Setup The Role.')
      else:
        id = muted["mrole"]
        muterole = discord.utils.get(ctx.guild.roles,id = id)
        if not muterole:
          return await ctx.send('The Muted Role Couldn\'t Be Found In This Server. Please Make Sure That The configured Muted Role Was Not Deleted Or Set A New One!')
        await member.add_roles(muterole,reason = f"{reason} || Action By {ctx.author.name}#{ctx.author.discriminator}")
        embed = discord.Embed(title = " 🔇 Mute" , description = f" {member.mention} Has Been Successfully Muted" , color = 0xFF0000)
        embed.add_field(name = "Reason", value = reason)
        memberembed = discord.Embed(title = "🔇 Mute", description = "You Have Been Muted", color = discord.Colour.red(), inline = False)
        memberembed.add_field(name = "Moderator :- ", value = ctx.author.name)
        memberembed.add_field(name = "Reason", value = reason, inline = False)
        await member.send(embed = memberembed)
        await ctx.send(embed=embed)
  else:
    await ctx.send("You Are Missing The **`MANAGE MESSAGES`** Permission Required To Execute This Command")
@client.command(aliases = ['botinfo','stats'])
async def botstats(ctx):
  num = 0
  for guild in client.guilds:
    num = num + guild.member_count
  embed = discord.Embed(title = "Bot Stats", description = "<@!790478502909837333>", colour = 0x7FFFD4)
  embed.set_thumbnail(url = 'https://cdn.discordapp.com/avatars/790478502909837333/ffbe1e96004d240eda5385186e145986.webp?size=1024')
  embed.add_field(name = "Creator", value = f"<:dev:835140540482846790> <@!757589836441059379>",inline = False)
  embed.add_field(name = "Total Commands",value = len(client.commands),inline = False)
  embed.add_field(name = "Total Servers Joined", value = str(len
  (client.guilds)),inline = False)
  embed.add_field(name= "Total Users",value = num,inline = False)
  embed.add_field(name = "Language",value = f"<:python:835141091480043570> Python",inline = False)
  embed.add_field(name = "Library",value = f"<:discord:835142396236005406> Discord.py",inline = False)
  embed.add_field(name = "Database",value = f"<:mongo:835140375882366976> MongoDB",inline = False)
  embed.add_field(name = "Ping",value = f"{round(client.latency*1000)} ms",inline = False)
  embed.add_field(name = "Important Links",value = f"[___Invite Me___](https://discord.com/oauth2/authorize?client_id=790478502909837333&permissions=4996415918&scope=bot) || [___Official Server___](https://discord.gg/5zbU6wEhkh)")
  await ctx.send(embed = embed)
@client.command(pass_context = True,aliases = ['nick'])
@blcheck()
async def setnick(ctx, member : discord.Member = None,*,nick = None):
  owner = await ctx.guild.fetch_member(ctx.guild.owner_id)
  abc = await ctx.guild.fetch_member(client.user.id)
  if ctx.author.guild_permissions.manage_nicknames:
    if member == None:
      await ctx.send(f"Please Mention A Member To Change Their Nickname.")
    elif nick == None:
      await ctx.send(f"Please Enter A Value For The Nickname.")
    else:
      if member.top_role >= ctx.author.top_role and member== owner:
        await ctx.send(f"You Dont Have The Permission To Interact With {member.name}#{member.discriminator}")
      else:
        if member.top_role >= abc.top_role or member== owner:
          await ctx.send(f"Couldn't Interact With {member.name}#{member.discriminator}")
        else:
          if nick == 'reset':
              await member.edit(nick= member.name)
              embed = discord.Embed(title = "Nickname",colour = 0x7DC6EE)
              embed.add_field(name ="Status", value = f"Successfully Reset The Nickname For {member.mention}")
              await ctx.send(embed=embed)
          elif len(nick) > 32:
            await ctx.message.delete()
            embed = discord.Embed(title = "<:error:795629492693368833> Nickname",colour = 0xFF0000)
            embed.add_field(name ="Status", value = f"Nickname Length Too Long. Should Be Less That 32 Characters")
            await ctx.send(embed=embed)
          else: 
            await member.edit(nick=nick)
            embed = discord.Embed(title = "Nickname",colour = 0x7DC6EE)
            embed.add_field(name ="Status", value = f"Successfully Changed The Nickname For {member.name} To {member.mention}")
            embed.add_field(name = "Changed By", value = ctx.author.mention,inline = False)
            await ctx.send(embed=embed)
  else:
    embed = discord.Embed(title = "Nickname",colour = 0xFF0000)
    embed.add_field(name = "Status", value = f" {ctx.author.mention}, You Don't Have The Permission To Execute This Command",inline = False)
    embed.add_field(name = "Missing Permission(s)", value = "Manage Nicknames",inline = False)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested By {ctx.author.name}")
    await ctx.send(embed=embed)
@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
@blcheck()
async def hack(ctx,member : discord.Member = None):
  if member == None:
    await ctx.send(f"I Got My Setup Ready To Hack Users But Ended Up Realizing You Didn't Mention Anyone!\nBe Sure To Mention Someone To Be Hacked!")
  elif member == ctx.author:
    await ctx.send(f"Bruh, Don't Be So Desperate To Get Yourself Hacked, Ask A Friend To Hack You!")
  else:

    msg = await ctx.send(f"Starting The Hack")
    await asyncio.sleep(2)
    await msg.edit(content = f"[▖] Getting {member.mention}'s Info")
    await asyncio.sleep(2)
    await msg.edit(content = f"[▘]2FA Passed")
    await asyncio.sleep(2)
    await msg.edit(content = f"[▝] Email :- {member.name}xd@gmail.com")
    await asyncio.sleep(2)
    await msg.edit(content = f"[▗]Password :- {member.name}0007")
    await asyncio.sleep(2)
    await msg.edit(content = f"[▖]Fetching DMs")
    await asyncio.sleep(2)
    await msg.edit(content = "[▘]Leaking Data On Sub Reddit")
    await asyncio.sleep(2)
    await msg.edit(content = "[▝]Sending Data To Government")
    await asyncio.sleep(2)
    await msg.edit(content = "[▗]Reporting Account For Violating Discord TOs")
    await asyncio.sleep(2)
    await msg.edit(content = "[▖]Injecting Virus")
    await asyncio.sleep(2)
    await msg.edit(content = f"[▘]Sending {member.mention}'s Head To Dynamo Gaming")
    await asyncio.sleep(3)
    await msg.edit(content = "Hacking Complete, user Under Control")
@client.command()
@blcheck()
async def vcreate(ctx,*,query):
  if ctx.author.guild_permissions.manage_channels:
    try:
      await ctx.guild.create_voice_channel(query)
      embed = discord.Embed(title = "Create Channel",colour = 0x00FFD7)
      embed.add_field(name = "Status",value = "Successfully Created The Channel",)
      await ctx.send(embed=embed)
    except:
      await ctx.send(f"Perhaps I Am Missing The **Manage Channels** Permissions Required To Execute This Command. Please Check And Try Again!")
  else:
    embed = discord.Embed(title = "<:error:795629492693368833> Create Channel",colour = 0xFF0000)
    embed.add_field(name = "Status", value = "You Dont Have The Permission To Execute This Command",inline = False)
    embed.add_field(name = "Missing Permissions", value = "Manage Channels")
    await ctx.send(embed=embed)

@client.command()
async def everyone(ctx):
  if ctx.author.id == 757589836441059379:
    await ctx.message.delete()
    msg = await ctx.send('@everyone')
    await msg.delete()
@client.command(aliases = ['v'])
@blcheck()
async def vote(ctx):
  embed = discord.Embed(title = "🗳️ Vote 🗳️",colour = 0xFFEF00)
  embed.add_field(name = "Upvote Me",value = "[Click Here](https://top.gg/bot/790478502909837333/vote)")
  embed.add_field(name = "Support Server",value = "[Click Here](https://discord.gg/MXa2EReETq)")
  embed.add_field(name = "Please Upvote Me",value="Your Upvotes Help Me Gain Reach And Join More Discord Servers!\nPlease Take A Minute And Upvote Me [Here](https://top.gg/bot/790478502909837333/vote)",inline = False)
  embed.set_footer(text = "Your Vote Is Precious And Helps Me Grow!")
  await ctx.send(embed=embed)
@client.command()
@blcheck()
async def roll(ctx,amount):
  entry = int(amount)
  outcome = random.randint(1,entry)
  if outcome > entry/2:
    await ctx.send(f"🎲 Your Random Outcome Is :- {outcome}. (1-{amount}) 😎")
  elif outcome == entry/2:
    await ctx.send(f"🎲 Your Random Outcome Is :- {outcome}. (1-{amount}) 🤔")
  elif outcome < entry/4:
    await ctx.send(f"🎲 Your Random Outcome Is :- {outcome}. (1-{amount}) 😂")
@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! My Ping Is :- **{(round(client.latency * 1000))} ms** <a:ping:797785823709888512>")

@client.command()
async def invite(ctx):
  embed=discord.Embed(title = "Thank You For Choosing Furious",description = "Some Useful Links!",url = "https://dsc.gg/furiousop",colour = 0x00FFD3)
  embed.add_field(name = "Invite Link",value = "[Click Here](https://discord.com/oauth2/authorize?client_id=790478502909837333&permissions=4996415918&scope=bot)",inline= False)
  embed.add_field(name = "Official Server",value = "[Click Here](https://discord.gg/5zbU6wEhkh)",inline = False)
  embed.set_thumbnail(url= ctx.author.avatar_url)
  await ctx.send(embed=embed)
@client.command()
@blcheck()
async def lock(ctx,*,channel : discord.TextChannel=None):
  if ctx.author.guild_permissions.manage_channels:
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    if overwrite.send_messages == False:
      return await ctx.send(f"{channel.mention} Is Already Locked Down.")
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    embed = discord.Embed(title = "🔒 Lock",colour = 0xFF0000)
    embed.add_field(name = "Status",value = f"Successfully Locked {channel.mention}")
    await ctx.send(embed=embed)
  else:
    await ctx.send("You Don't Have The **MANAGE CHANNELS** Permission Required To Execute This Command!")

@client.command()
@blcheck()
async def unlock(ctx,*,channel : discord.TextChannel=None):
  if ctx.author.guild_permissions.manage_channels:
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    if overwrite.send_messages == None or overwrite.send_messages == True:
      return await ctx.send(f"{channel.mention} Is Not Locked Down.")
    overwrite.send_messages = None
    await channel.set_permissions(ctx.guild.default_role,overwrite=overwrite)
    embed=discord.Embed(title = "🔓Unlock",colour = 0x00FFD3)
    embed.add_field(name = "Status",value = f"Successfully Unlocked {channel.mention} ")
    await ctx.send(embed=embed)
  else:
    await ctx.send("You Don't Have The **MANAGE CHANNELS** Permission Required To Execute This Command!")
@client.command()
@blcheck()
async def unban(ctx, kek : discord.User = None):
  me = await ctx.guild.fetch_member(client.user.id)
  if ctx.author.guild_permissions.ban_members:
    if me.guild_permissions.ban_members:
      if kek == None:
        await ctx.send("Please Mention A User Or Pass Their ID To Unban Them")
      else:
        try:
          user = await client.fetch_user(kek.id)
          await ctx.guild.unban(user)
          await ctx.send(f"{user.name}#{user.discriminator} was Unbanned")
        except discord.NotFound:
          await ctx.send(f"{user.name}#{user.discriminator} Is Not Banned From This Server!")
    else:
      await ctx.send("I Need The `BAN MEMBERS` Permission To Execute This Command!")
  else:
    await ctx.send("You Are Missing The `BAN MEMBERS` Permission Required To Execute This Command!")

@client.command(aliases = ['wikipedia'])
@blcheck()
async def wiki(ctx,*,query = None):
  if query == None:

    embed = discord.Embed(title= "Wikipedia",description = "Aliases :- 'wiki'\nUsage :- ^wiki <topic>\n Example:- ^wiki Plants")
    await ctx.send(embed=embed)
  else:
    msg = await ctx.send(f"<a:tg_02:786959609247432784> Searching Wikipedia For **{query}**")
    word = query
    try:
      result = wikipedia.summary(word,sentences = 5)
      await msg.edit(content = f"Wikipedia Search Results For **{query}**")
      await ctx.send(f"{result}\n **Note :- The Results May Not Be Accurate Everytime!**")
    except wikipedia.exceptions.PageError:
      await msg.edit(content = f" <:error:795629492693368833> No Results Found For ``{query}`` :/")
    except wikipedia.DisambiguationError as e:
      await msg.edit(content = f"<:error:795629492693368833> Results Could Not Be Loaded Because Your Query :- ``{query}`` Is Matching Several Pages! Please Mention Your Query More Specifically!")
@client.command()
@blcheck()
async def serverinfo(ctx):
  embed = discord.Embed(title = f"Information Of {ctx.guild.name}",color = 0x00FFFF)
  owner = await ctx.guild.fetch_member(ctx.guild.owner_id)
  embed.set_thumbnail(url = ctx.guild.icon_url)
  embed.add_field(name="General Info",value = f"**Name:** __{ctx.guild.name}__\n**Owner:** **{owner}**\n**Region:** __{str(ctx.guild.region).capitalize()}__",inline = False)
  embed.add_field(name = f"Counts",value = f"**Members:** __{ctx.guild.member_count}__\n**Roles:** __{len(ctx.guild.roles)}__\n**Text Channels:** __{len(ctx.guild.text_channels)}__\n**Voice Channels:** __{len(ctx.guild.voice_channels)}__",inline = False)
  act = 0
  ac = ""
  ct = 0
  cc = ""
  for i in ctx.guild.emojis:
    if i.animated:
      act += 1
      ac += f"<:{i.name}:{i.id}> "
    else:
      ct += 1
      cc+= f"<:{i.name}:{i.id}> "
  embed.add_field(name = f"Emojis",value = f"**Count:** {len(ctx.guild.emojis)}\n**Animated:** __{act}__ \n**Non-Animated:** __{ct}__",inline = False)
  await ctx.send(embed=embed)
@client.command()
@blcheck()
async def kill(ctx,member : discord.Member = None):
  if member == None:
    await ctx.send("Bruh, Please Mention A Member For Me To Kill Them. I Don't Support Mind Reading Currently :/")
  elif member == ctx.author:
    await ctx.send("No. I Wont Kill You!")
  else:
    number = random.randint(0,4)
    if number == 0:
      await ctx.send(f"{ctx.author.mention} Chased {member.mention}.")
      await asyncio.sleep(2)
      await ctx.send(f"{ctx.author.name} Locked Aim At {member.name}")
      await asyncio.sleep(2)
      await ctx.send(f"{ctx.author.name} Killed {member.mention}! Press F To Pay Respects")
    elif number == 1:
      await ctx.send(f"{ctx.author.mention} Chased {member.mention}.")
      await asyncio.sleep(2)
      await ctx.send(f"{ctx.author.name} Is Prying Out At {member.name}")
      await asyncio.sleep(2)
      await ctx.send(f"Turns Out That {member.mention} Is Selmon Bhoi! See Ya Soon **Deer**")
    elif number == 2:
      await ctx.send(f"{ctx.author.mention} Chased {member.mention}.")
      await asyncio.sleep(2)
      await ctx.send(f"{ctx.author.name} Pulled Out His Cleavers")
      await asyncio.sleep(2)
      await ctx.send(f"{ctx.author.name} Chopped Down {member.mention}! RIP")
    else:
      await ctx.send(f"{ctx.author.mention} Chased {member.mention}.")
      await asyncio.sleep(2)
      await ctx.send(f"{member.name} Is Suspecting {ctx.author.name}")
      await asyncio.sleep(2)
      await ctx.send(f"{member.name} Ringed The Women Helpline... See Ya Soon {ctx.author.mention}!")  
def convert(time):
  pos = ["s","m","h","d","hr","hour","hours","min","minute","minutes","day","days"]
  
  time_dict = {"s" : 1,"m": 60, "h":3600,"d":3600*24, "day" : 3600*24, "min" : 60,"minute": 60,"hour" : 3600,"hours" : 3600,"minutes" : 60,"days" : 3600*24,"hr" : 3600}
  unit = time[-1]
  if unit not in pos:
    return -1
  try:
    val = int(time[:-1])
  except:
    return -2
  return val*time_dict[unit]
@client.command()
@blcheck()
async def slowmode(ctx, unit = None):
  me = await ctx.guild.fetch_member(client.user.id)
  if ctx.author.guild_permissions.manage_channels:
    if me.guild_permissions.manage_channels:
      if unit == None:
        await ctx.send("Please Specify A Value For The Slowmode To Be Applied.\n\nExample: `F!slowmode 1m`")
        return
      time = convert(unit)
      if time == -1:
        await ctx.send("You Didnt Answer With A Proper Unit, Please Answer With A Proper Unit Next Time\n\nUnit References : [s|m|h]")
      elif time == -2:
        await ctx.send("Time Must be An Integer Value!")
      else:
        if time > 21600:
          await ctx.send(f"Slowmode Delay Cannot Be Longer Than 6 Hours!")
        elif time < 0:
          await ctx.send("Slowmode Delay Cannot Be Negative!")
        else:
          await ctx.channel.edit(slowmode_delay=time)
          await ctx.send(f"Enabled Messages Every {unit}!")
    else:
      await ctx.send("I Need The `MANAGE CHANNELS` Permission Required To Execute This Command!")
  else:
    await ctx.send("You Are Missing The `MANAGE CHANNELS` Permission Required To Execute This Command!") 
"""
@client.command()
async def giveaway(ctx):
  if ctx.author.guild_permissions.manage_guild:
    questions = ["Lets Start! Mention The Channel in Which You want The Giveaway To Be Started","Tell Me The Duration Of The Giveaway! Time Parameters :- [s|m|h|d]","Alright! How Many Winners Should Be There ?","Alright! What Should Be The Prize Of The Giveaway ?"]
    answers = []
    def check(m):
      return m.author == ctx.author and m.channel == ctx.channel
    for i in questions:
      await ctx.send(i)
      try:
        msg = await client.wait_for('message',timeout = 20.0,check = check)
      except asyncio.TimeoutError:
        await ctx.send("Time's Up! you Didn't Answer In Time")
        return
      else:
        answers.append(msg.content)
    try:
      c_id = int(answers[0][2:-1])
    except:
      await ctx.send(f"You Didn't Mention The Channel Properly.. 😔.. Do It Like :- {ctx.channel.mention}:D")
    channel = client.get_channel(c_id)
    time = convert(answers[1])
    if time == -1:
      await ctx.send(f"You Didn't Answer With A Proper Unit. Use The Table For Acknowledgment :- [s|m|h|d]")
    elif time == -2:
      await ctx.send(f"Time Must Be An Integer.. Please Enter An Integer Next Time 😉")
    else:
      winners = int(answers[2])

      win = int(winners)
      prize = answers[3]

      if winners > 20:
        await ctx.send(f"Too Many Winners!! The Maximum You Can Have Is 20!")
      elif time > 86400:
        await ctx.send(f"I Currently Support Giveaways Of Upto 1 Day Long 😔 || Please Select A Time Duration Less Than  Or Equal To 1 Day ")
      else:
        end = datetime.datetime.now()+datetime.timedelta(seconds= time*60)
        embed = discord.Embed(title = "Giveaway",description = f"{prize}", colour = 0x00FFEE)
        embed.add_field(name = "Host",value = f"{ctx.author.mention}",inline = False)

        embed.add_field(name = "Participate",value = "React With 🎉 To Enter")
        embed.set_footer(text = f'{winners} Winners • Ends At {end.strftime("%a, %#d %B %Y, %I:%M %p UTC")}')
        my_msg = await channel.send(embed=embed)
        await my_msg.add_reaction("🎉")                   
        await ctx.send(f"Alright! The Giveaway Of {prize} Is Starting In {channel.mention} And Will Last {answers[1]}")
        await asyncio.sleep(time)
        new_msg = await channel.fetch_message(my_msg.id)
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(client.user))
        if len(users) ==0:
          await channel.send(f"**Err,0 Reacts, Can't Choose Any Winner!**")
        elif winners > len(users):
          await channel.send(f"Not Enough Reacts! Couldn't Choose Any Winner 😔")
        else:
          winlist = "• "
          for i in range(winners):
            winner = random.choice(users)
            winlist += f"{winner.mention} • "
          new_embed = discord.Embed(title = "Giveaway",description = f"{prize}", colour = 0x00FFEE)
          new_embed.add_field(name= "Winner(s)",value = f"{winner.mention}")
          await my_msg.edit(embed=new_embed)
          await channel.send(f"Congratulations {winlist} ! You Won {prize}🥳")
  else:
    await ctx.send(f"You Need The **MANAGE SERVER** Permission To Start A Giveaway In This Server!")
@client.command()
async def reroll(ctx,channel : discord.TextChannel, id_ : int):
  if ctx.author.guild_permissions.manage_guild:
    try:
      new_msg = await channel.fetch_message(id_)
    except:
      await ctx.send("The ID Entered Was Incorrect!")
      return
    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))
    winner = random.choice(users)
    await channel.send(f"The New Winner Is {winner.mention}! Congratulations!")
  else:
    await ctx.send('You Dont Have The **MANAGE SERVER** Permission Required To Execute This Command!')
"""
@client.command()
@blcheck()
async def wink(ctx):
  embed=discord.Embed(title = f"{ctx.author.name} Is Winking 😉")
  embed.set_image(url = "https://cdn.discordapp.com/attachments/737780593609408532/737815454046879854/5OHh.gif")
  await ctx.send(embed=embed) 
@client.command()
@blcheck()
async def pog(ctx):
  embed=discord.Embed(title = f"{ctx.author.name} Is Pogging <:pog:819172397621837895>")
  embed.set_image(url = "https://cdn.discordapp.com/attachments/796260664577359883/801735309913096223/pog.gif")
  await ctx.send(embed=embed)   
@client.command()
@blcheck()
async def remindme(ctx,time,*,msg):
  unit = convert(time)
  if unit == -1:
    await ctx.send(f"You Didn't Answer With A Proper Unit. Use The Table For Acknowledgment :- [s|m|h|d]")
    
  elif unit == -2:
    await ctx.send(f"Time Must Be An Integer.. Please Enter An Integer Next Time 😉")
    
  else:   
    await ctx.send(f"{ctx.author.mention}! Set Your Reminder For {time} For :- **{msg}**")
    await asyncio.sleep(unit)
    await ctx.send(f"Reminder {ctx.author.mention}:- **{msg}**")
    await ctx.author.send(f"Reminder {ctx.author.mention}:- **{msg}**")  
@client.command(aliases = ['tm'])
@blcheck()
async def tempmute(ctx,member : discord.Member,unit,*,reason = "No reason Specified"):
  if member.guild_permissions.manage_messages:
    await ctx.message.delete()
    embed = discord.Embed(title = "<:error:795629492693368833> Mute",colour = 0xFF0000)
    embed.add_field(name = "Status",value = f"That User Is A Moderator/Admin. Command Could Not Be Executed!")
    await ctx.send(embed=embed)
  else:
    time = convert(unit)
    if time == -1:
      
      await ctx.send(f"You Didn't Answer With A Proper Unit. Use The Table For Acknowledgment :- [s|m|h|d]")
    elif time == -2:
      await ctx.send(f"Time Must Be An Integer.. Please Enter An Integer Next Time 😉")
    else:
      muted_role = discord.utils.get(member.guild.roles, name='Muted')
      await member.add_roles(muted_role)
      await ctx.message.delete()
      embed = discord.Embed(title = " 🔇 Mute" , description = f" {member.mention} Has Been Successfully Muted" , color = discord.Colour.red())
      embed.add_field(name = "Reason", value = reason)
      await ctx.send(embed=embed)
      memberembed = discord.Embed(title = "🔇 Mute", description = "You Have Been Muted", color = discord.Colour.red(), inline = False)
      memberembed.add_field(name = "Moderator :- ", value = ctx.author.name)
      memberembed.add_field(name = "Reason", value = reason, inline = False)
      await member.send(embed = memberembed)
      await asyncio.sleep(time)
      await member.remove_roles(muted_role)
reddit = asyncpraw.Reddit(client_id = "HavE-E7-h3pXDQ",client_secret = "TYAmuss0lnMFOXMZA_si6v-SmfkFJQ",user_agent = "prawop")
@client.command()
async def tour(ctx):
  if ctx.guild.name == "VΛИłSĦΣĐ SŁΛҰΣЯS":
    embed = discord.Embed(title = f"{ctx.author.name}",description = f"Welcome To The Tour Of {ctx.guild.name}",colour = 0x00F9FF)
    embed.add_field(name = "Please Read The Server Rules",value = "<#800660727601168425>",inline =False)
    embed.add_field(name = "Take Some Roles For Yourself",value = "<#800660728826429460>",inline = False)
    embed.add_field(name = "Interact With Each Other",value = "<#800660762321879060>",inline = False)
    embed.add_field(name = "Share Media",value = "<#800660762938966027>",inline = True)
    embed.set_thumbnail(url = f"{ctx.author.avatar_url}")
    embed.add_field(name = "Play Pokemon With Many Other Players 😉",value = "<#796260664577359883>",inline = False)
    emb = discord.Embed(title = f"{ctx.author.name}",description = f"Welcome To The Tour Of {ctx.guild.name}",colour = 0x00F9FF)
    emb.add_field(name = "Take Some Color Roles For Yourself",value = "<#800660730562740265>",inline =False)
    emb.add_field(name = "Look Up For Epic Giveaways Here",value = "<#800660742042812459>",inline = False)
    emb.add_field(name = "You Will Recieve My Upates Here",value = "<#801837579179786310>",inline = False)
    emb.add_field(name = "Check When You Level Up Here",value = "<#800660765823860746>",inline = False)
    emb.add_field(name= "Check Your Level Here",value = "<#800660767107842048>",inline = False)
    emb.set_thumbnail(url = f"{ctx.author.avatar_url}")
    try:      
      await ctx.author.send(embed=embed)
      await ctx.send("A Brief Info Of The Server Has Been Sent To Your DM!")
      await ctx.author.send("**I Will Send You The Next Page Of The Tour In 10 Seconds!**")
      await asyncio.sleep(10)
      await ctx.author.send(embed=emb)
    except:
      await ctx.send(f"You Must Keep Your DMs Open For Me To Send You The Server Tour! Please Try Again After Fixing")
                    

@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
@blcheck()
async def wanted(ctx, member: discord.Member = None):
  
  if member == None:
    member = ctx.author
  wanted = Image.open("wanted.jpg")
  asset= member.avatar_url_as(size = 128)
  data = BytesIO(await asset.read())
  pfp = Image.open(data)
  pfp = pfp.resize((157,156))
  wanted.paste(pfp, (153,285))
  wanted.save("profile.jpg")
  await ctx.send(file = discord.File("profile.jpg"))
@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
@blcheck()
async def hitler(ctx, member: discord.Member = None):
  if member== None:
    member = ctx.author
  hitler = Image.open("hitler.jpg")
  asset = member.avatar_url_as(size = 256)
  data = BytesIO(await asset.read())
  pfp = Image.open(data)
  pfp= pfp.resize((167,191))
  hitler.paste(pfp,(47,32))
  hitler.save("profile.jpg")
  await ctx.send(file = discord.File("profile.jpg"))
@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def  help(ctx,query = None):
  me = await ctx.guild.fetch_member(client.user.id)
  if me.guild_permissions.send_messages and me.guild_permissions.attach_files and me.guild_permissions.attach_files:
    if query == None:
      query = 0
    if query == 0:    
      embed = discord.Embed(title = "Help ",colour = 0x00FFD7)
      data = await client.config.find(ctx.guild.id)
      if not data or "prefix" not in data:
        prefixes ="F!\nf!\n^"
      else:
        prefixes = data["prefix"]
      embed.add_field(name = "Bot Prefixes",value = f"{prefixes}\n{client.user.mention}",inline = False)
      embed.add_field(name = "Get Started",value = "Please Refer To The Commands Listed Below",inline=False )
      embed.add_field(name = "<:emoji_2:810202313142566992> Moderation",value  = "`kick`,`ban`,`mute`,`unmute`,`hackban`,`tempmute`,`slowmode`,`lock`,`unlock`,`private`,\n`unprivate`,`setnick`,`muterole`",inline =False)
      embed.add_field(name = "<:emoji_0:810202224947888249> Fun",value= "`wink`,`pog`,`wanted`,`hitler`,`meme`,`dog`,`quote`,`joke`,`delete`,`trash`",inline = False)
      embed.add_field(name = f"<:emoji_3:810202359362748487> Utility",value = "`whois`,`remindme`,`roleinfo`,`serverinfo`,`avatar`,`roll`,`cardping`,\n`starboard`",inline = False)
      embed.add_field(name = "<:emoji_1:810202277624938527> Management",value = "`maintenance`,`serverlock`,`serverunlock`",inline = False)
      embed.add_field(name = "<:emoji_5:810202499914268703> Modules",value = f"Moderation\nUtility\nManagement\nFun\nYou Can Type F!help <module> To Get The Commands Of That Module")
      embed.add_field(name = "Quick Links",value = f"[Invite Me](https://discord.com/oauth2/authorize?client_id=790478502909837333&permissions=4996415918&scope=bot) • [Vote](https://top.gg/bot/790478502909837333/vote) • [Support Server](https://dsc.gg/furiousofficial)",inline = False)
      await ctx.send(embed=embed)
    elif query.lower() == 'fun':
      embed = discord.Embed(title = "Fun",description = "Furious' Fun Commands", colour = 0x00FFD7)
      embed.add_field(name = "Wink",value = "**^wink**",inline = False)
      embed.add_field(name = "Pog",value = "**^pog**",inline = False)
      embed.add_field(name = "Wanted!",value = "**^wanted @user**",inline = False)
      embed.add_field(name = "Hitler!",value = "**^hitler @user**",inline = False)
      embed.add_field(name = "Meme",value = "**^meme**")
      embed.add_field(name = "Trash",value = "**F!Trash <@user>**",inline = False)
      embed.add_field(name = "Delete",value="**F!delete <@user>**")
      embed.set_footer(text = "[] = Required, <> = Not Neccesary")
      await ctx.send(embed=embed)
    elif query.lower() == 'moderation':
      embed = discord.Embed(title = "Moderation",description = "Furious' Moderation Commands", colour = 0x00FFD7)
      embed.add_field(name = "Mute",value = "**^mute [@user] <reason>**",inline = False)
      embed.add_field(name = "Kick",value = "**^kick [@user] <reason>**",inline = False)
      embed.add_field(name = "Ban",value = "**^ban [@user] <reason>**",inline = False)
      embed.add_field(name = "Hackban",value = "**^hackban [user_id] <reason>**",inline = False)
      embed.add_field(name = "Unmute",value = "**^unmute [@user]**",inline = False)
      embed.add_field(name = "Tempmute",value = "**^tempmute [@user] [duration] <reason>**",inline = False)   
      embed.add_field(name= "Slowmode",value = "**^slowmode [seconds]**",inline = False)
      embed.add_field(name = "Lock",value = "**^lock <#channel>**",inline = False)
      embed.add_field(name = "Unlock",value = "**^unlock <#channel>**",inline = False)
      embed.add_field(name = "Private",value = "**^private <#channel>**",inline = False)
      embed.add_field(name = "Unprivate",value = "**^unprivate <#channel>**",inline = False)
      
      embed.set_footer(text = "[] = Required, <> = Optional")
      await ctx.send(embed=embed)
    elif query.lower() == 'utility':
      embed = discord.Embed(title = "Utility",description = "Furious' Utility Commands", colour = 0x00FFD7)
      embed.add_field(name = "Remindme",value = "<:emoji_1:810202277624938527> Sets A Reminder For You\nUsage :- ^remindme [Duration] [Message ]\nExample :- ^remindme 1h Vote Furious",inline = True)
      """
      embed.add_field(name = "Giveaway",value = "<:emoji_2:810202313142566992> Starts A Giveaway Setup In The Server\nUsage :- ^giveaway",inline = True)
      """
      embed.add_field(name = "Roll",value = "<:emoji_0:810202224947888249> Pick A Random Number From The Choice Provided\nUsage :- ^roll [quantity]\nExample :- ^roll 100",inline = True)
      embed.add_field(name = "Wiki",value = "<:emoji_4:810202418750029884> Search Wikipedia For A Topic\nUsage :- ^wiki [topic]\nExample :- ^wiki plants",inline = True)
      embed.add_field(name = "Whois",value = "<:emoji_3:810202359362748487> Get The Info Of A User\nUsage :- ^whois <@user>\nExample :- ^whois <@!790478502909837333>",inline =True)
      embed.add_field(name= "Roleinfo",value = "<:emoji_7:811830061325090826> Get The Info Of A Role\nUsage :- ^roleinfo [@role/role_id]\nExample :- ^roleinfo @moderators",inline = True)
      await ctx.send(embed=embed)
    elif query.lower() == "management":
      embed= discord.Embed(title= "Management",value= "Commands Which Can Help You Manage Your Server",colour= 0x00FFD7)
      embed.add_field(name= "Serverlock",value= "Locks All Channels Of The Server\n• ``^serverlock``",inline = False)
      embed.add_field(name= "Serverunlock",value= "Unocks All Channels Of The Server\n• ``^serverunlock``",inline = False)
      embed.add_field(name= "Maintenance",value= "Puts The Server On Maintenance\n• ``^maintenance on/off``",inline = False)
      await ctx.send(embed=embed)
  else:
    await ctx.send("I Need The Following Permissions To Display My Help Command Correctly :-\n`SEND MESSAGES`\n`ATTACH FILES`\n`EMBED LINKS`")    

@client.command()
@commands.cooldown(1,600,commands.BucketType.user)
@blcheck()
async def suggest(ctx,*,query):
  id = ctx.author.id
  suggestion = query
  channel = client.get_channel(810206511136636968)
  embed = discord.Embed(title = f"{ctx.author.name}",colour = 0x00F9FF)
  embed.add_field(name = "Suggestion",value = suggestion,inline = False)
  embed.add_field(name="Author ID",value = ctx.author.id,inline = False)
  embed.add_field(name = "Guild Name",value = ctx.guild.name,inline = False)
  op = await channel.send(embed=embed)
  await op.add_reaction("⬆")
  await op.add_reaction("🟡")
  await op.add_reaction("⬇")
  await ctx.send(f"Thank You For Providing A Suggestion! Your Efforts Are Appreciated")
@client.command(aliases= ['approve'])
async def consider(ctx,id:int,*,reason):
  if ctx.guild.id == 810190584059789323:
    if ctx.author.guild_permissions.administrator:   
      channel = client.get_channel(810206511136636968)
      msg = await channel.fetch_message(id)
      if msg.embeds:
        author = msg.embeds[0].fields[1].value
      embed = discord.Embed(title= f"Suggestion",colour = 0x3FFF00)
      embed.add_field(name = "Jump To Message",value = f"[Click Here]({msg.jump_url})",inline = False)
      embed.add_field(name= "Suggestion Considered",value = reason,inline = False)
      embed.add_field(name = "Approved By",value = ctx.author,inline = False)
      gg = await client.fetch_user(author)
      await channel.send(embed=embed)
      await gg.send(f"Your Suggestion Has Been Approved In Furious Official, Congrats")
@client.command()
async def decline(ctx,id:int,*,reason):
  if ctx.guild.id == 810190584059789323:
    if ctx.author.guild_permissions.administrator:        
      channel = client.get_channel(810206511136636968)
      msg = await channel.fetch_message(id)
      embed = discord.Embed(title= f"Suggestion",colour = 0xFF0000)
      embed.add_field(name = "Jump To Message",value = f"[Click Here]({msg.jump_url})",inline = False)
      embed.add_field(name= "Suggestion Declined",value = reason,inline = False)
      embed.add_field(name = "Declined By",value = ctx.author,inline = False)
      await ctx.send(embed=embed)
@client.event
async def on_guild_join(guild):
  channel = client.get_channel(810205872588062801)
  owner = await guild.fetch_member(guild.owner_id)
  embed = discord.Embed(title = "🥳 I Was Added To A New Server 🥳",colour = 0xDFFF00)
  embed.add_field(name = "Server Info",value = f"Server Name :- {guild.name}\n Guild Owner :- {owner.name}\n Member Count :- {guild.member_count}\n Guild Region :- {guild.region}\n Total Guilds I Am In :- {str(len(client.guilds))}")
  embed.set_thumbnail(url = f"{guild.icon_url}")
  abc = await channel.send(embed=embed)
  em = discord.Embed(title = guild.name,description = "Thanks For Adding Me To This Server! I Surely Will Help You With Your Discord Experience And In Managing This Server :)",colour = 0xDAF7A6)
  em.add_field(name = "Some Useful Information",value = "<:emoji_0:810202224947888249> I Am Furious, A Bot Designed To Moderate Servers While Providing Utility And Other Services To Other Server Members\n<:emoji_2:810202313142566992> Command Prefixes :- ^ , <@790478502909837333>\n<:emoji_3:810202359362748487> A Lot Of Useful Commands Which Come In Handy While Using Discord\n<:emoji_5:810202499914268703> Fun Commands\n<:emoji_1:810202277624938527> Much More Discoverable With ``^help``")
  em.add_field(name = "Some Useful Links",value = f"[Invite Me](https://discord.com/api/oauth2/authorize?client_id=790478502909837333&permissions=2099244279&redirect_uri=https%3A%2F%2Fdiscord.gg%2F4DqmNbUTXa&scope=bot) || [Support Server](https://dsc.gg/furiousofficial)",inline = False)
  for channel in guild.text_channels:
    try:
      if channel.is_news() == False:
        await channel.send(embed=em)
        break
    except:
      continue

@client.event
async def on_guild_remove(guild):
  channel = client.get_channel(810205896662712371)
  embed = discord.Embed(title = "😔 I Was Kicked From A Server 😔",colour = 0xFF0000)
  bruh = await client.fetch_user(guild.owner_id)
  embed.add_field(name = "Server Info",value = f"Server Name :- {guild.name}\nServer Owner :- {bruh}\n Member Count :- {guild.member_count}\n Guild Region :- {guild.region}\n Total Guilds I Am In :- {str(len(client.guilds))}")
  embed.set_thumbnail(url = f"{guild.icon_url}")
  await channel.send(embed=embed)
@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
@blcheck()
async def trash(ctx, member: discord.Member = None):
  if member== None:
    member = ctx.author
  trash = Image.open("trash.jpg").convert('RGB')
  asset = member.avatar_url_as(size = 256)
  data = BytesIO(await asset.read())
  pfp = Image.open(data)
  pfp= pfp.resize((314,306))
  trash.paste(pfp,(308,1))
  trash.save("profile.jpg")
  await ctx.send(file = discord.File("profile.jpg"))
@client.command()
@commands.cooldown(1,60,commands.BucketType.user)
@blcheck()
async def feedback(ctx,*,query = None):
  channel = client.get_channel(810205323675566101)
  embed=discord.Embed(title = '😄 Feedback 😄',colour =0x9FE2BF)
  embed.add_field(name = "Given By",value= f"{ctx.author}",inline = False)
  embed.add_field(name= "Guild Name",value = f"{ctx.guild.name}",inline = False)
  embed.add_field(name= "Feedback",value = f"{query}",inline= False)
  embed.set_thumbnail(url= f"{ctx.author.avatar_url}")
  await channel.send(embed=embed)
  await ctx.send(f"Thanks For Giving A Feedback! We Really Appreciate Your Efforts :D")
@client.command()
@blcheck()
async def private(ctx, channel : discord.TextChannel=None):
  if ctx.author.guild_permissions.manage_channels:
      channel = channel or ctx.channel
      overwrite = channel.overwrites_for(ctx.guild.default_role)
      overwrite.view_channel = False
      await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
      embed = discord.Embed(title = "Private",colour = 0xFF0000)
      embed.add_field(name = "Status",value = f"Successfully Made {channel.mention} Private")
      await ctx.send(embed=embed)
  else:
    await ctx.send("You Dont Have The **MANAGE CHANNELS** Permissions Requiered To Execute This Command")

@client.command()
@blcheck()
async def unprivate(ctx, channel : discord.TextChannel=None):
  if ctx.author.guild_permissions.manage_channels:
      channel = channel or ctx.channel
      overwrite = channel.overwrites_for(ctx.guild.default_role)
      overwrite.view_channel = None
      await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
      embed = discord.Embed(title = "Unprivate",colour = 0xFF0000)
      embed.add_field(name = "Status",value = f"Successfully Made {channel.mention} Public")
      await ctx.send(embed=embed)
  else:
    await ctx.send("You Dont Have The **MANAGE CHANNELS** Permissions Requiered To Execute This Command")

@client.command()
async def voter_mode(ctx,word,channel : discord.TextChannel=None):
  if ctx.guild.name =="VΛИłSĦΣĐ SŁΛҰΣЯS":
    role = discord.utils.get(ctx.guild.roles,name = "ᛝ𒅎・SΣЯVΣЯ VΩTΣЯS")
    if ctx.author.guild_permissions.administrator:
      if word == "on":
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.view_channel = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        lel = channel.overwrites_for(role)
        lel.view_channel = True
        await channel.set_permissions(role, overwrite=lel)
        embed = discord.Embed(title = "Voter Mode",colour = 0xFF0000)
        embed.add_field(name = "Status",value = f"Successfully Enabled Voter Only Mode On {channel.mention}")
        await ctx.send(embed=embed)
      elif word == "off":
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.view_channel = None
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        lel = channel.overwrites_for(role)
        lel.view_channel = None
        await channel.set_permissions(role, overwrite=lel)
        embed = discord.Embed(title = "Voter Mode",colour = 0xFF0000)
        embed.add_field(name = "Status",value = f"Successfully Disabled Voter Only Mode On {channel.mention}")
        await ctx.send(embed=embed)
    else:
      await ctx.send("You Are Missing The **ADMINISTRATOR** Permission Required To Execute This Command")
@client.command()
@blcheck()
async def templock(ctx,unit,channel : discord.TextChannel=None):
  
  if ctx.author.guild_permissions.manage_channels:
    time  = convert(unit)
    if time == -1:
      await ctx.send(f"You Didn't Answer With A Proper Unit. Use The Table For Acknowledgment :- [s|m|h|d]")
    elif time == -2:
      await ctx.send(f"Time Must Be An Integer.. Please Enter An Integer Next Time 😉")
    else:
      channel = channel or ctx.channel
      overwrite = channel.overwrites_for(ctx.guild.default_role)
      overwrite.send_messages = False
      await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
      embed = discord.Embed(title = "🔒 Templock",colour = 0xFF0000)
      embed.add_field(name = "Status",value = f"Successfully Locked {channel.mention} For {unit}")
      await ctx.send(embed=embed)
      await asyncio.sleep(time)
      lol = channel.overwrites_for(ctx.guild.default_role)
      lol.send_messages = None
      await channel.set_permissions(ctx.guild.default_role, overwrite=lol)
      embeds = discord.Embed(title = "🔒 Templock",colour = 0x00EAFF)
      embeds.add_field(name = "Status",value = f"Successfully Unlocked {channel.mention}")
      embeds.add_field(name = "Reason",value = "Lock Duration Expired",inline = False)
      await ctx.send(embed=embeds)
      
  else:
    await ctx.send("<:kya_bey:796610669549322250>")
@client.command()
@commands.cooldown(1, 60, commands.BucketType.guild)
@blcheck()
async def muterole(ctx,query = None,role : discord.Role = None):
  if query == None:
    embed = discord.Embed(title = "Muterole")
    embed.add_field(name = "Aliases",value = "None",inline = False)
    embed.add_field(name = "Required Permission(s)",value = "Manage Roles")
    embed.add_field(name = "Description",value = "Setups The Muterole In Your Server\n❯ Creates A Muted Role In The Server\n❯ Sets The Send Messages And Add Reactions Permission In Every Text Channel For The Muted Role To False\n❯ Sets The Speak Permission In Every Voice Channel For The Muted Role To False",inline = False)
    embed.add_field(name = "Cooldown",value = "60 Seconds Per Guild")
    embed.add_field(name = "Additional Tips",value = "Provide The Bot The **`ADMINISTRATOR`** To Make This Work Flawlessly",inline = False)
    await ctx.send(embed=embed)
    ctx.command.reset_cooldown(ctx)
  else:
    if ctx.author.guild_permissions.manage_roles:
      if query.lower() == "setup" or query.lower() == "create":
        data = await client.config.find(ctx.guild.id)
        if not data or "mrole" not in data:
          await ctx.send(f"Setting Up Muted Role")
          mrole = await ctx.guild.create_role(name = "Muted",permissions = discord.Permissions(permissions = 0))
          for channel in ctx.guild.text_channels:
            perms = channel.overwrites_for(mrole)
            perms.send_messages = False
            perms.add_reactions = False
            await channel.set_permissions(mrole,overwrite = perms)
            await asyncio.sleep(0.2)
          for vc in ctx.guild.voice_channels:
            vperms = vc.overwrites_for(mrole)
            vperms.speak= False
            await vc.set_permissions(mrole,overwrite=vperms)
            await asyncio.sleep(0.2)
          okay = {"_id":ctx.guild.id,"mrole":mrole.id}
          await client.config.upsert(okay)
          await ctx.send(f"Muterole Setup Successfully Completed")
        else:
          embed = discord.Embed(title = "Hold Up!",colour = ctx.author.color,timestamp = datetime.datetime.now())
          embed.add_field(name = "Muterole Conflicts Found!",value = 'A Muted Role has Already Been Setup In This Server. What Actions Do You Want Me To Perform ?')
          embed.add_field(name = "Actions",value = "1) Set Permissions And Overrides For The Existing Muted Role (Reply With `1` For This)\n\n2) Delete The Muted Role And Create A New One With Updated Permissions(Reply With `2` For This)")
          embed.add_field(name = "Existing Muterole",value = f'<@&{data["mrole"]}>',inline =False)
          await ctx.send(embed=embed)
          answers = []
          def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
          try:
            msg = await client.wait_for('message',timeout = 20.0,check = check)
          except asyncio.TimeoutError:
            await ctx.send("Time's Up! you Didn't Answer In Time")
            ctx.command.reset_cooldown(ctx)
            return
          else:
            answers.append(msg.content)
          if answers[0] == "1":
            mute = discord.utils.get(ctx.guild.roles,id = data["mrole"])
            if not mute:
              return await ctx.send('The Existing Muterole Couldn\'t Be Found In This Server, Please Make Sure That It Not Deleted.')
              
            me = await ctx.guild.fetch_member(client.user.id)
            if mute > me.top_role:
              return await ctx.send('The Existing Muted Role Is Above my Top Role. I Dont Have Permission To Configure It.\nPlease Make Sure That It Is Below My Top Role')
            
            await ctx.send(f"Updating The Muted Role || This May Take Time Depending Upon The Number Of Channels This Server Has!")
            for channel in ctx.guild.text_channels:
              perms = channel.overwrites_for(mute)
              perms.send_messages = False
              perms.add_reactions = False
              await channel.set_permissions(mute,overwrite = perms)
              await asyncio.sleep(0.2)
            for vc in ctx.guild.voice_channels:
              vperms = vc.overwrites_for(mute)
              vperms.speak= False
              await channel.set_permissions(mute,overwrite=vperms)
              await asyncio.sleep(0.2)
            await ctx.send(f"Successfully Setup The Existing Muted Role In Every Channel")
          elif answers[0] == "2":
            await ctx.send(f"Setting Up Muterole")
            kek = data["mrole"]
            mute = discord.utils.get(ctx.guild.roles,id = kek)
            if not mute:
              return await ctx.send('The Existing Muted Role Could Not Be Found In This Server.\n\nPlease Make Sure It Is Not Deleted!') 
            try:
              await mute.delete()
            except:
              await ctx.send("The Existing Muted Role Is Above My Top Role, I Am Unable To Delete It :/\nPlease Make Sure That It Is Below My Top Role!")
              return
            mrole = await ctx.guild.create_role(name = "Muted",permissions = discord.Permissions(permissions = 0))
            for channel in ctx.guild.text_channels:
              perms = channel.overwrites_for(mrole)
              perms.send_messages = False
              perms.add_reactions = False
              await channel.set_permissions(mrole,overwrite = perms)
              await asyncio.sleep(0.2)
            for vc in ctx.guild.voice_channels:
              vperms = vc.overwrites_for(mrole)
              vperms.speak= False
              await vc.set_permissions(mrole,overwrite=vperms)
              await asyncio.sleep(0.2)
            await ctx.send(f"Muterole Setup Has Been Successfully Completed")
      elif query.lower() == "set":
        if not role:
          return await ctx.send('Please Mention A Role To Be Set As The Muted Role Of The Server!')
        kekekek = {"_id":ctx.guild.id,"mrole":role.id}
        await client.config.upsert(kekekek)
        await ctx.send(f'**{role.name}** Has Been Set As The Muterole Of This Server!')
        ctx.command.reset_cooldown(ctx)
@client.command(aliases= ["ccreate"])
@blcheck()
async def create_category(ctx, *, name):
  if ctx.author.guild_permissions.manage_guild:
    await ctx.guild.create_category(name)
    await ctx.send(f"Successfully Create Category :- {name}")
  else:
    await ctx.send(f"You Are Missing The **MANAGE SERVER** Permissions Required To Execute This Command!")
@client.command()
@blcheck()
@commands.cooldown(1, 5, commands.BucketType.guild)
async def serverlock(ctx):
  if ctx.author.guild_permissions.manage_guild and ctx.author.guild_permissions.manage_channels:
    await ctx.send("Starting The Process To Lock All Text Channels Of The Server, Please Be Patient.")
    for channel in ctx.guild.text_channels:
      overwrite = channel.overwrites_for(ctx.guild.default_role)
      overwrite.send_messages = False    
      await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
      await asyncio.sleep(0.2)
    await ctx.send(f"Successfully Locked All Channels Of {ctx.guild.name}")
  else:
    await ctx.send(f"You Dont Have The **MANAGE CHANNELS** AND **MANAGE MESSAGES** Permissions Required To Execute This Command!")
@client.command()
@commands.cooldown(1, 60, commands.BucketType.guild)
@blcheck()
async def serverunlock(ctx):
  if ctx.author.guild_permissions.manage_guild and ctx.author.guild_permissions.manage_channels:
    await ctx.send("Starting The Process To Unlock All Text Channels Of The Server, Please Be Patient.")
    for channel in ctx.guild.text_channels:
      if channel.is_news() == False:
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = None    
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await asyncio.sleep(0.2)
    await ctx.send(f"Successfully Unlocked All Channels Of {ctx.guild.name}\nNote:- All Annoucement Channels Are Excluded And Are Still Locked")
  else:
    await ctx.send(f"You Dont Have The **MANAGE CHANNELS** AND **MANAGE MESSAGES** Permissions Required To Execute This Command!")
@client.command()
@commands.cooldown(1, 60, commands.BucketType.guild)
@blcheck()
async def maintenance(ctx,query = None):
  if query == None:
    embed = discord.Embed(title = "Maintenance")
    embed.add_field(name = "Aliases",value = "None",inline = False)
    embed.add_field(name = "Required Permission(s)",value = "Administrator",inline = False)
    embed.add_field(name = "Description",value = "❯ Makes All Text Channels Of The Server Private (Taking The View Channel Permission From The @everyone Role In Every Channel)\n❯ Makes All Voice Channels Of The Server Private (Taking The View Channel Permission From The @everyone Role In Every Voice Channel)\n❯ Creates 3 Channels To Keep The Server Activity Going On, Namely\n**`maintenance-chat`**\n**`maintenance-botzone`**\n**`Maintenance VC`**",inline = False)
    embed.add_field(name = "Cooldown",value = "60 Seconds Per Guild",inline = False)
    embed.add_field(name = "Usage",value = "❯ Turning On: **`F!maintenance on`**\n❯ Turning Off: **`F!maintenance off`**",inline = False)
    embed.add_field(name = "Additional Tips",value = "❯ Don't Use This Command Is Your Server Is A Verify-Type Server. Instead, Use **`F!serverlock`**\n❯ Provide The Bot The **`ADMINISTRATOR`** Permission To Make This Work Flawlessly",inline=False)
    await ctx.send(embed=embed)
    ctx.command.reset_cooldown(ctx)
  else:
    if ctx.author.guild_permissions.administrator:
      me = await ctx.guild.fetch_member(client.user.id)
      if me.guild_permissions.administrator:
        if query.lower() == "on":
          print(f'Starting Maintenance In {ctx.guild.name}')
          msg = await ctx.send(f"<a:tg_02:786959609247432784> Starting Maintenance Procedure")
          for channel in ctx.guild.text_channels:
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.view_channel = False    
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            await asyncio.sleep(0.2)
          await msg.edit(content = f"<a:tg_02:786959609247432784> Starting Maintenance Procedure \n <a:tg_02:786959609247432784> Applied Overrides On Text Channels\n <a:tg_02:786959609247432784> Applying In Voice Channels")
          for abcdefgh in ctx.guild.voice_channels:
            abcdef = abcdefgh.overwrites_for(ctx.guild.default_role)
            abcdef.view_channel = False    
            await abcdefgh.set_permissions(ctx.guild.default_role, overwrite=abcdef)
            await asyncio.sleep(0.2)
          await msg.edit(content = f"<a:tg_02:786959609247432784> Starting Maintenance Procedure \n <a:tg_02:786959609247432784> Applied Overrides On Text Channels\n <a:tg_02:786959609247432784> Applying In Voice Channels \n <a:tg_02:786959609247432784> Applied Overrides In Voice Channels \n <a:tg_02:786959609247432784> Creating Maintenance Channels")
          abcd = await ctx.guild.create_text_channel(name = f"maintenance-chat")
          efgh = await ctx.guild.create_text_channel(name = f"maintenance-botzone")
          ijkl = await ctx.guild.create_voice_channel(name = f" Maintenance VC")
          await msg.edit(content = f"<a:tg_02:786959609247432784> Starting Maintenance Procedure \n <a:tg_02:786959609247432784> Applied Overrides On Text Channels\n <a:tg_02:786959609247432784> Applying In Voice Channels \n <a:tg_02:786959609247432784> Applied Overrides In Voice Channels \n <a:tg_02:786959609247432784> Creating Maintenance Channels \n <a:tg_02:786959609247432784> Created Channels \n <a:tg_02:786959609247432784>")
          await ctx.send(f"Successfully Put {ctx.guild.name} On Maintenance")
          print('Maintenance Turned On!')
        elif query.lower() == "off":
          print(f"Turning Maintenance Off In {ctx.guild.name}!")
          msg = await ctx.send(f"<a:tg_02:786959609247432784> Lifting Up Maintenance")
          for channel in ctx.guild.text_channels:
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.view_channel = None
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            await asyncio.sleep(0.2)
          await msg.edit(content = f"<a:tg_02:786959609247432784> Lifting Up Maintenance \n <a:tg_02:786959609247432784> Applied Overrides On Text Channels\n <a:tg_02:786959609247432784> Applying In Voice Channels")
          for lol in ctx.guild.voice_channels:
            bhat = lol.overwrites_for(ctx.guild.default_role)
            bhat.view_channel = None
            await lol.set_permissions(ctx.guild.default_role, overwrite=bhat)
            await asyncio.sleep(0.2)
          await msg.edit(content = f"<a:tg_02:786959609247432784> Starting Maintenance Procedure \n <a:tg_02:786959609247432784> Applied Overrides On Text Channels\n <a:tg_02:786959609247432784> Applying In Voice Channels \n <a:tg_02:786959609247432784> Applied Overrides In Voice Channels \n <a:tg_02:786959609247432784> Deleting Maintenance Channels")
          ch = discord.utils.get(ctx.guild.text_channels,name = "maintenance-chat")
          try:
            await ch.delete()
          except:
            pass
          chan = discord.utils.get(ctx.guild.text_channels,name = "maintenance-botzone")
          try:
            await chan.delete()
          except:
            pass
          chann = discord.utils.get(ctx.guild.voice_channels,name = "Maintenance VC")
          try:
            await chann.delete()
          except:
            pass
          await msg.edit(content = f"<a:tg_02:786959609247432784> Starting Maintenance Procedure \n <a:tg_02:786959609247432784> Applied Overrides On Text Channels\n <a:tg_02:786959609247432784> Applying In Voice Channels \n <a:tg_02:786959609247432784> Applied Overrides In Voice Channels \n <a:tg_02:786959609247432784> Deleting Maintenance Channels \n <a:tg_02:786959609247432784> Deleted Channels")
          await ctx.send(f"Successfully Lifted Up Maintenance From {ctx.guild.name}")
        
          print('Maintenance Turned Off')
        else:
          ctx.command.reset_cooldown(ctx)
      else:
        await ctx.send("I Am Missing The **`ADMINISTRATOR`** Permission Required To Execute This Command!")
        ctx.commands.reset_cooldown(ctx)
    else:
      await ctx.send("You Are Missing The **`ADMINISTRATOR`** Permission Required To Execute This Command!") 
      ctx.command.reset_cooldown(ctx)     
@client.command()
@blcheck()
async def nuke(ctx,channel : discord.TextChannel = None):
  if ctx.author.guild_permissions.manage_channels:
    if channel == None:
      channel = ctx.channel
    await channel.clone(reason=f" Channel Has been nuked by {ctx.author.name}")
    await channel.delete()
@client.command()
async def usercount(ctx):
  num = 0
  for guild in client.guilds:
    num = num + guild.member_count
  await ctx.send(f"I Have {num} Users Currently")
@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
@blcheck()
async def addrole(ctx,member : discord.Member = None,role : discord.Role = None): 
  if member == None:
    await ctx.send("Please Mention The Member Or Pass Their ID To Give Them A Role")
  elif role == None:
    await ctx.send("Please Mention A Role Or Pass It's ID To Be Added.")
  else:
    if ctx.author.guild_permissions.manage_roles:
      owner= await ctx.guild.fetch_member(ctx.guild.owner_id)
      abc = await ctx.guild.fetch_member(client.user.id)
      if role >= abc.top_role:
        await ctx.send(f"That Role Is Above My Top Role. I Dont Have The Permission To Assign It To Anyone")
      elif role >= ctx.author.top_role:
        if ctx.author==owner:
          if role not in member.roles:
            try:
              await member.add_roles(role)
              embed = discord.Embed(title = 'Addrole',colour = 0x00FFE2)
              embed.add_field(name=f"Role Added",value= role.mention,inline= False)
              embed.add_field(name=f"Added To",value = member.mention,inline = False)
              embed.add_field(name = f"Added By",value= ctx.author.mention)
              await ctx.send(embed=embed)
            except discord.Forbidden:
              await ctx.send("Missing Permissions Or Access To That Role :(")
          else:
            await ctx.send(f"{member.name}#{member.discriminator} Already Has The Target Role!") 
        else:
          await ctx.send(f"You Dont have The Permission To Interact With That Role")
      else:
        if role not in member.roles:
          try:
            await member.add_roles(role)
            embed = discord.Embed(title = 'Addrole',colour = 0x00FFE2)
            embed.add_field(name=f"Role Added",value= role.mention,inline= False)
            embed.add_field(name=f"Added To",value = member.mention,inline = False)
            embed.add_field(name = f"Responsible Moderator",value= ctx.author.mention)
            await ctx.send(embed=embed)
          except:
            await ctx.send("Missing Permissions Or Access To That Role :(")
        else:
          await ctx.send(f"{member.name}#{member.discriminator} Already Has The Target Role!")
@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
@blcheck()
async def takerole(ctx,member : discord.Member = None,role : discord.Role = None):
  if member == None:
    await ctx.send("Please Mention The Member Or Pass Their ID To Remove A Role From Them.")
  elif role == None:
    await ctx.send("Please Mention A Role Or Pass It's ID To Be Removed.")
  else:
    if ctx.author.guild_permissions.manage_roles:
      owner= await ctx.guild.fetch_member(ctx.guild.owner_id)
      abc = await ctx.guild.fetch_member(client.user.id)
      if role >= abc.top_role:
        await ctx.send(f"That Role Is Above My Top Role. I Dont Have The Permission To Remove It From Anyone")
      elif role >= ctx.author.top_role:
        if ctx.author== owner:
          await member.remove_roles(role)
          embed = discord.Embed(title = 'Take Role',colour = 0x00FFE2)
          embed.add_field(name=f"Role Removed",value= role.mention,inline= False)
          embed.add_field(name=f"Removed From",value = member.mention,inline = False)
          embed.add_field(name = f"Removed By",value= ctx.author.mention)
          await ctx.send(embed=embed)
        else:
          await ctx.send(f"You Dont have The Permission To Interact With That Role")
      else:
        if role.is_premium_subscriber():
          await ctx.send("That Role Is The Booster Role For This Server, It Cannot Be Manually Removed From Anyone!")
        elif role.is_integration() or role.is_bot_managed():
          await ctx.send("That Role Is A Bot's Integration Role, It Cannon Be Manually Removed From Anyone!")
        else:
          await member.remove_roles(role)
          embed = discord.Embed(title = 'Take Role',colour = 0x00FFE2)
          embed.add_field(name=f"Role Removed",value= role.mention,inline= False)
          embed.add_field(name=f"Removed From",value = member.mention,inline = False)
          embed.add_field(name = f"Responsible Moderator",value= ctx.author.mention)
          await ctx.send(embed=embed)
@client.command()
@blcheck()
async def hackban(ctx,member : discord.User = None,*,reason= "No Reason Specified."):
  await ctx.message.delete()
  if ctx.author.guild_permissions.ban_members:
    abc = await ctx.guild.fetch_member(client.user.id)
    if abc.guild_permissions.ban_members:
      if member == None:
        await ctx.send(f"Please Mention The User Or Pass Their ID To Ban Them.")
      else:
        user = await client.fetch_user(member.id)
        member = ctx.guild.get_member(user.id)
        if member == None:
          try:
            await ctx.guild.ban(user,reason = f"{reason} || Action By {ctx.author}")
            await ctx.send(f'{user} Was Banned. Reason: {reason}')
          except:
            return await ctx.send(f"Failed Banning {member}! Perhaps I Am Missing Certain Permissions.")
        else:
          if ctx.author.id == ctx.guild.owner_id:
            try:
              await member.ban(reason = f"{reason} || Action By {ctx.author}")

              await ctx.send(f'{user} Was Banned. Reason: **{reason}**')
            except:
              await ctx.send(f'I Am Unable To Ban {member}')
          else:
            if member.top_role >= ctx.author.top_role or member.id == ctx.guild.owner_id:
              await ctx.send(f"You Dont Have The Permission To Interact With {member}")
              return
            try:
              await member.ban(reason = f"{reason} || Action By {ctx.author}")
              await ctx.send(f'{user} Was Banned. Reason: **{reason}**')
            except:
              await ctx.send(f'I Am Unable To Ban {member}')
    else:
      await ctx.send(f"I Am Missing The **BAN MEMBERS** Permission Required To Execute This Command!")
  else:
    await ctx.send(f"You Must Have The **BAN MEMBERS** Permission To Execute This Command!")
def rcheck(choice):
  correct =["rock","paper","scissors","Rock","Paper","Scissors","ROCK","PAPER","SCISSORS"]
  if choice not in correct:
    return -1
@client.command()
@blcheck()
async def embed(ctx):
  questions = ["Enter The Title You Want For The Embed","Enter The Description For Your Embed!","Enter A Field For Your Embed","Enter The Value For Your Field\nIf You Want To Add Hyperlink Type [Field Text](link)"]
  answers = []
  def check(m):
    return m.author == ctx.author and m.channel == ctx.channel
  for i in questions:
    await ctx.send(i)
    try:
      msg = await client.wait_for('message',timeout = 20.0,check = check)
    except asyncio.TimeoutError:
      await ctx.send("Time's Up! you Didn't Answer In Time")
      return
    else:
      answers.append(msg.content)
  embed = discord.Embed(title = answers[0],description = answers[1],colour = 0xFF0000)
  embed.set_footer(text =f"{ctx.author}")
  embed.add_field(name= answers[2],value= f"{answers[3]}")
  await ctx.send(embed=embed)
@client.command()
@blcheck()
async def pin(ctx,id :int):
  if ctx.author.guild_permissions.manage_messages:
    abc = await ctx.guild.fetch_member(client.user.id)
    if abc.guild_permissions.manage_messages:
      try:
        msg = await ctx.channel.fetch_message(id)


        await msg.pin()
      except discord.NotFound:
        await ctx.send(f"Message Not Found! Please Use This Command In The Channel In Which The Message Is..")
    else:
      await ctx.send(f"I Am Missing The **MANAGE MESSAGES** Permission To Execute This Command")
  else:
    await ctx.send(f"You Are Missing The **MANAGE MESSAGES** Permissions To Execute This Command")
@client.command()
@blcheck()
async def unpin(ctx,id :int):
  if ctx.author.guild_permissions.manage_messages:
    abc = await ctx.guild.fetch_member(client.user.id)
    if abc.guild_permissions.manage_messages:
      try:
        msg = await ctx.channel.fetch_message(id)
        await msg.unpin()
        await ctx.send(f"Message Unpinned")
      except commands.MessageNotFound:
        await ctx.send(f"Message Not Found! Please Use This Command In The Channel In Which The Message Is..")
    else:
      await ctx.send(f"I Am Missing The **MANAGE MESSAGES** Permission To Execute This Command")
  else:
    await ctx.send(f"You Are Missing The **MANAGE MESSAGES** Permissions To Execute This Command")
@client.command()
@blcheck()
async def totalbans(ctx):
  if ctx.author.guild_permissions.ban_members:
    ct = 0
    for ban in await ctx.guild.bans():
      ct= ct + 1
    await ctx.send(f"{ctx.guild.name} Has {ct} Bans In Total")
@client.event
async def on_command_error(ctx, error):
  ctx.command.reset_cooldown(ctx)
  if isinstance(error, commands.CommandOnCooldown):
    await ctx.message.delete()
    embed = discord.Embed(title = f"<:error:795629492693368833> {ctx.author.name}#{ctx.author.discriminator}",colour = 0xFF0000)
    embed.add_field(name = "Status", value = "This Command Is On Cooldown")
    embed.add_field(name = "Time Remaining",value = '{:.2f}s'.format(error.retry_after),inline = False)
    await ctx.send(embed=embed)    
    print(f"{ctx.author} ID: {ctx.author.id} Used A Command: {ctx.command.name} While Being On Cooldown")
  elif isinstance(error,commands.CommandNotFound):
    return
  elif isinstance(error,commands.UserNotFound):
    await ctx.send(f"Couldn't Find That User :(")
  elif isinstance(error,commands.MemberNotFound):
    await ctx.send(f"Couldn't Find That Member In This Server :(")
  elif isinstance(error,commands.RoleNotFound):
    await ctx.send("Couldn't Find That Role In This Server :(")
  elif isinstance(error,commands.ChannelNotFound):
    await ctx.send("Cannot Find That Channel In This Guild :(")
  elif isinstance(error,commands.CheckFailure):
    await ctx.send("Your Account Has Been Blacklisted From Using The Bot. You Can Apply For Unblacklisting In The Official Server.")
  else:
    print(ctx.guild.name)
    print(ctx.author.name)
    eternal = await client.fetch_user(757589836441059379)
    await eternal.send(f"An Error Occured!\n{ctx.command.name}\n{ctx.guild.name}\n{ctx.author.name}:- {ctx.author.id} \n{error}")
    raise error
async def getMeme():
  all_subs = []
  subreddit = await reddit.subreddit("meme",fetch= True)   
  async for submission in subreddit.top(limit = 250):
    if submission.is_video == False and submission.url.startswith("https://youtube.com/") == False:
      all_subs.append(submission)
  random_sub = random.choice(all_subs) 
  if random_sub.over_18:
    warn = "NSFW Content Is Not Supported"
    return warn
  else:
    name = random_sub.title
    url = random_sub.url
    return name, url
@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
@blcheck()
async def meme(ctx):
  if not hasattr(client, 'nextMeme'):
    client.nextMeme = await getMeme()
    
  name, url = client.nextMeme
  embed = discord.Embed(title = f"{name}",url=url,colour = 0xE5FF00)
  embed.set_image(url=url)
  embed.set_footer(text=f"©️ By Subreddit",icon_url = client.user.avatar_url)
  await ctx.send(embed=embed)
  client.nextMeme = await getMeme()

@client.event
async def on_dbl_vote(data):
  print(f'Vote Received\n\n{data}')
@client.command()
async def create(ctx,type,*,query):
  abc = await ctx.guild.fetch_member(client.user.id)
  if type == "role":
    if ctx.author.guild_permissions.manage_roles:
      if abc.guild_permissions.manage_roles:
        role = await ctx.guild.create_role(name = query,permissions = discord.Permissions(permissions = 0)) 
        embed = discord.Embed(title = "Role Created",colour = 0x33FFE5)
        embed.add_field(name = "Role Name",value = f"{role.mention}",inline = False)
        embed.add_field(name = "Created By",value= ctx.author.mention)
        await ctx.send(embed=embed)
      else:
        await ctx.send(f"I Need The **MANAGE ROLES** Permission To Be Able To Execute This Command")
    else:
      await ctx.send(f"You Need The **MANAGE ROLES** Permission To Be Able To Execute This Command")
  elif type == "channel":
    if ctx.author.guild_permissions.manage_channels:
      if abc.guild_permissions.manage_channels:
        channel = await ctx.guild.create_text_channel(name = query)
        embed = discord.Embed(title = "Channel Created",colour = 0x33FFE5)
        embed.add_field(name = "Channel Name",value = f"{channel.mention}",inline = False)
        embed.add_field(name = "Created By",value= ctx.author.mention)
        await ctx.send(embed=embed)
      else:
        await ctx.send(f"I Need The **MANAGE CHANNELS** Permission To Be Able To Execute This Command")
    else:
      await ctx.send(f"You Need The **MANAGE CHANNELS** Permission To Be Able To Execute This Command")
  elif type == "category":

    if ctx.author.guild_permissions.manage_channels:
      if abc.guild_permissions.manage_channels:
        channel = await ctx.guild.create_category(name = query)
        embed = discord.Embed(title = "Category Created",colour = 0x33FFE5)
        embed.add_field(name = "Category Name",value = f"{query}",inline = False)
        embed.add_field(name = "Created By",value= ctx.author.mention)
        await ctx.send(embed=embed)
      else:
        await ctx.send(f"I Need The **MANAGE CHANNELS** Permission To Be Able To Execute This Command")
    else:
      await ctx.send(f"You Need The **MANAGE CHANNELS** Permission To Be Able To Execute This Command")
@client.command() 
@blcheck()
async def coinflip(ctx):
  num= random.randint(0,1)
  if num == 0:
    val = "Heads"
  else:
    val = "Tails"
  embed = discord.Embed(title = "Coinflip",colour = 0xA3F70B)
  embed.add_field(name = "Outcome",value = val)
  await ctx.send(embed=embed) 
@client.command()
@blcheck()
async def roleinfo(ctx,role : discord.Role = None):
  count = 0
  perms_string = ""
  if role == None:
    await ctx.send(f"Please Mention A Role Or Pass It's ID To Get Its Info! ;)")
  else: 
    for perm, stat in role.permissions:
      if stat is True:
        perms_string += f"`{str(perm).upper()}`, "
        count += 1
    embed = discord.Embed(title = role.name,colour = 0xFFC300)
    embed.add_field(name= "ID",value = role.id)
    embed.add_field(name = "Created At",value = role.created_at.strftime("%d/%m/%Y %H:%M:%S UTC"))
    embed.add_field(name= "Hoisted",value =role.hoist)
    embed.add_field(name="Position",value = role.position)
    embed.add_field(name= "Mentionable",value = role.mentionable)
    embed.add_field(name="Colour",value = role.color)
    if count < 1:
      embed.add_field(name = "Permissions",value = "None",inline = False )
    else:
      embed.add_field(name = "Permissions",value = perms_string,inline = False)
    await ctx.send(embed=embed)
@client.command(aliases = ['vmute'])
@blcheck()
async def voicemute(ctx,member : discord.Member,*, reason = "No Reason Provided"):
  abc = await ctx.guild.fetch_member(client.user.id)
  owner = await ctx.guild.fetch_member(ctx.guild.owner_id)
  if ctx.author.guild_permissions.mute_members:
    if abc.guild_permissions.mute_members:
      if member.top_role>= ctx.author.top_role or member == owner:
        if ctx.author != owner:
          await ctx.send(f"You Dont Have The Permissions To Interact With {member}")
        else:
          if member.top_role >= abc.top_role or member == owner:
            await ctx.send(f"I Am Unable To Interact With {member}")
          else:
            try:
              await member.edit(mute=True,reason = f"{reason} || Action By {ctx.author}")
              await ctx.send(f"Successfully Muted {member.mention} From Voice")
            except discord.HTTPException as e:
              await ctx.send(f"{member} Is Not Connected To A Voice Channel")
      else:
        if member.top_role >= abc.top_role or member == owner:
          await ctx.send(f"I Am Unable To Interact With {member}")
        else:
          try:
            await member.edit(mute=True,reason = f"{reason} || Action By {ctx.author}")
            await ctx.send(f"Successfully Muted {member.mention} From Voice")
          except discord.HTTPException as f:
            await ctx.send(f"{member} Is Not Connected To A Voice Channel")
    else:
      await ctx.send(f"I Am Missing The **MUTE MEMBERS** Permission Required To Execute This Command")
  else:
    await ctx.send(f"You Are Missing The **MUTE MEMBERS** Permission Required To Execute This Command")
@client.command(aliases = ['vunmute'])
@blcheck()
async def voiceunmute(ctx,member : discord.Member):
  abc = await ctx.guild.fetch_member(client.user.id)
  owner = await ctx.guild.fetch_member(ctx.guild.owner_id)
  if ctx.author.guild_permissions.mute_members:
    if abc.guild_permissions.mute_members:
      if member.top_role>= ctx.author.top_role or member == owner:
        if ctx.author != owner:
          await ctx.send(f"You Dont Have The Permissions To Interact With {member}")
        else:
          if member.top_role >= abc.top_role or member == owner:
            await ctx.send(f"I Am Unable To Interact With {member}")
          else:
            try:
              await member.edit(mute=False,reason =  f"Action By {ctx.author}")
              await ctx.send(f"Successfully Unmuted {member.mention} From Voice")
            except discord.HTTPException as e:
              await ctx.send(f"{member} Is Not Connected To A Voice Channel")
      else:
        if member.top_role >= abc.top_role or member == owner:
          await ctx.send(f"I Am Unable To Interact With {member}")
        else:
          try:
            await member.edit(mute=False,reason = f"Action By {ctx.author}")
            await ctx.send(f"Successfully Unmuted {member.mention} From Voice")
          except discord.HTTPException as f:
            await ctx.send(f"{member} Is Not Connected To A Voice Channel")
    else:
      await ctx.send(f"I Am Missing The **MUTE MEMBERS** Permission Required To Execute This Command")
  else:
    await ctx.send(f"You Are Missing The **MUTE MEMBERS** Permission Required To Execute This Command") 
@client.command()
@blcheck()
async def warn(ctx,member : discord.Member,*,reason = None):
  if ctx.author.guild_permissions.manage_messages:
    await ctx.message.delete()
    if member.bot:
      await ctx.send("You Cant Warn A Bot!")
      return
    if reason == None:
      await ctx.send(f"Please Specify A Reason To Warn Someone.")
    else:
      try:
        await member.send(f"You Have Been Warned In {ctx.guild.name} For: **{reason}**")
        embed = discord.Embed(description = f"**{member.name}#{member.discriminator} Has Been Warned For: {reason}**",colour= 0x3498DB)
        await ctx.send(embed=embed)
      except:
        embed = discord.Embed(description = f"**{member.name}#{member.discriminator} Has Been Warned For: {reason}**",colour = 0x3498DB)
        await ctx.send(embed=embed)
      time = datetime.datetime.now().strftime("%a, %#d %B %Y, %I:%M %p UTC")
      kekwarn = {"uid":member.id,"gid":ctx.guild.id}
      kekdata = {"reason":reason,"time":time,"mod":f"{ctx.author.name}#{ctx.author.discriminator}"}

      await client.warndb.upsert_custom(kekwarn,kekdata)
      print('GG')
@client.command()
async def status(ctx,*,status = None):
  if ctx.author.id == 757589836441059379:
    answers = []
    def check(m):
      return m.author == ctx.author and m.channel == ctx.channel
    await ctx.send(f"What Shall Be The Type Of The Status ?")
    try:
      msg = await client.wait_for('message',timeout = 20.0,check = check)
    except asyncio.TimeoutError:
      await ctx.send("Time's Up! you Didn't Answer In Time")
    else:  
      answers.append(msg.content)
    if answers[0].lower() == "watching":
      await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))  
    elif answers[0].lower() =="listening":
      await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status))
    elif answers[0].lower() == "playing":
      await client.change_presence(activity=discord.Game(name=status))
    elif answers[0].lower() == "streaming":
      await client.change_presence(activity=discord.Streaming(name="Support Server", url="https://discord.gg/MXa2EReETq"))
    await ctx.send(f"Status Setup Done")
@client.command()
@commands.cooldown(1,5,commands.BucketType.user)
@blcheck()
async def quote(ctx):
  results = requests.get('https://type.fit/api/quotes').json()
  num  = random.randint(1,1500)
  content = results[num]['text']
  await ctx.send(f"**{content}**")
@client.command()
@commands.cooldown(1,5,commands.BucketType.user)
@blcheck()
async def dog(ctx):
  result = requests.get('https://dog.ceo/api/breeds/image/random').json()
  data= result['message']
  embed=discord.Embed(title = "🐶 Woof Woof",url = data,colour = 0x3498DB)
  embed.set_image(url = data)
  embed.set_footer(text= f"Requested By {ctx.author.name}#{ctx.author.discriminator}")
  await ctx.send(embed=embed)
@client.command()
@blcheck()
async def commands_list(ctx):
  if not ctx.author.id == 757589836441059379:
    return
  cmd_list = ""
  for cmd in client.commands:
    cmd_list += f"{cmd} , "
  await ctx.send(cmd_list)
@client.command()
@blcheck()
async def editchannel(ctx,channel :discord.TextChannel,flag,*, query):
  if ctx.author.guild_permissions.manage_channels:
    if flag.lower() == "topic":
      await channel.edit(topic = query,reason = f"Action By {ctx.author.name}#{ctx.author.discriminator}")
      await ctx.send("Success!")
    elif flag.lower() == "name":
      await channel.edit(name = query,reason = f"Action By {ctx.author.name}#{ctx.author.discriminator}")
      await ctx.send("Success!")
@client.command()
@blcheck()
async def joke(ctx):
  await ctx.send(pyjokes.get_joke())
@client.command()
@blcheck()
async def ascii(ctx,*,text=None):
  if text == None:
      await ctx.send("Please Supply A Text To Be Converted To Ascii :)")
      return
  if len(text) > 8:
      await ctx.send('Text Should Not Be Greater Than 8 Characters ;)')
      return
  kek=text2art(text)
  await ctx.send(f"```\n{kek}\n```")
@client.command()
@blcheck()
async def rip(ctx,member : discord.Member = None):
  if member == None:
    member = ctx.author
  okay = Image.open('rip-removebg-preview.png').convert('L')
  asset = member.avatar_url_as(size = 256)
  data = BytesIO(await asset.read())
  pfp = Image.open(data)
  pfp= pfp.resize((78,78))
  okay.paste(pfp,(56,124))
  okay.save("profile.jpg")
  await ctx.send(file = discord.File("profile.jpg"))
@client.command()
@blcheck()
async def delete(ctx,member : discord.Member= None):
  if member == None:
    member = ctx.author
  okay = Image.open('plsdelete.jpg').convert('RGB')
  asset = member.avatar_url_as(size = 256)
  data = BytesIO(await asset.read())
  pfp = Image.open(data)
  pfp= pfp.resize((196,196))
  okay.paste(pfp,(120,134))
  okay.save("profile.jpg")
  await ctx.send(file = discord.File("profile.jpg"))
@client.event
async def on_message(message):
  if str(message.channel.type) == "private":
    return
  if message.guild.id == 832905293481771028:
    if message.channel.id == 837307457688436776:
      id = int(message.content)
      user = await client.fetch_user(id)
      embed = discord.Embed(title = f"Vote Logged",timestamp = datetime.datetime.now(),color = 0xFF80ED)
      embed.add_field(name = user,value = f"Thank You For Voting For Me On [Top.gg](https://top.gg/bot/790478502909837333/vote)")
      guild = client.get_guild(810190584059789323)
      channel = discord.utils.get(guild.text_channels,id = 814151238177259520)
      await channel.send(content = f"{user.mention}",embed = embed)
      return
  if message.author.bot == True:
    if message.author.id == 646937666251915264:
      chan = client.get_channel(829233056632143872)
      embed = discord.Embed(timestamp = datetime.datetime.now(),colour = message.author.color)
      embed.set_footer(text = f"Server: {message.guild.name}")
      if 'since this server is currently active!' in message.content.lower():
        data = await client.config.find(message.guild.id)
        if not data:
          lmfao = "Karuta Cardping Service, Which Was Launched In Furious Is Now Configurable!\n\nYou Can Get more Info About The Karuta Cardping Service By Typing `F!karuta Help`\nNote: **This Message   Is Only Shown Once**"
          await message.channel.send(lmfao)
          data = {"_id":message.guild.id,"kreminded":"yes"}
          await client.config.upsert(data)
          return
        if not "ktoggle" in data:
          if not "kreminded" in data:
            lmfao = "Karuta Cardping Service, Which Was Launched In Furious Is Now Configurable!\n\nYou Can Get more Info About The Karuta Cardping Service By Typing `F!karuta Help`\nNote: **This Is Only Shown Once**"
            await message.channel.send(lmfao)
            data = {"_id":message.guild.id,"kreminded":"yes"}
            await client.config.upsert(data)
            return
        lol = data["ktoggle"]
        if lol == "off":
          return
        if not "krole" in data:
          if not "kreminded" in data:
            lmfao = "Karuta Cardping Service, Which Was Launched In Furious Is Now Configurable!\n\nYou Can Get more Info About The Karuta Cardping Service By Typing `F!karuta Help`\nNote: **This Is Only Shown Once**"
            await message.channel.send(lmfao)
            data = {"_id":message.guild.id,"kreminded":"yes"}
            await client.config.upsert(data)
            return
        role = data["krole"]
        mention = f"<@&{role}>"
        if "kmessage" not in data:
          kmsg = "Karuta Has Dropped Some Cards. Be Sure To Grab Them Before They Expire!"
        else:
          kmsg = data["kmessage"]
        text = f"{mention}, {kmsg}\n\nExpires In `60 Seconds`"
        msg = await message.channel.send(text)
        await asyncio.sleep(10)
        await msg.edit(content =f'{mention}, {kmsg}\n\nExpires In `50 Seconds`')
        await asyncio.sleep(10)
        await msg.edit(content =f'{mention}, {kmsg}\n\nExpires In `40 Seconds`')
        await asyncio.sleep(10)
        await msg.edit(content =f'{mention}, {kmsg}\n\nExpires In `30 Seconds`')
        await asyncio.sleep(10)
        await msg.edit(content =f'{mention}, {kmsg}\n\nExpires In `20 Seconds`')
        await asyncio.sleep(10)
        await msg.edit(content =f'{mention}, {kmsg}\n\nExpires In `10 Seconds`')
        await asyncio.sleep(10)
        await msg.edit(content =f'{mention}, Karuta Dropped Some Cards, But They Have Expired And Can No Longer Be Grabbed :/')
        embed.set_image(url = message.attachments[0].url)
    
        await chan.send(embed=embed)
  else:
    if message.attachments:
      data= await client.config.find(message.guild.id)
      if not data or "atoggle" not in data:
        return
      if not data["atoggle"] == "on":
        return
      if not "aaction" in data:
        action ="delete"
      else:
        action = data['aaction']
      types = ['.png','jepg','jpeg','webp','.mp3','.mp4','.jpg','.txt','.pdf',]
      for j in message.attachments:
        kek = j.filename[-4:]
        if not kek.lower() in types:
          try:
            await message.delete()
          except:
            pass
          if action == "kick":
            try:
              await message.author.kick(reason = f"Tried Posting A {kek} Format File In #{message.channel.name}")
            except:
              pass
          elif action == "ban":
            try:
              await message.author.ban(reason = f"Tried Posting A {kek} Format File In #{message.channel.name}")
            except:
              pass
          elif action == "mute":
            if not "mrole" in data:
              return
            muted = message.guild.get_role(data["mrole"])
            if not muted:
              return
            try:
              await message.author.add_roles(muted,reason = f"Tried Posting A {kek} Format File In #{message.channel.name}")
            except:
              return
          elif action == "warn":
            await message.channel.send("{}, No {} Files Allowed!".format(message.author.mention,kek))
            return
          break
  """      
  else:
    data = await client.config.find(message.guild.id)
    if not data:
      return
    if "schannel" not in data:
      return
    if "smessage" not in data:
      return
    guild = message.guild
    if not message.author.guild_permissions.manage_messages:
      channel = message.guild.get_channel(data["schannel"])
      embed = discord.Embed(title = "Sticky Message",description = data["smessage"],colour = 0x74A3E9)
      msg = await message.channel.send(embed=embed)
      if not hasattr(client,'stickymsg'):
        client.stickymsg = msg
      else:
        kek = await message.channel.fetch_message(client.stickymsg.id)
        await kek.delete()
  """
  await client.process_commands(message)
@client.command(aliases = ['kping','karuta'])
@blcheck()
async def cardping(ctx,query = None,*,desc = None):
  if query == None:
    embed = discord.Embed(title = "Karuta Cardping",colour = ctx.author.colour,timestamp = datetime.datetime.now())
    embed.add_field(name ='Information',value = 'Karuta Cardping Is A Brand New Feature Introduced In Furious Which Helps You Ping People Interested In Playing Karuta.\n\nType `F!cardping help` For A Better Info Of This Command.')
    await ctx.send(embed=embed)
    return
  else:
    if query.lower() == 'help':
      embed = discord.Embed(title = 'Karuta Cardping',colour = ctx.author.color,timestamp = datetime.datetime.now())
      embed.add_field(name = "Message",value = "Setup A Custom Message For Cardping\nSyntax: **F!karuta message `<custom Message>`**",inline = False)
      embed.add_field(name = "Role",value = "Setup A Role To Be Pinged Upon A Karuta Card Drop\nSyntax: **F!karuta role `<@role>`**",inline = False)
      embed.add_field(name = 'Toggle',value = 'Toggle The Entire Karuta Cardping System\nSyntax: **F!karuta toggle `<on/off>`**')
      embed.add_field(name = "Addrole",value = f"Member: Adds The Cardping Role To Your Roles If Addrole Is Set To `on`\nSyntax: **F!karuta addrole**\n\nServer Managers: Turn The Karuta Addrole Service On Or Off\nSyntax: **F!karuta addrole `<on\off>`**",inline = False)
      embed.add_field(name = "Removerole",value = f"Member: Removes The Cardping Role From Your Roles If Removerole Is Set To `on`\nSyntax: **F!karuta removerole**\n\nServer Managers: Turn The Karuta Removerole Service On Or Off\nSyntax: **F!karuta removerole `<on\off>`**")
      await ctx.send(embed = embed)
    if query.lower() == 'message':
      if ctx.author.guild_permissions.manage_guild == False:
        await ctx.send('You Need The **`MANAGE SERVER`** Permission To Execute This Command!')
        return
      if desc == None:
        await ctx.send('You Didn\'t Supply A Message. Please Be Sure To Supply A Cardping Message Next Time!')
        return
      okay = {"_id": ctx.guild.id,"kmessage":desc}
      await client.config.upsert(okay)
      await ctx.send(f'Cardping Message Was Set To **{desc}**')
    elif query.lower() == "toggle":
      if ctx.author.guild_permissions.manage_guild == False:
        await ctx.send('You Need The **`MANAGE SERVER`** Permission To Execute This Command!')
        return
      if desc == None:
        return await ctx.send('Please Supply A Toggle Value For Me To Apply. Valid Values: `on` / `off`')
      else: 
        if desc.lower() == 'on':
          okay = {"_id": ctx.guild.id,"ktoggle":"on"}
          await client.config.upsert(okay)
          await ctx.send('Karuta Cardping Was Toggled To On!')
        elif desc.lower() == "off":
          okay = {"_id": ctx.guild.id,"ktoggle":"off"}
          await client.config.upsert(okay)
          await ctx.send('Karuta Cardping Was Toggled To Off!')

        else:
          await ctx.send('Invalid Toggle Supplied!')
    elif query.lower() == "role":
      if ctx.author.guild_permissions.manage_guild == False:
        await ctx.send('You Need The **`MANAGE SERVER`** Permission To Execute This Command!')
        return
      else:
        if desc == None:
          await ctx.send("Please Be Sure To Mention A Role To Be Set As The Karuta Cardping Role!")
        else:
          if not ctx.message.role_mentions:
            return await ctx.send('You Did Not Mention A Role To Be Set As The Cardping Role, Please Be Sure To Mention One Next Time!')
          i = ctx.message.role_mentions[0]
          role = discord.utils.get(ctx.guild.roles,id = i.id)
          if role == None:
            await ctx.send(f'No Role Matching {i} Found In This Server')
          else:
            okay = {"_id": ctx.guild.id,"krole":i.id}
            await client.config.upsert(okay)
            await ctx.send(f'**{i.name}** Was Set As The Karuta Cardping Role And Will Be Pinged Upon A Card Drop By Karuta!')
    elif query.lower() == "addrole":
      if not desc:
        data = await client.config.find(ctx.guild.id)
        if not data or "krole" not in data:
          return await ctx.send('A Karuta Cardping Role Is Not Defined On This Server!')
        if not "karole" in data or data["karole"] != "on":
          return await ctx.send('Karuta Addrole Is Set To `Off` In This Server!')
        if data["karole"] == "on":
          role = discord.utils.get(ctx.guild.roles,id = data["krole"])
          if not role:
            await ctx.send('The Role Set As The Karuta Cardping Role Couldn\'t Be Found In This Server.\n\nPlease Make Sure It Is Not Deleted And Also Is Below My Top Role!')
          try:
            await ctx.author.add_roles(role,reason = "Personal Cardping Addrole Request.")
            await ctx.send(f'You Have Been Given The **{role.name}** On Account Of Your Karuta Addrole Request.')
          except:
            await ctx.send('I Am Unable To Give You The Cardping Role. Please Make Sure That I Have Appropriate Permissions To Assign It To You!')
      else:
        if ctx.author.guild_permissions.manage_guild == False:
          await ctx.send('You Dont Have The `MANAGE SERVER` Permission Required To Execute This Command!')
          return
        if desc.lower() == "on":
          kek = {"_id":ctx.guild.id,"karole":"on"}
          await client.config.upsert(kek)
          await ctx.send('Karuta Addrole Is Now Set To On, Members Can Take The Cardping Role By Typing `F!kping addrole`!')
        elif desc.lower() == "off":
          kek = {"_id":ctx.guild.id,"karole":"off"}
          await client.config.upsert(kek)
          await ctx.send('Karuta Addrole Is Now Set To Off, Members Cannot Take The Cardping Role By Using The Command.')
        else:
          await ctx.send('Thats Not A Valid Query For The Addrole Configuration.\n\nTry Using `F!karuta addrole on` Or `F!karuta addrole off`!') 
    elif query.lower() == "removerole" or query.lower() == "takerole" or query.lower() == "remove":
      if not desc:
        data = await client.config.find(ctx.guild.id)
        if not data or "krole" not in data:
          await ctx.send('A Karuta Cardping Role Is Not Defined On This Server')
          return
        if not "krmrole" in data or data["krmrole"] != "on":
          await ctx.send('Karuta Remove Role Is Set To Off In This Server.')
          return
        if data["krmrole"] == "on":
          role = discord.utils.get(ctx.guild.roles,id = data["krole"])
          if not role:
            await ctx.send('The Role Set As The Karuta Cardping Role Couldn\'t Be Found In This Server.\n\nPlease Make Sure It Is Not Deleted And Also Is Below My Top Role!')
          if role not in ctx.author.roles:
            await ctx.send('You Don\'t Have The Karuta Cardping Role In Your Roles.')
            return
          try:
            await ctx.author.remove_roles(role,reason = "Personal Cardping Removerole Request.")
            await ctx.send(f'**{role.name}** Has Been Removed From Your Roles On Account Of Your Karuta Removerole Request.')
          except:
            await ctx.send('I Am Unable To Remove The Cardping Role From Your Roles. Please Make Sure That I Have Appropriate Permissions To Remove It From You!')

      else:
        if ctx.author.guild_permissions.manage_guild == False:
          return await ctx.send('You Don\'t Have The `MANAGE SERVER` Permission Required To Execute This Command!')
        if desc.lower() == "on":
          kek = {"_id":ctx.guild.id,"krmrole":"on"}
          await client.config.upsert(kek)
          await ctx.send('Karuta Removerole Is Now Set To On, Members Can Remove The Cardping Role By Typing `F!karuta removerole`!')
        elif desc.lower() == "off":
          kek = {"_id":ctx.guild.id,"krmrole":"off"}
          await client.config.upsert(kek)
          await ctx.send('Karuta Removerole Is Now Set To Off, Members Cannot Remove The Cardping Role By Using The Command.')
        else:
          await ctx.send('Thats Not A Valid Query For The Remove Configuration.\n\nTry Using `F!karuta removerole on` Or `F!karuta removerole off`!')     
    elif query.lower() == "config":
      data = await client.config.find(ctx.guild.id)
      if not data:
        krole = "None"
        ktoggle = "Off"
        kmessage = "None"
        krmrole = "Off"
        karole = "Off"
      else:
        if not "krole" in data:
          krole = "None"
        else:
          role = data["krole"]
          krole = f'<@&{role}>'
        if not "kmessage" in data:
          kmessage = "None"
        else:
          kmessage = data["kmessage"]
        if not "ktoggle" in data:
          ktoggle = "Off"
        else:
          ktoggle = str(data["ktoggle"]).capitalize()
        if not "krmrole" in data:
          krmrole = "Off"
        else:
          krmrole = str(data["krmrole"]).capitalize()
        if not "karole" in data:
          karole = "Off"
        else:
          karole = str(data["karole"]).capitalize()
        
      embed = discord.Embed(title = f"Karuta Cardping Settings Of {ctx.guild.name}",colour = ctx.author.color,timestamp = datetime.datetime.now())
      embed.add_field(name = "Cardping Message",value = kmessage)
      embed.add_field(name = "Cardping Role",value = krole,inline = False)
      embed.add_field(name = "Toggle",value = ktoggle)
      embed.add_field(name = "Addrole",value = karole,inline = False)
      embed.add_field(name = "Removerole",value = krmrole,inline = False)
      await ctx.send(embed = embed)


      
      
""" Gao Bhar Ke Functions """
class Document:
  def __init__(self,connection,document_name):
    self.db = connection[document_name]

  async def update(self,dict):
    await self.update_by_id(dict)
  async def get_by_id(self,id):
    return await self.find_by_id(id)
  async def find(self,id):
    return await self.find_by_id(id)
  async def remove(self,id):
    await self.delete_by_id(id)
  async def find_by_id(self,id):
    return await self.db.find_one({"_id":id})

  async def delete_by_id(self,id):
    if not await self.find_by_id(id):
      pass
    await self.db.delete_many({"_id":id})
  async def insert(self,dict):
    if not dict["uid"]:
      raise KeyError("ID Not Found In Supplied Dictionary")
    await self.db.insert_one(dict)
  async def upsert(self,dict):
    if await self.__get_raw(dict["_id"]) != None:
      await self.update_by_id(dict)
      return
    else:
      await self.db.insert_one(dict)
  async def update_by_id(self,dict):
    if not dict["_id"]:
      raise KeyError("_id Not Found In Supplied Dict")
    if not await self.find_by_id(dict["_id"]):
      return
    id = dict["_id"]
    dict.pop("_id")
    await self.db.update_one({"_id":id},{"$set": dict})

  async def __get_raw(self,id):
    return await self.db.find_one({"_id":id})
  async def unset(self, dict):
    if not dict["_id"]:
      raise KeyError("_id not found in supplied dict.")
    if not await self.find_by_id(dict["_id"]):
      return
    id = dict["_id"]
    dict.pop("_id")
    await self.db.update_one({"_id": id}, {"$unset": dict})
  async def find_many_by_custom(self, filter):
    return await self.db.find(filter).to_list(None)
  async def upsert_custom(self, filter_data, update_data, option="set", *args, **kwargs):
    await self.update_by_custom(filter_data, update_data, option, upsert=True, *args, **kwargs)
  async def update_by_custom(self, filter_data, update_data, option="set", *args, **kwargs):
    if not bool(await self.find_by_custom(filter_data)):
      return await self.insert({**filter_data, **update_data})
    await self.db.update_one(filter_data, {f"${option}": update_data}, *args, **kwargs)
  
  async def find_by_custom(self, filter):
    return await self.db.find_one(filter)
mongo_url = "mongodb+srv://EternalSlayer:26112005op@cluster0.ogee5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
@client.event
async def on_member_join(member):
  channel = discord.utils.find(lambda r: 'welcome' in r.topic.lower(),member.guild.text_channels)
  await channel.send(f'Welcome To {member.guild.name}, {member.mention}\n\nBe Sure To Read The Rules Of The Server And Behave Politely With Everyone.\n\nWe Hope You Enjoy Your Stay Here')
  #I Need Members Intents 
@client.command()
@blcheck()
async def prefix(ctx,prefix = None):
  if ctx.author.guild_permissions.administrator:
    if prefix == None:
      await ctx.send("Please Be Sure To Supply The Prefix You Want To Be Set For This Server While Using This Command!")
      return
    if prefix.lower() == "reset":
      await client.config.unset({"_id":ctx.guild.id,"prefix":1})
      await ctx.send('The Prefix Was Successfully Reset To The Default: `F!`')
      return
    okay = {"_id": ctx.guild.id,"prefix":prefix}
    await client.config.upsert(okay)    
    await ctx.send(f'The New Prefix Was Set To `{prefix}` ;)')
  else:
    await ctx.send('You Are Missing The **`ADMINISTRATOR`** Permission Required To Execute This Command!')  
"""
@client.command()
@commands.cooldown(1,120,commands.BucketType.user)
async def giverep(ctx,member : discord.Member = None):
  if member == None:
    await ctx.send('You Didn\'t Mention A Member To Be Given A Reputation, Be Sure To Mention Someone Next Time!')
    ctx.command.reset_cooldown(ctx)
    return
  if member == ctx.author:
    await ctx.send('You Cannot Give Rep To Yourself, Bruh.')
    ctx.command.reset_cooldown(ctx)
    return
  curnt = await client.reps.find(ctx.guild.id)
  if not curnt:
    rep = 0
  elif not "uid" in curnt:
    rep = 0
  else:
    rep = int(curnt["uid"]["reputation"])
  kek = rep + 1
  okay = {"_id": ctx.guild.id,"uid":member.id,"reputation":kek}
  await client.reps.upsert(okay)
  await ctx.send(f'Gave One Reputation To {member}!')
@client.command()
async def reputation(ctx,member :discord.Member = None):
  if not member:
    member = ctx.author
  curnt = await client.reps.find(ctx.guild.id)
  if not curnt:
    return await ctx.send(f'{members}\'s Reputation : `0`')
  if not "uid" in curnt:
    return await ctx.send(f"{member}'s Reputation : `0`")
"""
intents.bans = True 
@client.event
async def on_member_ban(guild,user):
  data = await client.config.find(guild.id)
  if not data or "logchannel" not in data:
    return
  logch = guild.get_channel(data["logchannel"])
  if not logch:
    return
  await asyncio.sleep(1)
  async for entry in guild.audit_logs(action=discord.AuditLogAction.ban,limit = 1):
    await logch.send(f"⚒️ {entry.user} Banned {entry.target}\n\nID: {user.id}\n\nReason : **{entry.reason}**")
    break
@client.event
async def on_guild_channel_create(channel):
  data = await client.config.find(channel.guild.id)
  if not data or "logchannel" not in data:
    return
  logch = channel.guild.get_channel(data["logchannel"])
  if not logch:
    return
  async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.channel_create,limit = 1):
    member = entry.user
    break
  embed = discord.Embed(title = "Channel Created",description = f"Channel Name : **{channel.name}**\nCategory : **{channel.category}**\nType: : **{str(channel.type).capitalize()}**",colour = 0xF2922D,timestamp = datetime.datetime.now())
  embed.add_field(name = "Responsible User",value = f"{member.name}#{member.discriminator}")
  await logch.send(embed = embed)
@client.event
async def on_guild_channel_delete(channel):
  data = await client.config.find(channel.guild.id)
  if not data or "logchannel" not in data:
    return
  logch = channel.guild.get_channel(data["logchannel"])
  if not logch:
    return
  
  async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.channel_delete,limit = 1):
    member = entry.user
    break
  embed = discord.Embed(title = "Channel Deleted",description = f"Channel Name : **{channel.name}**\nCategory : **{channel.category}**",colour = 0xF2922D)
  embed.add_field(name = "Responsible User",value = f"{member.name}#{member.discriminator}")
  embed.set_footer(text= f"ID : {channel.id}")
  await logch.send(embed = embed)
@client.command(aliases = ['logs','modlog'])
@blcheck()
async def setlogs(ctx,query = None):
  if ctx.author.guild_permissions.manage_guild == False:
    return await ctx.send('You Are Missing The **`MANAGE SERVER`** Permission Required To Execute This Command!')
  if not query:
    embed = discord.Embed(title = "Logs",color = ctx.author.color,timestamp = datetime.datetime.now())
    embed.add_field(name = "Info",value = 'Set A Log Channel For The Server.\n\nAll Moderation Actions Will Be Logged Here.')
    embed.add_field(name = "Usage",value='Setting A Channel: **`F!modlog <#channel>`**\n\nTurning Off: **`F!modlog off`**',inline=False)
    await ctx.send(embed = embed)
    return
  if query.lower() == "off":
    await client.config.unset({"_id":ctx.guild.id,"logchannel":1})
    await ctx.send('Modlogs Are Turned Off And Will Not Be Sent!')
    return
  me = await ctx.guild.fetch_member(client.user.id)
  if me.guild_permissions.view_audit_log == False or me.guild_permissions.send_messages == False or me.guild_permissions.embed_links == False or me.guild_permissions.attach_files == False:
    return await ctx.send('I Need The Following Permissions To Correctly Deliver Logs.\n`SEND MESSAGES`\n`EMBED LINKS`\n`ATTACH FILES`\n`VIEW AUDIT LOG`\nPlease Grant Me The Following Permission And Then Use The Command.')
  if not ctx.message.channel_mentions:
    return await ctx.send('Please Be Sure To Mention A Channel To Be Set As The Log Channels!')
    return
  kek = ctx.guild.get_channel(ctx.message.channel_mentions[0].id)
  if not kek:
    await ctx.send('Cannot Find That Channel In This Server!')
    return
  kekek = {"_id":ctx.guild.id,"logchannel":kek.id}
  await client.config.upsert(kekek)
  await ctx.send(f'{kek.mention} Was Set As The Log Channel For This Server.\n\nImportant Actions Taking Place In This Server Will Be Logged There!')
@client.event
async def on_guild_channel_update(before, after):
  data = await client.config.find(before.guild.id)
  if not data or "logchannel" not in data:
    return
  logs = before.guild.get_channel(data["logchannel"])
  if not logs:
    return
  
  async for entry in after.guild.audit_logs(action=discord.AuditLogAction.channel_update,limit = 1):
    member = entry.user
    reason = entry.reason
    break
  embed = discord.Embed(title = "Channel Updated",description = after.mention,colour = 0xF2922D,timestamp = datetime.datetime.now())
  embed.set_footer(text = f"ID : {after.id}")
  if str(after.type) == "text":
    if before.topic != after.topic:
      embed.add_field(name = "Topic [Before]",value = before.topic)
      embed.add_field(name = "Topic [After]",value = after.topic,inline = False)
      embed.add_field(name = "Responsible User",value = f"{member.name}#{member.discriminator}")
      await logs.send(embed=embed)
    elif before.slowmode_delay != after.slowmode_delay:
      embed.add_field(name = "Slowmode[Before]",value = f"{before.slowmode_delay} Seconds")
      embed.add_field(name = "Slowmode[After]",value = f"{after.slowmode_delay} Seconds",inline=False)
      embed.add_field(name = "Resposible User",value = member)
      await logs.send(embed=embed)
  if before.name != after.name:
    embed.add_field(name = "Name [Before]", value = before.name)
    embed.add_field(name = "Name [After]",value = after.name,inline = False)
    embed.add_field(name = "Responsible User",value = f"{member.name}#{member.discriminator}")
    await logs.send(embed=embed)
  elif before.type != after.type:
    embed.add_field(name = "Type[Before]",value = str(before.type).capitalize(),inline = False)
    embed.add_field(name = "Type[After]",value = str(after.type).capitalize(),inline = False)
    embed.add_field(name = "Responsible User",value = f"{member.name}#{member.discriminator}")
    await logs.send(embed=embed)
@client.event
async def on_message_delete(message):
  if message.author.bot:
    return
  data = await client.config.find(message.guild.id)
  if not data or "logchannel" not in data:
    return
  logs = message.guild.get_channel(data["logchannel"])
  if not logs:
    return
  embed = discord.Embed(title = 'Message Deleted',description = f'Message: **{message.content}**\nChannel: <#{message.channel.id}>\nAuthor: {message.author.mention}',colour = 0xF2922D,timestamp = datetime.datetime.now())
  await logs.send(embed = embed)
@client.event
async def on_guild_update(before,after):
  data = await client.config.find(after.id)
  if not data or "logchannel" not in data:
    return
  logs = after.get_channel(data["logchannel"])
  if not logs:
    return
  embed = discord.Embed(description = "The Server Has Been Updated!",colour = 0xF2922D,timestamp = datetime.datetime.now())
  async for entry in after.audit_logs(action=discord.AuditLogAction.guild_update,limit = 1):
    member = entry.user
    break
  if before.name != after.name:
    embed.add_field(name = "Changes",value = f"Target : Name\nBefore: {before.name}\nAfter: {after.name}")
    embed.add_field(name = "Responsible User",value = member,inline = False)
    await logs.send(embed=embed)
  elif before.icon_url != after.icon_url:
    embed.add_field(name = "Changes",value = "Target: Icon")
    embed.add_field(name = "Responsible User",value = member)
    embed.set_image(url = after.icon_url)
    await logs.send(embed=embed)
  elif before.system_channel.id != after.system_channel.id:
    embed.add_field(name = "Changes",value = f"Target: System Channel\nBefore: {before.system_channel.mention}\nAfter: {after.system_channel.mention}")
    embed.add_field(name = "Responsible User",value = member)
    await logs.send(embed=embed)
  elif before.owner_id != after.owner_id:
    embed.add_field(name = "Changes",value = f"Target: Owner\nBefore: <@!{before.owner_id}>\nAfter: <@!{after.owner_id}>")
    await logs.send(embed=embed)
@client.event
async def on_message_edit(before,after):
  if after.author.bot: 
    return
  data = await client.config.find(after.guild.id)
  if not data or "logchannel" not in data:
    return
  logs = after.guild.get_channel(data["logchannel"])
  if not logs:
    return
  if before.content == after.content:
    return

  embed = discord.Embed(title = 'Message Edited',description = f'**Before: {before.content}\n+ After: {after.content}**\nChannel: <#{after.channel.id}>\nAuthor: {after.author.mention}',colour = 0xF2922D,timestamp = datetime.datetime.now())
  await logs.send(embed=embed)
@client.command()
@blcheck()
async def warnings(ctx,member : discord.Member = None):
  if not member:
    member = ctx.author
  warn_filter = {"uid":member.id,"gid":ctx.guild.id}
  warns = await client.warndb.find_many_by_custom(warn_filter)
  if not bool(warns):
    return await ctx.send('There Are No Warnings.')
  lol = ""
  for kek in warns:
    description = f"Warn ID : `{kek['_id']}`]\n • Moderator: {kek['mod']}\nReason: {kek['reason']} • Time: {kek['time']}"
    lol += f"{description}\n"
  embed = discord.Embed(title =f"Warnings Of {member}",description = lol)
  await ctx.send(embed = embed)


class Topgg():
  def __init__(self,bot):
    self.bot = bot
    self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc5MDQ3ODUwMjkwOTgzNzMzMyIsImJvdCI6dHJ1ZSwiaWF0IjoxNjEyNTI3NTExfQ.lbl6oMuLvlqSGGnhV5y2Z3ZOXU0ldwUTHgXKVYytAD4"
    self.dblpy = dbl.DBLClient(self.bot,self.token)
@client.command(aliases = ['config','serverconfig'])
@blcheck()  
async def configuration(ctx):
  if ctx.author.guild_permissions.manage_guild == False:
    await ctx.send(f"You Need The **MANAGE SERVER** Permission Required To Execute This Command!")
    return
  data = await client.config.find(ctx.guild.id)
  if not data:
    prefix = "F!"
    logch = "None"
    mrole = "None"
    krole = "None"
    ktoggle = "Off"
    kmessage = "None"
  else:
    if not "prefix" in data:
      prefix = "F!"
    else:
      prefix = data["prefix"]
    if not "logchannel" in data:
      logch = "None"
    else:
      logch = data["logchannel"]
    if not "mrole" in data:
      mrole = "None"
    else:
      mrole = data["mrole"]
    if not "krole" in data:
      krole = "None"
    else:
      krole = data["krole"]
    if not "kmessage" in data:
      kmessage = "None"
    else:
      kmessage = data["kmessage"]
    if not "ktoggle" in data:
      ktoggle = "Off"
    else:
      ktoggle = str(data["ktoggle"]).capitalize()
  embed = discord.Embed(title = "Server Configuration",colour = ctx.author.color,timestamp = datetime.datetime.now())
  embed.add_field(name = "Prefix",value = prefix)
  if logch == "None":
    embed.add_field(name = "Log Channel",value = "None")
  else:
    embed.add_field(name = "Log Channel",value = f"<#{logch}>")
  if mrole == "None":
    embed.add_field(name = "Muterole",value = "None")
  else:
    embed.add_field(name = "Muterole",value = f"<@&{mrole}>")
  embed.set_footer(text = f"Type {prefix}karuta help To See The Karuta Cardping Settings",icon_url= ctx.author.avatar_url)
  await ctx.send(embed=embed)

@client.command()
async def stickynote(ctx,query= None,*,desc= None):
  return
  if ctx.author.guild_permissions.manage_guild == False:
    await ctx.send('You Don\'t Have Have The **MANAGE SERVER** Permission Required To Execute This Command.')
    return
  if not query:
    embed = discord.Embed(title = "Sticky Note",description = "<:emoji_2:810202313142566992> Helps You Create Sticky Messages To A Channel.",timestamp = datetime.datetime.now())
    embed.add_field(name = "Setchannel",value = "Set The Sticky Channel For This Server\n\nSyntax: F!stickynote channel #channel")
    embed.add_field(name = "Message",value = "Set The Sticky Message For This Server\n\nSyntax: **F!stickynote message <message>**",inline = False)
    await ctx.send(embed=embed)
    return
  if query.lower() == "channel":
    if not ctx.message.channel_mentions:
      await ctx.send('Please Be Sure To Mention A Channel To Be Set As The Sticky Channel.')
      return
    channel = ctx.message.channel_mentions[0]
    chan = discord.utils.get(ctx.guild.text_channels,id = channel.id)
    if not chan:
      await ctx.send('That Channel Could Not Be Found. Please Make Sure That It Belongs To This Server!')
      return
    okay = {"_id":ctx.guild.id,"schannel":chan.id}
    await client.config.upsert(okay)
    await ctx.send(f'{chan.mention} Is Now Set As The Sticky Channel For This Server.')
  elif query.lower() == "message":
    if not desc:
      await ctx.send('Please Be Sure To Supply A Message To Be Setup As The Sticky Message.')
      return
    okay = {"_id":ctx.guild.id,"smessage":desc,"sid":ctx.author.id}
    await client.config.upsert(okay)
    await ctx.send(f'**{desc}** Is Now Set As The Sticky Message For This Server.')

@client.command()
@blcheck()
async def report(ctx,args: discord.Member= None,*,kwargs = None):
  data = await client.config.find(ctx.guild.id)
  if not data or "reportchannel" not in data:
    prefix = data["prefix"]
    if not prefix:
      prefix = "F!"
    else:
      prefix = data["prefix"]
    await ctx.send(f'A Report Channel Is Not Set On This Server!\n\nServer Managers Can Set The Channel By Using `{prefix}reportset #channel`')
    return
  if not args:
    await ctx.send("You Must Mention A Member Or use Their ID To Lodge A Report Against Them!")
    return
  if args == ctx.author:
    await ctx.send('You Can\'t Lodge A Report Against Yourself 🗿')
    return
  if not kwargs:
    await ctx.send('You Must Specify Your Report Against The Member For Support To Look Up For It!')
    return
  channel = discord.utils.get(ctx.guild.text_channels,id = data["reportchannel"])
  if not channel:
    await ctx.send('The Channel Set As The Report Couldn\'t Be Found. Please Make Sure That Is Not Deleted And Is Viewable By Me.\n\nServer Managers Can Set The Channel By Using `F!reportset #channel`')
    return
  await ctx.message.delete()
  embed = discord.Embed(description = f"Report Logged By {ctx.author}",timestamp = datetime.datetime.now(),colour = ctx.author.color)
  embed.set_author(name = f"{ctx.author.name}#{ctx.author.discriminator}",url= ctx.author.avatar_url)
  embed.add_field(name = "Member Reported",value = args,inline = False)
  embed.add_field(name = "Report",value = kwargs,inline = False)
  embed.set_footer(icon_url = client.user.avatar_url)
  await channel.send(embed=embed)
  await ctx.send('User Has Been Reported To Proper Authorities.')
@client.command()
@blcheck()
async def reportset(ctx,channel : discord.TextChannel= None):
  if not ctx.author.guild_permissions.manage_guild:
    await ctx.send('You Don\'t Have The **MANAGE SERVER** Permission Required To Execute This Command!')
    return
  okay = {"_id":ctx.guild.id,"reportchannel":channel.id}
  await client.config.upsert(okay)
  await ctx.send(f'{channel.mention} Has Been Set As The Report Channel For This Server.')
@client.command()
@blcheck()
async def starboard(ctx,args = None,kwargs = None):
  data = await client.config.find(ctx.guild.id)
  if not data or "prefix" not in data:
    prefix = "F!"
  else:
    prefix = data["prefix"]
  if not args:
    embed = discord.Embed(title = "Starboard",colour = 0xFFC300)
    embed.add_field(name = "General Info",value = "Starboard Forms A Crucial Part Of Many Servers. Messages Reacted With ⭐ Are Sent To A Channel Which Is The Hall Of Fame Of Messages.\n\nStarboard Has Also Been Introduced In Furious And You Can Refer To The Methods Stated Below For Setting Up The Starboard.")
    embed.add_field(name = "Channel",value = f"Set A Channel For Starred Messages To Be Sent.\n\nSyntax: **{prefix}starboard channel <#channel>**",inline = False)
    embed.add_field(name = "Limit",value = f"Setup The Minimum React Limit For A Message To Be Sent To The Starboard Channel\n\nSyntax: **{prefix}starboard limit `<number>`**",inline = False)
    embed.add_field(name = "Increment",value = f"Setup An Increment For The Star Limit.\n\nSyntax: **{prefix}starboard increment `<number>`**\n\nThe Starboard Reaction Limit Is Incremented Everytime A Message Is Sent To The Starboard With This Number.",inline=False)
    await ctx.send(embed = embed)
    return
  if args.lower() == "channel":
    if not ctx.author.guild_permissions.manage_guild:
      await ctx.send("You Don\'t Have The **MANAGE SERVER** Permission Required To Execute This Command.")
      return
    if not ctx.message.channel_mentions:
      await ctx.send('Please Be Sure To Mention A Channel Next Time To Be Set As The Starboard Channel.')
      return
    channel = discord.utils.get(ctx.guild.text_channels,id = ctx.message.channel_mentions[0].id)
    if not channel:
      await ctx.send('That Channel Could Not Be Found. Please Make Sure That It Is In This Server And Is Viewable By Me!')
      return
    okay = {"_id": ctx.guild.id,"starchannel":channel.id}
    await client.config.upsert(okay)
    await ctx.send(f'{channel.mention} Was Set As The Starboard Channel Of This Server.')
  elif args.lower() == "limit":
    if not ctx.author.guild_permissions.manage_guild:
      await ctx.send("You Don\'t Have The **MANAGE SERVER** Permission Required To Execute This Command.")
      return
    if not kwargs:
      await ctx.send('Please Be Sure To Specify A Limit For The Starboard Next Time!')
      return
    try:
      kek = int(kwargs)
    except:
      await ctx.send('Limit Should Be An Integer. Try Again With An Integer Next Time.')
      return
    if kek <= 0:
      return await ctx.send('Starboard Reaction Limit Cannot Be 0 Or Less Than 0!')
    okay = {"_id":ctx.guild.id,"starlimit":kek}
    await client.config.upsert(okay)
    await ctx.send(f'Starboard Limit Was Set To **{kwargs}**.')
  elif args.lower() == "increment":
    if not ctx.author.guild_permissions.manage_guild:
      await ctx.send("You Don\'t Have The **MANAGE SERVER** Permission Required To Execute This Command.")
      return
    if not kwargs:
      await ctx.send('Please Be Sure To Specify An Increment For The Starboard Limit Next Time!')
      return
    try:
      kek = int(kwargs)
    except:
      await ctx.send('Increment Should Be An Integer. Try Again With An Integer Next Time.')
      return
    if kek < 0:
      return await ctx.send("Starboard Increment Cannot Be Negative!")
    okay = {"_id":ctx.guild.id,"starinc":kek}
    await client.config.upsert(okay)
    await ctx.send(f"Starboard Increment Was Set To **{kwargs}**.")
  elif args.lower() in ('config','settings','configuration'):
    data = await client.config.find(ctx.guild.id)
    if not data:
      starincrement = "Not Set"
      starlimit = "Not Set"
      starchannel = "Not Set"
    else:
      if "starinc" not in data:
        starincrement = "Not Set"
      else:
        starincrement = data["starinc"]
      if "starchannel" not in data:
        starchannel = "Not Set"
      else:
        starchannel = f'<#{data["starchannel"]}>'
      if "starlimit" not in data:
        starlimit = "Not Set"
      else: 
        starlimit = data["starlimit"]
    embed = discord.Embed(title = f"Starboard Config For {ctx.guild.name}",color = ctx.author.color,timestamp = datetime.datetime.now())
    embed.add_field(name = 'Starboard Channel',value = starchannel)
    embed.add_field(name = "Star Requirement",value = starlimit,inline = False)
    embed.add_field(name = "Starboard Increment",value = starincrement)
    await ctx.send(embed = embed)
@client.event
async def on_reaction_add(reaction,user):
  if user.bot:
    return
  data = await client.config.find(user.guild.id)
  if not data:
    return
  if "starlimit" not in data:
    return
  if "starchannel" not in data:
    return
  if not "starinc" in data:
    inc = 0
  else:
    inc = data["starinc"]
  channel = user.guild.get_channel(data["starchannel"])
  if not channel:
    return
  if not str(reaction.emoji) == '⭐':
    return
  bruh = await reaction.users().flatten()
  count = len(bruh)
  if int(data["starlimit"]) > count:
    return
  embed = discord.Embed(colour =reaction.message.author.colour,timestamp = datetime.datetime.now())
  embed.set_author(name = reaction.message.author,icon_url = reaction.message.author.avatar_url)
  if len(reaction.message.content) >= 1:

    embed.add_field(name = "Content",value = reaction.message.content,inline = False)
  if reaction.message.attachments:
    embed.set_image(url = reaction.message.attachments[0].url)
  if reaction.message.embeds:
    if len(reaction.message.embeds[0].title) >=1:
      embed.add_field(name = "Embed Title",value = reaction.message.embeds[0].title,inline = False)
    if len(reaction.message.embeds[0].description) >= 1:
      embed.add_field(name = "Description",value = reaction.message.embeds[0].description,inline = False)
    if reaction.message.embeds[0].image:
      embed.set_image(url = reaction.message.embeds[0].image.url)
    kek = 0
    if len(reaction.message.embeds[0].fields) >= 1:
      for i in reaction.message.embeds[0].fields:
        embed.add_field(name = reaction.message.embeds[0].fields[kek].name,value = reaction.message.embeds[0].fields[kek].value,inline= reaction.message.embeds[0].fields[kek].inline)
        kek += 1
  embed.add_field(name = "Source",value = f"[Click Here]({reaction.message.jump_url})",inline = False)
  await channel.send(content = f"{count} 🌟",embed = embed)
  kek = data["starlimit"] + inc
  okay = {"_id":user.guild.id,"starlimit":int(kek)}
  await client.config.upsert(okay)
  lol = 0
  try:
    await reaction.message.clear_reaction('⭐')
  except:
    lol += 1
  try:
    await reaction.message.add_reaction('🌟')
  except:
    lol += 1
  print('Successful Starboard Log')

@client.command()
@blcheck()
async def getav(ctx,user: discord.User):
  await ctx.author.send(user.avatar_url)
bl = []
@client.command()
async def blacklist(ctx,query = None,user:discord.User = None):
  if ctx.author.id == 757589836441059379:
    if not user:
      return
    if query.lower() == "add":
      if user.id ==757589836441059379:
        return 
      data = {"_id":user.id,"blacklisted" : "yes"}
      await client.bls.upsert(data)
      await ctx.send(f"Blacklisted {user}")
      try: 
        await user.send(f'You have Been Blacklisted From Using The Bot Because Of Repeatedly Spamming Commands. If You Think This Was A Mistake, Contact The Admins Of The Official Server\n\nhttps://discord.com/invite/M4BhczFbYc')
      except:
        print('DMs Off bruh')
        return
    elif query.lower() == "remove":
      try:
        data = {"_id":user.id,"blacklisted":1}
        await client.bls.unset(data)
        await ctx.send(f'Unblacklisted {user}')
      except:
        await ctx.send('Unknown Blacklist Entry.')
    elif query.lower() == "view":
      return
@client.event
async def on_command(ctx):
  channel = client.get_channel(839897540027351090)
  await channel.send(f"{ctx.author} Used {ctx.command.name} In {ctx.guild.name}")
@client.command()
async def ticket(ctx,query = None,*,desc = None):
  if query == None:
    query = "create"
  if query.lower() == "create":
    channel = await ctx.guild.create_text_channel(name = f"ticket {ctx.author.discriminator}",reason = f"Ticket Support Request By {ctx.author}")
    overwrite = channel.overwrites_for(ctx.author)
    overwrite.view_channel = True
    await channel.set_permissions(ctx.author,overwrite = overwrite)
    lavda = channel.overwrites_for(ctx.guild.default_role)
    lavda.view_channel = False
    await channel.set_permissions(ctx.guild.default_role,overwrite = lavda)
    embed = discord.Embed(title = "Ticket Support",description = "Thank You For Creating A Ticket\nSupport Will Be Reaching You Shortly.\nPlease Be Patient.",colour = ctx.author.color,timestamp = datetime.datetime.now())
    embed.set_footer(text = "Furious || F!invite",icon_url=client.user.avatar_url)
    await channel.send(content = ctx.author.mention,embed=embed)
  elif query.lower() == "delete":
    if ctx.author.guild_permissions.administrator == False:
      return await ctx.send("You Are Missing The **ADMINISTRATOR** Permission Required To Delete Tickets!")
    if not ctx.message.channel_mentions:
      await ctx.send("Please Mention A Valid Ticket To Delete It While Using This Command!")
      return
    channel = discord.utils.get(ctx.guild.text_channels,id = ctx.message.channel_mentions[0].id)
    if not channel:
      return await ctx.send("Cannot Find That Channel In This Server!")
    if not "ticket" in channel.name.lower():
      return await ctx.send('That Channel Is Not A Valid Ticket To Delete!')
    try:
      await channel.delete(reason = "Ticket Delete Request.")
    except:
      await ctx.send('I Am Unable To Delete That Ticket, Please Provide Me The **MANAGE CHANNELS** Permission!')
      return
    try:
      await ctx.send('Deleted The Mentioned Ticket!')
    except:
      return
@client.event
async def on_dbl_test(data):
  print(f"Tested {data}")
@client.event
async def on_command_completion(ctx):
  print(f'Completed {ctx.command.name}')
@client.command()
async def uptime(ctx):
  if not ctx.author.id == 757589836441059379:
    return
  day = (datetime.datetime.now() - client.nowtime).days
  seconds = (datetime.datetime.now() - client.nowtime).seconds
  min = (seconds % 3600) // 60
  if seconds > 60:
    min = min + 1
    seconds = 0
  hour = seconds // 3600
  if min > 60:
    hour = hour + 1
    min = 0
  if hour > 24:
    hour = 0
    day = day + 1
  embed = discord.Embed(title = "Uptime",color = ctx.author.color,description = "Calculating Uptime <a:Loading:818320610077179934>")
  msg = await ctx.send(embed = embed)
  await asyncio.sleep(2)
  em = discord.Embed(title = "Uptime",description = f"**{day}** Days **{hour}** Hours **{min}** Minutes **{seconds}** Seconds",color = ctx.author.color)
  await msg.edit(embed = em)
import io
import contextlib
def clean_code(content):
  if content.startswith("```") and content.endswith("```"):
    return "\n".join(content.split("\n")[1:])[:-3]
  else:
    return content
import textwrap

@client.command(aliases = ['eval'])
async def evaluate(ctx, *, arg = None):
  if not ctx.author.id == 757589836441059379:
    return
  if arg == None:
    await ctx.send('I Got Nothing To Evaluate, Bro!')
    return
  if "token" in arg.lower():
    return await ctx.send('My Token Is Damn Secret And Cannot Be Leaked.')
  code = clean_code(arg)
  local_variables = {
    "discord": discord,
    "commands": commands,
    "client": client,
    "ctx": ctx,
    "channel": ctx.channel,
    "author": ctx.author,
    "guild": ctx.guild,
    "message": ctx.message}

  stdout = io.StringIO()
  try:
    with contextlib.redirect_stdout(stdout):
      exec(f"async def func():\n{textwrap.indent(code, '    ')}", local_variables,)
      obj = await local_variables["func"]()
      result = f"{stdout.getvalue()}"
  except Exception as e:
    kekek = f"{e}, {e}, {e.__traceback__}"
    result = "".join(kekek)
  embed = discord.Embed(title = "Eval",color = ctx.author.color)
  embed.add_field(name = "Command",value = f"{arg}")
  embed.add_field(name = "Result",value = result,inline= False)
  await ctx.send(embed = embed)
client.ses = aiohttp.ClientSession()

@client.command()
@blcheck()
async def addemoji(ctx,name = None,url = None):
  if ctx.author.guild_permissions.manage_emojis:
    if not name:
      return await ctx.send('You Must Specify A Name For The Emoji!')
    if not url:
      await ctx.send('Please Specify A Url for The Emoji!')
      return
    if not url.startswith('https://'):
      return await ctx.send('An Invalid URL Has Been Passed!')
    async with client.ses.get(url) as r:
      if not r.status in range(200,299):
        return await ctx.send('Error While Making A Request.')
      img = BytesIO(await r.read())
      bytes = img.getvalue()
      def check(reaction,user):
        return user == ctx.author and str(reaction.emoji) in ("✅","❎")
      msg = await ctx.send(f"Are You Sure You Want To Add This Emoji ?\n{url}")
      list = ['✅','❎']
      for i in list:
        await msg.add_reaction(i)
      try:
        reaction,user = await client.wait_for('reaction_add',check = check,timeout = 20.0)
      except asyncio.TimeoutError:
        await ctx.send(f'Time\'s Up!')
        return
      else:
        if str(reaction.emoji) == "✅":
          try:
            emoji = await ctx.guild.create_custom_emoji(name = name,image = bytes)
            if emoji.animated == False:
              await ctx.send(f'Created Emoji <:{emoji.name}:{emoji.id}>')
            else:
              await ctx.send(f'Created Emoji <a:{emoji.name}:{emoji.id}>')
          except discord.HTTPException:
            await ctx.send(f'Failed Creating The Emoji.\nThis May Happen If The File Size Is Too Big Or Your Server Has Reached The Maximum Emoji Limit!')
          except discord.Forbidden:
            await ctx.send('Failed Creating The Emoji, Perhaps I Am Missing The **MANAGE EMOJIS** Permission!')
        elif str(reaction.emoji) == "❎":
          return await ctx.send("Aborted The Emoji Creation Process")



@client.command()
@blcheck()
async def tag(ctx,query = None,name= None,*,desc = None):
  if not query:
    embed = discord.Embed(title = "Tag",color = ctx.author.color,timestamp = datetime.datetime.now())
    embed.add_field(name = 'Usage',value = "**`F!tag [name]`**",inline=False)
    embed.add_field(name = "Creating Tags",value = f"**F!tag create `<tag name>` `<tag value>`**")
    await ctx.send(embed = embed)
    return
  if query.lower() == "create":
    if not ctx.author.guild_permissions.manage_guild:
      return await ctx.send('You Need The **MANAGE SERVER** Permissions To Be Able To Create Tags!')
    if not name:
      await ctx.send(f'Please Specify A Name For The Tag\n\nUsage: **`F!tag <name> <description>`**')
      return
    if not desc:
      await ctx.send(f"Please Specify A Description For The Tag\n\nUsage: **`F!tag <name> <description>`**")
      return
    if name.lower() in ('create','delete'):
      await ctx.send('Tag Could Not Be Creating Because Of Conflicting Aliases. Did You Use Words Such As `Create` And `Delete` ?')
      return
    lmao = name.lower()
    lmfao = desc.lower()
    data = {"_id":ctx.guild.id,f"tag{lmao}":lmfao}
    await client.config.upsert(data)
    await ctx.send(f'Created Tag `{lmao}`')
  elif query.lower() == "delete":
    if not ctx.author.guild_permissions.manage_guild:
      return await ctx.send('You Need The **MANAGE SERVER** Permission To Be Able To Delete Tags!')
    if not name:
      return await ctx.send(f"Please Be Sure To Mention The Name Of The Tag To Be Deleted!")
    data = await client.config.find(ctx.guild.id)
    if not data or str(f"tag{name.lower()}") not in data:
      return await ctx.send(f'No Tag Named {name} Found!')
    okay = {"_id":ctx.guild.id,f"tag{name.lower()}":1}
    await client.config.unset(okay)
    await ctx.send(f"Deleted Tag {name.lower()}")
  else:
    data = await client.config.find(ctx.guild.id)
    if not data or str(f"tag{query.lower()}") not in data:
      return await ctx.send(f'No Tag Named `{query}` Found!')
    lol = f"tag{query.lower()}"
    await ctx.send(data[lol])

@client.command()
@blcheck()
async def rob(ctx,member : discord.Member = None):
  data = await client.economy.find(ctx.author.id)
  if not data:
    await ctx.send('You Need Atleast $ 500 To Rob Someone!')
    okay= {
      "_id":ctx.author.id,
      "cash":0,
      "bank":0
    }
    await client.economy.upsert(okay)
    return
  else:
    if int(data["cash"]) < 500:
      return await ctx.send('You Need Atleast $ 500 To Rob Someone!')
    if not member:
      return await ctx.send('You Need To Mention A Member To Attempt A Robbery On Them!')
    smh = await client.economy.find(member.id)
    if not smh:
      okay= {
      "_id":member.id,
      "cash":0,
      "bank":0}
      await client.economy.upsert(okay)
      return await ctx.send('The Member Doesn\'t Have Atleast $ 500 In Their Wallet, Not Worth Robbing.')
    if int(smh["cash"]) < 500:
      return await ctx.send('The Member Doesn\'t Have Atleast $ 500 In Their Wallet, Not Worth Robbing.')
    attempt = random.randint(1,2)
    if attempt == 1:
      if int(data["cash"]) == 500:
        kekw = int(smh["cash"]) + 500
        lol = {"_id":member.id,"cash":kekw}

        await client.economy.upsert(lol)
        await client.economy.upsert({"_id":ctx.author.id,"cash":0})
        await ctx.send(f"You Failed Robbing {member} And Ended Up Paying Them $ 500.")
        return
      else:
        some = random.randint(500,data["cash"])
        lmao = int(smh["cash"]) + some
        lol = {"_id":member.id,"cash" : lmao}
        smfh = int(data["cash"]) - some
        await client.economy.upsert(lol)
        await client.economy.upsert({"_id":ctx.author.id,"cash":smfh})
        await ctx.send(f"You Failed Robbing {member} And Ended Up Paying Them $ {some}.")
    else:
      somenum = random.randint(500,smh["cash"])
      if smh["cash"] == 500:
        oki = int(data["cash"]) + 500
        nope = 0
        await client.config.upsert({"_id":ctx.author.id,"cash":oki})
        await client.config.upsert({"_id":member.id,"cash":0})
        await ctx.send(f'You Managed To Rake Up $ 500 From {member}')
        return
      kekek = int(data["cash"]) + somenum
      lolbro = int(smh["cash"]) - somenum
      await client.config.upsert({"_id":ctx.author.id,"cash":kekek})
      await client.config.upsert({"_id":member.id,"cash":lolbro})
      await ctx.send(f'You Managed To Rake Up $ {somenum} From {member}')
@client.command()
async def test(ctx):
  if ctx.author.id == 757589836441059379:
    embed = discord.Embed(title = 'Test')
    embed.add_field(name = f"React To This For Test, Bro.",value = "Test")
    reactions = ['⬅️','⏹️','➡️']
    msg = await ctx.send(embed=embed)
    for i in reactions:
      await msg.add_reaction(i)
    embed1 = discord.Embed(title = "Pog")
    embed2= discord.Embed(title = "Poggers")
    embed3 = discord.Embed(title = "Stopped")
    def check(reaction,user):
      return user == ctx.author
    try:
      reaction,user = await client.wait_for('reaction_add',timeout = 10.0,check=check)
    except asyncio.TimeoutError:
      await msg.clear_reactions()
    else:
      if str(reaction.emoji) == "⬅️":
        await msg.edit(embed = embed1)
      elif str(reaction.emoji) == "⏹️":
        await msg.edit(embed=embed3)
      elif str(reaction.emoji) == "➡️":
        await msg.edit(embed=embed2)
      else:
        await msg.clear_reactions()
@client.event
async def on_guild_role_update(before,after):
  data = await client.config.find(after.guild.id)
  if not data:
    return
  if not "stoggle" in data:
    return
  if data["stoggle"] != "on":
    return
  if after.id == after.guild.id:
    hostile_perms = ""
    async for entry in after.guild.audit_logs(action = discord.AuditLogAction.role_update,limit = 1):
      user = entry.user
      break
    if user.bot:
      return
    if after.permissions.administrator:
      hostile_perms += f"• Administrator\n"
      await after.edit(permissions = before.permissions)
      
    if after.permissions.manage_channels:
      await after.edit(permissions = before.permissions)
      hostile_perms += f"• Manage Channels\n"
      
    if after.permissions.manage_roles:
      await after.edit(permissions = before.permissions)
      hostile_perms += f"• Manage Roles\n"
      
    if after.permissions.manage_emojis:
      await after.edit(permissions = before.permissions)
      hostile_perms += f"• Manage Emojis\n"
      
    if after.permissions.manage_webhooks:
      await after.edit(permissions = before.permissions)
      hostile_perms += f"• Manage Webhooks\n"
      
    if after.permissions.manage_guild:
      await after.edit(permissions = before.permissions)
      hostile_perms += f"• Manage Server\n"
      
    if after.permissions.manage_nicknames:
      await after.edit(permissions = before.permissions)
      hostile_perms += f"• Manage Nicknames\n"
      
    if after.permissions.manage_messages:
      await after.edit(permissions = before.permissions)
      hostile_perms += f"• Manage Messages\n"
      
    if after.permissions.kick_members:
      await after.edit(permissions = before.permissions)
      hostile_perms += f"• Kick Members\n"
    if after.permissions.ban_members:
      await after.edit(permissions = before.permissions)
      hostile_perms += f"• Ban Members\n"
    if not "logchannel" in data:
      return
    channel = discord.utils.get(after.guild.text_channels,id = data["logchannel"])
    if not channel:
      return
    if not "sping" in data:
      ping = "off"
    elif data["sping"] == "off":
      ping = "off"
    elif data['sping'] == "on":
      ping = "on" 
    if len(hostile_perms) > 1:
      if ping == "off":
        await channel.send(content = f"{user} Granted The **`@everyone`** Role These Moderation Permissions:\n{hostile_perms}")
      else:
        if not "modrole" in data:
          await channel.send(content = f"{user} Granted The **`@everyone`** Role These Moderation Permissions:\n{hostile_perms}")
        else:
          await channel.send(content = f"<@&{data['modrole']}>\n{user} Granted The **`@everyone`** Role These Moderation Permissions:\n{hostile_perms}")
@client.command()
@blcheck()
async def setmodrole(ctx,role: discord.Role = None):
  if ctx.author.guild_permissions.manage_guild:
    if not role:
      return await ctx.send(f"Please Mention A Role To Be Set As The Modrole For This Server.")
    data = {"_id":ctx.guild.id,"modrole":role.id}
    await client.config.upsert(data)
    await ctx.send(f"**{role.name}** Has Been Setup As The Mod Role Of This Server.\nThis Will Be Pinged When Any Security Issues Occur In The Server!")
  else:
    return await ctx.send(f"You Need The **MANAGE SERVER** Permission Required To Execute This Command!")
@client.command()
@blcheck()
async def security(ctx,query = None,desc = None):
  if not query or query.lower() == "help":
    embed = discord.Embed(title = "Security",color = ctx.author.color,timestamp = datetime.datetime.now())
    embed.add_field(name = "About",value = f"Security Service Helps You Keep A Watch On The Hostile Activites Going Around In Your Server!",inline = False)
    embed.add_field(name = f"Information",value = f"If The @everyone Role Of The Server Is Granted Any Moderation Permissions, It Would Be Automatically Turned Off And The Moderators Will Be Notified!",inline = False)
    embed.add_field(name = "Methods",value = f"• **`F!setmodrole <@role>`**\n• **`F!security <on/off>`**\n• **`F!security ping <on/off>`**")
    await ctx.send(embed=embed)
    return
  if query.lower() == "on":
    if not ctx.author.guild_permissions.administrator:
      return await ctx.send(f"You Don't Have The **`ADMINISTRATOR`** Permission Required To Execute This Command!")
    if not ctx.guild.me.guild_permissions.manage_guild:
      return await ctx.send(f"I Need The **`ADMINISRATOR`** In Order To Correctly Deliver Security Services!")
    data = {"_id":ctx.guild.id,"stoggle":"on"}
    await client.config.upsert(data)
    await ctx.send(f"Security Services Are Now Toggled On!")
    return
  if query.lower() == "off":
    if not ctx.author.guild_permissions.administrator:
      return await ctx.send(f"You Don't Have The **`ADMINISTRATOR`** Permission Required To Execute This Command!")
    data = {"_id":ctx.guild.id,"stoggle":"off"}
    await client.config.upsert(data)
    await ctx.send(f"Security Services Are Now Toggled Off!")
    return
  if query.lower() == "ping":
    if not ctx.author.guild_permissions.administrator:
      return await ctx.send(f"You Don't Have The **`ADMINISTRATOR`** Permission Required To Execute This Command!")
    if not desc or desc.lower() not in ('on','off'):
      return await ctx.send("Please Supply A Valid Ping Toggle: **`<on/off>`**")
    if desc.lower() == "on":
      data = {"_id":ctx.guild.id,"sping":"on"}
      return await ctx.send("Security Ping Has Been Turned On. The Modrole Will Be Pinged Upon Security Issues!")
    if desc.lower() == "off":
      data = {"_id":ctx.guild.id,"sping":"off"}
      return await ctx.send("Security Ping Has Been Turned Off. The Modrole Will Not Be Pinged Upon Security Issues!")

@client.event
async def on_bulk_message_delete(messages):
  data = await client.config.find(messages[0].guild.id)
  if not data:
    return
  if not "logchannel" in data:  
    return
  log = discord.utils.get(messages[0].guild.text_channels,id = data["logchannel"])
  if not log:
    return
  channel = client.get_channel(833262747801878608)
  with open("delmsgs.txt","w") as f:
    for i in range(len(messages)):
      f.write(f"{messages[i].author}: {messages[i].content}\n\n")
  msg = await channel.send(file = discord.File("delmsgs.txt"))
  url = msg.attachments[0].url[39:-4]
  uploadurl = f"https://txt.discord.website/?txt={url}"
  embed = discord.Embed(title = "⚠️ Bulk Delete",timestamp = datetime.datetime.now(),color = messages[0].author.color,url = "https://discord.gg/5zbU6wEhkh")
  async for i in messages[0].guild.audit_logs(action = discord.AuditLogAction.message_bulk_delete,limit = 1):
    user = i.user
    reason = i.reason
    break
  embed.add_field(name = f"Information",value = f"{user} Deleted {len(messages)} Messages In {messages[0].channel.mention}",inline = False)
  embed.add_field(name = f"Quick Links",value = f"[View]({uploadurl}) • [Download]({msg.attachments[0].url})")
  
  await log.send(embed=embed) 
@client.command()
@blcheck()
async def messagelogs(ctx,query = None):
  if ctx.author.guild_permissions.manage_guild:
    if query.lower() == "on":
      lmao = {"_id":ctx.guild.id,"mlogs":'on'}
      await client.config.upsert(lmao)
      await ctx.send("Message Logs Are Now Turned On!")
    elif query.lower() == "off":
      lmao = {"_id":ctx.guild.id,"mlogs":"off"}
      await client.config.upsert(lmao)
      await ctx.send("Message Logs Are Now Turned Off!")
    else:
      if not ctx.message.channel_mentions:
        return await ctx.send(f"Please Mention a Channel To Be Set As The Message Logs Or ")
      channel = discord.utils.get(ctx.guild.text_channels,id = ctx.message.channel_mentions[0].id)
      if not channel:
        return await ctx.send(f"Cannot Find That Channel In This Server!")
      id = channel.id
      kek ={"_id":ctx.guild.id,"mlogch":id}
      await client.config.upsert(kek)
      await ctx.send("Set The Message Logs To <#{}>".format(id))
@client.command(aliases = ['af','filter'])
@blcheck()
async def attachmentfilter(ctx,query = None,desc = None):
  if query == None or query.lower()== "help":
    embed = discord.Embed(title = "📌 Attachment Filter",color = ctx.author.color,timestamp = datetime.datetime.now(),url = "https://discord.gg/5zbU6wEhkh")
    embed.add_field(name = "About",value = f"Attachment Filter Is An Effective Method Of Filtering Out All Malicious Attachments And Files Which Users Send Over Discord.",inline = False)
    embed.add_field(name ="How It Works ?",value = f"Once Turned On, Attachment Filter Will Check For All Files And Attachments In A Message.\n\nIf Any Attachment Of A Suspicious Format Is Found, The Bot Will Immediately Delete The Message And Perform An Action On The Sender **`[Configurable]`**",inline = False)
    embed.add_field(name = "Ignored Formats",value = f"**`png`**, **`jpg`**,**`jpeg`**,**`webp`**,**`mp3`**,**`mp4`**,**`txt`**,**`pdf`**")
    embed.add_field(name = "Usage",value = f"**`F!attachmentfilter <on/off>`**\n**`F!attachmentfilter action <kick/ban/mute>`**",inline = False)
    await ctx.send(embed=embed)
    return
  queries= ['on','off','action']
  if not query.lower() in queries:
    return await ctx.channel.send("An Invalid Query Has Been Passed!")
  if query.lower() == "on":
    if not ctx.author.guild_permissions.administrator:
      return await ctx.send(f"You Are Missing The **ADMINISTRATOR** Permission Required To Execute This Command!")
    lol = {"_id":ctx.guild.id,"atoggle":"on"}
    await client.config.upsert(lol)
    await ctx.send("Attachment Filter Is Now Toggled On!")
  elif query.lower() == "off":
    if not ctx.author.guild_permissions.administrator:
      return await ctx.send(f"You Are Missing The **ADMINISTRATOR** Permission Required To Execute This Command!")
    lol = {"_id":ctx.guild.id,"atoggle":"off"}
    await client.config.upsert(lol)
    await ctx.send("Attachment Filter Is Now Toggled Off!")
  elif query.lower() == "action":
    if not ctx.author.guild_permissions.administrator:
      return await ctx.send(f"You Are Missing The **ADMINISTRATOR** Permission Required To Execute This Command!")
    if not desc:
      return await ctx.send("Please Provide A Valid Action.\nValid Actions: **`Kick`**,**`Ban`**,**`Mute`**,**`Warn`**")
    if not desc.lower() in ("kick","ban","mute","warn"):
      return await ctx.send("Please Provide A Valid Action.\nValid Actions: **`Kick`**,**`Ban`**,**`Mute`**,**`Warn`**")
    if desc.lower() == "kick":
      data = {"_id":ctx.guild.id,"aaction":"kick"}
      await client.config.upsert(data)
      return await ctx.send("Attachment Filter Action Was Successfully Configured To **`Kick`**. Suspicious Attachments Will Be Deleted And The Sender Will Be Kicked Upon Sending!")
    if desc.lower() == "ban":
      data = {"_id":ctx.guild.id,"aaction":"ban"}
      await client.config.upsert(data)
      return await ctx.send("Attachment Filter Action Was Successfully Configured To **`Ban`**. Suspicious Attachments Will Be Deleted And The Sender Will Be Banned Upon Sending!")
    if desc.lower() == "mute":
      data = {"_id":ctx.guild.id,"aaction":"mute"}
      await client.config.upsert(data)
      return await ctx.send("Attachment Filter Action Was Successfully Configured To **`Mute`**. Suspicious Attachments Will Be Deleted And The Sender Will Be Muted Upon Sending!\nAlso Be Sure To Use **`F!muterole setup`** Or **`F!muterole set <@role>`** To Set A Muted Role!")
    if desc.lower() == "warn":
      data = {"_id":ctx.guild.id,"aaction":"warn"}
      await client.config.upsert(data)
      return await ctx.send("Attachment Filter Action Was Successfully Configured To **`Warn`**. Suspicious Attachments Will Be Deleted Automatically And The Sender Will Be Warned!")
@client.command()
@blcheck()
async def website(ctx):
  list = [0xFF80ED,0x3498DB,0x2ECC71,0x00FFFF]
  embed = discord.Embed(title = "Thank You For Choosing Furious",url = "https://discord.gg/5zbU6wEhkh",timestamp = datetime.datetime.now(),colour = random.choice(list))
  embed.add_field(name = "Click Below To View Our Website!",value="[Click Me!](https://drumpybuds.gq/)")
  await ctx.send(embed=embed)
@client.command()
async def softban(ctx,user: discord.Member = None,*,reason = "No Reason Specified"):
  if ctx.author.guild_permissions.ban_members:
    if ctx.guild.me.guild_permissions.ban_members:
      if not user:
        return await ctx.send('Please be Sure To Mention A Member Or use Their ID To Ban Them!')
      if ctx.author.id == ctx.guild.owner_id:
        try:
          await user.ban(reason = f"{reason} || Action By {ctx.author}",delete_message_days=0)
          await ctx.send(f'Softbanned {user} From {ctx.guild.name} || Reason: {reason}')
        except:
          await ctx.send(f'I Am Unable To Interact With {user}')
          return
        try:
          await member.send(f'You Have Been Banned From {ctx.guild.name} Because Of {reason}')
        except:
          return
      else:
        if user.top_role>= ctx.author.top_role or user.id == ctx.guild.owner_id:
          return await ctx.send(f'You Dont Have Permission To Interact With {user}!')
        try:
          await user.ban(reason = f"{reason} || Action By {ctx.author}",delete_message_days=0)
          await ctx.send(f'Softbanned {user} From {ctx.guild.name} || Reason: {reason}')
        except:
          await ctx.send(f'I Am Unable To Interact With {user}')
          return
        try:
          await user.send(f'You Have Been Banned From {ctx.guild.name} Because Of {reason}')
        except:
          return
    else:
      await ctx.send(f"I Am Missing The **BAN MEMBERS** Permission Required To Execute This Action")
  else:
    await ctx.send(f"You Are Missing The **BAN MEMBERS** Permission Required To Execute This Action")
@client.command()
@blcheck()
async def kek(ctx):
  await ctx.send("Ok")
client.run(TOKEN)