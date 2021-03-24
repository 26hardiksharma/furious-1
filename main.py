import discord
import os
from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter
import json
import asyncio
import random
import wikipedia
import datetime
import praw 
from PIL import Image
from io import BytesIO
import datetime
import time
import dbl
import requests
import pyjokes
import aiohttp
TOKEN = 'NzkwNDc4NTAyOTA5ODM3MzMz.X-BMeQ.QMkidb3B5HSVnSZMvIQLDtlxsfU'
dbl_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc5MDQ3ODUwMjkwOTgzNzMzMyIsImJvdCI6dHJ1ZSwiaWF0IjoxNjEyNTI3NTExfQ.lbl6oMuLvlqSGGnhV5y2Z3ZOXU0ldwUTHgXKVYytAD4"
dbl_webhook = "https://discord.com/api/webhooks/814525601175437342/FlvD7x4oaoNQvT9PhsvIRIpwv2Q_-J5muSQ1nP1A3U1RVI4GmTLrMELHZN17MFBr2nkt"
client = commands.Bot(command_prefix =["^","<@!790478502909837333> ","F!","f!"],help_command=None,case_insensitive = True)
dbl_client = dbl.DBLClient(bot = client,token =dbl_token,webhook_path=dbl_webhook)
intents = discord.Intents.default()
@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"New Prefixes •  f!help"))
  print('Connected to bot: {}'.format(client.user.name))
  print('Bot ID: {}'.format(client.user.id))
intents.guilds = True
@client.command()
async def kick(ctx,user:discord.Member,*,reason = "No Reason Specified"):
  await ctx.message.delete()
  abc = ctx.guild.get_member(client.user.id)
  owner  = await ctx.guild.fetch_member(ctx.guild.owner_id) 
  if ctx.author.guild_permissions.kick_members:
    if abc.guild_permissions.kick_members:
      if user.top_role >= ctx.author.top_role and ctx.author != owner:
        await ctx.send(f"You Dont Have The Permission To Interact With {user.name}#{user.discriminator}")
      else:
        if abc.top_role > user.top_role and user != owner:
          await user.kick(reason = f"{reason} || Action By {ctx.author.name}#{ctx.author.discriminator}")
          embed = discord.Embed(title = "Kick",description = f"{user.mention} **Has Been Successfully Kicked Out Because Of** :-  {reason}",colour = 0xFF0000)
          await ctx.send(embed=embed)
          try:
            await member.send(f"**You Have Been Kicked From {ctx.guild} Because Of : {reason}**")
          except:
            pass
        else:
          await ctx.send(f"Unable To Interact With {user.name}#{user.discriminator}")
    else:
      await ctx.send(f"I Am Missing The **KICK MEMBERS** Permission Required To Execute This Action")
  else:
    await ctx.send(f"You Are Missing The **KICK MEMBERS** Permission Required To Execute This Action")
@client.command()
async def ban(ctx,user: discord.Member,*,reason = "No Reason Specified"):
  await ctx.message.delete()
  abc = ctx.guild.get_member(client.user.id)
  owner  = await ctx.guild.fetch_member(ctx.guild.owner_id) 
  if ctx.author.guild_permissions.ban_members:
    if abc.guild_permissions.ban_members:
      if user.top_role >= ctx.author.top_role and ctx.author != owner:
        await ctx.send(f"You Dont Have The Permission To Interact With {user.name}#{user.discriminator}")
      else:
        if abc.top_role > user.top_role and user != owner:
          await user.ban(reason = f"{reason} || Action By {ctx.author.name}#{ctx.author.discriminator}")
          embed = discord.Embed(title = "Ban",description = f"{user.mention} **Has Been Successfully Banned Because Of** :-  {reason}",colour = 0xFF0000)
          await ctx.send(embed=embed)
          try:
            await member.send(f"**You Have Been Banned From {ctx.guild} Because Of : {reason}**")
          except:
            pass
        else:
          await ctx.send(f"Unable To Interact With {user.name}#{user.discriminator}")
    else:
      await ctx.send(f"I Am Missing The **BAN MEMBERS** Permission Required To Execute This Action")
  else:
    await ctx.send(f"You Are Missing The **BAN MEMBERS** Permission Required To Execute This Action")
@client.command(aliases = ['um'])
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
async def whois(ctx, member : discord.Member = None):
  if member == None:
    member = ctx.author
  rc = 0
  role_str = ""
  for role in member.roles[1:]:
    role_str += f"{role.mention} "
    rc += 1
  embed = discord.Embed(title = "User Info" , description = member.mention , colour = 0xE91E63)
  embed.add_field(name = "ID", value = member.id , inline = False)  
  embed.set_thumbnail(url = member.avatar_url)
  embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
  embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
  embed.set_footer(icon_url = ctx.author.avatar_url, text = 
  f"Requested By {ctx.author.name}")
  embed.add_field(name= "Avatar Link",value = f"[Click Here]({member.avatar_url})")
  if rc >= 1:
    try:
      embed.add_field(name=f"Roles[{rc}]", value=role_str,inline = False)
    except:
      embed.add_field(name = f"Roles[{rc}]",value = "User Has Too Many Roles!",inline = False)
    embed.add_field(name="Highest Role:", value=member.top_role.mention,inline = False)
  else:
    embed.add_field(name = "Roles",value = "None",inline = False)
  await ctx.send(embed=embed)




@client.command(aliases = ['av'])
async def avatar(ctx, member : discord.Member=None):
  if ctx.author.guild_permissions.manage_messages:
    member = member or ctx.author
    embed = discord.Embed(title = f" {member.name}'s Avatar")
    embed.set_image(url = member.avatar_url)
    await ctx.send(embed=embed)
  else:
    embed = discord.Embed(title = " Avatar")
    embed.add_field(name = "Status", value = f" {ctx.author.mention}, You Don't Have The Permission To Execute This Command",inline = False)
    embed.add_field(name = "Missing Permission(s)", value = "Manage Messages",inline = False)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested By {ctx.author.name}")
    await ctx.send(embed=embed)
