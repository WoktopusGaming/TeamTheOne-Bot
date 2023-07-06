from discord.ext import commands
from discord import app_commands
from discord import Member
from discord import utils

import json
import discord
import random
import traceback
import logging
import datetime
import time

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


async def open_account(user):
    users = await get_users_data()

    if str(user.id) in users["Users"]:
        try:
            if users["Users"][f"{user.id}"]["Username"] != (user.name + "#" + str(user.discriminator)):
                users["Users"][f"{user.id}"]["Username"] = user.name + "#" + str(user.discriminator)
        except KeyError:
            users["Users"][f"{user.id}"]["Username"] = user.name + "#" + str(user.discriminator)
            
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
                users["Users"][f"{user.id}"]["Inventory"][f"{i}"] = 0
    else:
        users["Users"][f"{user.id}"] = {}
        users["Users"][f"{user.id}"]["Wallet"] = 0
        users["Users"][f"{user.id}"]["TTO"] = 0
        users["Users"][f"{user.id}"]["Username"] = user.name + "#" + str(user.discriminator)
        users["Users"][f"{user.id}"]["Last Daily"] = 0
        users["Users"][f"{user.id}"]["Streaks"] = {}
        users["Users"][f"{user.id}"]["Streaks"]["Daily"] = 1
        users["Users"][f"{user.id}"]["Inventory"] = {}
        for i in users["Shop"]["Items"]:
            users["Users"][f"{user.id}"]["Inventory"][f"{i}"] = 0

    with open("db/users.json", 'w') as f:
        json.dump(users, f, indent='\t')

    return True


@discord.app_commands.describe(cpage = "Chooses the changelog page in the catalog. 0 shows all changelogs's other specifications.", eph = "Checks if you want it ephemeral or not. True by default.")
@commands.hybrid_command(brief="Shows up the changelog")
@commands.before_invoke(record)
async def changelog(ctx, cpage: int, eph = True):
    number = 0
    with open('db/updatelog.json', 'r') as f:
        changelog = json.load(f)

    for i in changelog["Changelogs"]:
        number += 1
    
    try:
        em = discord.Embed(color=0x00FF90)
        em.add_field(name="Changelog", value=changelog['Changelogs'][str(cpage)]['Detailed Changelog'])
        em.add_field(name="Versions", value=f"- {changelog['Changelogs'][str(cpage)]['Compact Version']}\n- {changelog['Changelogs'][str(cpage)]['Detailed Version']}\n- {changelog['Changelogs'][str(cpage)]['Second Version Number']}")
        em.add_field(name="Version Name and Number", value=f'- {changelog["Changelogs"][str(cpage)]["Version Name"]}\n- Changelog N°{changelog["Changelogs"][str(cpage)]["Number"]}')
        await ctx.send(embed=em, ephemeral=eph)
    except KeyError:
        if cpage == 0:
            versions = f""
            versionnames = f""
            changelognumbers = f""
            em = discord.Embed(color=0x00FF90)

            for i in changelog["Changelogs"]:
                versions += f"- {changelog['Changelogs'][str(i)]['Compact Version']} / {changelog['Changelogs'][str(i)]['Second Version Number']}\n"
                versionnames += f'- {changelog["Changelogs"][str(i)]["Version Name"]}\n'
                changelognumbers += f"- Changelog N°**{changelog['Changelogs'][str(i)]['Number']}**\n"
                
            em.add_field(name="All changelogs versions", value=versions)
            em.add_field(name="All changelogs names", value=versionnames)
            em.add_field(name="All changelogs numbers", value=changelognumbers)

            await ctx.send(embed=em, ephemeral=eph)
        else:
            em = discord.Embed(color=0xEB1F1F)
            em.add_field(name="Unexisting changelog", value=f"You've put an unexistant changelog number.\nThere is **{number}** registered changelogs up to now.\n</changelog:1097887315948470382> cpage 0 to list all changelog names.")
            await ctx.send(embed=em, ephemeral=eph)
    except Exception as e:
        await ctx.send('I might have broke myself while retrieving the changelogs...', ephemeral=eph)
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
        users["Users"][str(ctx.author.id)]["Username"] = ctx.author.name + "#" + str(ctx.author.discriminator) 
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
        users["Users"][str(ctx.author.id)]["Username"] = ctx.author.name + "#" + str(ctx.author.discriminator)
        with open("db/users.json", "w") as f:
          json.dump(users, f, indent="\t")
  except Exception as e:
    await ctx.send("I sent my report to the developers. I might have broke the casino machine... Make sure to have an account open using </wallet:1066510029299134569>.")
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
      if users[str(ctx.author.id)]["Wallet"] <= earnings:
        await ctx.send("Failed to give money: not enough money.")
        return
      users["Users"][str(ctx.author.id)]["Wallet"] -= earnings
      users["Users"][str(mem.id)]["Wallet"] += earnings
      users["Users"][str(ctx.author.id)]["Username"] = ctx.author.name + "#" + str(ctx.author.discriminator)
      users["Users"][str(mem.id)]["Username"] = mem.name + "#" + str(mem.discriminator)
      with open("db/users.json", "w") as f:
        json.dump(users, f, indent="\t")
      await ctx.send(f"Successfully given {earnings} to {mem.display_name}!")
    except Exception:
      await ctx.send("I sent my report to the developers. I might have broke the giving machine...")
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
        users_amt = users["Users"][str(user.id)]["TTO"]
        users["Users"][str(user.id)]["Username"] = user.name + "#" + str(user.discriminator)

        em = discord.Embed(title=f"{mem.name}'s balance.", color=discord.Color.teal())
        em.add_field(name="Multiserver Wallet Balance", value=wallet_amt)
        em.add_field(name="TeamTheOne Wallet Balance", value=users_amt)
        await ctx.send(embed=em)
    except Exception as e:
        await ctx.send("I sent my report to the developers. I might have broke the bank system...")
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
    users["Users"][str(user.id)]["Username"] = user.name + "#" + str(user.discriminator)
    with open("db/users.json", 'w') as f:
        json.dump(users, f, indent="\t")
    await ctx.send(f"Someone gave you {earnings} coins! You added them to your multiserver wallet.")
      



