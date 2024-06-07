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

# note to self
# Item reminder:
# - Type 1 = Unconsumable
# - Type 2 = Consumable
#
# Duration (seconds): 60 = 1 min; 3600 = 1h; 86400 = 1d; etc.

#async def record - command invoke recorder for statistics / VERSION 1

async def record(ctx):
    with open("discord.com.log", "a") as f:
        f.write(f"{ctx.author} used /{ctx.command} at \"{ctx.message.created_at}\"\n")
    f.close()

#end separation


async def get_users_data():
    with open("db/users.json") as f:
        users = json.load(f)
    return users

async def update_account(user, users):
    try:
        if users["Users"][f"{user.id}"]["Wallet"] != 0:
            pass
    except KeyError:
        users["Users"][f"{user.id}"]["Wallet"] = 0
            
    try:
        if users["Users"][f"{user.id}"]["Username"] != user.name:
            users["Users"][f"{user.id}"]["Username"] = user.name
    except KeyError:
        users["Users"][f"{user.id}"]["Username"] = user.name
            
    try:
        if users["Users"][f"{user.id}"]["Last Daily"] != 0:
            pass
    except KeyError:
        users["Users"][f"{user.id}"]["Last Daily"] = 0
        
    try:
        if users["Users"][f"{user.id}"]["Streaks"]["Daily"] != 0:
            pass
    except KeyError:
        users["Users"][f"{user.id}"]["Streaks"] = {}
        users["Users"][f"{user.id}"]["Streaks"]["Daily"] = 0
        
    for i in users["Shop"]["Items"]:
        try:
            if users["Users"][f"{user.id}"]["Inventory"][f"{i}"] == 0:
                users["Users"][f"{user.id}"]["Inventory"][f"{i}"] = 0
        except KeyError:
            try:
                users["Users"][f"{user.id}"]["Inventory"][f"{i}"] = 0
            except KeyError:
                users["Users"][f"{user.id}"]["Inventory"] = {}
                users["Users"][f"{user.id}"]["Inventory"][f"{i}"] = 0
                
    for i in users["Keys"]:
        if str(i) == "KeysNum":
            pass
        else:
            try:
                if users["Users"][f"{user.id}"]["Keys"][f"{i}"] != False:
                    pass
            except KeyError:
                try:
                    users["Users"][f"{user.id}"]["Keys"][f"{i}"] = False
                except:
                    users["Users"][f"{user.id}"]["Keys"] = {}
                    users["Users"][f"{user.id}"]["Keys"][f"{i}"] = False
    
    for i in users["Users"][f"{user.id}"]["Keys"]:
        if users["Users"][f"{user.id}"]["Keys"][f"{i}"] == False:
            del users["Users"][f"{user.id}"]["Keys"][f"{i}"]
    
    return users
    
async def update_database(users):
    for i in users["Users"]:
        try:
            if users["Users"][f"{i}"]["Wallet"] != 0:
                pass
        except KeyError:
            users["Users"][f"{i}"]["Wallet"] = 0
    
        try:
            if users["Users"][f"{i}"]["Last Daily"] != 0:
                pass
        except KeyError:
            users["Users"][f"{i}"]["Last Daily"] = 0
            
        try:
            if users["Users"][f"{i}"]["Streaks"]["Daily"] != 0:
                pass
        except KeyError:
            users["Users"][f"{i}"]["Streaks"] = {}
            users["Users"][f"{i}"]["Streaks"]["Daily"] = 0
        
        for n in users["Shop"]["Items"]:
            try:
                if users["Users"][f"{i}"]["Inventory"][f"{n}"] == 0:
                    users["Users"][f"{i}"]["Inventory"][f"{n}"] = 0
            except KeyError:
                try:
                    users["Users"][f"{i}"]["Inventory"][f"{n}"] = 0
                except KeyError:
                    users["Users"][f"{i}"]["Inventory"] = {}
                    users["Users"][f"{i}"]["Inventory"][f"{n}"] = 0
                
        for n in users["Keys"]:
            try:
                if users["Users"][f"{i}"]["Keys"][f"{n}"] != False:
                    pass
            except KeyError:
                try:
                    users["Users"][f"{i}"]["Keys"][f"{n}"] = False
                except:
                    users["Users"][f"{i}"]["Keys"] = {}
                    users["Users"][f"{i}"]["Keys"][f"{n}"] = False
        
    return users