@client.command(pass_context=True, aliases = ['clear'])
@commands.cooldown(1,10,commands.BucketType.user)
async def purge(ctx,amt: int = None):
    if ctx.author.guild_permissions.manage_messages:
      if amt == None:
        await ctx.send(f"Please Specify The Number Of Messages To Be Purged")
      else: 
        if amt > 100:
          await ctx.send(f"The Maximum Amount You Can Purge At A Time Is 100!\nPlease Use The Command Multiple Times To Purge More Messages")   
        else:
          try:
            await ctx.message.delete()
            await ctx.channel.purge(limit = amt)
            msg = await ctx.send(f"<a:EO_rtick:798248741429706814> Successfully Purged {amt} Messages")
            await asyncio.sleep(3)
            await msg.delete()
          except commands.BadArgument as e:
            await ctx.send(f"Please Enter Only Integer Value For The Number Of Messages To Be Purged")
    else:
      embed = discord.Embed(title = "Purge")
      embed.add_field(name = "Status", value = f" {ctx.author.mention}, You Don't Have The Permission To Execute This Command",inline = False)
      embed.add_field(name = "Missing Permission(s)", value = "Manage Messages",inline = False)
      embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested By {ctx.author.name}, Made by Eternal_Slayer#0069")
      await ctx.send(embed=embed)
@client.command(aliases = ['m'])
async def mute(ctx,member : discord.Member,*,reason = "No reason Specified"):
  if ctx.author.guild_permissions.manage_messages:
    if member.guild_permissions.manage_messages:
      await ctx.message.delete()
      embed = discord.Embed(title = "<:error:795629492693368833> Mute",colour = 0xFF0000)
      embed.add_field(name = "Status",value = f"That User Is A Moderator/Admin. Command Could Not Be Executed!")
      await ctx.send(embed=embed)
    else:
      rc = 0 
      for r in ctx.guild.roles:
        if "mute" in r.name.lower():
          rc += 1
      if rc == 0:
        await ctx.send("Couldn't Find A Muted Role In This Server!")
      elif rc > 1:
        await ctx.send("Multiple Roles Found Marked As ``Muted`` In This Server! Please Make Sure That There Is Only One Role Named ``Muted`` In This Server")
      else:
        for muted in ctx.guild.roles:
          if "mute" in muted.name.lower():
            await member.add_roles(muted,reason = f"{reason} || Action By {ctx.author.name}#{ctx.author.discriminator}")
            embed = discord.Embed(title = " 🔇 Mute" , description = f" {member.mention} Has Been Successfully Muted" , color = 0xFF0000)
            embed.add_field(name = "Reason", value = reason)
            memberembed = discord.Embed(title = "🔇 Mute", description = "You Have Been Muted", color = discord.Colour.red(), inline = False)
            memberembed.add_field(name = "Moderator :- ", value = ctx.author.name)
            memberembed.add_field(name = "Reason", value = reason, inline = False)
            await member.send(embed = memberembed)
            await ctx.send(embed=embed)
            break
  else:
    await ctx.send("You Are Missing The **`MANAGE MESSAGES`** Permission Required To Execute This Command")
@client.command()
async def botstats(ctx):
  num = 0
  for guild in client.guilds:
    num = num + guild.member_count
  embed = discord.Embed(title = "Bot Stats", description = "<@!790478502909837333>", colour = 0x7FFFD4)
  embed.set_thumbnail(url = 'https://cdn.discordapp.com/avatars/790478502909837333/ffbe1e96004d240eda5385186e145986.webp?size=1024')
  embed.add_field(name = "Creator", value = f"<@!757589836441059379>",inline = False)
  embed.add_field(name= "Prefix",value = "' ^ ', <@!790478502909837333> " )
  embed.add_field(name = "Total Servers Joined", value = str(len
  (client.guilds)),inline = False)
  embed.add_field(name= "Total Users",value = num,inline = False)
  embed.add_field(name = "Ping",value = f"{round(client.latency*1000)} ms",inline = False)
  await ctx.send(embed = embed)
@client.command(pass_context = True,aliases = ['nick'])
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
@commands.cooldown(1, 300, commands.BucketType.user)
async def helpme(ctx,member : discord.Member,*,query):
  if member.guild_permissions.manage_messages:
    await ctx.message.delete()
    dmembed = discord.Embed(title = "Help",description = f"{ctx.author} Needs Your Help", colour = 0x00F2FF)
    dmembed.add_field(name = "Sent By", value = ctx.author,inline= False)
    dmembed.add_field(name = "Message", value = query,inline = False)
    dmembed.add_field(name = "Server",value = ctx.guild.name)
    await member.send(embed=dmembed)
    embed = discord.Embed(title = " <a:tick:796380226963636234> Help Me",colour = 0x00F2FF)
    embed.add_field(name = "Status",value = f"Successfully Sent The Help Call  To {member.mention}",inline = False)
    embed.add_field(name = "Sent By",value = f"{ctx.author.mention}")
    await ctx.send(embed = embed)
  else:

    await ctx.message.delete()
    embed = discord.Embed(title = "<:error:795629492693368833> Help Me",colour = 0xFF0000)
    embed.add_field(name = "Status", value = f"{ctx.author.mention},The Member You Mentioned Is Not A Moderator/Admin")
    await ctx.send(embed=embed)
@helpme.error
async def helpme_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      await ctx.message.delete()
      embed = discord.Embed(title = "<:error:795629492693368833> Help Me",colour = 0xFF0000)
      embed.add_field(name = "Status", value = "You Are Still On Cooldown")
      embed.add_field(name = "Time Remaining",value = '{:.2f}s'.format(error.retry_after),inline = False)
      await ctx.send(embed=embed)      
    else:
        raise error
@client.command()
async def everyone(ctx):
  if ctx.author.guild_permissions.administrator:
    await ctx.message.delete()
    await ctx.send('@everyone')
    await ctx.channel.purge(limit=1)
@client.command(aliases = ['v'])
async def vote(ctx):
  embed = discord.Embed(title = "🗳️ Vote 🗳️",colour = 0xFFEF00)
  embed.add_field(name = "Upvote Me",value = "[Click Here](https://top.gg/bot/790478502909837333/vote)")
  embed.add_field(name = "Support Server",value = "[Click Here](https://discord.gg/MXa2EReETq)")
  embed.add_field(name = "Please Upvote Me",value="Your Upvotes Help Me Gain Reach And Join More Discord Servers!\nPlease Take A Minute And Upvote Me [Here](https://top.gg/bot/790478502909837333/vote)",inline = False)
  embed.set_footer(text = "Voting Gives You A Special Coloured Role In Our Server")
  await ctx.send(embed=embed)
@client.command()
async def misc(ctx):
  embed=discord.Embed(title = "Miscellaneous Commands",colour = 0x00FFD7)
  embed.add_field(name = "Vote",value = "Gives The Top.gg Link Of Our Official Server")
  embed.add_field(name = "Hack",value = "Have Fun Hacking Your Friends",inline=False)
  await ctx.send(embed=embed)
