# This code is based on the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot
import asyncio # imports the asynchronized module
import urllib.request # imports the URL request from the URL library
import discord # imports the discord library
import logging # imports the logging module
import os # imports the operating system module
import traceback # imports the traceback module
import logging.handlers # imports the logging handlers
import time # imports the time library
import sys # imports the system library
import json # imports the json library
import filecmp # imports the file comparison library

import socket # imports the socket library
import aiohttp # imports the aiohttp library

from dexer import dexer # imports the dexer function from dexer.py (dashboard module)
import update # imports the whole update.py file (update and checking module)

from discord import Member # imports the Member class from discord library (used as a shortcut in code)
from discord.ext import commands # imports the commands module from discord's extended library
from discord.ext import tasks # imports the tasks module from discord's extended library
from discord import app_commands # imports the app_commands library from discord library
#"from pretty_help import AppMenu, PrettyHelp" # ignore

dexer() # runs the dexer function (runs the dashboard)

logger = logging.getLogger('discord') # gets logger "discord" (basic logger from discord library)
logger.setLevel(logging.INFO) # sets console information level to "info"
logging.getLogger('discord.http').setLevel(logging.INFO) # gets the HTTP logger from discord library with level "info"

handler = logging.handlers.RotatingFileHandler(
    filename='discord.log',
    encoding='utf-8',
    maxBytes=50 * 1024 * 1024,  # 50 MiB
    backupCount=5,  # Rotate through 5 files before stopping
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

#update.check_for_updates()

logger.info("Checking for bot and updater updates...")
upd = update.check_for_updates()

target_url = "https://raw.githubusercontent.com/WoktopusGaming/TeamTheOne-Bot/master/update.py"
data = urllib.request.urlopen(target_url)
with open("temp.update.py", "w") as f:
    for line in data:
        f.write(line.decode("utf-8"))
        
    comp = filecmp.cmp("update.py", "temp.update.py", shallow=False)
    if comp:
        os.remove("temp.update.py")
    else:
        logger.info("Update for updater was found. Installing...")
        os.remove("update.py")
        os.rename("temp.update.py", "update.py")
        logger.info("Update for updater was installed. Restarting main app...")
        os.system("main.py")
            
if upd == False:
    pass
elif upd == True:
    logger.info("A bot update was found. Installing update...")
    update.get_updates()
        

    

#end separation
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
#delete startup.py if setup configured

#target_url = "https://raw.githubusercontent.com/WoktopusGaming/TeamTheOne-Bot/master/startup.py"
#data = urllib.request.urlopen(target_url)

try:
    with open("db/users.json") as f:
        users = json.load(f)
except FileNotFoundError:
    try:
        os.system('startup.py')
    except FileNotFoundError:
        with open("startup.py", "w") as d:
            for line in data:
                d.write(line.decode("utf-8"))
            d.close()
        os.system('startup.py')
    quit(code=sys._ExitCode)
except Exception as e:    
    logger.error(traceback.format_exc(e))
    quit(code=sys._ExitCode)

try:
    f = open('.token')
except FileNotFoundError:
    try:
        os.system('startup.py')
    except FileNotFoundError:
        with open("startup.py", "w") as d:
            for line in data:
                d.write(line.decode("utf-8"))
            d.close()
        os.system('startup.py')
    quit(code=sys._ExitCode)
except Exception as e:
    logger.error(traceback.format_exc(e))
    quit(code=sys._ExitCode)

try:
    if users['bot-configured'] == True and users['bot-startup'] == True:
        os.remove('startup.py')
except FileNotFoundError:
    pass
except Exception as e:
    logger.error(traceback.format_exc(e))
    quit(code=sys._ExitCode)
else:
    pass


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
                                  name="TeamTheOne Bot | owned by WoktopusGaming | BETA v2.2.0"))

    try:
        await bot.load_extension("ext.economy")
    except discord.ExtensionAlreadyLoaded:
        pass
        
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
            f"Slow down! Your command \"/{ctx.command}\" is on cooldown! You just need to wait {round(error.retry_after, 0)} seconds before retrying it again. \n(Error TTO-100)"
        )
        await ctx.send(embed=em, delete_after=10)
        return 0
    if isinstance(error, commands.MissingPermissions):
        em = discord.Embed(color=0xEB2113) #red color
        em.add_field(
            name="I don't really recognize you...",
            value=
            f"I'm sorry, but I don't recognize you well, even if you look familiar. \n\"/{ctx.command}\" returned that you don't have the permissions for that command. \nI cannot evaluate you at the moment. (Error TTO-101)"
        )
        await ctx.send(embed=em, delete_after=10)
        return 0
    if isinstance(error, commands.NotOwner):
        em = discord.Embed(color=0xEB2113) #red color
        em.add_field(
            name="Don't surpass to my owner!",
            value=
            f"You tried to use a Owner-Only command. Well, bad luck for you, you ain't! (Error TTO-102)"
        )
        await ctx.send(embed=em, delete_after=10)
    if isinstance(error, commands.NoPrivateMessage):
        em = discord.Embed(color=0xEB2113) #red color
        em.add_field(
            name="Hey! Discord blocked me!",
            value=
            f"I cannot use that command inside DMs. Please join a guild having the bot in order to use it. (Error TTO-103)"
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
        await bot.tree.sync()
    except Exception as e:
        await ctx.send('Can\'t load extension. (Error TTO-107)', ephemeral=True)
        logger.error(traceback.format_exc())


@bot.hybrid_command()
@commands.is_owner()
async def unload(ctx, ext):
    try:
        await bot.unload_extension(ext)
        await ctx.send(f'Extension \"{ext}\" successfully unloaded.', ephemeral=True)
        await bot.tree.sync()
    except Exception as e:
        await ctx.send('Can\'t unload extension. (Error TTO-108)', ephemeral=True)
        logger.error(traceback.format_exc())


@bot.hybrid_command()
@commands.is_owner()
async def reload(ctx, ext):
    try:
        if ext == "all":
            await bot.reload_extension("ext.economy")
            em = discord.Embed(color=0x008525)
            em.add_field(name="Reloaded all extensions",
                         value=f"We successfully reloaded all extensions!")
            await ctx.send(embed=em, ephemeral=True)
            await bot.tree.sync()
            return 0
        await bot.reload_extension(ext)
        em = discord.Embed(color=0x008525)
        em.add_field(name="Reloaded extension",
                     value=f'We reloaded this extension successfully: \"{ext}\".')
        await ctx.send(embed=em, ephemeral=True)
        await bot.tree.sync()
    except Exception as e:
        if ext == "all":
            await ctx.send('Can\'t reload all extensions. (Error TTO-109)', ephemeral=True)
        else:
            await ctx.send(f'Can\'t reload extension {ext}. (Error TTO-109)', ephemeral=True)
        logger.error(traceback.format_exc())


@bot.hybrid_command(alias="say")
@commands.guild_only()
@commands.before_invoke(record)
async def echo(ctx, message):
    await ctx.send(
        "I have an error sending your message. Please contact it with developers. I am collecting error data so it can be sent to developers. (Error TTO-104)",
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
                "Why would I ban my developers??? They brought me to life! Use another commands or ban them by yourself. :D (Error TTO-105)"
            )
            logger.warning(
                f"Ban try from {ctx.author.name} affecting developers."
            )
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
            f"Oops! I cannot kick {member} from the server because you either had no permission or that the member you tried to kick is higher than me. (Error TTO-106)"
        )
        logger.debug(f"Kick didn't work for {ctx.author.name}.")
        
