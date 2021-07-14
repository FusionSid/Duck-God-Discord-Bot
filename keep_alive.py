from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Duck is alive and hunting frogs"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()