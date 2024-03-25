import urllib.request
import json
import os
import traceback
import filecmp

def download_update(default_url, tempfilename, filename):
    print(f"Downloading \"{filename}\" from repository...")
    try:
        target_url = f"{default_url}{filename}"
        data = urllib.request.urlopen(target_url)
    
        with open(f"{tempfilename}", "w") as f:
            for line in data:
                f.write(line.decode("utf-8"))
        
        return True
    except Exception as e:
        print(f"Please open an issue on Github including this:\n")
        print("Error code TTO-001 - file download failed")
        traceback.format_exc(e)
        return False
        

def comparison_check(tempfilename, filename):
    print(f"Checking for any changes...")
    try:
        comp = filecmp.cmp(f"{filename}", f"{tempfilename}", shallow=False)
        if comp:
            print("Files are indentical, skipping...")
            os.remove(f"{tempfilename}")
        else:
            print("Changes were made, installing...")
            os.remove(f"{filename}")
            os.rename(f"{tempfilename}", f"{filename}")
        return True
    except Exception as e:
        print(f"Please open an issue on Github including this:\n")
        print("Error code TTO-002 - file comparison failed")
        traceback.format_exc(e)
        return False

def check_for_updates():
    try:    
        target_url = "https://raw.githubusercontent.com/WoktopusGaming/TeamTheOne-Bot/master/db/updatelog.json"
        data = urllib.request.urlopen(target_url)

        with open("db/temp.updatelog.json", "w") as f:
            for line in data:
                f.write(line.decode("utf-8"))
    
        with open("db/temp.updatelog.json") as f: 
            users = json.load(f)

        with open("db/updatelog.json") as d:
            changelog = json.load(d)

        if users["stable-latest-number"] == changelog["stable-latest-number"] and users["stable-latest-version-num"] == changelog["stable-latest-version-num"] and users["stable-latest-version-com"] == changelog["stable-latest-version-com"]:
            os.remove("db/temp.updatelog.json")
            return False
        else:
            return True
    except Exception as e:
        print(f"Please open an issue on Github including this:\n")
        print("Error code TTO-003 - update check failed")
        traceback.format_exc(e)
        return False
    

    
def get_updates():
    with open("db/temp.updatelog.json") as f:
        changelog = json.load(f)
    with open("db/alldirs.json") as f:
        alldirs = json.load(f)
    
    default_target_url = f"https://raw.githubusercontent.com/WoktopusGaming/TeamTheOne-Bot/{changelog['stable-latest-version-num']}/{changelog['stable-latest-version-com']}/"
    
    for i in range(0, len(alldirs["normal-allinone"]), 1):
        download_update(default_target_url, alldirs["temp-allinone"][i], alldirs["normal-allinone"][i])
        comparison_check(alldirs["temp-allinone"][i], alldirs["normal-allinone"][i])
        print(" ")
    