gengui = [947175286787690527]
ascup = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

@commands.hybrid_command(brief="Generates up to 5 codes giving the same reward.", with_app_command = True)
@discord.app_commands.describe(amount = "How many codes to generate", hidemsg = "Hides message from others (send ephemeral)", strnum="Determines how many characters the code(s) must contain", keytype="Determines the reward of reedeming this code", value="Depending on choosen type, defines the value behind the code.")
@commands.guild_only()
@commands.is_owner()
@commands.before_invoke(record)
#"Multiserver Coins" is choice 1
#"TTO Coins" is choice 2
async def gen(ctx, amount = 1, hidemsg = True, strnum = 8, keytype = 1, value = 0):
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
        keys["Keys"]["Keys"] += 1
        keys["Keys"][key] = {}
        keys["Keys"][key]["Available"] = True
        keys["Keys"][key]["Type"] = keytype
        if keytype == 1:
            if value == 0 or value >= 1000:
              keys["Keys"][key]["Amount"] = random.randrange(30, 1000)
            else:
              keys["Keys"][key]["Amount"] = value
            keys["Keys"][key]["Wallet"] = "Wallet"
        elif keytype == 2:
            if value == 0 or value >= 400:
              keys["Keys"][key]["Amount"] = random.randrange(10, 400)
            else:
              keys["Keys"][key]["Amount"] = value
            keys["Keys"][key]["Wallet"] = "TTO"
        normal += f'\n- \"{key}\"'
    await ctx.send(normal, ephemeral=hidemsg)
    with open("db/users.json", 'w') as f:
        json.dump(keys, f, indent="\t")
  except Exception as e:
    await ctx.send('While generating codes, I might have lost the keys...')
    await logging.error(traceback.format_exc())


