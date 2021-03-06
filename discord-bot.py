import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from operations import *
import operations


load_dotenv()
token = os.environ['TOKEN']

bot = commands.Bot(command_prefix='.')

dfmgr = Dotfiles()
dfmgr.create_database()

@bot.event
async def on_ready():
    print(f"{bot.user} has logged into Discord")


@bot.command(name='add')
async def adddotfile(ctx, name, filename, *args):
    dfmgr.add_config(name, filename, ' '.join(args))
    await ctx.send("added config")

@bot.command(name='remove')
async def removedotfile(ctx, name):
    delete_file(name)
    await ctx.send(f"Deleted the file {name}")

@bot.command(name='update')
async def dotfileupdate(ctx, name, *args):
    update_file(name, ' '.join(args))
    await ctx.send("file updated")

@bot.command(name='view')
async def view(ctx, name):
    await ctx.send(get_file(name))

bot.run(token)
