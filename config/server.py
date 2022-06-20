from flask import Flask, redirect, url_for
from threading import Thread

app = Flask("")

@app.route("/")
def main():
  return "globalchatbot"


def run():
  app.run("0.0.0.0", port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()
