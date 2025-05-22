from flask import render_template, Flask as Quart #, send_from_directory
#from quart import render_template, Quart, send_from_directory - soon
from threading import Thread
from random import randrange
import os

#app definition
app = Quart(__name__)

#site routes - define them all here
@app.route('/')
def home():
    return render_template('index.html')

#run site
def run():
    app.run(host='0.0.0.0', port='5000')

#will run on your local address (127.0.0.1:5000 / localhost:5000)
#and local Wi-Fi address (x.x.x.x:5000)
#if using CLI "flask --app path/to/dexer.py run", it will run localhost on same port
#to change to local only for all times, change host to 127.0.0.1


#dexer definition (used in main.py to run website)
def dexer():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    print("Please, do not start dexer.py as the starting file.\nStart main.py instead. We will do it for you.\nStarting main.py...")
    os.system("main.py")

#side note: dexer isn't required for main.py
#you can define dexer() as break/pass instead if you dont use it

#note: if you use Termux on Android, do the following:
#- cd to repo folder, then type "git pull", then "editor"
#- type ^R^T (ctrl+R, ctrl+T)
#- using arrows and enter, browse to {repo}/dexer.py
#- replace dexer()'s code by "pass" or "return None"
#- type ^O^T (ctrl+o, ctrl+T)
#- browse again to {repo}/dexer.py
#- type Y, then ^X (ctrl+X)
