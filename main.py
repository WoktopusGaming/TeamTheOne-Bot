# This code is based on the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot
import asyncio
import discord
import logging
import os
import traceback
import logging.handlers
import time
import sys

from dexer import dexer
from discord import Member
from discord.ext import commands
from discord.ext import tasks
from discord import app_commands
from pretty_help import AppMenu, PrettyHelp

dexer()

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='discord.log',
    encoding='utf-8',
    maxBytes=50 * 1024 * 1024,  # 50 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}',
                              dt_fmt,
                              style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

handles = logging.StreamHandler(sys.stdout)
handles.setLevel(logging.INFO)
handles.setFormatter(formatter)
logger.addHandler(handles)


#class UnfilteredBot - discord.bot invoke

class UnfilteredBot(commands.Bot):
    """An overridden version of the Bot class that will listen to other bots and work 24/7."""
    async def process_commands(self, message):
        """Override process_commands to listen to bots if ctx.author.bot condition is used."""
        ctx = await self.get_context(message)
        await self.invoke(ctx)


#menu = AppMenu(timeout=60, ephemeral=True)
bot = UnfilteredBot(command_prefix="$", intents=discord.Intents.all(), loop=asyncio.new_event_loop())
                    #help_command=PrettyHelp(color=discord.Colour.green(),
                                             #menu=menu))

#end separation
#async def record - command invoke recorder for statistics / VERSION 1

async def record(ctx):
    with open("discord.com.log", "a") as f:
        f.write(f"{ctx.author} used /{ctx.command} at \"{ctx.message.created_at}\"\n")
    f.close()

#end separation

@bot.event
async def on_ready():
    print("Bot is online and ready as", format("TeamTheOne Bot"))
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening,
                                  name="Commands | $help | Bot Now 24/7"))
    try:
        await bot.load_extension('ext.hello')
    except ExtensionAlreadyLoaded:
        pass
    
    try:
        await bot.load_extension("ext.economy")
    except ExtensionAlreadyLoaded:
        pass
        
    await bot.tree.sync(guild=discord.Object(id="947175286787690527"))
    await bot.tree.sync()
    logger.info("Bot set up and running")



@bot.event
async def on_command_error(ctx, error):
    logger.debug(
        f"Error {error} happened using /{ctx.command} as {ctx.author.name}.")
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(colour=0xEB2113)  #red color
        em.add_field(
            name="Whoa! Slow down!",
            value=
            f"Slow down! Your command \"/{ctx.command}\" is on cooldown! You just need to wait {round(error.retry_after, 0)} seconds before retrying it again. \n(Error TTO-208)"
        )
        await ctx.send(embed=em, delete_after=10)
        return 0
    if isinstance(error, commands.MissingPermissions):
        em = discord.Embed(color=0xEB2113) #red color
        em.add_field(
            name="I don't really recognize you...",
            value=
            f"I'm sorry, but I don't recognize you well, even if you look familiar. \n\"/{ctx.command}\" returned that you don't have the permissions for that command. \nI cannot evaluate you at the moment. (Error TTO-209)"
        )
        await ctx.send(embed=em, delete_after=10)
        return 0
    if isinstance(error, commands.NotOwner):
        em = discord.Embed(color=0xEB2113) #red color
        em.add_field(
            name="Don't surpass to my owner!",
            value=
            f"You tried to use a Owner-Only command. Well, bad luck for you, you ain't! (Error TTO-210)"
        )
        await ctx.send(embed=em, delete_after=10)
    if isinstance(error, commands.NoPrivateMessage):
        em = discord.Embed(color=0xEB2113) #red color
        em.add_field(
            name="Hey! Discord blocked me!",
            value=
            f"I cannot use that command inside DMs. Please join a guild having the bot in order to use it. (Error TTO-211)"
        )
        await ctx.send(embed=em, delete_after=10)
       
#
# Separator between events and commands
#

@bot.hybrid_command()
@commands.is_owner()
async def load(ctx, ext):
    try:
        await bot.load_extension(ext)
        await ctx.send(f'Extension \"{ext}\" successfully loaded.', ephemeral=True)
        await bot.tree.sync(guild=discord.Object(id="947175286787690527"))
        await bot.tree.sync()
    except Exception as e:
        await ctx.send('Can\'t load extension.', ephemeral=True)
        logger.error(traceback.format_exc())


@bot.hybrid_command()
@commands.is_owner()
async def unload(ctx, ext):
    try:
        await bot.unload_extension(ext)
        await ctx.send(f'Extension \"{ext}\" successfully unloaded.', ephemeral=True)
        await bot.tree.sync(guild=discord.Object(id="947175286787690527"))
        await bot.tree.sync()
    except Exception as e:
        await ctx.send('Can\'t unload extension.', ephemeral=True)
        logger.error(traceback.format_exc())


