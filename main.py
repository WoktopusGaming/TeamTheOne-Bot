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

try:
    from dexer import dexer # imports the dexer function from dexer.py (dashboard module)
except ModuleNotFoundError or NameError:
    pass
except Exception as e:
    traceback.format_exc(e)

try:
    import update # imports the whole update.py file (update and checking module)
    updateoop = 0
except ModuleNotFoundError or NameError:
    updateoop = 1
except Exception as e:
    traceback.format_exc(e)

from discord import Member # imports the Member class from discord library (used as a shortcut in code)
from discord.ext import commands # imports the commands module from discord's extended library
from discord.ext import tasks # imports the tasks module from discord's extended library
from discord import app_commands # imports the app_commands library from discord library
#"from pretty_help import AppMenu, PrettyHelp" # ignore

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

# vnum section

def get_vnum():
    return 11.02

def get_vbranch():
    return "Beta"

# end separation

# note to self:
# 0x87CDAF = Light Green / Seaborn - succesful embeds
# 0xCD87A6 = Light Red / Pastel Magenta - error embeds
# 0x66CAFE = Light Blue / Blue Mana - info or TTO embeds (funny cafe)
# found colors with https://colorkit.co/color/

# updating section

if updateoop != 1:
    logger.info("Checking for bot and updater updates...")
    upd = update.check_for_updates(get_vbranch())
else:
    logger.error("Could not check for updates: updater missing.\n- Please download it from \n- https://raw.githubusercontent.com/WoktopusGaming/TeamTheOne-Bot/master/update.py \n- and restart the app.")

target_url = "https://raw.githubusercontent.com/WoktopusGaming/TeamTheOne-Bot/master/update.py"
data = urllib.request.urlopen(target_url)
target_url = "https://raw.githubusercontent.com/WoktopusGaming/TeamTheOne-Bot/master/db/updatelog.json"
changelogreq = urllib.request.urlopen(target_url)
changelog = json.load(changelogreq)

main_version = get_vnum()
main_branch = get_vbranch()
update_version = update.get_vnum()
devmode = 0

if update_version < changelog["stable-updpy"]:
    with open("temp.update.py", "w") as f:
        for line in data:
            f.write(line.decode("utf-8"))
    if updateoop != 1:
        comp = filecmp.cmp("update.py", "temp.update.py", shallow=False)
        if comp:
            os.remove("temp.update.py")
        else:
            logger.info("Update for updater was found. Installing...")
            os.remove("update.py")
            os.rename("temp.update.py", "update.py")
            logger.info("Update for updater was installed. Restarting main app...")
            os.system("main.py")
    else:
        logger.info("Updater was not found. Installing...")
        os.rename("temp.update.py", "update.py")
        logger.info("Updater is now installed. Restarting main app...")
        os.system("main.py")



if updateoop != 1:
    if upd == False:
        logger.info("No update was found.")
        pass
    elif upd == True:
        if main_branch == "Beta":
                logger.info("An update was found for the Beta version. Installing update...")
                logger.warn(f"WARNING: Beta versions are unstable, and any change will be installed and will overwrite any current file! It is recommended you use a stable version instead! Ignore if you are aware of the consequences this could give with your clients. If you do not want this to be shown again, you can add a # at the start of lines 117 and 118 in main.py, needing to be readded every time the update happens. If you are fine with overwriting any file, press any letter then Enter. If you are not, please type \"exit\" then Enter. Thank you for your understanding.")
                upd_exit = input()
                try:
                    if upd_exit == "exit":
                        logger.info("Beta version update installation cancelled.")
                        pass
                    else:
                        update.get_updates("Beta")
                except NameError:
                    logger.info("Skipping Beta version update warning.")
                    update.get_updates("Beta")
        else:
            if main_version < changelog["stable-latest-number"]:
                logger.info("An update was found for the stable release. Installing update...")
                update.get_updates()
    elif upd == None:
        devmode = 1
        pass
            

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

target_url = "https://raw.githubusercontent.com/WoktopusGaming/TeamTheOne-Bot/master/startup.py"
data = urllib.request.urlopen(target_url)

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
        quit()
except Exception as e:
    logger.error(traceback.format_exc(e))

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
        quit()
except Exception as e:
    logger.error(traceback.format_exc(e))

try:
    if users['bot-configured'] == True and users['bot-startup'] == True:
        if devmode != 1:
            os.remove('startup.py')
        else:
            print("Developer mode enabled, skipping startup.py deletion check.")
            pass
except FileNotFoundError:
    pass