async def open_account(user):
    users = await get_users_data()
    
    if str(user.id) in users["Users"]:
        users = await update_account(user, users)
        users = await update_database(users)
    else:
        users["Users"][f"{user.id}"] = {}
        users["Users"][f"{user.id}"]["Wallet"] = 0
        users["Users"][f"{user.id}"]["Username"] = user.name
        users["Users"][f"{user.id}"]["Last Daily"] = 0
        users["Users"][f"{user.id}"]["Streaks"] = {}
        users["Users"][f"{user.id}"]["Streaks"]["Daily"] = 1
        
        users["Users"][f"{user.id}"]["Inventory"] = {}
        for i in users["Shop"]["Items"]:
            users["Users"][f"{user.id}"]["Inventory"][f"{i}"] = 0
        
        users["Users"][f"{user.id}"]["Keys"] = {}
        for i in users["Keys"]:
            users["Users"][f"{user.id}"]["Keys"][f"{i}"] = False

    with open("db/users.json", 'w') as f:
        json.dump(users, f, indent='\t')

    return True


@discord.app_commands.describe(cpage = "Chooses the changelog page in the catalog. 0 shows all changelogs's other specifications.", eph = "Checks if you want it ephemeral or not. True by default.")
@commands.hybrid_command(brief="Shows up the changelog")
@commands.before_invoke(record)
async def changelog(ctx, cpage = 0, eph = True):
    number = 0
    with open('db/updatelog.json', 'r') as f:
        changelog = json.load(f)

    for i in changelog["Changelogs"]:
        number += 1
    
    try:
        em = discord.Embed(color=0x66CAFE)
        em.add_field(name="Changelog", value=changelog['Changelogs'][str(cpage)]['Detailed Changelog'])
        em.add_field(name="Versions", value=f"- {changelog['Changelogs'][str(cpage)]['Compact Version']}\n- {changelog['Changelogs'][str(cpage)]['Second Version Number']}")
        em.add_field(name="Version Name and Number", value=f'- {changelog["Changelogs"][str(cpage)]["Version Name"]}\n- Changelog N°{changelog["Changelogs"][str(cpage)]["Number"]}')
        await ctx.send(embed=em, ephemeral=eph)
    except KeyError:
        if cpage == 0:
            versions = f""
            versionnames = f""
            changelognumbers = f""
            em = discord.Embed(color=0x66CAFE)

            for i in changelog["Changelogs"]:
                if int(i) <= changelog["changelog-startpoint"]:
                    pass
                else:
                    versions += f"- {changelog['Changelogs'][str(i)]['Compact Version']} / {changelog['Changelogs'][str(i)]['Second Version Number']}\n"
                    versionnames += f'- {changelog["Changelogs"][str(i)]["Version Name"]}\n'
                    changelognumbers += f"- Changelog N°**{changelog['Changelogs'][str(i)]['Number']}**\n"
                
            em.add_field(name="All changelogs versions", value=versions)
            em.add_field(name="All changelogs names", value=versionnames)
            em.add_field(name="All changelogs numbers", value=changelognumbers)

            await ctx.send(f"Hey there! This command now shows the latest changelogs instead of all of them due to a changelog overfill. If you'd like to see a specific changelog, please use the cpage argument when using the command until developers find a workaround. Thank you!\n\- WoktopusGaming, owner/developer.", embed=em, ephemeral=eph)
        else:
            em = discord.Embed(color=0xCD87A6)
            em.add_field(name="Unexisting changelog", value=f"You've put an unexistant changelog number.\nThere is **{number}** registered changelogs up to now.\nUse </changelog:1097887315948470382> to list the last 5 changelog names. **(Error TTO-110)**")
            await ctx.send(embed=em, ephemeral=eph)
    except Exception as e:
        await ctx.send('I might have broke myself while retrieving the changelogs... **(Error TTO-111)**', ephemeral=eph)
        logging.error(traceback.format_exc())
        