@client.command()
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
  embed.add_field(name = "Invite Link • Normal",value = "[Click Here](https://discord.com/api/oauth2/authorize?client_id=790478502909837333&permissions=2099244279&redirect_uri=https%3A%2F%2Fdiscord.gg%2F4DqmNbUTXa&scope=bot)")
  embed.add_field(name = "Invite Link • Administrator",value = "[Click Here](https://discord.com/api/oauth2/authorize?client_id=790478502909837333&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.gg%2F4DqmNbUTXa&scope=bot)",inline= False)
  embed.add_field(name = "Official Server",value = "[Click Here](https://discord.gg/MXa2EReETq)",inline = False)
  embed.set_thumbnail(url= ctx.author.avatar_url)
  await ctx.send(embed=embed)
@client.command()
async def lock(ctx, channel : discord.TextChannel=None):
  if ctx.author.guild_permissions.manage_channels:
      channel = channel or ctx.channel
      overwrite = channel.overwrites_for(ctx.guild.default_role)
      overwrite.send_messages = False
      await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
      embed = discord.Embed(title = "🔒 Lock",colour = 0xFF0000)
      embed.add_field(name = "Status",value = f"Successfully Locked {channel.mention}")
      await ctx.send(embed=embed)
  else:
    await ctx.send("<:kya_bey:796610669549322250>")

@client.command()
async def unlock(ctx, channel : discord.TextChannel=None):
  if ctx.author.guild_permissions.manage_channels:
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = None
    await channel.set_permissions(ctx.guild.default_role,overwrite=overwrite)
    embed=discord.Embed(title = "🔓Unlock",colour = 0x00FFD3)
    embed.add_field(name = "Status",value = f"Successfully Unlocked {channel.mention} ")
    await ctx.send(embed=embed)
  else:
    embed=discord
    await ctx.send("<:kya_bey:796610669549322250>")
@client.command()
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
async def serverinfo(ctx):
  ccount = 0
  for channel in ctx.guild.text_channels:
    ccount = ccount + 1
  vcount= 0
  for vc in ctx.guild.voice_channels:
    vcount = vcount + 1
  owner = await ctx.guild.fetch_member(ctx.guild.owner_id)
  embed = discord.Embed(title = f"{ctx.guild.name}",colour = 0x00FF12)
  embed.add_field(name = "Owner",value = owner.mention,inline = False)
  embed.add_field(name = "Region",value = f"{ctx.guild.region}",inline = False  )
  embed.add_field(name = "Member Count",value = f"{ctx.guild.member_count}",inline = False)
  embed.add_field(name = "Boosts",value = ctx.guild.premium_subscription_count)
  embed.add_field(name ="Boost Tier",value = f"{ctx.guild.premium_tier}")
  embed.add_field(name = "Verification Level",value= ctx.guild.verification_level)
  embed.add_field(name="Explicit Content Filter",value = ctx.guild.explicit_content_filter)
  embed.add_field(name ="Text Channels",value = f"{ccount}")
  embed.add_field(name ="Voice Channels",value = f"{vcount}")
  embed.set_thumbnail(url = ctx.guild.icon_url)
  await ctx.send(embed=embed)
@client.command()
async def kill(ctx,member : discord.Member):
  if ctx.guild.name == 'VΛИłSĦΣĐ SŁΛҰΣЯS':
    voter = discord.utils.get(ctx.guild.roles,name = "ᛝ𒅎・SΣЯVΣЯ VΩTΣЯS")
    if voter in ctx.author.roles:
      
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
    else:
      embed = discord.Embed(title = "Kill",colour = 0x00FFD3)
      embed.add_field(name = "Status", value = "Only Server Voters Are Allowed To Use This Command 😋")
      embed.add_field(name = "Vote Server",value = "[Click Me](https://top.gg/servers/758381318404308994/vote)",inline = False)
      await ctx.send(embed=embed)
  else:
    embed = discord.Embed(title = "Hack",colour = 0xFF0000)
    embed.add_field(name = "Status", value = "This Command Is Currently Limited To Our Official Server Only")
    embed.add_field(name = "Official Server",value = "[Server Link](https://discord.gg/uKh8Y2fhmJ)",inline = False)
    await ctx.send(embed=embed)  
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
async def slowmode(ctx, unit):
  me = await ctx.guild.fetch_member(client.user.id)
  if ctx.author.guild_permissions.manage_channels:
    if me.guild_permissions.manage_channels:
      time = convert(unit)
      if time == -1:
        await ctx.send("You Didnt Answer With A Proper Unit, Please Answer With A Proper Unit Next Time\n\nUnit References : [s|h|m]")
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
@client.command()
async def giveaway(ctx):
  if ctx.author.guild_permissions.manage_guild:
    await ctx.send(f"So Nice Of You To Create A Giveaway :D... Lets Start With The Setup")
    questions = ["Mention The Channel in Which You want The Giveaway To Be Started","Tell Me The Duration Of The Giveaway! Time Parameters :- [s|m|h|d]","Alright! How Many Winners Should Be There ?","Alright! What Should Be The Prize Of The Giveaway ?"]
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
        embed.set_footer(text = f"{winners} Winners • Ends At {end}")
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
  try:
    new_msg = await channel.fetch_message(id_)
  except:
    await ctx.send("The ID Entered Was Incorrect!")
    return
  users = await new_msg.reactions[0].users().flatten()
  users.pop(users.index(client.user))
  winner = random.choice(users)
  await channel.send(f"The New Winner Is {winner.mention}! Congratulations!")
@client.command()
async def revive(ctx):
  if ctx.author.guild_permissions.administrator:
    await ctx.message.delete()
    msg = await ctx.send(f"**Alert!** DEAD CHAT || @everyone ||")
    await msg.edit(content =f"**DEAD CHAT, PLEASE BE ACTIVE**")
@client.command()
async def wink(ctx):
  embed=discord.Embed(title = f"{ctx.author.name} Is Winking 😉")
  embed.set_image(url = "https://cdn.discordapp.com/attachments/737780593609408532/737815454046879854/5OHh.gif")
  await ctx.send(embed=embed) 
@client.command()
async def pog(ctx):
  embed=discord.Embed(title = f"{ctx.author.name} Is Pogging <:Pog:793075474645254185>")
  embed.set_image(url = "https://cdn.discordapp.com/attachments/796260664577359883/801735309913096223/pog.gif")
  await ctx.send(embed=embed)   
@client.command()
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
      memberembed.set_footer(text = "Made By EternalSlayer#0069")
      await member.send(embed = memberembed)
      await asyncio.sleep(time)
      await member.remove_roles(muted_role)
