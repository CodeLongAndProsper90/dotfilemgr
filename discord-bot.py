import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from operations import *


load_dotenv()
token = os.environ['TOKEN']

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print(f"{bot.user} has logged into Discord")

@bot.command(name='add')
async def adddotfile(ctx, name, filename, *args):
    add_config(name, filename, ' '.join(args))

@bot.command(name='remove')
async def removedotfile(ctx, name):
    pass

@bot.command(name='update')
async def dotfileupdate(ctx, name, *args):
    pass

@bot.command(name='view')
async def view(ctx, name):
    pass

bot.run(token)
