# This code got some of its bases thanks to the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot
# before going its own way, yet using the documentation

# I'm planning on working on the documentation, so you don't have to look at the whole code
# I removed comments at the end of each single line, I'm sorry
# - WoktopusGaming, aka Etchy / Echazarel

import argparse

mainparser = argparse.ArgumentParser(description="TeamTheBot main Python app.")
mainparser.add_argument("--devmode", action="store_true", dest="devparse", default=False, help="Enables developer mode without database checks.")
args = mainparser.parse_args()

import aiohttp
import asyncio
import discord
import filecmp
import json
import logging
import os
import sys
import time
import traceback

import logging.handlers
import urllib.request

from discord import Member
from discord.ext import commands
#"from discord.ext import tasks" # ignore
#"from pretty_help import AppMenu, PrettyHelp" # ignore

try:
    from dexer import dexer
except ModuleNotFoundError or NameError:
    pass
except Exception as e:
    traceback.format_exc(e)

try:
    import update
    updateoop = 0
except ModuleNotFoundError or NameError:
    updateoop = 1
except Exception as e:
    traceback.format_exc(e)

logger = logging.getLogger('discord')

logging.CDEBUG = 15
logging.addLevelName(logging.CDEBUG, "CDEBUG")

def cdebug(self, message, *args, **kws):
    if self.isEnabledFor(logging.CDEBUG):
        self._log(logging.CDEBUG, message, args, **kws)

logging.Logger.cdebug = cdebug

logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='discord.log',
    encoding='utf-8',
    maxBytes=1 * 1024 * 1024,
    backupCount=5
)
handler.setLevel(logging.CDEBUG)

dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(
    '[{asctime}] [{levelname:<8}] {name}: {message}',
    dt_fmt,
    style='{'
)

handler.setFormatter(formatter)
logger.addHandler(handler)

handlee = logging.handlers.RotatingFileHandler(
    filename='fulldiscord.log',
    encoding='utf-8',
    maxBytes=100 * 1024 * 1024,
    backupCount=5
)
handlee.setLevel(logging.DEBUG)
handlee.setFormatter(formatter)
logger.addHandler(handlee)

handles = logging.StreamHandler(sys.stdout)
handles.setLevel(logging.INFO)
handles.setFormatter(formatter)
logger.addHandler(handles)

# version section

def get_vnum():
    return 0.1107

def get_vbranch():
    return "unreleased"

# end separation

# note to self:
# 0x87CDAF = Light Green / Seaborn - succesful embeds
# 0xCD87A6 = Light Red / Pastel Magenta - error embeds
# 0x66CAFE = Light Blue / Blue Mana - info or TTO embeds (funny cafe)
# found colors with https://colorkit.co/color/

# updating section

devmode = 0

with open("db/users.json") as f:
    dev = json.load(f)

try:
    if dev["developermode"] == True or args.devparse:
        devmode = 1
        print("Developer mode enabled, skipping update check.\n- Refer to documentation if you do not know what is developer mode.\n- It is not what you may think.")
except Exception:
    pass

if updateoop != 1 and devmode == 0:
    logger.info("Checking for bot and updater updates...")
    upd = update.check_for_updates(get_vbranch())
elif updateoop == 1:
    logger.error("Could not check for updates: updater missing.\n- Please download it from \n- https://raw.githubusercontent.com/WoktopusGaming/TeamTheOne-Bot/master/update.py \n- and restart the app.")

target_url = "https://raw.githubusercontent.com/WoktopusGaming/TeamTheOne-Bot/master/update.py"
data = urllib.request.urlopen(target_url)
target_url = "https://raw.githubusercontent.com/WoktopusGaming/TeamTheOne-Bot/master/db/updatelog.json"
changelogreq = urllib.request.urlopen(target_url)
changelog = json.load(changelogreq)

main_version = get_vnum()
main_branch = get_vbranch()
update_version = update.get_vnum()

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



if updateoop != 1 and devmode == 0:
    if upd == False:
        logger.info("No update was found.")
        pass
    elif upd == True:
        if main_branch == "unreleased":
                logger.info("An update was found for the unreleased version. Installing update...")
                logger.warning(f"WARNING: Non-release versions are unstable, and any change will be installed and will overwrite any current file! It is recommended you use a stable version instead! Ignore if you are aware of the consequences this could give with your clients. If you do not want this to be shown again because you accept, you can add a # at the start of lines 154 and 155 in main.py, needing to be readded every time the update happens. If you are fine with overwriting any file, press any letter then Enter. If you are not, please type \"exit\" then Enter. Thank you for your understanding.")
                upd_exit = input()
                try:
                    if upd_exit == "exit":
                        logger.info("Unreleased version update installation cancelled.")
                        pass
                    else:
                        update.get_updates("unreleased")
                except NameError:
                    logger.info("Skipping unreleased version update warning.")
                    update.get_updates("unreleased")
        else:
            if main_version < changelog["stable-latest-number"]:
                logger.info("An update was found for the stable release. Installing update...")
                update.get_updates()
    elif upd == None:
        devmode = 1
        pass