#
# Separator between launching modules and commands
#

f = open(".token", 'r') # opens a file named ".token" (used for token)
r = f.readlines() # makes a variable which contains the file's lines
a = str(r[0]) # gets the first line of the registered lines
f.close # closes the file

async def main(): # defines an asynchronized function named main()
    async with bot: # adds the variable/function "bot" to main()
        await bot.start(a) # waits for the variable/function "bot" to start with the token from the variable "a"

while True: # starts an infinite loop
    try: # tries the code registered under
        try: 
            loop = asyncio.get_running_loop() # makes a variable called loop which gets the current asynchronized running loop
        except RuntimeError:  # if the tried code failed - In case of a 'RuntimeError: There is no current event loop...'
            loop = None # makes a variable called loop which contains None (nothing)

        if loop and loop.is_running(): # if an asynchronized loop exists and runs at the same time
            tsk = loop.create_task(main()) # makes a task on the current loop which adds the main function to it
            tsk.add_done_callback(lambda t: print(f'Task done with result={t.result()}  << return val of main()')) # ignore this
        else:
            result = asyncio.run(main()) # if no current loop is running, it will run the main function independently
    except discord.HTTPException as e: # if discord returns an HTTP error
        if e.status == 429: # if discord returned a ratelimited status (429)
            logger.warning( # logs a warning on the console side
                "The Discord servers denied the connection for making too many requests -/- Error 429 (Error TTO-004)" # ratelimit message
            ) 
            os.system('restart.py') # uses a independant restarter, the console runs that file as its main (replit/server-hosted, deprecated)
            os.system('kill 1') # kills the current process of this current file, closing it / restarting everything (replit/server-hosted)
        else:
            logger.warning(f"HTTP error {e} was raised. Please correct it ASAP.") # if another HTTP error was raised, warns on console side and retries again
    except Exception as e: # if anything else was raised during the infinite loop (code error, for example)
        if type(e) == aiohttp.client_exceptions.ClientConnectorError: # if no Internet connection (deprecated?)
            #
            logger.warning(f"WHOOPS! Seems you're offline! Checking again in 5 seconds. (Error TTO-005)")
            #
            time.sleep(5) # sleeps the loop for one second
            logger.info(f"Restarting main process...")
            os.system('main.py')
        else:
            logger.warning(f"Error \"{e}\" (\"{type(e)}\") was raised. Please correct it ASAP. (Error TTO-000)") # raises a warning
            logger.warning(traceback.format_exc(e)) # reports the whole traceback (necessary as it doesn't do automatically)
            time.sleep(5) # sleeps the loop for five seconds
            raise e # raises the error
            quit(code=sys._ExitCode)