@commands.hybrid_command()
@commands.guild_only()
@commands.before_invoke(record)
async def rob(ctx, member:Member):
  users = await get_users_data()
  if users["Users"][str(ctx.author.id)]["Wallet"] <= 150:
    await ctx.send("You cannot rob because you're too poor, and everyone wants to run away from you.")
    return 0
  if users["Users"][str(member.id)]["Wallet"] <= 150:
    await ctx.send("You cannot rob a poor, you're crazy?")
    return 0
  num = random.randrange(11)
  if num != 1:
      coinless = random.randrange(151)
      users["Users"][str(ctx.author.id)]["Wallet"] -= coinless
      users["Users"][str(ctx.author.id)]["Username"] = ctx.author.name + "#" + str(ctx.author.discriminator)
      with open("db/users.json", "w") as f:
        json.dump(users, f, indent="\t")
      await ctx.send(f"Bad luck! {member.display_name} saw you trying to rob his money! He thought you robbed already, so you apologized and lost {coinless} coins.")
      return 0
  else:
    coinless = random.randrange(151)
    users["Users"][int(ctx.author.id)]["Wallet"] += coinless
    users["Users"][int(member.id)]["Wallet"] -= coinless
    users["Users"][str(ctx.author.id)]["Username"] = ctx.author.name + "#" + str(ctx.author.discriminator)
    users["Users"][str(member.id)]["Username"] = member.name + "#" + str(member.discriminator)
    with open("db/users.json", "w") as f:
      json.dump(users, f, indent="\t")
    await ctx.send(f"You successfully robbed {member.display_name} and won {coinless}.")