#end separation

class UnfilteredBot(commands.Bot): pass

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
            print("Skipping startup.py deletion check.")
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
    dexer()
except NameError:
    pass
except Exception as e:
    traceback.format_exc(e)

@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing, 
            name="TeamTheBot"
            )
        )

    alldirs = json.load(open("db/alldirs.json"))
    for i in range(0, len(alldirs["bot-extensions"]), 1):
        try: await bot.load_extension(alldirs["bot-extensions"][i])
        except Exception: pass
        
    logger.info("Successfully connected to Discord API")



@bot.event
async def on_command_error(ctx, error):
    logger.cdebug(
        f"Error {error} happened using /{ctx.command} as {ctx.author.name}.")
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(color=0xCD87A6)
        em.add_field(
            name="Whoa! Slow down!",
            value=
            f"Slow down! Your command \"/{ctx.command}\" is on cooldown! You just need to wait {round(error.retry_after, 0)} seconds before retrying it again. \n(Error TTO-100)"
        )
        await ctx.send(embed=em, delete_after=10)
        return 0
    if isinstance(error, commands.MissingPermissions):
        em = discord.Embed(color=0xCD87A6)
        em.add_field(
            name="I don't really recognize you...",
            value=
            f"I'm sorry, but I don't recognize you well, even if you look familiar. \n\"/{ctx.command}\" returned that you don't have the permissions for that command. \nI cannot evaluate you at the moment. (Error TTO-101)"
        )
        await ctx.send(embed=em, delete_after=10)
        return 0
    if isinstance(error, commands.NotOwner):
        em = discord.Embed(color=0xCD87A6)
        em.add_field(
            name="Don't surpass to my owner!",
            value=
            f"You tried to use a bot owner-only command. Well, bad luck for you, I can differentiate one from another! (Error TTO-102)"
        )
        await ctx.send(embed=em, delete_after=10)
    if isinstance(error, commands.NoPrivateMessage):
        em = discord.Embed(color=0xCD87A6)
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
    except Exception as e:
        await ctx.send('Can\'t load extension. (Error TTO-107)', ephemeral=True)
        logger.error(traceback.format_exc())


@bot.hybrid_command()
@commands.is_owner()
async def unload(ctx, ext):
    try:
        await bot.unload_extension(ext)
        await ctx.send(f'Extension \"{ext}\" successfully unloaded.', ephemeral=True)
    except Exception as e:
        await ctx.send('Can\'t unload extension. (Error TTO-108)', ephemeral=True)
        logger.error(traceback.format_exc())


@bot.hybrid_command()
@commands.is_owner()
async def reload(ctx, ext, id: discord.Guild = None):
    try:
        if ext == "all":
            alldirs = json.load(open("db/alldirs.json"))
            for i in range(0, len(alldirs["bot-extensions"]), 1):
                try:
                    await bot.reload_extension(alldirs["bot-extensions"][i])
                except discord.ext.commands.errors.ExtensionNotLoaded as e:
                    await bot.load_extension(alldirs["bot-extensions"][i])
            
            em = discord.Embed(color=0x87CDAF)
            em.add_field(
                name="Reloaded all extensions", 
                value=f"We successfully reloaded all extensions!"
            )

            if id == None:
                await bot.tree.sync()
            else:
                try:
                    await bot.tree.sync(guild=discord.Object(id=id))
                except Exception:
                    await bot.tree.sync()
            
            await ctx.send(embed=em, ephemeral=True)
            logger.info(f"Reloaded all extensions")
            return None
        
        try:
            await bot.reload_extension(ext)
        except discord.ext.commands.errors.ExtensionNotLoaded as e:
            await bot.load_extension(ext)
        
        em = discord.Embed(color=0x87CDAF)
        em.add_field(
            name="Reloaded extension",
            value=f'We reloaded this extension successfully: \"{ext}\".'
        )

        if id == 0:
            await bot.tree.sync()
        else:
            try: 
                await bot.tree.sync(guild=discord.Object(id=id))
            except Exception as e: 
                em.add_field(
                    name="Tree sync failed",
                    value=f'Tree synchronisation to guild {id} failed. Exiting synchronisation process. (Error TTO-112)'
                )
        
        await ctx.send(embed=em, ephemeral=True)
        logger.info(f"Reloaded extension {ext}")
    except Exception as e:
        if ext == "all":
            await ctx.send('Can\'t reload all extensions. (Error TTO-109)', ephemeral=True)
        else:
            await ctx.send(f'Can\'t reload extension {ext}. (Error TTO-109)', ephemeral=True)
        logger.error(traceback.format_exc())


