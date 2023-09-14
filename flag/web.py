import json
import os
from uuid import uuid4
from flask import Flask, send_from_directory, request

from .game import Game
from .sysadmin_agent import SysAdminAgent

app = Flask(__name__)

games = {}


def gen_game():
    id = str(uuid4())
    game = Game()
    game.pushToNextAgent(SysAdminAgent())
    game.applyNextAgent()
    games[id] = game
    return id


def get_game(id):
    return games[id]


@app.route("/", methods=["GET"])
def index():
    return send_from_directory(".", "index.html")


@app.route("/newgame", methods=["POST"])  # type: ignore
def newgame():
    return gen_game()


@app.route("/send", methods=["POST"])  # type: ignore
def send():
    game_id = request.json.get("gameid")  # type: ignore
    if game_id is None:
        return "err"
    game = get_game(game_id)
    input = request.json.get("input")  # type: ignore
    return json.dumps(game.handleInput(input))


@app.route("/checkflag", methods=["POST"])
def checkflag():
    return "1" if request.json.get("flag") == "32935GJ25GAZEIFJAEZ" else "0"  # type: ignore