@discord.app_commands.describe(key = "The key to redeem (UUID-4 format)", eph = "Checks if you want it ephemeral or not. True by default.")
@commands.hybrid_command(brief="For code redeem", help="Redeems code, used normally for economy system.")
@commands.guild_only()
@commands.before_invoke(record)
async def redeem(ctx, key, eph = True):
    try:  
        await open_account(ctx.author.id)
        await get_users_data()
    except Exception as e:
        await ctx.send('I\'m overprocessing, sorry. Try again.', ephemeral=eph)
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
            daily = random.randrange(500)
            streakth = streak * 0.5
            
            if streakth == 0:
                pass
                
            streakdailycount = 1 + streakth
            daily *= streakdailycount
            daily = round(daily)
            users["Users"][str(ctx.author.id)]["Last Daily"] = ts
            
            if ctx.author.guild.id == 947175286787690527:
                dailytto = random.randrange(25) * streakdailycount
                dailytto = round(dailytto)
                role = utils.get(ctx.guild.roles, id=1110685038237982860)
                if role in ctx.author.roles:
                    daily = daily * 5
                    dailytto = dailytto * 5
                    await ctx.send(f"You've got {daily} coins and {dailytto} TTO coins as a bonus of claiming in the corresponding partnered server!\nYou've also got a **5x** bonus from being Premium (TTO Coins too)\*!\nCome back at midnight GMT (UTC) to claim again!\nStreak Count: {streak+1} days (**{streakdailycount}**x bonus\*)\n\n\*Boost was applied before messaging", ephemeral=eph)
                else:
                    role = utils.get(ctx.guild.roles, id=1110685408058167316)
                    if role in ctx.author.roles:
                        daily = daily * 4
                        dailytto = dailytto * 4
                        await ctx.send(f"You've got {daily} coins and {dailytto} TTO coins as a bonus of claiming in the corresponding partnered server!\nYou've also got a **4x** bonus from being MVP++ (TTO Coins too)!\*\nCome back at midnight GMT (UTC) to claim again!\nStreak Count: {streak+1} days (**{streakdailycount}**x bonus\*)\n\n\*Boost was applied before messaging", ephemeral=eph)
                    else:
                        role = utils.get(ctx.guild.roles, id=1110685424009105459)
                        if role in ctx.author.roles:
                            daily = daily * 4
                            await ctx.send(f"You've got {daily} coins and {dailytto} TTO coins as a bonus of claiming in the corresponding partnered server!\nYou've also got a **4x** bonus from being MVP+ (excludes TTO Coins)\*!\nCome back at midnight GMT (UTC) to claim again!\nStreak Count: {streak+1} days (**{streakdailycount}**x bonus\*)\n\n\*Boost was applied before messaging", ephemeral=eph)
                        else:
                            role = utils.get(ctx.guild.roles, id=1110685444586340413)
                            if role in ctx.author.roles:
                                daily = daily * 3
                                await ctx.send(f"You've got {daily} coins and {dailytto} TTO coins as a bonus of claiming in the corresponding partnered server!\nYou've also got a **3x** bonus from being MVP (excludes TTO Coins)\*!\nCome back at midnight GMT (UTC) to claim again!\nStreak Count: {streak+1} days (**{streakdailycount}**x bonus\*)\n\n\*Boost was applied before messaging", ephemeral=eph)
                            else:
                                role = utils.get(ctx.guild.roles, id=1110685458276556910)
                                if role in ctx.author.roles:
                                    daily = daily * 2
                                    await ctx.send(f"You've got {daily} coins and {dailytto} TTO coins as a bonus of claiming in the corresponding partnered server!\nYou've also got a **2x** bonus from being VIP+ (excludes TTO Coins)\*!\nCome back at midnight GMT (UTC) to claim again!\nStreak Count: {streak+1} days (**{streakdailycount}**x bonus\*)\n\n\*Boost was applied before messaging", ephemeral=eph)
                                else:
                                    await ctx.send(f"You've got {daily} coins and {dailytto} TTO coins as a bonus of claiming in the corresponding partnered server!\nCome back at midnight GMT (UTC) to claim again!\nStreak Count: {streak+1} days (**{streakdailycount}**x bonus\*)\n\n\*Boost was applied before messaging", ephemeral=eph)
                users["Users"][str(ctx.author.id)]["TTO"] += dailytto
            else:                        
                await ctx.send(f"You've got {daily} coins! Come back at midnight GMT (UTC) to claim again!\nStreak Count: {streak+1} days (**{streakdailycount}**x bonus\*)\n\n\*Boost was applied before messaging", ephemeral=eph)
            users["Users"][str(ctx.author.id)]["Wallet"] += daily
        else:
            thinkity = ts - users['Users'][str(ctx.author.id)]['Last Daily']
            if thinkity <= 59:
                await ctx.send(f"You'll have to wait {thinkity} seconds before being able to collect again your daily bonus. It ain't long!", ephemeral=eph)
            elif thinkity <= 3599:
                await ctx.send(f"You'll have to wait {thinkity//60} minutes and {thinkity%60} seconds before being able to collect again your daily bonus. It's not very long!", ephemeral=eph)
            else:
                await ctx.send(f"You'll have to wait {thinkity//3600} hours, {thinkity%3600//60} minutes and {thinkity%60} seconds before being able to collect again your daily bonus.", ephemeral=eph)
        with open('db/users.json', 'w') as f:
            json.dump(users, f, indent="\t")
    except Exception as e:
        await ctx.send(f"I am sorry but for an unknown reason I can't retrieve something...", ephemeral=eph)
        await logging.error(traceback.format_exc())

@discord.app_commands.describe(eph = "Checks if you want it ephemeral or not. True by default.")
@commands.hybrid_group(fallback="view")
@commands.guild_only()
@commands.before_invoke(record)
async def shop(ctx, eph = True):
    try:
        await ctx.send("We are sorry, the shop isn't yet opened.", ephemeral=eph)
    except Exception as e:
        await ctx.send(f"We are sorry {ctx.author.mention}, but an error occured. I've let the developer know this.", ephemeral=eph)
        await logging.error(traceback.format_exc())



async def setup(bot):
  bot.add_command(gen)
  #bot.add_command(redeem)
  bot.add_command(changelog)
  bot.add_command(beg)
  bot.add_command(wallet)
  bot.add_command(rob)
  bot.add_command(give)
  bot.add_command(gamble)
  bot.add_command(shop)
  bot.add_command(daily)