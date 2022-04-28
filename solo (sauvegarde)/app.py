from flask import Flask, render_template 
from flask_socketio import SocketIO
from game_backend import Game

app = Flask(__name__)
socketio = SocketIO(app)
game = Game()


@app.route("/")
def index():
    map = game.getMap()
    return render_template("index.html", mapdata=map, n_row=len(map), n_col=len(map[0]), n_items=game._player.inventaire.Nslots,inventory_list=game._player.inventaire.symbols(), gold_count = game._player.gold, hp_count=game._player.hp_tag, attack=game._player.attack, defence= game._player.defence ,experience =0 )

@socketio.on("move")
def on_move_msg(json, methods=["GET", "POST"]):
    print("received move ws message")
    dx = json['dx']
    dy = json["dy"]

    data, ret, event = game.move(dx,dy)

    arg1 = False
    arg2 = event
    if event == 5 : #si on change de map, il faut renvoyer la map en argument
        print("il faut changer de map")
        arg1 = True
        arg2 = game.getMap()      

    args = [data, arg1, arg2]
    if ret:
        socketio.emit("response", args)

    if event == 2 : # récupération d'un item
        socketio.emit("refresh_stats",game._player.data_stats())
    
    result_monster = game.monster_move()
    for data_monster in result_monster :
        socketio.emit("response_monster", data_monster)

@socketio.on("use")
def on_use_msg(json, methods=["GET", "POST"]):
    print("received use message")
    slot=json['slot']
    data, ret = game.use_item(slot)
    print(data)
    if ret :
        socketio.emit("refresh_stats",data)

@socketio.on("loot")
def on_loot_msg(json, methods=["GET", "POST"]):
    print("received use message")
    slot=json['slot']
    data, ret = game.loot_item(slot)
    print(data)
    if ret :
        socketio.emit("change_slab",data[0]) # canal pour ne chager qu'une dalle de la map
        socketio.emit("refresh_stats",data[1:3])

if __name__=="__main__":
    socketio.run(app, port=5001)


