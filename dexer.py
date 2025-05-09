from flask import render_template, Flask as Quart #, send_from_directory
#from quart import render_template, Quart, send_from_directory - soon
from threading import Thread
from random import randrange
import os

#app definition
app = Quart(__name__)

#site route
@app.route('/')
def home():
    return render_template('index.html')

#run site
def run():
    app.run(host='0.0.0.0', port='5000')


#dexer definition (used in main.py to run website)
def dexer():
    t = Thread(target=run)
    t.start()
    
if __name__ == "__main__":
    print("Please, do not start dexer.py as the starting file.\nStart main.py instead. We will do it for you.\nStarting main.py...")
    os.system("main.py")
