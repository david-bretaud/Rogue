from flask import Flask, render_template 
from flask_socketio import SocketIO
from game_backend import Game
import time
import threading
import pickle

app = Flask(__name__)
socketio = SocketIO(app)
players=2
game = Game(number_of_players=players)
deja_un_thread_monstre = False


@app.route("/master")
def master_render():
    return render_template("master.html")

@socketio.on("master")
def master(json, methods=["GET","POST"]):
    global players # je viens modifier la variable globale
    players =int(json["players"])
    print(f"Passage à {players} joueurs")
    global game
    game = Game(number_of_players=players)

@socketio.on("save")
def save():
    global game
    pickle.dump(game,open("save.pickle","wb"))

@socketio.on("load")
def load():
    global game
    game=pickle.load(open("save.pickle","rb"))
    global players
    players=len(game._players)

@app.route('/player/<j>')
def index(j):
    i=int(j)
    if i<=players:
        map = game.getMap()
        return render_template("index.html", mapdata=map, n_row=len(map), n_col=len(map[0]), n_items=game._players[i-1].inventaire.Nslots,inventory_list=game._players[i-1].inventaire.symbols(), gold_count = game._players[i-1].gold, hp_count=game._players[i-1].hp_tag, attack=game._players[i-1].attack, defence= game._players[i-1].defence ,experience =0 )

@socketio.on("move")
def on_move_msg(json, methods=["GET", "POST"]):
    def action_joueur():
        print("received move ws message")
        dx = json['dx']
        dy = json["dy"]
        player=json['player']

        data, ret, event = game.move(int(player),dx,dy)

        arg1 = False
        arg2 = event
        if event == 5 : #si on change de map, il faut renvoyer la map en argument
            print("il faut changer de map")
            arg1 = True
            arg2 = game.getMap()


        args = [data, arg1, arg2]
        if ret:
            socketio.emit("actualize_map", args)

        # if event == 2 : # récupération d'un item
        #on actualise les stats des deux joueurs
        for player in game._players:
            socketio.emit("refresh_stats",player.data_stats())
    
    
    def action_monstre():
        i = True
        while i == True :
            result_monster = game.monster_move()
            for data_monster in result_monster :
                socketio.emit("response_monster", data_monster)
            time.sleep(3)
    t1 = threading.Thread(target = action_joueur)
    
    global deja_un_thread_monstre
    
    t1.start()
    if deja_un_thread_monstre == False:
        deja_un_thread_monstre = True
        t2 = threading.Thread(target = action_monstre)
        t2.start()

    t1.join()

@socketio.on("use")
def on_use_msg(json, methods=["GET", "POST"]):
    print("received use message")
    slot=json['slot']
    player=json['player']
    print(type(player))
    data, ret = game.use_item(int(player),slot)
    print(data)
    if ret :
        socketio.emit("refresh_stats",data)

@socketio.on("loot")
def on_loot_msg(json, methods=["GET", "POST"]):
    print("received use message")
    player=json['player']
    slot=json['slot']
    data, ret = game.loot_item(int(player),slot)
    print(data)
    if ret :
        socketio.emit("change_slab",data[0]) # canal pour ne changer qu'une dalle de la map
        socketio.emit("refresh_stats",data[1:4])

# if __name__=="__main__":
#     socketio.run(app, port=5002)

if __name__=="__main__":
    socketio.run(app, port=5001)




