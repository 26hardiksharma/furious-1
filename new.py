import discord
from discord.ext import commands
client = commands.Bot(command_prefix =["^","furious ","<@!790478502909837333> "],help_command=None,case_insensitive = True)
@client.command()
async def hello(ctx):
    await ctx.channel.send("Hello")