reddit = praw.Reddit(client_id = "HavE-E7-h3pXDQ",client_secret = "TYAmuss0lnMFOXMZA_si6v-SmfkFJQ",user_agent = "prawop",check_for_async= False)
subreddit = reddit.subreddit("memes")
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
async def help(ctx,query = None):
  me = await ctx.guild.fetch_member(client.user.id)
  if me.guild_permissions.send_messages and me.guild_permissions.attach_files and me.guild_permissions.attach_files:
    if query == None:
      query = 0
    if query == 0:    
      embed = discord.Embed(title = "Help ",colour = 0x00FFD7)
      embed.add_field(name = "Bot Prefixes",value = f"F!\n^\n{client.user.mention}",inline = False)
      embed.add_field(name = "Get Started",value = "Please Refer To The Commands Listed Below",inline=False )
      embed.add_field(name = "<:emoji_2:810202313142566992> Moderation",value  = "`kick`,`ban`,`mute`,`unmute`,`hackban`,`tempmute`,`slowmode`,`lock`,`unlock`,`private`,\n`unprivate`,`setnick`,`muterole`",inline =False)
      embed.add_field(name = "<:emoji_0:810202224947888249> Fun",value= "`wink`,`pog`,`wanted`,`hitler`,`meme`,`dog`,`quote`,`joke`",inline = False)
      embed.add_field(name = "<:emoji_3:810202359362748487> Utility",value = "`whois`,`remindme`,`giveaway`,`roleinfo`,`serverinfo`,`avatar`,`roll`",inline = False)
      embed.add_field(name = "<:emoji_1:810202277624938527> Management",value = "`maintenance`,`serverlock`,`serverunlock`",inline = False)
      embed.add_field(name = "<:emoji_5:810202499914268703> Modules",value = f"Moderation\nUtility\nManagement\nFun\nYou Can Type F!help <module> To Get The Commands Of That Module")
      embed.add_field(name = "Quick Links",value = f"[Invite Me](https://discord.com/api/oauth2/authorize?client_id=790478502909837333&permissions=2099244279&redirect_uri=https%3A%2F%2Fdiscord.gg%2F4DqmNbUTXa&scope=bot) • [Vote](https://top.gg/bot/790478502909837333/vote) • [Support Server](https://discord.gg/MXa2EReETq)",inline = False)
      await ctx.send(embed=embed)
    elif query.lower() == 'fun':
      embed = discord.Embed(title = "Fun",description = "Furious' Fun Commands", colour = 0x00FFD7)
      embed.add_field(name = "Wink",value = "**^wink**",inline = False)
      embed.add_field(name = "Pog",value = "**^pog**",inline = False)
      embed.add_field(name = "Wanted!",value = "**^wanted @user**",inline = False)
      embed.add_field(name = "Hitler!",value = "**^hitler @user**",inline = False)
      embed.add_field(name = "Meme",value = "**^meme**")
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
      embed.add_field(name = "Giveaway",value = "<:emoji_2:810202313142566992> Starts A Giveaway Setup In The Server\nUsage :- ^giveaway",inline = True)
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
async def suggest(ctx,*,query):
  id = ctx.author.id
  if id in blacklists:
    await ctx.send(f"You Are Blacklisted And Revoked From Using The Suggest Command")
  else:
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
  await abc.add_reaction("🥳")
  await abc.add_reaction("🙏")
  em = discord.Embed(title = guild.name,description = "Thanks For Adding Me To This Server! I Surely Will Help You With Your Discord Experience And In Managing This Server :)",colour = 0xDAF7A6)
  em.add_field(name = "Some Useful Information",value = "<:emoji_0:810202224947888249> I Am Furious, A Bot Designed To Moderate Servers While Providing Utility And Other Services To Other Server Members\n<:emoji_2:810202313142566992> Command Prefixes :- ^ , <@790478502909837333>\n<:emoji_3:810202359362748487> A Lot Of Useful Commands Which Come In Handy While Using Discord\n<:emoji_5:810202499914268703> Fun Commands\n<:emoji_1:810202277624938527> Much More Discoverable With ``^help``")
  em.add_field(name = "Some Useful Links",value = f"[INVITE ME](https://discord.com/api/oauth2/authorize?client_id=790478502909837333&permissions=2099244279&redirect_uri=https%3A%2F%2Fdiscord.gg%2F4DqmNbUTXa&scope=bot) || [SUPPORT SERVER](https://discord.gg/gMHkNEYW4H)",inline = False)
  await guild.text_channels[0].send(embed = em)

@client.event
async def on_guild_remove(guild):
  channel = client.get_channel(810205896662712371)
  embed = discord.Embed(title = "😔 I Was Kicked From A Server 😔",colour = 0xFF0000)
  embed.add_field(name = "Server Info",value = f"Server Name :- {guild.name}\n Member Count :- {guild.member_count}\n Guild Region :- {guild.region}\n Total Guilds I Am In :- {str(len(client.guilds))}")
  embed.set_thumbnail(url = f"{guild.icon_url}")
  await channel.send(embed=embed)
@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def trash(ctx, member: discord.Member = None):
  if member== None:
    member = ctx.author
  trash = Image.open("trash.jpg")
  asset = member.avatar_url_as(size = 256)
  data = BytesIO(await asset.read())
  pfp = Image.open(data)
  pfp= pfp.resize((314,306))
  trash.paste(pfp,(308,1))
  trash.save("profile.jpg")
  await ctx.send(file = discord.File("profile.jpg"))
@client.command()
async def feedback(ctx,*,query):
  channel = client.get_channel(802203624566030366)
  embed=discord.Embed(title = '😄 Feedback 😄',colour =0x9FE2BF)
  embed.add_field(name = "Given By",value= f"{ctx.author}",inline = False)
  embed.add_field(name= "Guild Name",value = f"{ctx.guild.name}",inline = False)
  embed.add_field(name= "Feedback",value = f"{query}",inline= False)
  embed.set_thumbnail(url= f"{ctx.author.avatar_url}")
  await channel.send(embed=embed)
  await ctx.send(f"Thanks For Giving A Feedback! We Really Appreciate Your Efforts :D")