@discord.app_commands.describe(amt = "Amount of money to gamble", level = "(Optionnal) Sets the reward level, default is 0 (auto).")
@commands.hybrid_command()
@commands.guild_only()
@commands.before_invoke(record)
async def gamble(ctx, amt:int, level:int = 0):
  try:
    users = await get_users_data()
    earnings = amt
    
    try:
        money = users["Users"][str(ctx.author.id)]["Wallet"]
    except KeyError:
        await open_account(ctx.author) #opens account and registers DB
        users = await get_users_data() #refresh DB
        if earnings <= 50:
            gibgib = earnings
            gibgib += 1
            users["Users"][str(ctx.author.id)]["Wallet"] += gibgib #add money as newgiver (bypass NO COINS system)
        money = users["Users"][str(ctx.author.id)]["Wallet"]
    
    await open_account(ctx.author)
    if users["Users"][str(ctx.author.id)]["Wallet"] <= earnings:
      await ctx.send(f"You wanted to gamble {earnings} coins, but you'll be left with {money - earnings} coins, if you lose, and I can't let you with no money left nor with your account overdrawn.")
      return 0
    if level == 0:
      if amt < 75:
        level = 1
      elif amt < 125:
        level = 2
      elif amt < 175:
        level = 3
      elif amt <= 250:
        level = 4
      else:
        level = 5
    elif level >= 6:
      level = 5
    elif level <= 3:
      level = 4
       
    if random.randrange(4) == 1:
      await ctx.send(f"You got {random.randrange(34)} and lost {amt} coins.")
      money -= earnings
      users["Users"][str(ctx.author.id)]["Wallet"] = money
      users["Users"][str(ctx.author.id)]["Username"] = ctx.author.name + "#" + str(ctx.author.discriminator)
      with open("db/users.json", "w") as f:
        json.dump(users, f, indent='\t')
    else:
      #separate win sections
      #level 1 rewards better, level 5 rewards lesser
      if random.randrange(3) == 1:
        if level == 5:
          #earnings gets multiplied by 0.5
          m = 0.5
          earnings //= 2
        elif level == 4:
          #earnings gets multiplied by 1
          #earnings is already 1, pass
          m = 1
        elif level == 3:
          #earnings gets multiplied by 1.5
          m = 1.5
          earnings //= 0.5
        elif level == 2:
          #earnings gets multiplied by 2
          m = 2
          earnings *= 2
        else:
          #earnings gets multiplied by 2.5
          m = 2.5
          earnings //= 0.4
        await ctx.send(f"You got {random.randrange(33, 67)} and won {earnings}, which is **{m}x** your bets (you lost nothing).")
        round(earnings)
        users["Users"][str(ctx.author.id)]["Wallet"] += earnings
        users["Users"][str(ctx.author.id)]["Username"] = ctx.author.name
        with open("db/users.json", "w") as f:
          json.dump(users, f, indent="\t")
      else:
        if level == 5:
          #earnings get multiplied by 1
          #already 1x, skip
          m = 1
        elif level == 4:
          #earnings get multiplied by 2
          m = 2
          earnings *= 2
        elif level == 3:
          #earnings get multiplied by 3
          m = 3
          earnings *= 3
        elif level == 2:
          #earnings get multiplied by 4
          m = 4
          earnings *= 4
        else:
          #earnings get muliplied by 5
          m = 5
          earnings *= 5
        await ctx.send(f"You got {random.randrange(66, 101)} and won {earnings}, which is **{m}x** your bets (you won the jackpot, and so lost nothing).")
        round(earnings)
        users["Users"][str(ctx.author.id)]["Wallet"] += earnings
        users["Users"][str(ctx.author.id)]["Username"] = ctx.author.name
        with open("db/users.json", "w") as f:
          json.dump(users, f, indent="\t")
  except Exception as e:
    await ctx.send("I sent my report to the developers. I might have broke the casino machine... Make sure to have an account open using </wallet:1066510029299134569>. (Error TTO-112 (deprecated, no Github support will be given))")
    logging.error(traceback.format_exc())


@commands.hybrid_command()
@commands.guild_only()
@commands.before_invoke(record)
async def give(ctx, amt:int, mem:Member):
    try:
        await open_account(ctx.author)
        await open_account(mem)
        users = await get_users_data()
        earnings = amt
        if users["Users"][str(ctx.author.id)]["Wallet"] == 0:
            await ctx.send("Failed to give money: not enough money.")
            return
        if users["Users"][str(ctx.author.id)]["Wallet"] <= earnings:
            await ctx.send("Failed to give money: not enough money.")
            return
        users["Users"][str(ctx.author.id)]["Wallet"] -= earnings
        users["Users"][str(mem.id)]["Wallet"] += earnings
        users["Users"][str(ctx.author.id)]["Username"] = ctx.author.name
        users["Users"][str(mem.id)]["Username"] = mem.name
        with open("db/users.json", "w") as f:
            json.dump(users, f, indent="\t")
        await ctx.send(f"Successfully given {earnings} to {mem.display_name}!")
    except Exception:
        await ctx.send("I sent my report to the developers. I might have broke the giving machine... (Error TTO-113)")
        logging.error(traceback.format_exc())



