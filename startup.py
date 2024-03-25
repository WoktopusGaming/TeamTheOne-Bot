import json
import traceback
import os
import sys

def rangewrite(file):
    lines = f.readlines()
    x = len(lines)
    v = ""
    
    for i in range(x): 
        v += f"{lines[i]}"
    return v
    

print(f"Welcome! You launched TeamTheOne Bot for the first time!\nWe will configurate a few files before starting the app.")
a = 0

print(" ")
print("Looking for a .token file...")
try:
    f = open(".token", 'r')
except FileNotFoundError:
    a += 1
    print("File wasn't found!")
    print(f"Please input your bot token, it will only be used on bot startup and for Discord interactions.\nWARNING: Make sure it is ONLY the bot token, this is the only time this file will be launched and available.")
    print("Token: ")
    b = input()
    print("Saving into file...")
    with open('.token', 'w') as f:
        f.write(b)
        f.close()
    print("Finished!")
except Exception as e:
    print(f"An error occured.\nPlease report it to the creator using the Issue section of the repository you downloaded it from.\nInclude the traceback with your report. (Error TTO-006)")
    traceback.format_exc(e)
else:
    print("Found one!")

print(" ")
print("Looking for a \"users.json\" file in the database directory...")
try:
    with open("db/users.json") as f:
        users = json.load(f)
except json.JSONDecodeError:
    a += 1
    print(f"Found one! But it seems this file was misformatted...\nWe will save a backup of that file, and format another one for you.")
    print("Rewriting...")
    with open("db/users.json") as f:
        with open("db/users.backup.json", "w") as d:
            d.write(f"{rangewrite(f)}")
            d.close()
        f.close()
    with open("db/users.json", "w") as f:
        d = open("db/users.temp.json", "w")
        d.write("{\n\n}")
        d.close
        d = open("db/users.temp.json")
        users = json.load(d)
        
        users["bot-configured"] = True
        users["bot-startup"] = True
        users["Keys"] = {}
        users["Keys"]["KeysNum"] = 0
        users["Shop"] = {}
        users["Shop"]["Items"] = {}
        
        json.dump(users, f, indent="\t")
        d.close()
        f.close()
    os.remove("db/users.temp.json")
    print("Finished!")
except FileNotFoundError:
    a += 1
    print(f"File wasn't found!\nWe will make one for you.")
    print("Writing...")
    with open("db/users.json", "w") as f:
        d = open("db/users.temp.json", "w")
        d.write("{\n\n}")
        d.close
        d = open("db/users.temp.json")
        users = json.load(d)
        
        users["Keys"] = {}
        users["Keys"]["KeysNum"] = 0
        users["Shop"] = {}
        users["Shop"]["Items"] = {}
        users["bot-configured"] = True
        users["bot-startup"] = True
        
        json.dump(users, f, indent="\t")
        d.close()
        f.close()
    os.remove("db/users.temp.json")
    print("Finished!")
except Exception as e:
    print(f"An error occured.\nPlease report it to the creator using the Issue section of the repository you downloaded it from.\nInclude the traceback with your report. (Error TTO-007)")
    traceback.format_exc(e)
else:
    print("Found one!")
    
print(" ")
print("Looking for the Discord and Flask libraries...")
try:
    import discord
    import flask
except ImportError:
    a += 1
    print(f"I did not find one or more of these librairies!\nI will automatically install the latest version of these modules for you!")
    print("Installing libraries...")
    print(" ")
    os.system("python.exe -m pip install --upgrade discord flask pip")
except Exception as e:
    print(f"An error occured.\nPlease report it to the creator using the Issue section of the repository you downloaded it from.\nInclude the traceback with your report. (Error TTO-008)")
    traceback.format_exc(e)
else:
    print("Found the libraries!")

print(" ")

if a == 0:
    print(f"If it is already well configured, did you use it before or you set everything up after download?\nI expect no answers, so no worries.\nHave fun with the bot!")
else:
    print("The configuration is finished!")
print("We will launch the bot for you, please wait...")
print(" ")
os.system("main.py")
quit(code=sys._ExitCode)