@client.command()
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
async def muterole(ctx,query = None):
  if query == None:
    embed = discord.Embed(title = "Muterole")
    embed.add_field(name = "Aliases",value = "None",inline = False)
    embed.add_field(name = "Required Permission(s)",value = "Manage Roles")
    embed.add_field(name = "Description",value = "Setups The Muterole In Your Server\n❯ Creates A Muted Role In The Server\n❯ Sets The Send Messages And Add Reactions Permission In Every Text Channel For The Muted Role To False\n❯ Sets The Speak Permission In Every Voice Channel For The Muted Role To False",inline = False)
    embed.add_field(name = "Cooldown",value = "60 Seconds Per Guild")
    embed.add_field(name = "Additional Tips",value = "Provide The Bot The **`ADMINISTRATOR`** To Make This Work Flawlessly",inline = False)
    await ctx.send(embed=embed)
  else:
    if ctx.author.guild_permissions.manage_roles:
      if query == "setup" or "create":
        mute= discord.utils.get(ctx.guild.roles,name = "Muted")
        if mute in ctx.guild.roles:
          
          await ctx.send("A Muted Role Already Exists In This Guild! What Actions Do You Want me To Perform ?\n1) Set Permissions And Overrides For The Existing Muted Role (Reply With **1** For This)\n2) Delete The Muted Role And Create A New One With Updated Permissions(Reply With **2** For This)")
          answers = []
          def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
          try:
            msg = await client.wait_for('message',timeout = 20.0,check = check)
          except asyncio.TimeoutError:
            await ctx.send("Time's Up! you Didn't Answer In Time")
            return
          else:
            answers.append(msg.content)
          if answers[0] == "1":
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
            await mute.delete()
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
            await ctx.send(f"Muterole Setup Successfully Completed")
        else:
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
          await ctx.send(f"Muterole Setup Successfully Completed")
@client.command(aliases= ["ccreate"])
async def create_category(ctx, *, name):
  if ctx.author.guild_permissions.manage_guild:
    await ctx.guild.create_category(name)
    await ctx.send(f"Successfully Create Category :- {name}")
  else:
    await ctx.send(f"You Are Missing The **MANAGE SERVER** Permissions Required To Execute This Command!")
@client.command()
@commands.cooldown(1, 5, commands.BucketType.guild)
async def serverlock(ctx):
  if ctx.author.guild_permissions.manage_guild and ctx.author.guild_permissions.manage_channels:
    for channel in ctx.guild.text_channels:
      overwrite = channel.overwrites_for(ctx.guild.default_role)
      overwrite.send_messages = False    
      await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
      await asyncio.sleep(0.2)
    await ctx.send(f"Successfully Locked All Channels For {ctx.guild.name}")
  else:
    await ctx.send(f"You Dont Have The **MANAGE CHANNELS** AND **MANAGE MESSAGES** Permissions Required To Execute This Command!")
@client.command()
@commands.cooldown(1, 60, commands.BucketType.guild)
async def serverunlock(ctx):
  if ctx.author.guild_permissions.manage_guild and ctx.author.guild_permissions.manage_channels:
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
async def maintenance(ctx,query = None):
  if query == None:
    embed = discord.Embed(title = "Maintenance")
    embed.add_field(name = "Aliases",value = "None",inline = False)
    embed.add_field(name = "Required Permission(s)",value = "Administrator",inline = False)
    embed.add_field(name = "Description",value = "❯ Makes All Text Channels Of The Server Private (Taking The View Channel From The @everyone Role In Every Channel)\n❯ Makes All Voice Channels Of The Server Private (Taking The View Channel From The @everyone Role In Every Voice Channel)\n❯ Creates 3 Channels To Keep The Server Activity Going On, Namely\n**`maintenance-chat`**\n**`maintenance-botzone`**\n**`Maintenance VC`**",inline = False)
    embed.add_field(name = "Cooldown",value = "60 Seconds Per Guild",inline = False)
    embed.add_field(name = "Usage",value = "❯ Turning On: **`F!maintenance on`**\n❯ Turning Off: **`F!maintenance off`**",inline = False)
    embed.add_field(name = "Additional Tips",value = "❯ Don't Use This Command Is Your Server Is A Verify-Type Server. Instead, Use **`F!serverlock`**\n❯ Provide The Bot The **`ADMINISTRATOR`** Permission To Make This Work Flawlessly",inline=False)
    await ctx.send(embed=embed)
  else:
    if ctx.author.guild_permissions.administrator:
      me = await ctx.guild.fetch_member(client.user.id)
      if me.guild_permissions.administrator:
        if query == "on":
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
        elif query == "off":
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
      else:
        await ctx.send("I Am Missing The **`ADMINISTRATOR`** Permission Required To Execute This Command!")
    else:
      await cts.send("You Are Missing The **`ADMINISTRATOR`** Permission Required To Execute This Command!")      
@client.command()
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
async def invites(ctx,member : discord.Member= None):
  if member == None:
    member = ctx.author
  total = 0
  for i in await ctx.guild.invites():
    if i.inviter == member:
      total = total + i.uses
  embed = discord.Embed(title = "Invites",description = ctx.guild.name,colour = 0x00EAFF)
  embed.add_field(name= f"{member.name}'s Invites",value = total)
  await ctx.send(embed=embed)
@client.command()
async def ticket(ctx,query = "create" , channel : discord.TextChannel = None):
  if query == "create":
    num = random.randint(0,100)
    ch = await ctx.guild.create_text_channel(name = f"ticket {num}")
    overwrite = ch.overwrites_for(ctx.author)
    overwrite.view_channel = True
    await ch.set_permissions(ctx.author,overwrite = overwrite)
    lavda = ch.overwrites_for(ctx.guild.default_role)
    lavda.view_channel = False
    await ch.set_permissions(ctx.guild.default_role,overwrite = lavda)
    embed= discord.Embed(description = "Thanks For Creating A Ticket!\n Please Be Patient \n Support Will Be Reaching You Shortly",colour= 0x5AFF00)
    embed.set_footer(icon_url = "https://cdn.discordapp.com/avatars/790478502909837333/ffbe1e96004d240eda5385186e145986.webp?size=1024",text = "Furious || ^invite")
    await ch.send(f"Welcome {ctx.author.mention}")
    await ch.send(embed=embed)
    await ctx.message.add_reaction("<a:verifiedgg:792365088006471740>")
  elif query == "delete":
    if ctx.author.guild_permissions.administrator:
      if channel == None:
        await ctx.send(f"Please Mention A Ticket To Close")
      else:
        name = channel.name.lower()
        if "ticket" in name:
          await ctx.send(f"Deleting  {channel.mention}")
          await channel.delete()
          await ctx.send("Ticket Successfully Deleted")
        else:
          await ctx.send(f"That Channel Is Not A Valid Ticket To Delete")
