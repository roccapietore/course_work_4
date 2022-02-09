from typing import Dict, Type
from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect
from game.characters import characters, Character
from game.equipment import EquipmentData
from game.functions import load_equipment
from game.hero import Player, Enemy, Hero
from game.controller import Game
from functools import wraps

app = Flask(__name__)
app.url_map.strict_slashes = False
EQUIPMENT: EquipmentData = load_equipment()

heroes: Dict[str, Hero] = {}
game = Game()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/choose-hero', methods=["GET", "POST"])
def choose_hero():
    if request.method == "GET":
        return render_template('hero_choosing.html',
                               header="Выберите героя",
                               classes=characters.values(),
                               result=EQUIPMENT,
                               next_button="Выберите врага")

    heroes["player"] = Player(player_class=characters[request.form["unit_class"]],
                              weapon=EQUIPMENT.get_weapon(request.form["weapon"]),
                              armor = EQUIPMENT.get_armor(request.form["armor"]),
                              name=request.form["name"])

    return redirect(url_for("choose_enemy"))


@app.route('/choose-enemy', methods=["GET", "POST"])
def choose_enemy():
    if request.method == "GET":
        return render_template('hero_choosing.html',
                               header="Выберите врага",
                               classes=characters.values(),
                               result=EQUIPMENT,
                               next_button="Начать бой")

    heroes["enemy"] = Enemy(player_class=characters[request.form["unit_class"]],
                              weapon=EQUIPMENT.get_weapon(request.form["weapon"]),
                              armor=EQUIPMENT.get_armor(request.form["armor"]),
                              name=request.form["name"])

    return redirect(url_for("fight"))


@app.route('/fight')
def fight():
    if "player" in heroes and "enemy" in heroes:
        game.run(**heroes)
        return render_template('fight.html', heroes=heroes, result="Бой начался!")
    return redirect(url_for("index"))


@app.route('/fight/hit')
def hit():
    if game.game_processing:
        return render_template('fight.html', heroes=heroes, result=game.player_hit())
    if game.game_results:
        return render_template('fight.html', heroes=heroes, result=game.game_results)
    return redirect(url_for("index"))

@app.route('/fight/use-skill')
def use_skill():
    if game.game_processing:
        return render_template('fight.html', heroes=heroes, result=game.use_skill())
    if game.game_results:
        return render_template('fight.html', heroes=heroes, result=game.game_results)
    return redirect(url_for("index"))

@app.route('/fight/pass-turn')
def pass_turn():
    if game.game_processing:
        return render_template('fight.html', heroes=heroes, result=game.next_turn())
    if game.game_results:
        return render_template('fight.html', heroes=heroes, result=game.game_results)
    return redirect(url_for("index"))


@app.route('/fight/end-fight')
def end_fight():
    if game.game_processing:
        return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True)