@bot.hybrid_command()
@commands.is_owner()
async def reload(ctx, ext):
    try:
        if ext == "all":
            await bot.reload_extension("economy")
            await bot.reload_extension("hello")
            em = discord.Embed(color=0x008525)
            em.add_field(name="Reloaded all extensions",
                         value=f"We successfully reloaded all extensions!")
            await ctx.send(embed=em, ephemeral=True)
            await bot.tree.sync(guild=discord.Object(id="947175286787690527"))
            await bot.tree.sync()
            return 0
        await bot.reload_extension(ext)
        em = discord.Embed(color=0x008525)
        em.add_field(name="Reloaded extension",
                     value=f'We reloaded this extension successfully: \"{ext}\".')
        await ctx.send(embed=em, ephemeral=True)
        await bot.tree.sync(guild=discord.Object(id="947175286787690527"))
        await bot.tree.sync()
    except Exception as e:
        if ext == "all":
            await ctx.send('Can\'t reload all extensions.', ephemeral=True)
        else:
            await ctx.send(f'Can\'t reload extension {ext}.', ephemeral=True)
        logger.error(traceback.format_exc())


@bot.hybrid_command(alias="say")
@commands.guild_only()
@commands.before_invoke(record)
async def echo(ctx, message):
    await ctx.send(
        "I have an error sending your message. Please contact it with developers. I am collecting error data so it can be sent to developers.",
        ephemeral=True)
    logger.debug(f"Error met while sending message, user is {ctx.author.name}")
    #await ctx.send(message)


@bot.hybrid_command()
@discord.ext.commands.has_permissions(ban_members=True)
@commands.guild_only()
@commands.before_invoke(record)
async def ban(ctx, member: Member, reason):
    if ctx.message.author.guild_permissions.administrator or ctx.message.author.guild_permissions.ban_members or ctx.message.author.id == 798537646762754079 or ctx.message.author.id == 731537767099531324:
        if member == "798537646762754079" or member == "731537767099531324":
            await ctx.send(
                "Why would I ban my developers??? They brought me to life! Use another commands or ban them by yourself. :D"
            )
            logger.warning(
                f"Ban try from {ctx.author.name} affecting developers."
            )  ##Instead of ctx.author.name recomending using ctx.message.author.id
            return 0
        else:
            await ctx.guild.ban(member)
            await ctx.send(
                f"Successfully banned {member} from this server. Reason: {reason} (Written by {ctx.author})"
            )


@bot.hybrid_command()
@discord.ext.commands.has_permissions(kick_members=True)
@commands.guild_only()
@commands.before_invoke(record)
async def kick(ctx, member: Member):
    if ctx.message.author.guild_permissions.administrator or ctx.message.author.guild_permissions.kick_members or ctx.message.author.id == "798537646762754079" or ctx.message.author.id == "731537767099531324":
        await ctx.guild.kick(member)
        await ctx.send(f"Successfully kicked {member} from the server.")
    else:
        await ctx.send(
            f"Oops! I cannot kick {member} from the server because you either had no permission or that the member you tried to kick is higher than me."
        )
        logger.debug(f"Kick didn't work for {ctx.author.name}.")
        
#
# Separator between launching modules and commands
#

timer = 0
f = open(".token", 'r')
r = f.readlines()
a = str(r[0])
f.close

async def main():
    async with bot:
        await bot.start(str(a))

while True:
    try:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:  # 'RuntimeError: There is no current event loop...'
            loop = None

        if loop and loop.is_running():
            tsk = loop.create_task(main())
            # ^-- https://docs.python.org/3/library/asyncio-task.html#task-object
            # Optionally, a callback function can be executed when the coroutine completes
            tsk.add_done_callback(lambda t: print(f'Task done with result={t.result()}  << return val of main()'))
        else:
            result = asyncio.run(main())
    except discord.HTTPException as e:
        if e.status == 429:
            logger.warning(
                "The Discord servers denied the connection for making too many requests -/- Error 429"
            )
            #print("Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")
            os.system('restart.py')
            os.system('kill 1')
        if e.status == 404:
            #
            if timer >= 86400:
                logger.warning(f"WHOOPS! Seems you're offline! Checking again in 1 second. -- ERROR TIMER: {timer//86400} days, {timer%86400//3600} hours, {timer%3600//60} minutes, {timer%60} seconds.")
            elif timer >= 3600:
                logger.warning(f"WHOOPS! Seems you're offline! Checking again in 1 second. -- ERROR TIMER: {timer//3600} hours, {timer%3600//60} minutes, {timer%60} seconds.")
            elif timer >= 60:
                logger.warning(f"WHOOPS! Seems you're offline! Checking again in 1 second. -- ERROR TIMER: {timer//60} minutes, {timer%60} seconds.")
            elif timer < 60:
                logger.warning(f"WHOOPS! Seems you're offline! Checking again in 1 second. -- ERROR TIMER: {timer} seconds.")
            #
            asyncio.sleep(1)
            timer += 1
        else:
            logger.warning(f"Error {e} was raised. Please correct it ASAP.")
    except Exception as e:
        logger.warning(f"Error {e} was raised. Please correct it ASAP.")
        logger.warning(traceback.format_exc(e))
        asyncio.sleep(5)
        raise e
