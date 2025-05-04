from urllib.error import HTTPError
import urllib.request
import json
import os
import traceback
import filecmp
import argparse

parser = argparse.ArgumentParser(description="TeamTheBot updater Python app.")
parser.add_argument("--install", action="store_true", dest="install", default=False, help="Switches updater to install mode upon invoke of argument.")
parser.add_argument("--upgrade", action="store_true", dest="update", default=False, help="Switches updater to force update mode upon invoke of argument.")
args = parser.parse_args()

def get_vnum():
    return 1.04

def download_update(default_url, fail_url, tempfilename, filename):
    print(f"Downloading file from repository...")
    try:
        target_url = f"{default_url}/{filename}"
        print(f"File link: {target_url}")
        data = urllib.request.urlopen(target_url)
    
        with open(f"{tempfilename}", "w") as f:
            for line in data:
                f.write(line.decode("utf-8"))
        
        return True
    except HTTPError as e:
        if e.status != 404:
            raise Exception
        print("File from stable release not found. Looking for master branch...")
        if fail_url == "unreleased":
            print(f"Please open an issue on Github including this:\n")
            print(f"Error code TTO-001 - file download failed (branch {fail_url}, error code 404)")
            traceback.format_exc()
            return False
        target_url = f"{fail_url}/{filename}"
        print(f"File link: {target_url}")
        data = urllib.request.urlopen(target_url)
    
        with open(f"{tempfilename}", "w") as f:
            for line in data:
                f.write(line.decode("utf-8"))
  
        return True
    except FileNotFoundError:
        mdir = tempfilename.rsplit("/", 1)
        os.makedirs(f"{mdir[0]}")

        target_url = f"{default_url}/{filename}"
        data = urllib.request.urlopen(target_url)
    
        with open(f"{tempfilename}", "w") as f:
            for line in data:
                f.write(line.decode("utf-8"))
    except Exception as e:
        print(f"Please open an issue on Github including this:\n")
        print("Error code TTO-001 - file download failed")
        traceback.format_exc()
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
    except FileNotFoundError:
        print("New file. Installing...")
        os.rename(f"{tempfilename}", f"{filename}")
    except Exception as e:
        print(f"Please open an issue on Github including this:\n")
        print("Error code TTO-002 - file comparison failed")
        traceback.format_exc()
        return False

def check_for_updates(vbranch = "stable"):
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

        if vbranch == "stable":
            if users["stable-latest-number"] == changelog["stable-latest-number"] and users["stable-latest-version-num"] == changelog["stable-latest-version-num"] and users["stable-latest-version-com"] == changelog["stable-latest-version-com"]:
                os.remove("db/temp.updatelog.json")
                return False
            elif users["stable-latest-number"] > changelog["stable-latest-number"] and users["stable-latest-version-num"] != changelog["stable-latest-version-num"] and users["stable-latest-version-com"] != changelog["stable-latest-version-com"]:
                return True
            else:
                os.remove("db/temp.updatelog.json")
                print(f"- Sorry. Your file 'db/changelog.json' got manually overwritten data, or data errors. Please redownload the repository from\n- https://github.com/WoktopusGaming/TeamTheOne-Bot/\n- for the updater to rightfully run afterwards. Thank you for your understanding.\nError code TTO-004 - file manually edited")
        else:
            if users["unreleased-latest-number"] == changelog["unreleased-latest-number"] and users["unreleased-latest-version-num"] == changelog["unreleased-latest-version-num"] and users["unreleased-latest-version-com"] == changelog["unreleased-latest-version-com"]:
                os.remove("db/temp.updatelog.json")
                return False
            elif users["unreleased-latest-number"] > changelog["unreleased-latest-number"]:
                return True
            elif users["unreleased-latest-number"] < changelog["unreleased-latest-number"]:
                print("Skipping update: repository in developer mode.\n- Refer to documentation if you do not know what is developer mode.\n- It is not what you may think.")
                os.remove("db/temp.updatelog.json")
                return None
            else:
                os.remove("db/temp.updatelog.json")
                print(f"- Sorry. Your file 'db/changelog.json' got manually overwritten data, or data errors. Please redownload the repository from\n- https://github.com/WoktopusGaming/TeamTheOne-Bot/\n- for the updater to rightfully run afterwards. Thank you for your understanding.\nError code TTO-004u - file manually edited (UNRELEASED)") 
    except Exception as e:
        print(f"Please open an issue on Github including this:\n")
        print("Error code TTO-003 - update check failed")
        traceback.format_exc()
        return False


    
def get_updates(vbranch = "stable"):
    oldupd = 0
    
    with open("db/temp.updatelog.json") as f:
        changelog = json.load(f)
        f.close()

    if vbranch == "stable":
        default_target_url = f"https://raw.githubusercontent.com/WoktopusGaming/TeamTheOne-Bot/{changelog['stable-latest-version-num']}/{changelog['stable-latest-version-com']}"
        secondary_target_url = f"https://raw.githubusercontent.com/WoktopusGaming/TeamTheOne-Bot/master"
    else:
        default_target_url = f"https://raw.githubusercontent.com/WoktopusGaming/TeamTheOne-Bot/master"
        secondary_target_url = f"unreleased"
    
    try:
        with open("db/alldirs.json") as f:
            alldirs = json.load(f)
            f.close()
    except FileNotFoundError:
        print("db/alldirs.json (old to new update or new install exception)")
        download_update(default_target_url, secondary_target_url, "db/temp.alldirs.json", "db/alldirs.json")
        comparison_check("db/temp.alldirs.json", "db/alldirs.json")
        print(" ")
        oldupd = 1
        with open("db/alldirs.json") as f:
            alldirs = json.load(f)
            f.close()
    
    for i in range(0, len(alldirs["normal-allinone"]), 1):
        if oldupd == 1 and i+1 < len(alldirs["normal-allinone"]):
            i += 1
        elif oldupd == 1: break
        
        print(alldirs["normal-allinone"][i])

        if alldirs["normal-allinone"][i] != "db/updatelog.json":
            download_update(default_target_url, secondary_target_url, alldirs["temp-allinone"][i], alldirs["normal-allinone"][i])

        comparison_check(alldirs["temp-allinone"][i], alldirs["normal-allinone"][i])

        if oldupd == 0 and alldirs["normal-allinone"][i] == "db/alldirs.json":
            with open("db/alldirs.json") as f:
                alldirs = json.load(f)
                f.close()
        print(" ")

if __name__ == "__main__":
    if args.install:
        print("Starting installation. Please do not exit the program whilst it is running.")
        try: get_updates()
        except Exception as e: traceback.format_exc(e); print("The program will quit. If it's an issue you may not know, please contact the developer."); quit()
        print("Installation is complete. You can run main.py now."); quit()
    elif args.update:
        print("Starting updating. Please do not exit the program whilst it is running.")
        try:
            upd = check_for_updates()
            if upd == True: get_updates()
        except Exception as e: traceback.format_exc(e); print("\n\n\nThe program will quit. If it's an issue you may not know, please contact the developer."); quit()
        print("Update is complete."); quit()
    else:
        print("Please, do not start update.py as the starting file.\nStart main.py instead. We will do it for you.\nStarting main.py...")
        try: os.system("main.py")
        except FileNotFoundError: print("We did not find main.py, please use the command line and add the \"--install\" argument at the end.")