@bot.hybrid_command()
@commands.guild_only()
async def echo(ctx, message, channel: discord.TextChannel = None):
    try:
        echo = bot.get_channel(channel.id) or bot.get_channel(ctx.channel.id)
        await echo.send(message)

        # modified @commands.before_invoke(record) specially for echos
        with open("discord.com.log", "a") as f:
            if len(message) >= 75:
                f.write(f"{ctx.author} used /{ctx.command} at \"{ctx.message.created_at}\":\n-------------\n{message}\n-------------\n")
            else:
                f.write(f"{ctx.author} used /{ctx.command} at \"{ctx.message.created_at}\": \"{message}\"\n")
        f.close()
        # end separation

        await ctx.send("Sent!", ephemeral=True)
    except Exception as e:
        await ctx.send("I have an error sending your message. (Error TTO-104)", ephemeral=True)
        logger.cdebug(f"Failed to send message, command runner: {ctx.author.name}.")
        traceback.format_exc()

@bot.hybrid_command()
@discord.ext.commands.has_permissions(ban_members=True)
@commands.guild_only()
@commands.before_invoke(record)
async def ban(ctx, member: Member, reason = "No specification was given.", eph = False):
    try:
        try:
            em = discord.Embed(
                color=0xCD87A6,
                description=f"You have been banned in **{ctx.guild.name}**. || {reason}"
            )
            await member.send(f"You have been banned from **{ctx.guild.name}**.", embed=em)
        except discord.errors.HTTPException:
            pass

        em = discord.Embed(color=0xCD87A6, title="Ban Notification (sent)")
        em.add_field(
            name="User:",
            value=f"{member.mention}"
        )
        em.add_field(
            name="Server staff member:",
            value=f"{ctx.author.mention}"
        )
        em.add_field(
            name="Reason:",
            value=f"{reason}"
        )
        sc = discord.Embed(
            color=0x87CDAF,
            description=f":white_check_mark: ***{member} was banned.***"
        )
        await ctx.guild.ban(member, reason=reason)
        await ctx.send(
            embeds = [sc, em],
            ephemeral = eph
        )
    except Exception as e:
        await ctx.send(
            f"Oops! I cannot ban {member} from the server! Try a manual ban instead? (Error TTO-105)"
        )
        logger.cdebug(f"Ban failed, command runner: {ctx.author.name}.")
        logger.error(traceback.format_exc())


@bot.hybrid_command()
@discord.ext.commands.has_permissions(kick_members=True)
@commands.guild_only()
@commands.before_invoke(record)
async def kick(ctx, member: Member):
    try:
        await ctx.guild.kick(member)
        await ctx.send(f"Successfully kicked {member} from the server.")
    except Exception:
        await ctx.send(
            f"Oops! I cannot kick {member} from the server because the member you tried to kick is higher than me. Make a manual kick instead? (Error TTO-106)"
        )
        logger.cdebug(f"Kick failed, comamand runner: {ctx.author.name}.") # will output in log file set to CDEBUG
        
#
# Separator between launching modules and commands
#

f = open(".token", 'r')
r = f.readlines()
a = str(r[0])
f.close

async def main():
    async with bot:
        await bot.start(a)

try:
    try: 
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        tsk = loop.create_task(main())
        tsk.add_done_callback(lambda t: print(f'Task done with result={t.result()}  << return val of main()'))
    else:
        asyncio.run(main())
except discord.HTTPException as e:
    if e.status == 429:
        logger.warning("The Discord servers denied the connection for making too many requests - Error 429")
    else:
        logger.warning(f"HTTP error {e} was raised. Correct immediately or contact developer.")
except KeyboardInterrupt:
    logger.info("Main task was interrupted. Program will close within the next few seconds.")
    quit()
except Exception as e:
    if type(e) == aiohttp.client_exceptions.ClientConnectorError:
        logger.warning(f"WHOOPS! Seems you're offline! Checking again in 5 seconds. (Error TTO-005)")
        time.sleep(5)
        logger.info(f"Restarting main process...")
        os.system('main.py')
    else:
        logger.warning(f"Error \"{e}\" (\"{type(e)}\") was raised. Please correct it ASAP. (Error TTO-000)")
        logger.warning(traceback.format_exc())
        time.sleep(5)
        raise e
