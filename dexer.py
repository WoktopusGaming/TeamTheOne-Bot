from flask import render_template, Flask as Quart, send_from_directory
#from quart import render_template, Quart, send_from_directory - soon
from threading import Thread
from random import randrange
import os
import traceback
import socket
from contextlib import closing
   
def check_socket(host, port):
  try:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((host, port)) == 0:
            return 2
        else:
            return 1
  except Exception as e:
    print("Socket couldn't be checked. (Error TTO-009)")
    traceback.format_exc()
    return 0

#app definition
app = Quart(__name__)


def randport():
  num = check_socket('0.0.0.0', 8080)
  if num == 2:
    return randrange(3000, 9000)
  elif num == 1:
    return 8080
  else:
    return randrange(7900, 8100)

#site route
@app.route('/')
def home():
    return render_template('index.html')

#run site
def run():
    app.run(host='0.0.0.0', port=randport())


#dexer definition (used in main.py to run website)
def dexer():
    t = Thread(target=run)
    t.start()
    
if __name__ == "__main__":
    print("Please, do not start dexer.py as the starting file.\nStart main.py instead. We will do it for you.\nStarting main.py...")
    os.system("main.py")
