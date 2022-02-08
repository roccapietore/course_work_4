from typing import Dict, Type
from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect
from game.characters import characters, Character
from game.equipment import EquipmentData
from game.functions import load_equipment
from game.hero import Player, Enemy, Hero

app = Flask(__name__)
app.url_map.strict_slashes = False
EQUIPMENT: EquipmentData = load_equipment()

heroes: Dict[str, Hero] = {}


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
    print(request.form["weapon"])
    return redirect(url_for("fight"))


@app.route('/fight')
def fight():
    if "player" in heroes and "enemy" in heroes:
        return render_template('fight.html', heroes=heroes, result="Бой начался!")
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)