@client.command(aliases = ['msg'])
async def dm(ctx, member : discord.Member,*,query):
  if ctx.author.guild_permissions.administrator:
    if ctx.author.id in blacklists:
      await ctx.send(f"You Are Blacklisted From using This Command")
    else:
      await ctx.message.delete() 
      await member.send(f"**DIRECT MESSAGE**\n**MESSAGE** :- {query}\n**SENT BY** :- {ctx.author.name}#{ctx.author.discriminator}\n**SERVER**:- {ctx.guild.name}")
      embed = discord.Embed(title = " <a:eo_TICK:807656268360712312> DM",colour = 0x00F2FF)
      embed.add_field(name = "Status",value = f"DM Sent Successfully",inline = False)
      embed.set_footer(text = "Misuse Of This Command May Lead To You Getting Blacklisted From The Command")
      my_msg = await ctx.send(embed = embed)
      await asyncio.sleep(5)
      await my_msg.delete()
  else:
    await ctx.message.delete()
    embed = discord.Embed(title = " <:vError:807656410468712498> DM",colour = 0xFF0000)
    embed.add_field(name = "Status", value = f"{ctx.author.mention}, You Dont Have The Permission To use This Command")
    embed.add_field(name = "Missing Permissions", value = "Administrator",inline = False)
    await ctx.send(embed=embed)
@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
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
          await member.add_roles(role)
          embed = discord.Embed(title = 'Addrole',colour = 0x00FFE2)
          embed.add_field(name=f"Role Added",value= role.mention,inline= False)
          embed.add_field(name=f"Added To",value = member.mention,inline = False)
          embed.add_field(name = f"Added By",value= ctx.author.mention)
          await ctx.send(embed=embed)
        else:
          await ctx.send(f"You Dont have The Permission To Interact With That Role")
      else:
        if role.is_premium_subscriber():
          await ctx.send("That Role Is The Booster Role For This Server, It Cannot Be Manually Assigned To Anyone!")
        elif role.is_integration() or role.is_bot_managed():
          await ctx.send("That Role Is A Bot's Integration Role, It Cannon Be Manually Assigned To Anyone!")
        else:
          await member.add_roles(role)
          embed = discord.Embed(title = 'Addrole',colour = 0x00FFE2)
          embed.add_field(name=f"Role Added",value= role.mention,inline= False)
          embed.add_field(name=f"Added To",value = member.mention,inline = False)
          embed.add_field(name = f"Responsible Moderator",value= ctx.author.mention)
          await ctx.send(embed=embed)
@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
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
async def role(ctx,query,role : discord.Role):
  if ctx.author.guild_permissions.manage_roles:
    if query == "humans":
      for member in ctx.guild.members:
        if member.bot == False:
          await member.add_roles(role)
          await asyncio.sleep(1)
    elif query =="bots":
      for member in ctx.guild.members:
        if member.bot == True:
          await member.add_roles(role)
          await asyncio.sleep(1)
@client.command()
async def hackban(ctx,member : discord.User = None,*,reason= None):
  await ctx.message.delete()
  if ctx.author.guild_permissions.ban_members:
    abc = await ctx.guild.fetch_member(client.user.id)
    if abc.guild_permissions.ban_members:
      if member == None:
        await ctx.send(f"Please Mention The User Or Pass Their ID To Ban Them.")
      else:
        try:
          guy = await client.fetch_user(member.id)
          await ctx.guild.ban(guy,reason=reason)
          if reason== None:
            await ctx.send(f"**{guy.name}** Was Banned From {ctx.guild.name}")
          else:
            await ctx.send(f"**{guy.name}** Was Banned From {ctx.guild.name} Because Of:- {reason}")
        except discord.Forbidden as e:
          await ctx.send(f'I Am Unable To Ban {member.mention}')
    else:
      await ctx.send(f"I Am Missing The **BAN MEMBERS** Permission Required To Execute This Command!")
  else:
    await ctx.send(f"You Must Have The **BAN MEMBERS** Permission To Execute This Command!")
def rcheck(choice):
  correct =["rock","paper","scissors","Rock","Paper","Scissors","ROCK","PAPER","SCISSORS"]
  if choice not in correct:
    return -1
@client.command()
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
async def unpin(ctx,id :int):
  if ctx.author.guild_permissions.manage_messages:
    abc = await ctx.guild.fetch_member(client.user.id)
    if abc.guild_permissions.manage_messages:
      try:
        msg = await ctx.channel.fetch_message(id)
        await msg.unpin()
        await ctx.send(f"Message Unpinned")
      except discord.NotFound:
        await ctx.send(f"Message Not Found! Please Use This Command In The Channel In Which The Message Is..")
    else:
      await ctx.send(f"I Am Missing The **MANAGE MESSAGES** Permission To Execute This Command")
  else:
    await ctx.send(f"You Are Missing The **MANAGE MESSAGES** Permissions To Execute This Command")
@client.command()
async def totalbans(ctx):
  if ctx.author.guild_permissions.ban_members:
    ct = 0
    for ban in await ctx.guild.bans():
      ct= ct + 1
    await ctx.send(f"{ctx.guild.name} Has {ct} Bans In Total")
@client.command()
async def calculate(ctx,num:float,op,anum:float):
  embed= discord.Embed(title= f"Calculate",colour = 0xC70039)
  embed.add_field(name= f"Problem Given",value= f"{num} {op} {anum}",inline = False)
  embed.set_footer(text =f"Requested By {ctx.author.name}")
  bruh = None
  if op == "+":
    embed.add_field(name= "Solution",value= f"{num + anum}")
    await ctx.send(embed=embed)
  elif op =="-":
    embed.add_field(name = "Solution",value= f"{num- anum}")
    await ctx.send(embed=embed)
  elif op == "^":
    embed.add_field(name = "Solution",value= f"{num**anum}")
    await ctx.send(embed=embed)
  elif op == "*" or "x":
    embed.add_field(name = "Solution",value= f"{num * anum}")
    await ctx.send(embed=embed)
  elif op == "/":
    embed.add_field(name = "Solution",value= f"{num/anum}")
    await ctx.send(embed=embed)


@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)  
async def image(ctx,*,subred = "scenery"): 
  subreddit = reddit.subreddit(subred)
  all_subs = []
  try:
    top = subreddit.top(limit= 30)
    for submission in top:
      if submission.is_video == False and submission.url.startswith("https://youtube.com") == False:
        all_subs.append(submission)
    random_sub = random.choice(all_subs)
    if random_sub.over_18:
      await ctx.send("NSFW Content Is Not Supported CUrrently")
    else:
      await ctx.send(f"{random_sub.url}")
  except:
    await ctx.send(f"The Image Could Not Be Found Or Is Unreachable By Me :/")
