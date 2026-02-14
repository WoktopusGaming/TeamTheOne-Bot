# notes to self
# Item reminder:
# - Type 1 = Unconsumable
# - Type 2 = Consumable
# - Type 3 = Usable Uncomsumable (special items)

# Rarity reminder:
# - Rarity 0 = Discontinued / Deprecated
# - Rarity 1 = Very Common
# - Rarity 2 = Common
# - Rarity 3 = Uncommon
# - Rarity 4 = Rare
# - Rarity 5 = Very Rare
# - Rarity 6 = Epic
# - Rarity 7 = Legendary
# - Rarity 8 = Mythical
# - Rarity 9 = Celestial
# - Rarity 10 = Exclusive
# - Rarity 11 = Server Exclusive

# Market reminder:
# Price is equal to the price of the sell
# - Pricetype 1 = Set price for all items
# - Pricetype 2 = Set price for one item
# Items is equal to the amount of items sold
# MarketID is equal to the market ID
# Selltime is equal to the timestamp the item was put into the market (in seconds)
# All of the market is separated into item ID

# Average price is stored inside the item registry (avgp)
# A list exist for the last ten unitary prices sells (avgpl)

# Wheel reminder:
# Currency is equal to the wheel fee. Null = free. Number = currency number.
# Fee is equal to the amount of currency per wheel roll (if currency != null)
# Items are the items and chances of being rolled on. Total must be 100. Include only items in wheel.

# Statuses reminder:
# Sorted by status name
# Cancellable is equal to a switch (true/false) that indicates if it can be cancelled or not.
# Type is the buff it gives - all implemented in code.
# Multiplier is the multiplier of the bufftype.

# Crafting reminder:
# Sorted by crafting ID.
# Defaultunlocked is equal to the unlock requirement.
# - If true, levelunlock is equal to the level it unlocks the recipe.
# - If false, the recipe is by default unlocked.
# Itemreq is equal to all items required. Wallet and currencies can be demanded.
# IDresult is equal to the item ID of the result. Crafting this recipe gives this item.
# Difficulty is equal to the required amount of progress (similar to FF14)
# HQ is if high quality is possible or not. (Currently, all are set to false)

# https://discord.com/developers/applications/1170856100078309418/emojis
# for all emojis used in the shop and all systems

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