except NameError:
    try:
        os.system('startup.py')
    except FileNotFoundError:
        with open("startup.py", "w") as d:
            for line in data:
                d.write(line.decode("utf-8"))
            d.close()
        os.system('startup.py')
        quit()
except Exception as e:
    logger.error(traceback.format_exc(e))


#end separation
#async def record - command invoke recorder for statistics / VERSION 1

async def record(ctx):
    with open("discord.com.log", "a") as f:
        f.write(f"{ctx.author} used /{ctx.command} at \"{ctx.message.created_at}\"\n")
    f.close()

#end separation

try:
    dexer() # runs the dexer function (runs the dashboard)
except NameError:
    pass
except Exception as e:
    traceback.format_exc(e)

@bot.event
async def on_ready():
    print("Bot is online and ready as", format("TeamTheOne Bot"))
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing, 
            name="on BETA v2.2.0 | TTO"
            )
        )

    alldirs = json.load(open("db/alldirs.json"))
    for i in range(0, len(alldirs["bot-extensions"]), 1):
        await bot.load_extension(alldirs["bot-extensions"][i])
        
    await bot.tree.sync()
    logger.info("Bot set up and running")



@bot.event
async def on_command_error(ctx, error):
    logger.debug(
        f"Error {error} happened using /{ctx.command} as {ctx.author.name}.")
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(color=0xCD87A6) #light red color
        em.add_field(
            name="Whoa! Slow down!",
            value=
            f"Slow down! Your command \"/{ctx.command}\" is on cooldown! You just need to wait {round(error.retry_after, 0)} seconds before retrying it again. \n(Error TTO-100)"
        )
        await ctx.send(embed=em, delete_after=10)
        return 0
    if isinstance(error, commands.MissingPermissions):
        em = discord.Embed(color=0xCD87A6) #light red color
        em.add_field(
            name="I don't really recognize you...",
            value=
            f"I'm sorry, but I don't recognize you well, even if you look familiar. \n\"/{ctx.command}\" returned that you don't have the permissions for that command. \nI cannot evaluate you at the moment. (Error TTO-101)"
        )
        await ctx.send(embed=em, delete_after=10)
        return 0
    if isinstance(error, commands.NotOwner):
        em = discord.Embed(color=0xCD87A6) #light red color
        em.add_field(
            name="Don't surpass to my owner!",
            value=
            f"You tried to use a Owner-Only command. Well, bad luck for you, you ain't! (Error TTO-102)"
        )
        await ctx.send(embed=em, delete_after=10)
    if isinstance(error, commands.NoPrivateMessage):
        em = discord.Embed(color=0xCD87A6) #light red color
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
            alldirs = json.load(open("db/alldirs.json"))
            for i in range(0, len(alldirs["bot-extensions"]), 1):
                await bot.reload_extension(alldirs["bot-extensions"][i])
            em = discord.Embed(color=0x87CDAF)
            em.add_field(name="Reloaded all extensions",
                         value=f"We successfully reloaded all extensions!")
            await ctx.send(embed=em, ephemeral=True)
            await bot.tree.sync()
            return 0
        await bot.reload_extension(ext)
        em = discord.Embed(color=0x87CDAF)
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
    logger.debug(f"{ctx.author.name} used /echo! But the bot was immune...")
    #await ctx.send(message)


@bot.hybrid_command()
@discord.ext.commands.has_permissions(ban_members=True)
@commands.guild_only()
@commands.before_invoke(record)
async def ban(ctx, member: Member, reason):
    if ctx.message.author.guild_permissions.administrator or ctx.message.author.guild_permissions.ban_members:
        await ctx.guild.ban(member)
        await ctx.send(
            f"Successfully banned {member} from this server. Reason: {reason} (Written by {ctx.author}.)"
        )
    else:
        await ctx.send(
            f"Oops! I cannot ban {member} from the server because the member you tried to ban is higher than me. Make a manual ban instead? (Error TTO-105)"
        )
        logger.debug(f"Ban didn't work for {ctx.author.name}.")


@bot.hybrid_command()
@discord.ext.commands.has_permissions(kick_members=True)
@commands.guild_only()
@commands.before_invoke(record)
async def kick(ctx, member: Member):
    if ctx.message.author.guild_permissions.administrator or ctx.message.author.guild_permissions.kick_members:
        await ctx.guild.kick(member)
        await ctx.send(f"Successfully kicked {member} from the server.")
    else:
        await ctx.send(
            f"Oops! I cannot kick {member} from the server because the member you tried to kick is higher than me. Make a manual kick instead? (Error TTO-106)"
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
                "The Discord servers denied the connection for making too many requests -/- Error 429" # ratelimit message
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
            quit()