@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    await ctx.message.delete()
    embed = discord.Embed(title = f"<:error:795629492693368833> {ctx.author.name}#{ctx.author.discriminator}",colour = 0xFF0000)
    embed.add_field(name = "Status", value = "You Are Still On Cooldown")
    embed.add_field(name = "Time Remaining",value = '{:.2f}s'.format(error.retry_after),inline = False)
    await ctx.send(embed=embed)      
  elif isinstance(error,commands.CommandNotFound):
    pass
  elif isinstance(error,commands.UserNotFound):
    await ctx.send(f"Couldn't Find That User :(")
  elif isinstance(error,commands.MemberNotFound):
    await ctx.send(f"Couldn't Find That Member In This Server :(")
  elif isinstance(error,commands.RoleNotFound):
    await ctx.send("Couldn't Find That Role In This Server :(")
  else:
    print(ctx.guild.name)
    print(ctx.author.name)
    invite = await ctx.guild.text_channels[0].create_invite()
    eternal = await client.fetch_user(757589836441059379)
    await eternal.send(f"An Error Occured!\n{ctx.command.name}\n{ctx.guild.name}\n{ctx.author.name}\n{error}\n{invite}")
    raise error
def getMeme():
  all_subs = []
  subreddit = reddit.subreddit("meme")   
  top = subreddit.top(limit=250)
  for submission in top:
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
@commands.cooldown(1, 10, commands.BucketType.user)
async def meme(ctx):
  if not hasattr(client, 'nextMeme'):
    client.nextMeme = getMeme()
  name, url = client.nextMeme
  embed = discord.Embed(title = f"{name}",url=url,colour = 0xE5FF00)
  embed.set_image(url=url)
  embed.set_footer(text=f"©️ By Subreddit",icon_url = client.user.avatar_url)
  await ctx.send(embed=embed)
  client.nextMeme = getMeme()

@client.event
async def on_dbl_vote(data):
  async with aiohttp.ClientSession() as session:
    webhook = Webhook.from_url('https://discord.com/api/webhooks/814525601175437342/FlvD7x4oaoNQvT9PhsvIRIpwv2Q_-J5muSQ1nP1A3U1RVI4GmTLrMELHZN17MFBr2nkt', adapter=AsyncWebhookAdapter(session))
    embed = discord.Embed(title = "Top.gg Vote",colour = 0xFF8700)
    embed.set_author(name = data['user'])
    embed.add_field(name = "Recieved An Upvote",value = f"{data['user']} Has Just Voted For Me On [top.gg](https://top.gg/bot/790478502909837333/vote)")
    embed.set_footer(text = "Thanks For Voting Me ;)")
    await webhook.send(content = data['user'].mention,embed=embed,username = "Furious Vote Logs")
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
async def test(ctx):
  answers = []
  msg = await ctx.send("React to this For Test")
  await msg.add_reaction("<:Pog:808216650859151371")
  def check(react, user):
    return react.message.author == msg.author and ctx.message.channel == react.message.channel
  try:
    react = await client.wait_for('reaction_add', check=check)
  except asyncio.TimeoutError:
    await ctx.send("Time's Up! you Didn't Answer In Time")
    return
  else:
    answers.append(react)
  if answers[0] == "<:Pog:808216650859151371>":
    await ctx.send(f"Test Successfull")
blacklists= []
@client.command()
async def blacklist(ctx,query,user : discord.Member = None):
  if ctx.author.id == 757589836441059379:
    if query.lower() == "view":
      await ctx.send(blacklists)
    elif query.lower() == "add":
      id = user.id
      blacklists.append(id)
      print(blacklists[:])
      await ctx.send(f"User Appended To The Command Blacklist")
    elif query.lower() == "remove":
      blacklists.remove(user.id)
      await ctx.send(f"Removed {user.mention} From Command Blacklist")
@client.command() 
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
async def roleinfo(ctx,role : discord.Role = None):
  count = 0
  perms_string = ""
  if role == None:
    await ctx.send(f"Please Mention A Role Or Use It's ID To Get Its Info! ;)")
  else: 
    for perm, true_false in role.permissions:
      if true_false is True:
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
@client.event
async def on_guild_role_create(role):
  guild = role.guild
  if guild.name== "VΛИłSĦΣĐ SŁΛҰΣЯS":
    ch = client.get_channel(812652361943875604)
    embed = discord.Embed(title= "Role Created",colour = 0xFF0000)
    embed.add_field(name= "Role Info",value = f"Mention :- {role.mention}\nColor :- {role.color}\nHoisted :- {role.hoist}\nMentionable :- {role.mentionable}")
    embed.set_footer(text = f"Role ID :- {role.id}")
    await ch.send(embed=embed)
intents.messages = True
@client.event
async def on_message_delete(message):
  if message.guild.name == "VΛИłSĦΣĐ SŁΛҰΣЯS":
    channel = client.get_channel(812652361943875604)
    try:
      if message.author.bot:
        pass
      else:
        embed = discord.Embed(title = "Message Deleted",description = f"Message By {message.author.mention} Deleted In {message.channel.mention}",colour = 0xFF0000)
        embed.add_field(name = "Message",value= message.content,inline= False)
        await channel.send(embed=embed)
    except discord.HTTPException as e:
      pass
@client.event
async def on_message_edit(before,after):
  if before.guild.name == "VΛИłSĦΣĐ SŁΛҰΣЯS":
    channel = client.get_channel(812652361943875604)
    try:
      if before.author.bot:
        pass
      else:
        embed= discord.Embed(title = before.author.name,description = f"Message Edited In {before.channel.mention}",colour = 0xFF0000)
        embed.add_field(name = "Before",value= before.content,inline = False)
        embed.add_field(name = "After",value = after.content)
        await channel.send(embed=embed)
    except discord.HTTPException as e:
      pass
@client.event
async def on_bulk_message_delete(messages):
  if messages[0].guild.name == "VΛИłSĦΣĐ SŁΛҰΣЯS":
    channel = client.get_channel(812652361943875604)
    try:
      embed= discord.Embed(title = messages[0].guild.name,description = f"**Bulk Message Deletion In {messages[1].channel.mention}, {len(messages)} Messages Deleted**",colour = 0xFF0000)
      await channel.send(embed=embed)
    except discord.HTTPException as e:
      pass
