from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect
from game.characters import heroes
from game.equipment import EquipmentData
from game.functions import load_equipment

app = Flask(__name__)
app.url_map.strict_slashes = False
EQUIPMENT: EquipmentData = load_equipment()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/choose-hero/', methods=["GET", "POST"])
def choose_hero():
    if request.method == "GET":
        return render_template('hero_choosing.html',
                               header="Выберите героя",
                               classes=heroes.values(),
                               result=EQUIPMENT,
                               next_button="Выберите врага")
    return redirect(url_for("choose_enemy"))


@app.route('/choose-enemy/', methods=["GET", "POST"])
def choose_enemy():
    if request.method == "GET":
        return render_template('hero_choosing.html',
                               header="Выберите врага",
                               classes=heroes.values(),
                               result=EQUIPMENT,
                               next_button="Начать бой")
    #return redirect(url_for("fight"))


if __name__ == '__main__':
    app.run(debug=True)

