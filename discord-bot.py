import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print("Bot is ready!")

@bot.command(name='add')
async def adddotfile(ctx, name, *args):
    pass

@bot.command(name='remove')
async def removedotfile(ctx, name):
    pass

@bot.command(name='update')
async def dotfileupdate(ctx, name, *args):
    pass

@bot.command(name='view')
async def view(ctx, name):
    pass

bot.run("NzU2OTcyMjk1NDgxODUyMDI3.X2ZnYw.eJoH3mOqSuHK3jNdlqmkiYxrM9M")
