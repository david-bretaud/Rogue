from .inventaire import Inventaire
import random


class Player:
    def __init__(self,game, symbol="@",hp_init=5,hp_max=5,attack=3,defence=0):
        self._symbol = symbol
        self.game=game  # On utilise ça pour récupérer les différents attributs du jeu
        self._x = None
        self._y = None
        self.gold = 0
        self.hp_max=hp_max
        self.hp = hp_init
        self.hp_tag= '%'*self.hp + "~" *(hp_max-self.hp)
        self.attack = attack
        self.defence = defence
        self.inventaire = Inventaire()
        self.slab_occupee="x" # cet attrubut sert quand on passe sur un item et qu'on ne le récupère pas

    def hp_change(self,var_hp=0):
        """Permet à la fois de changer les HP (avec condition hpmax et mort) et de gérer le tag pour l'affichage"""
        self.hp+=var_hp
        if self.hp>self.hp_max:
            self.hp=self.hp_max
        self.hp_tag='%'*self.hp + "~" *(self.hp_max-self.hp)
        return 0

    def hp_max_change(self,var_hp_max=0):
        self.hp_max+=var_hp_max
        self.hp_tag='%'*self.hp + "~" *(self.hp_max-self.hp)
        return 0
        

    def initPos(self, _map):
        n_row = len(_map)
        #n_col = len(_map[0])

        y_init = n_row//2
        found = False
        while found is False:
            y_init += 1
            for i,c in enumerate(_map[y_init]):
                if c == ".":
                    x_init = i
                    found = True
                    break

        self._x = x_init
        self._y = y_init
        print(f"pos init {self._x} {self._y}")

        _map[self._y][self._x] = self._symbol

    def move(self, dx, dy):
        new_x = self._x + dx
        new_y = self._y + dy

        list_items=self.game._list_items # On initialise les différents éléments à regarder, ça va être une copie dynamique donc pas de pb
        list_monster = self.game._list_monster
        map=self.game._map

        event = 0 ; 
        """ event contient l'information de ce qu'il vient de se passer :
        0 pour un déplacement simple
        1 pour une pièce d'argent récupérée
        2 pour une potion récupérée
        3 pour une attaque
        4 pour une offensive de monstre
        5 pour un changement de map
        """

        if map[new_y][new_x] == "." or map[new_y][new_x] == "x" :
            ret =True
            map[new_y][new_x] = self._symbol
            map[self._y][self._x] = self.slab_occupee
            data = [{"i": f"{self._y}", "j":f"{self._x}", "content":self.slab_occupee}, {"i": f"{new_y}", "j":f"{new_x}", "content":self._symbol}, {"content": f"{self.gold}"}, {"content": f"{self.hp_tag}"},{"content": f"{self.attack}"},{"content": f"{self.defence}"}]
            self.slab_occupee="x"
            self._x = new_x
            self._y = new_y
        elif map[new_y][new_x] == "G" :
            ret =True
            map[new_y][new_x] = self._symbol
            map[self._y][self._x] = self.slab_occupee
            self.gold += 1
            data = [{"i": f"{self._y}", "j":f"{self._x}", "content":self.slab_occupee}, {"i": f"{new_y}", "j":f"{new_x}", "content":self._symbol}, {"content": f"{self.gold}"}, {"content": f"{self.hp_tag}"},{"content": f"{self.attack}"},{"content": f"{self.defence}"}]
            self.slab_occupee="x"
            self._x = new_x
            self._y = new_y
            event = 1  
        # elif map[new_y][new_x] == "&" :
        #     ret =True
        #     map[new_y][new_x] = self._symbol
        #     map[self._y][self._x] = "x"
        #     self.hp_change(1)
        #     data = [{"i": f"{self._y}", "j":f"{self._x}", "content":"x"}, {"i": f"{new_y}", "j":f"{new_x}", "content":self._symbol}, {"content": f"{self.gold}"}, {"content": f"{self.hp_tag}"},{"content": f"{self.attack}"},{"content": f"{self.defence}"}]
        #     self._x = new_x
        #     self._y = new_y 
        elif map[new_y][new_x] == "#" :
            ret = False
            data = []
            return data,ret, event
        else:
            ret = False
            data = []
            
        if list_monster != []:
            for m in list_monster :
                if map[new_y][new_x] == map[m._y][m._x] :
                    self.assault(m)
                    event = 3
                    if m.is_alive == False :
                        ret = True
                        map[new_y][new_x] = self._symbol
                        map[self._y][self._x] = self.slab_occupee
                        data = [{"i": f"{self._y}", "j":f"{self._x}", "content":self.slab_occupee}, {"i": f"{new_y}", "j":f"{new_x}", "content":self._symbol}, {"content": f"{self.gold}"}, {"content": f"{self.hp_tag}"},{"content": f"{self.attack}"},{"content": f"{self.defence}"}]
                        self.slab_occupee="x"
                        self._x = new_x
                        self._y = new_y
                    else :
                        self.damage_in_return(m)
                        ret = True
                        event = 4
                        data = [{"i": f"{self._y}", "j":f"{self._x}", "content":self._symbol}, {"i": f"{new_y}", "j":f"{new_x}", "content":m.symbol}, {"content": f"{self.gold}"}, {"content": f"{self.hp_tag}"},{"content": f"{self.attack}"},{"content": f"{self.defence}"}]
                    break
        if list_items !=[]: # Je reprends un peu la même syntaxe que pour les mobs mais pour les items
            for i in list_items :
                if new_y == i._y and new_x == i._x:
                    if not i._holder :
                        catched = self.grab(i) 
                        if i.symbol=="L": #on sort si c'était une porte (ça fixe le bug où le personnage restait à la position de la porte) # Je pense que cette condition peut êtree remplacée par un ret=False car tout est remis à 0
                            event = 5
                            ret=True
                            data = [{"i": f"{self._y}", "j":f"{self._x}", "content":self.slab_occupee}, {"i": f"{new_y}", "j":f"{new_x}", "content":self._symbol}, {"content": f"{self.gold}"}, {"content": f"{self.hp_tag}"},{"content": f"{self.attack}"},{"content": f"{self.defence}"}]
                            self.slab_occupee="x"
                            return data, ret, event
                        if catched :
                            event = 2
                            ret = True
                            map[new_y][new_x] = self._symbol
                            map[self._y][self._x] = "x" # Il faut changer la variable data pour envoyer au html le fait qu'on doit actualiser l'inventaire de ce que j'ai compris (Thomas pour Rémy)
                            data = [{"i": f"{self._y}", "j":f"{self._x}", "content":"x"}, {"i": f"{new_y}", "j":f"{new_x}", "content":self._symbol}, {"content": f"{self.gold}"}, {"content": f"{self.hp_tag}"},{"content": f"{self.attack}"},{"content": f"{self.defence}"}]
                            self._x = new_x
                            self._y = new_y
                        else :
                            event=0
                            ret=True
                            map[new_y][new_x] = self._symbol
                            map[self._y][self._x] = self.slab_occupee
                            data = [{"i": f"{self._y}", "j":f"{self._x}", "content":self.slab_occupee}, {"i": f"{new_y}", "j":f"{new_x}", "content":self._symbol}, {"content": f"{self.gold}"}, {"content": f"{self.hp_tag}"},{"content": f"{self.attack}"},{"content": f"{self.defence}"}]
                            self.slab_occupee=i.symbol
                            self._x = new_x
                            self._y = new_y
                    break
        return data, ret, event


    def assault(self,target):
        """target : le monstre que l'on veut attaquer"""
        degat = self.attack - target.defence
        target.hp -= degat
        if target.hp <= 0:
            target.is_alive = False
        return 0

    def damage_in_return(self,monster):
        """monster : le monstre que l'on a attaqué et qui riposte"""
        degat = monster.attack - self.defence
        self.hp_change(-degat)
        return 0

    def grab(self,item):
        """"Pour attrapper un item""" # On verra plus tard pour les inventaires pleins et quand on ne veut pas attraper l'item, pour l'instant on attrape tout
        if item.symbol=="L": # Traitement spécial de la porte, qui n'est pas mise dans l'inventaire
            self.game._list_items.remove(item)
            item._holder=self
            item.do_grab_effect()
        else:
            ret = self.inventaire.add(item)
            if ret:
                self.game._list_items.remove(item)
                item._holder=self
                print(f"Item attrappé : {item}")
                print(f"Il y a {len(self.inventaire)} objets dans l'inventaire")
                item.do_grab_effect()
                return True
            else :
                print("Item non attrappé, inventaire plein")
                return False

    def use(self,num_item):
        """utilisation de l'item numéro num_item"""
        if num_item<=self.inventaire.Nslots:
            ret=self.inventaire[num_item-1].do_effect() # True si l'effet de l'item a changé qq chose
            print(f"{num_item}e item utilisé : Il y a {len(self.inventaire)} objets dans l'inventaire")
            data=[]
            ret=True
            if ret:
                data=self.data_stats()
            return data, ret
    
    def data_stats(self):
        """Pour renvoyer une donnée contenant les stats du joueur simplement"""
        data=[]
        data = [[{"content": f"{self.gold}"}, {"content": f"{self.hp_tag}"},{"content": f"{self.attack}"},{"content": f"{self.defence}"}]]
        data.append(self.inventaire.symbols())
        return data
    
    def loot(self,num_item):
        ret=False
        data=[]
        if num_item<=self.inventaire.Nslots:
            ret,item=self.inventaire.pop(num_item-1)
            
        if ret:
            map=self.game._map
            item_x=self._x
            item_y=self._y
            cpt=0
            while item_x<0 or item_x>self.game.map_width or item_y<0 or item_y>self.game.map_height or (map[item_y][item_x]!="." and map[item_y][item_x]!="x"):
                item_x=random.randint(self._x-3,self._x+4)
                item_y=random.randint(self._y-3,self._y+4)
                if cpt>1000: #au cas ou on se débrouille pour être encerclé
                    ret=False
                    break
                retpos=True
            if retpos:
                item.do_loot_effect()
                item.init_pos(self.game._map,item_x,item_y)
                item._holder=None
                self.game._list_items.append(item)
                data=[{"i": f"{item_y}", "j":f"{item_x}", "content":item.symbol}]+self.data_stats()
            return data,ret