@commands.hybrid_command(brief="Check how many money you have.")
@commands.before_invoke(record)
async def wallet(ctx, member:Member = commands.parameter(default=lambda ctx: ctx.author)):
    try:
        mem = member or ctx.author     
        await open_account(mem)

        user = mem

        users = await get_users_data()
    
        wallet_amt = users["Users"][str(user.id)]["Wallet"]
        users["Users"][str(user.id)]["Username"] = user.name

        em = discord.Embed(title=f"{mem.name}'s balance.", color=0x66CAFE)
        em.add_field(name="Multiserver Wallet Balance", value=wallet_amt)
        await ctx.send(f"Hey there! If you had any TTO coin, we have transferred the amounts to your multi-server wallet, with a rate of 100 coins per TTO coin. Thank you for having used this currency at the first place. We will add more in the future, so stay tuned to updates!\n\- WoktopusGaming, owner / developer", embed=em)
    except Exception as e:
        await ctx.send("I sent my report to the developers. I might have broke the bank system... (Error TTO-114)")
        logging.error(traceback.format_exc())



@discord.ext.commands.cooldown(1, 15, commands.BucketType.user)
@commands.hybrid_command(brief="Begs someone to give you money.")
@commands.guild_only()
@commands.before_invoke(record)
async def beg(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_users_data()
    earnings = random.randrange(126)
    users["Users"][str(user.id)]["Wallet"] += earnings
    users["Users"][str(user.id)]["Username"] = user.name
    with open("db/users.json", 'w') as f:
        json.dump(users, f, indent="\t")
    await ctx.send(f"Someone gave you {earnings} coins! You added them to your multiserver wallet.")
      

@commands.hybrid_command()
@commands.guild_only()
@commands.before_invoke(record)
async def rob(ctx, member:Member):
  await open_account(ctx.author)
  users = await get_users_data()
  if users["Users"][str(ctx.author.id)]["Wallet"] <= 250:
    await ctx.send("You cannot rob because you're too poor, and everyone wants to run away from you.")
    return 0
  if users["Users"][str(member.id)]["Wallet"] <= 250:
    await ctx.send("You cannot rob a poor, you're crazy?")
    return 0
  num = random.randrange(11)
  if num != 1:
      coinless = random.randrange(251)
      users["Users"][str(ctx.author.id)]["Wallet"] -= coinless
      users["Users"][str(member.id)]["Wallet"] += 5
      users["Users"][str(ctx.author.id)]["Username"] = ctx.author.name
      users["Users"][str(member.id)]["Username"] = member.name
      with open("db/users.json", "w") as f:
        json.dump(users, f, indent="\t")
      await ctx.send(f"Bad luck! {member.display_name} saw you trying to rob his money! He thought you robbed already, so you apologized and lost {coinless} coins.")
      return 0
  else:
    coinless = random.randrange(251)
    users["Users"][str(ctx.author.id)]["Wallet"] += coinless * 5
    users["Users"][str(member.id)]["Wallet"] -= coinless
    users["Users"][str(ctx.author.id)]["Username"] = ctx.author.name
    users["Users"][str(member.id)]["Username"] = member.name
    with open("db/users.json", "w") as f:
      json.dump(users, f, indent="\t")
    await ctx.send(f"You successfully robbed {member.display_name} and won {coinless * 5}.")


ascup = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

@commands.hybrid_command(brief="Generates up to 5 codes giving the same reward.", with_app_command = True)
@discord.app_commands.describe(amount = "Number of codes to generate - maximum 5", hidemsg = "Hides message from others on success (send ephemeral)", strnum="Determines how many characters the code(s) must contain - minimum 4, maximum 20", keytype="Determines the reward of reedeming this code (leave blank for now)", value="Depending on choosen type, defines the value behind the code - 0 sets it randomly", availabletype="Determines the availability of the code - 1 is one-time key, 2 needs a manual disable")
@commands.guild_only()
@commands.is_owner()
@commands.before_invoke(record)
# "Multiserver Coins" is keytype 1
# 
# "One-time reach (first redeemed first gotten)" is availabletype 1
# "Forever reaches" is availabletype 2
async def gen(ctx, amount = 1, hidemsg = True, strnum = 8, keytype = 1, value = 0, availabletype = 2):
    try: 
        if amount >= 6:
            await ctx.send("I cannot generate over 5 codes at once.")
            return
        if amount <= 0:
            await ctx.send("I cannot generate a negative amount of codes.")
            return
        if strnum < 4 or strnum > 20:
            await ctx.send("I cannot generate under 4 or above 20 characters per code.")
            return
        key_amt = range(amount)
        num = strnum
        keys = await get_users_data()
        normal = "Keys:"
        for x in key_amt:
            key = "".join(random.choices(ascup + digits, k=num))
            keys["Keys"]["KeysNum"] += 1
            keys["Keys"][key] = {}
            keys["Keys"][key]["Available"] = True
            keys["Keys"][key]["Availability"] = availabletype
            if keytype == 1:
                if value == 0 or value >= 10001:
                    keys["Keys"][key]["Amount"] = random.randrange(10, 10000)
                else:
                    keys["Keys"][key]["Amount"] = value
                keys["Keys"][key]["Wallet"] = "Wallet"
            normal += f'\n- \"{key}\"'
        await ctx.send(normal, ephemeral=hidemsg)
        with open("db/users.json", 'w') as f:
            json.dump(keys, f, indent="\t")
    except Exception as e:
        await ctx.send('While generating codes, I might have lost the keys for access to vault... (Error TTO-115)')
        await logging.error(traceback.format_exc())



@discord.app_commands.describe(key = "The key to redeem", eph = "Checks if you want it ephemeral or not")
@commands.hybrid_command(brief="Redeem your codes you found out using this command")
@commands.guild_only()
@commands.before_invoke(record)
async def redeem(ctx, key, eph = True):
    await open_account(ctx.author)
    keys = await get_users_data()
    
    try:
        try:
            keycheck = keys["Keys"][key]
        except Exception as e:
            em = discord.Embed(color=0xCD87A6) #light red color
            em.add_field(
                name="Invalid Key Typed",
                value=
                f"Your key typed is invalid. It might be your spelling or that the key is removed.\nAll letters are CAPS LOCKED if any, to help you. (Error TTO-116)"
            )
            await ctx.send(embed=em, ephemeral=eph)
            return
        
        if keys["Keys"][key]["Available"] == False:
            em = discord.Embed(color=0xCD87A6) #light red color
            if keys["Keys"][key]["Availability"] == 1:
                em.add_field(
                    name="Unavailable Key",
                    value=
                    f"The key you typed is unavailable. It might have been redeemed by someone else. Contact the developers for any issues. (Error TTO-117)"
                )
            else:
                em.add_field(
                    name="Unavailable Key",
                    value=
                    f"The key you typed is unavailable. It might have been removed. Contact the developers for any issues. (Error TTO-118)"
                )
            await ctx.send(embed=em, ephemeral=eph)
            return
            
        if keys["Users"][str(ctx.author.id)]["Keys"][key] == True:
            em.add_field(
                name="Key Already Redeemed",
                value=
                f"You have already redeemed this key. (Error TTO-119)"
            )
            await ctx.send(embed=em, ephemeral=eph)
            return
            
        if keys["Keys"][key]["Available"] == True:
            if keys["Keys"][key]["Availability"] == 1:
                keys["Keys"][key]["Available"] = False
            
            if keys["Keys"][key]["Wallet"] == "Wallet":
                value = keys["Keys"][key]["Amount"]
                keys["Users"][str(ctx.author.id)]["Wallet"] += value
                em = discord.Embed(color=0x87CDAF)
                if keys["Keys"][key]["Availability"] == 1:
                    em.add_field(
                        name="Key Redeemed!",
                        value=
                        f"YAYYY! You got a key! It's incredible. You got it faster than anyone else. WOWWW! You recieved {value} coins in your wallet. Enjoy!"
                    )
                else:
                    em.add_field(
                        name="Key Redeemed!",
                        value=
                        f"YAYYY! You got a key! It's incredible. You recieved {value} coins in your wallet. Enjoy!"
                    )
                await ctx.send(embed=em, ephemeral=eph)
                keys["Users"][str(ctx.author.id)]["Keys"][key] = True
                
            with open("db/users.json", "w") as f:
                json.dump(keys, f, indent="\t")
    except Exception as e:
        await ctx.send('While searching codes, I might have lost the keys to access the code database... (Error TTO-120)')
        await logging.error(traceback.format_exc())
  


@discord.app_commands.describe(eph = "Checks if you want it ephemeral or not. True by default.")
@commands.hybrid_command()
@commands.before_invoke(record)
async def daily(ctx, eph = True):
    try:
        await open_account(ctx.author)
        users = await get_users_data()
        
        dt = datetime.datetime.now(datetime.timezone.utc) #UTC Datetime
        ts = int(datetime.datetime.timestamp(dt)) #UTC Timestamp
        ts_seconds = ts % 86400
        ts_days = ts // 86400
        
        streak = users["Users"][str(ctx.author.id)]["Streaks"]["Daily"]
        
        ld = users["Users"][str(ctx.author.id)]["Last Daily"]
        ld_seconds = ld % 86400
        ld_days = ld // 86400
        
        if ld_days < ts_days:
            if (ld_days + 1) == ts_days:
                users["Users"][str(ctx.author.id)]["Streaks"]["Daily"] += 1
            else:
                streak = 0
                users["Users"][str(ctx.author.id)]["Streaks"]["Daily"] = 0
            daily = random.randrange(750)
            streakth = streak * 0.5
            
            if streakth == 0:
                pass
                
            streakdailycount = 1 + streakth
            daily *= streakdailycount
            daily = round(daily)
            users["Users"][str(ctx.author.id)]["Last Daily"] = ts                       
            await ctx.send(f"You've got {daily} coins! Come back at midnight GMT (UTC) to claim again!\nStreak Count: {streak+1} days (**{streakdailycount}**x bonus\*)\n\n\*Boost was applied before messaging", ephemeral=eph)
            users["Users"][str(ctx.author.id)]["Wallet"] += daily
        else:
            thinkity = 86400 - ts_seconds
            if thinkity <= 59:
                await ctx.send(f"You'll have to wait {thinkity} seconds before being able to collect again your daily bonus. It ain't long!", ephemeral=eph)
            elif thinkity <= 3599:
                await ctx.send(f"You'll have to wait {thinkity//60} minutes and {thinkity%60} seconds before being able to collect again your daily bonus. It's not very long!", ephemeral=eph)
            else:
                await ctx.send(f"You'll have to wait {thinkity//3600} hours, {thinkity%3600//60} minutes and {thinkity%60} seconds before being able to collect again your daily bonus.", ephemeral=eph)
        with open('db/users.json', 'w') as f:
            json.dump(users, f, indent="\t")
    except Exception as e:
        await ctx.send(f"I am sorry but for an unknown reason I can't retrieve something... (Error TTO-121)", ephemeral=eph)
        await logging.error(traceback.format_exc())

@discord.app_commands.describe(eph = "Checks if you want it ephemeral or not. True by default.")
@commands.hybrid_group(fallback="view")
@commands.before_invoke(record)
async def shop(ctx, eph = True):
    try:
        em = discord.Embed(color=0x66CAFE)
        em.add_field(
            name="Shop",
            value="We, as in our group coding this project, are sorry to announce the shop still unopened and in works. Would be a pleasure if you could come back later... We are sorry."
        )
        await ctx.send(embed=em, ephemeral=eph)
    except Exception as e:
        await ctx.send(f"We are sorry {ctx.author.mention}, but an error occured. I've let the host know this. (Error TTO-123)", ephemeral=eph)
        await logging.error(traceback.format_exc())



async def setup(bot):
  bot.add_command(gen)
  bot.add_command(redeem)
  bot.add_command(changelog)
  bot.add_command(beg)
  bot.add_command(wallet)
  bot.add_command(rob)
  bot.add_command(give)
  #bot.add_command(gamble)
  bot.add_command(shop)
  bot.add_command(daily)
  
if __name__ == "__main__":
    print("Please, do not start an extension as the starting file, they will always be loaded in the bot.\n-Start main.py instead. We will do it for you.\n-Starting main.py from project directory...\n- (This will only work if you enabled indexing in global settings, case of Visual Basic Studio, or if you use a host provider, e.g. Replit.)")
    os.system(f"main.py")
    print("Starting main.py from command line directory...")
    os.chdir("..")
    os.system(f"main.py")