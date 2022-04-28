window.addEventListener("DOMContentLoaded", (event) => {
    var socket = io.connect("http://" + document.domain + ":" + location.port);

    var btn_apply=document.getElementById("btn_apply");
    var nplayers=document.getElementById("num_of_players")
    btn_apply.onclick= function(e) {
        var nb_players = nplayers.value;
        alert("Nombre de joueurs : " + nb_players);
        socket.emit("master",{players: nb_players});
    };

    var btn_save=document.getElementById('btn_save');
    btn_save.onclick=function(e) {
        alert("Partie Sauvegardée")
        socket.emit("save");
    };

    var btn_load=document.getElementById('btn_load');
    btn_load.onclick=function(e) {
        alert("Chargement d'une partie sauegardée");
        socket.emit("load");
    };
});