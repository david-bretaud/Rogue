function creerListe(mot){
    let n = mot.length; 
    let L = new Array(n);
    for(let j =0; j<n; j++){
        L[j]=mot[j];
    }
    return L;
}

window.addEventListener("DOMContentLoaded", (event) => {
    var socket = io.connect("http://" + document.domain + ":" + location.port );

    // ---------- TRACER DE LA MAP ----------
    
    /* Eléments constants*/
    var dessinMap = document.getElementById("dessinMap");
    var ctx = dessinMap.getContext("2d"); //ctx.fillStyle = ("green"); ctx.fillRect(0, 0, 300, 200);
    var dessinInventaire = document.getElementById("dessin_inventaire");
    var ctx2 = dessinInventaire.getContext("2d");
    var picture_player = document.getElementById("picture_player");
    var picture_monster = document.getElementById("picture_monster");
    var picture_wall = document.getElementById("picture_wall");
    var picture_gold = document.getElementById("picture_gold");
    var picture_seller = document.getElementById("picture_seller");
    var picture_potion = document.getElementById("picture_potion");
    var picture_ground0 = document.getElementById("picture_ground0");
    var picture_ground = document.getElementById("picture_ground1");
    var picture_ground2 = document.getElementById("picture_ground2");
    var picture_vortex = document.getElementById("picture_vortex");
    var picture_empty_slot = document.getElementById("picture_empty_slot");
    var bruitage_vortex = document.getElementById("bruitage_vortex");
    var nrow = document.getElementById("nrow").innerHTML;
    var ncol = document.getElementById("ncol").innerHTML;
    var tailleX =14; 
    var tailleY =18;
    var nitems = 8; //document.getElementById("nitems").innerHTML;
    var slot_size =32;

    function dessiner_map(){
        /* On parcourt les spans de la map qui contiennent l'information
        */
        var dat;
        for(let p=0; p<nrow; p++){
            for(let q=0; q<ncol;q++ ){
                var cell = "cell " + p + "-" + q;
                var dat = document.getElementById(cell).innerText;
                switch(dat){
                    case "@":
                        ctx.drawImage(picture_ground, q*tailleX, p*tailleY, tailleX, tailleY);
                        ctx.drawImage(picture_player, q*tailleX, p*tailleY+(tailleY-tailleX)/2, tailleX, tailleY);
                        break ;
                    case "G":
                        ctx.drawImage(picture_ground, q*tailleX, p*tailleY, tailleX, tailleY);
                        ctx.drawImage(picture_gold, q*tailleX, p*tailleY+(tailleY-tailleX)/2, tailleX, tailleX);
                        break ;
                    case "w":
                        ctx.drawImage(picture_ground, q*tailleX, p*tailleY, tailleX, tailleY);
                        ctx.drawImage(picture_monster, q*tailleX, p*tailleY+(tailleY-tailleX)/2, tailleX, tailleX);
                        break ;
                    case "e":
                        ctx.drawImage(picture_ground, q*tailleX, p*tailleY, tailleX, tailleY);
                        ctx.drawImage(picture_monster, q*tailleX, p*tailleY+(tailleY-tailleX)/2, tailleX, tailleX);
                        break ;
                    case "#":
                        ctx.drawImage(picture_wall, q*tailleX, p*tailleY, tailleX, tailleY);
                        break ;
                    case ".":
                        ctx.drawImage(picture_ground, q*tailleX, p*tailleY, tailleX, tailleY);
                        break ;
                    case "x":
                        ctx.drawImage(picture_ground2, q*tailleX, p*tailleY, tailleX, tailleY);
                        break ;
                    case "&":
                        ctx.drawImage(picture_ground, q*tailleX, p*tailleY, tailleX, tailleY);
                        ctx.drawImage(picture_potion, q*tailleX, p*tailleY+(tailleY-tailleX)/2, tailleX, tailleX);
                        break ;
                    case "L":
                        ctx.drawImage(picture_ground, q*tailleX, p*tailleY, tailleX, tailleY);
                        ctx.drawImage(picture_vortex, q*tailleX, p*tailleY+(tailleY-tailleX)/2, tailleX, tailleX);
                }
            }
        }

    }
    window.addEventListener("load", dessiner_map);

    function dessiner_inventaire(){
        var dat;
        for (let i=1;i<=nitems;i++){
            item_id="item"+i;
            dat=document.getElementById(item_id).innerText;
            switch(dat){
                case "&":
                    ctx2.drawImage(picture_empty_slot, i*slot_size,0,slot_size,slot_size);
                    ctx2.drawImage(picture_potion, i*slot_size,0,slot_size,slot_size);
                    break ;
                case "°":
                    ctx2.drawImage(picture_empty_slot, i*slot_size,0,slot_size,slot_size);
                    break ;
            }
        }
    }
    window.addEventListener("load", dessiner_inventaire);

    /*
    Redessine l'image à la position (p,q) de la map avec le symbole symb. L'image de rajoute par dessus l'ancienne !*/
    function redessiner_map(q, p, symb){
        switch(symb){
            case "@":
                ctx.drawImage(picture_player, q*tailleX, p*tailleY+(tailleY-tailleX)/2, tailleX, tailleX);
                break ;
            case "G":
                ctx.drawImage(picture_gold, q*tailleX, p*tailleY+(tailleY-tailleX)/2, tailleX, tailleX);
                break ;
            case "w":
                ctx.drawImage(picture_monster, q*tailleX, p*tailleY+(tailleY-tailleX)/2, tailleX, tailleX);
                break ;
            case "e":
                ctx.drawImage(picture_monster, q*tailleX, p*tailleY+(tailleY-tailleX)/2, tailleX, tailleX);
                break ;
            case "#":
                ctx.drawImage(picture_wall, q*tailleX, p*tailleY, tailleX, tailleY);
                break ;
            case ".":
                ctx.drawImage(picture_ground, q*tailleX, p*tailleY, tailleX, tailleY);
                break ;
            case "x":
                ctx.drawImage(picture_ground2, q*tailleX, p*tailleY, tailleX, tailleY);
                break ;
            case "&":
                ctx.drawImage(picture_ground2, q*tailleX, p*tailleY, tailleX, tailleY);
                ctx.drawImage(picture_potion, q*tailleX, p*tailleY+(tailleY-tailleX)/2, tailleX, tailleX);
                break ;
        }
    }

    /*
    Après un certain nombre de déplacements, la page web a dessiné beaucoup d'images. On efface donc le canvas
    et on redessine comme au lancement la map, grâce aux données sauvegardées dans map !*/
    function clearMap(compt){
        if (compt> 20){
            ctx.width += 0;
            dessiner_map();
            return 0;
        }
        else{
            return compt ;
        }
    }

    function new_map(tab){
        var ndat;
        ctx.width += 0;
        var cell_id ;
        var new_span ;
        for(let p=0; p<nrow; p++){
            for(let q=0; q<ncol;q++ ){
                cell_id = "cell " + p + "-" + q;
                ndat=tab[p][q];
                new_span = document.getElementById(cell_id);
                new_span.textContent = ndat ;
                switch(ndat){
                    case "@":
                        ctx.drawImage(picture_ground, q*tailleX, p*tailleY, tailleX, tailleY);
                        ctx.drawImage(picture_player, q*tailleX, p*tailleY+(tailleY-tailleX)/2, tailleX, tailleY);
                        break ;
                    case "G":
                        ctx.drawImage(picture_ground, q*tailleX, p*tailleY, tailleX, tailleY);
                        ctx.drawImage(picture_gold, q*tailleX, p*tailleY+(tailleY-tailleX)/2, tailleX, tailleX);
                        break ;
                    case "w":
                        ctx.drawImage(picture_ground, q*tailleX, p*tailleY, tailleX, tailleY);
                        ctx.drawImage(picture_monster, q*tailleX, p*tailleY+(tailleY-tailleX)/2, tailleX, tailleX);
                        break ;
                    case "e":
                        ctx.drawImage(picture_ground, q*tailleX, p*tailleY, tailleX, tailleY);
                        ctx.drawImage(picture_monster, q*tailleX, p*tailleY+(tailleY-tailleX)/2, tailleX, tailleX);
                        break ;
                    case "#":
                        ctx.drawImage(picture_wall, q*tailleX, p*tailleY, tailleX, tailleY);
                        break ;
                    case ".":
                        ctx.drawImage(picture_ground, q*tailleX, p*tailleY, tailleX, tailleY);
                        break ;
                    case "x":
                        ctx.drawImage(picture_ground2, q*tailleX, p*tailleY, tailleX, tailleY);
                        break ;
                    case "&":
                        ctx.drawImage(picture_ground, q*tailleX, p*tailleY, tailleX, tailleY);
                        ctx.drawImage(picture_potion, q*tailleX, p*tailleY+(tailleY-tailleX)/2, tailleX, tailleX);
                        break ;
                    case "L":
                        ctx.drawImage(picture_ground, q*tailleX, p*tailleY, tailleX, tailleY);
                        ctx.drawImage(picture_vortex, q*tailleX, p*tailleY+(tailleY-tailleX)/2, tailleX, tailleX);
                }
            }
        }
        bruitage_vortex.play();
    }

    // ---------- TRACER BARRE D'INVENTAIRE ----------

    function draw_inventaire(inv){
        var new_span ;
        var ndat;
        var item_id;
        for (let i=1;i<=nitems;i++){
            item_id="item"+i;
            ndat=inv[i-1];
            new_span = document.getElementById(item_id);
            new_span.textContent = ndat;
            switch(ndat){
                case "&":
                    ctx2.drawImage(picture_empty_slot, i*slot_size,0,slot_size,slot_size);
                    ctx2.drawImage(picture_potion, i*slot_size ,0,slot_size,slot_size);
                    break ;
                case "°":
                    ctx2.drawImage(picture_empty_slot, i*slot_size,0,slot_size,slot_size);
                    break ;
            }
        }
    }

    // ---------- MUSIQUE ----------

        // Elements
    var musique1 = document.getElementById("mus1");
    var musique2 = document.getElementById("mus2");
    var musique3 = document.getElementById("mus3");
    var button_play =document.getElementById("button_play");
    var button_pause =document.getElementById("button_pause");
    var button_nextmusic =document.getElementById("button_nextmusic");
    var listeMusics = new Array(musique1, musique2, musique3);
    
        // Fonctions
    function changeMusic(){
        stopMusic();
        var buffer ;
        buffer = listeMusics[0] ;
        var n =listeMusics.length;
        for (var i=0; i<n-1; i++){
            listeMusics[i] = listeMusics[i+1];
        }
        listeMusics[n-1]=buffer ;
        playMusic();
    }
    function playMusic(){
        listeMusics[0].play();
        if (listeMusics[0].ended){changeMusic();}
    }
    function stopMusic(){
        listeMusics[0].pause();
    }
    button_play.addEventListener('click', playMusic);
    button_nextmusic.addEventListener('click',changeMusic);
    button_pause.addEventListener('click',stopMusic);


    // ---------- TRACER INITIAL DE LA BARRE DE HP ----------
    
    var hp_init = document.getElementById("hp_count");
    var listeCaracInit =creerListe(hp_init.innerHTML);
    var nInit = listeCaracInit.length;
    var healthBar = document.getElementById("healthBar");
    var lMax = healthBar.getAttribute("width") ;
    var h = healthBar.getAttribute("height");
    class RectangleInit {
        rect ; 
        // ----- Constructeur -----
        constructor(h, l, x, y){
            this.rect = document.createElementNS("http://www.w3.org/2000/svg", 'rect');
            this.rect.setAttribute("width", l);
            this.rect.setAttribute("height", h);
            this.rect.setAttribute("x", x);
            this.rect.setAttribute("y", y);
        }
        // ----- Fonction pour dessiner la barre -----
        static dessiner(){
            let rec ;
            for(let i =0; i<nInit; i++){
                rec = new RectangleInit(h, 0.97*lMax/nInit, i*lMax/nInit, 0);
                if (listeCaracInit[i]=="%"){rec.rect.style.fill="green";}
                else{rec.rect.style.fill="darkred";}
                healthBar.append(rec.rect);
            }
        }
    } 
    RectangleInit.dessiner();    
    

    // ---------- ANIMATIONS ----------

        // Elements 
    var bruitage_punch = document.getElementById("bruitage_punch");
    var bruitage_gold = document.getElementById("bruitage_gold");
    var bruitage_grab = document.getElementById("bruitage_grab");

        //Fonctions
    function changeColor(col){
        /* changer la couleur de fond du game en fonction de la couleur donnée
        */
        var gameBackground = document.getElementById("gameBackground");
        gameBackground.style.backgroundColor = col;
        console.log("Changement couleur background");
    }

    function animation(num){
        /*Envoie l'animation en fonction du numéro reçu :
        0 : c'est un déplacement simple, on ne fait rien
        1 : on récupère une pièce d'or
        2 : on récupère une potion
        3 : on tape le monstre
        4 : le monstre attaque
        5 : changement de map, considéré à part (à la fin du socket response)
        De même, on jouera à part la consommation de potion
        */ 
        if (num==1) bruitage_gold.play();
        else if (num==2) bruitage_grab.play();
        else if (num==3) bruitage_punch.play();
    }

    // ---------- INTERACTION CLAVIER ----------

    document.onkeydown = function(e){
        switch(e.keyCode){ // boutons appuyés
            case 37:
                socket.emit("move", {dx:-1, dy:0});
                break;
            case 38:
                socket.emit("move", {dx:0, dy:-1});
                break;
            case 39:
                socket.emit("move", {dx:1, dy:0});
                break;
            case 40: 
                socket.emit("move", {dx:0, dy:1});
                break;
            case 65: //A (on utilise Azerty tant que pas les numéros)
                socket.emit("use",{slot:1});
                break;
            case 90: //Z
                socket.emit("use",{slot:2});
                break;
            case 69: //E
                socket.emit("use",{slot:3});
                break;
            case 82: //R
                socket.emit("use",{slot:4});
                break;
            case 84: //T
                socket.emit("use",{slot:5});
                break;
            case 89: //Y
               socket.emit("use",{slot:6});
               break;
            case 85: //U
               socket.emit("use",{slot:7});
               break;
            case 73: //I
               socket.emit("use",{slot:8});
               break;
            case 81: //Q on utilise les touches du dessous pour looter
                socket.emit("loot",{slot:1});
                break;
            case 83: //S
                socket.emit("loot",{slot:2});
                break;
            case 68: //D
                socket.emit("loot",{slot:3});
                break;
            case 70: //F
                socket.emit("loot",{slot:4});
                break;
            case 71: //G
                socket.emit("loot",{slot:5});
                break;
            case 72: //H
                socket.emit("loot",{slot:6});
                break;
            case 74: //J
                socket.emit("loot",{slot:7});
                break;
            case 75: //K
                socket.emit("loot",{slot:8});
                break;
                                    
            
        }
    };


    // ---------- INTERACTION ECRAN ----------
    
    var btn_n = document.getElementById("go_n");
    btn_n.onclick = function(e) {
        console.log("Clicked on button north");
        socket.emit("move", {dx:0, dy:-1});
    };

    var btn_s = document.getElementById("go_s");
    btn_s.onclick = function(e) {
        console.log("Clicked on button south");
        socket.emit("move", {dx:0, dy:1});
    };

    var btn_w = document.getElementById("go_w");
    btn_w.onclick = function(e) {
        console.log("Clicked on button w");
        socket.emit("move", {dx:-1, dy:0});
    };

    var btn_e = document.getElementById("go_e");
    btn_e.onclick = function(e) {
        console.log("Clicked on button e");
        socket.emit("move", {dx:1, dy:0});
    };


    // ---------- COMMUNICATION SOCKET-GAME ----------

    var compteur = 0 ; //compteur pour refresh la map (qui en fait accumule et superpose toujours des images)
    socket.on("response", function(args){
        var data = args[0];
        var arg1 = args[1];
        var arg2 = args[2];
        console.log(data);
        for( var i=0; i<2; i++){
            var cell_id = "cell " + data[i].i + "-" + data[i].j;
            var span_to_modif = document.getElementById(cell_id);
            span_to_modif.textContent = data[i].content;
            redessiner_map(data[i].j, data[i].i, data[i].content);
        }
        document.getElementById("gold_count").innerHTML = data[2].content;
        document.getElementById("at").innerHTML = data[4].content;
        document.getElementById("def").innerHTML = data[5].content;
        document.getElementById("exp").innerHTML = 0;

        compteur = compteur +1 ;
        compteur = clearMap(compteur);


        // ---------- TRACER DE LA BARRE DE HP ----------

        var hpString = data[3].content;
        var listeCarac = creerListe(hpString);
        var n = hpString.length;
        class Rectangle {
            rect ; 
            // ----- Constructeur -----
            constructor(h, l, x, y){
                this.rect = document.createElementNS("http://www.w3.org/2000/svg", 'rect');
                this.rect.setAttribute("width", l);
                this.rect.setAttribute("height", h);
                this.rect.setAttribute("x", x);
                this.rect.setAttribute("y", y);
            }
            // ----- Fonction pour dessiner la barre -----
            static dessiner(){
                let rec ;
                rec = new Rectangle(h, lMax, 0, 0);
                rec.rect.style.fill="cyan";
                healthBar.append(rec.rect);
                for(let i =0; i<n; i++){
                    rec = new Rectangle(h, 0.97*lMax/n, i*lMax/n, 0);
                    if (listeCarac[i]=="%"){rec.rect.style.fill="green";}
                    else{rec.rect.style.fill="darkred";}
                    healthBar.append(rec.rect);
                }
            }
        } 
        Rectangle.dessiner(); 

        // ---------- ANIMATION / NOUVELLE MAP----------
        if (arg1==true) {
            new_map(arg2);  
        }
        else{
            animation(arg2);
        }      
    });
	
	socket.on("response_monster", function(data){
		console.log(data);
        for( var i=0; i<2; i++){
            var cell_id = "cell " + data[i].i + "-" + data[i].j;
            var span_to_modif = document.getElementById(cell_id);
            span_to_modif.textContent = data[i].content;
            redessiner_map(data[i].j, data[i].i, data[i].content);
        }
    
	});

    socket.on("refresh_stats", function(args){
        var inv = args[1];
        var data = args[0];
        console.log(inv);
        // for(var i = 0; i<=nitems; i++){
        //     var item_id="item"+i
        //     draw_inventaire(item_id,data[4].item_id)
        // }
        document.getElementById("gold_count").innerHTML = data[0].content;
        document.getElementById("at").innerHTML = data[2].content;
        document.getElementById("def").innerHTML = data[3].content;

        var hpString = data[1].content;
        var listeCarac = creerListe(hpString);
        var n = hpString.length;
        class Rectangle {
            rect ; 
            // ----- Constructeur -----
            constructor(h, l, x, y){
                this.rect = document.createElementNS("http://www.w3.org/2000/svg", 'rect');
                this.rect.setAttribute("width", l);
                this.rect.setAttribute("height", h);
                this.rect.setAttribute("x", x);
                this.rect.setAttribute("y", y);
            }
            // ----- Fonction pour dessiner la barre -----
            static dessiner(){
                let rec ;
                rec = new Rectangle(h, lMax, 0, 0);
                rec.rect.style.fill="cyan";
                healthBar.append(rec.rect);
                for(let i =0; i<n; i++){
                    rec = new Rectangle(h, 0.97*lMax/n, i*lMax/n, 0);
                    if (listeCarac[i]=="%"){rec.rect.style.fill="green";}
                    else{rec.rect.style.fill="darkred";}
                    healthBar.append(rec.rect);
                }
            }
        } 
        Rectangle.dessiner(); 

        draw_inventaire(inv);
    });

    socket.on("change_slab", function(data){
        console.log(data);
        var cell_id = "cell " + data.i + "-" + data.j;
        var span_to_modif = document.getElementById(cell_id);
        span_to_modif.textContent = data.content;
        redessiner_map(data.j, data.i, data.content);
    });

});


