# notes to self
# Duration (seconds): 60 = 1 min; 3600 = 1h; 86400 = 1d; etc.

from discord.ext import commands
from discord import app_commands
from discord import Member
from discord import utils

import json
import os
import discord
import random
import traceback
import logging
import datetime
import time

logger = logging.getLogger('discord')

#async def record - command invoke recorder for statistics / VERSION 1

async def record(ctx):
    with open("discord.com.log", "a") as f:
        f.write(f"{ctx.author} used /{ctx.command} at \"{ctx.message.created_at}\"\n")
    f.close()

#end separation

@commands.hybrid_group(name="shop", fallback="view", brief="View the current shop!")
@discord.app_commands.describe(eph = "Checks if you want it ephemeral or not. True by default.")
@commands.before_invoke(record)
async def shop_view(ctx, eph = True):
    try:
        em = discord.Embed(color=0x66CAFE)
        em.add_field(
            name="Shop",
            value="We, as in our group coding this project, are sorry to announce the shop still unopened and in works. Would be a pleasure if you could come back later... We are sorry."
        )
        await ctx.send(embed=em, ephemeral=eph)
    except Exception as e:
        await ctx.send(f"We are sorry {ctx.author.mention}, but an error occured. I've let the host know this. (Error TTO-123)", ephemeral=eph)
        logger.error(traceback.format_exc())

@shop_view.command(name="add", brief="Add an item to the shop.")
@discord.app_commands.describe(eph = "Checks if you want it ephemeral or not. True by default.")
@commands.before_invoke(record)
async def shop_add(ctx, eph = True):
    try:
        em = discord.Embed(color=0x66CAFE)
        em.add_field(
            name="Shop",
            value="We, as in our group coding this project, are sorry to announce the shop still unopened and in works. Would be a pleasure if you could come back later... We are sorry."
        )
        await ctx.send(embed=em, ephemeral=eph)
    except Exception as e:
        await ctx.send(f"We are sorry {ctx.author.mention}, but an error occured. I've let the host know this. (Error TTO-123)", ephemeral=eph)
        logger.error(traceback.format_exc())


async def setup(bot):
    bot.add_command(shop_view)
    logger.info("Loaded extension ext.shop")

async def teardown(bot):
    logger.info("Unloaded extension ext.shop")

if __name__ == "__main__":
    print("Please, do not start an extension as the starting file, they will always be loaded in the bot.\n-Start main.py instead. We will do it for you.\n-Starting main.py from project directory...\n- (This will only work if you enabled indexing in global settings, case of Visual Basic Studio, or if you use a host provider, e.g. Replit.)")
    os.system(f"main.py")
    print("Starting main.py from command line directory...")
    os.chdir("..")
    os.system(f"main.py")