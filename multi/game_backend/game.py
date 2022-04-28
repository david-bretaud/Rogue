import random
from .map_generator import Generator
from .player import Player
from .monster import bat,gobelin
from .items import Potion, NextLevelDoor
import numpy as np

#hp,hp_max,attack,defence
Liste_potions=np.loadtxt('Potions.csv',delimiter=',').astype('int').tolist()
#Liste_potions=[[2,0,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0],[-1,0,0,0],[0,1,0,0],[0,1,0,0],[0,1,0,0],[0,1,0,0],[0,-1,0,0],[0,0,1,0],[0,0,1,0],[0,0,1,0],[0,0,-1,0],[0,0,0,1],[0,0,0,1],[0,0,0,1],[0,0,0,-1]]


class Game:
    def __init__(self,number_of_players=1, width=96, height=32):
        self.map_width=width
        self.map_height=height # On stocke comme attribut du jeu les dmensions de la maps, pour qu'elles restent accessibles
        self._players=[]
        for i in range(number_of_players):
            self._players.append(Player(self,player_id=i+1))
        self.new_level() # Cette methode combine tout ce qu'il y avait ici avant, elle crée le niveau, l'avantage c'est qu'on peut maintenant la ré-appeller

        #self._player.initPos( self._map )

    def place_items(self):
        for item in self._list_items:
            x_i = random.randint(0,(self.map_width -1))
            y_i = random.randint(0,(self.map_height -1))
            while self._map[y_i][x_i] != '.': # tant qu'on a pas une case de sol
                y_i = random.randint(0,(self.map_height -1))
                x_i = random.randint(0,(self.map_width -1))
            item.init_pos(self._map,x_i,y_i) # si l'item avait déja une position elle ne va pas être changée (on est pas en mode forcé)

    def getMap(self):
        return self._map

    def move(self,player_num, dx, dy):
        for player in self._players:
            if player.player_id==player_num:
                return player.move(dx,dy)
        return [],False,0

    def use_item(self,player_num, slot):
        for player in self._players:
            if player.player_id==player_num:   
                print("on est entré dans le if") 
                return player.use(slot)
        return [],False
    
    def loot_item(self,player_num, slot):
        for player in self._players:
            if player.player_id==player_num:
                return player.loot(slot)
        return [],False
    
    def monster_move(self):
        result = []
        for monster in self._list_monster:
            if monster.is_alive :
                data,ret = monster.move(self._map)
                if ret :
                    result.append(data)
        return result
        
    def new_level(self):
        """Cette méthode génère un ouveau niveau, la map, les items, les monstres ... /!\ pas le joueur qui qui reste une constante, même si on pourra lui faire faire un init_pos sur les joueurs pour les remettre à leur place, il faudra changer le init_pos du joueur car il est pour l'instant déterministe"""
        self._generator = Generator(width=self.map_width, height=self.map_height)
        self._generator.gen_level()
        self._generator.gen_tiles_level()
        self._map = self._generator.tiles_level


        self._list_items=[]

        # On génère les différents items 
        
        self.gen_items()

        print(f"Il y a {len(self._list_items)} instance de Item sur la map")

        # On place tous les items de manière aléatoire (si ils n'ont pas de position, cf la methode init_pos de item)
        self.place_items()

        self._bat_1 = bat(10,10)
        self._bat_1.init_pos(self._map)
        self._bat_2 = bat(20,10)
        self._bat_2.init_pos(self._map)
        self._bat_3 = bat(20,20)
        self._bat_3.init_pos(self._map)

        self._list_monster = [self._bat_1,self._bat_2,self._bat_3]

        for player in self._players:
            player.initPos(self._map)

    def gen_items(self):
        """Fonction qui va décider pour unn niveau donné quels items vont être présents"""
        # Pour l'instant c'est un nombre aléatoire de potions aléatoires (a esperance positive), mais ca vaut le coup de faire évoluer les probas
        N=random.randint(20,30)
        # for i in range(N):
        #     hp=random.randint(-2,4)
        #     hp_max=random.randint(-1,2)
        #     attack=random.randint(-2,5)
        #     defence=random.randint(-2,5)
        #     self._list_items.append(Potion(hp_effect=hp, hp_max_effect=hp_max,attack_effect=attack,defence_effect=defence))

        for i in range(N):
            P=random.choice(Liste_potions)
            hp,hp_max,attack,defence=P
            self._list_items.append(Potion(hp_effect=hp, hp_max_effect=hp_max,attack_effect=attack,defence_effect=defence))
           

        # On met forcémment une trappe
        self._list_items.append(NextLevelDoor())


    # def monster_move(self):
    #     result = []
    #     for monster in self._list_monster:
    #         if monster.aggro_test(self._player._x, self._player._y):
    #             data, ret = monster.move(self._player._x,self._player._y, self._map)
    #             result.append( [data, ret] )
    #     return result
    
    