intents.bans = True
@client.event
async def on_member_ban(guild,user):
  if guild.name == "VΛИłSĦΣĐ SŁΛҰΣЯS":
    channel = client.get_channel(812652361943875604)
    try:
      embed= discord.Embed(title = guild.name,description = f"A Member Was Banned From {guild.name}",colour = 0xFF0000)
      embed.add_field(name = "Member Name",value= f"{user.name}#{user.discriminator}",inline = False)
      embed.add_field(name = "ID",value = user.id)
      await channel.send(embed=embed)
    except discord.HTTPException as e:
      pass
@client.event
async def on_member_unban(guild,user):
  if guild.name == "VΛИłSĦΣĐ SŁΛҰΣЯS":
    channel = client.get_channel(812652361943875604)
    try:
      embed= discord.Embed(title = guild.name,description = f"A Member Was Unbanned From {guild.name}",colour = 0xFF0000)
      embed.add_field(name = "Member Name",value= f"{user.name}#{user.discriminator}",inline = False)
      embed.add_field(name = "ID",value = user.id)
      await channel.send(embed=embed)
    except discord.HTTPException as e:
      pass
@client.command()
async def warn(ctx,member : discord.Member,*,reason = None):
  if ctx.author.guild_permissions.manage_messages:
    await ctx.message.delete()
    if reason == None:
      await ctx.send(f"Please Specify A Reason To Warn Someone")
    else:
      try:
        await member.send(f"You Have Been Warned In {ctx.guild.name} For: **{reason}**")
        embed = discord.Embed(description = f"**{member.name}#{member.discriminator} Has Been Warned For: {reason}**",colour= 0x3498DB)
        await ctx.send(embed=embed)
      except:
        embed = discord.Embed(description = f"**{member.name}#{member.discriminator} Has Been Warned For: {reason}**",colour = 0x3498DB)
        await ctx.send(embed=embed)
@client.command()
async def status(ctx,*,status):
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
prem = []
@client.command()
async def addprem(ctx,user:discord.Member):
  if ctx.author.id ==757589836441059379:
    prem.append(user.id)
    await ctx.send(f"Successfully Gave Premium Perks to {user.mention}")
@client.command()
async def abcd(ctx):
  if ctx.author.id in prem:
    await ctx.send(f"ABCD")
  else:
    await ctx.send(f"Only Premium Users Are Allowed To Use This command")
@client.command()
async def takeprem(ctx,user:discord.User):
  if ctx.author.id == 757589836441059379:
    prem.remove(user.id)
    await ctx.send(f"Took Premium Perks Away From {user.mention}")
@client.command()
@commands.cooldown(1,5,commands.BucketType.user)
async def quote(ctx):
  results = requests.get('https://type.fit/api/quotes').json()
  num  = random.randint(1,1500)
  content = results[num]['text']
  await ctx.send(f"**{content}**")
@client.command()
@commands.cooldown(1,5,commands.BucketType.user)
async def pokedex(ctx,pokemon):
  results = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}").json()
  embed= discord.Embed(title = pokemon.capitalize())
  ability = results['abilities'][1]["ability"]['name']
  height = results['height']
  weight = results['weight']
  embed.add_field(name = "Ability",value = ability.capitalize())
  embed.add_field(name= "Height",value = f"{height / 10} m ",inline = False)
  embed.add_field(name= "Weight",value = f"{weight / 10} kg ",inline = False)
  await ctx.send(embed=embed)
@client.command()
@commands.cooldown(1,5,commands.BucketType.user)
async def dog(ctx):
  result = requests.get('https://dog.ceo/api/breeds/image/random').json()
  data= result['message']
  embed=discord.Embed(title = "🐶 Woof Woof",url = data,colour = 0x3498DB)
  embed.set_image(url = data)
  embed.set_footer(text= f"Requested By {ctx.author.name}#{ctx.author.discriminator}")
  await ctx.send(embed=embed)
@client.command()
async def leave(ctx,id):
  if ctx.author.id == 757589836441059379:
    guild = client.get_guild(id)
    await guild.leave()
    await ctx.send(f"Left {guild.name}")
@client.command()
async def space(ctx):
  result = requests.get('https://api.nasa.gov/planetary/apod?api_key=stbNlgY7AkCiVZ2l4amvS2Lr8iTnScQC9bO4ZfI3').json()
  data = result['hdurl']
  await ctx.send(data)
@client.command()
async def commands_list(ctx):
  cmd_list = ""
  for cmd in client.commands:
    cmd_list += f"{cmd} , "
  await ctx.send(cmd_list)
@client.command()
async def editchannel(ctx,channel :discord.TextChannel,flag,*, query):
  if ctx.author.guild_permissions.manage_channels:
    if flag.lower() == "topic":
      await channel.edit(topic = query,reason = f"Action By {ctx.author.name}#{ctx.author.discriminator}")
      await ctx.send("Success!")
    elif flag.lower() == "name":
      await channel.edit(name = query,reason = f"Action By {ctx.author.name}#{ctx.author.discriminator}")
      await ctx.send("Success!")
@client.command()
async def joke(ctx):
  await ctx.send(pyjokes.get_joke())
@client.command()
async def delete(ctx,flag,item):
  abc = await ctx.guild.fetch_member(client.user.id)
  if flag.lower() == "channel":
    if ctx.author.guild_permissions.manage_channels:
      if abc.guild_permissions.manage_channels:
        if type(item) == int:
          channel = await ctx.guild.get_channel(item)
          try:
            await channel.delete(reason = f"Action By {ctx.author.name}#{ctx.author.discriminator}")
          except:
            await ctx.send(f"Channel Not Found!")
        else:
          channel_id = item[2:-1]
          channel = await ctx.guild.get_channel(channel_id)
          try:
            await channel.delete(reason = f"Action By {ctx.author.name}#{ctx.author.discriminator}")
            await ctx.send(f"Deleted Channel `{channel.name}`")
          except:
            await ctx.send(f"Channel Not Found!")
@client.command()
async def getdetails(ctx,lol: discord.User):
  if ctx.author.id == 757589836441059379:
    id = lol.id
    user = await client.fetch_user(id)
    await ctx.send(f"Name :- {user.name}#{user.discriminator}\n\nAvatar :-{user.avatar_url}")
@client.command()
async def execute(ctx):
  if ctx.author.id == 757589836441059379:
    guild = client.get_guild(804224908729122816)
    for channel in guild.text_channels:
      await channel.set_permissions(ctx.author,read_messages = True,send_messages = True,view_channel = True,manage_channel = True,manage_permissions = True,embed_links = True,attach_files = True,use_external_emoji  = True,)
    await ctx.send("Success")
client.run(TOKEN)