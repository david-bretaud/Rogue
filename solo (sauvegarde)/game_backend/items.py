

class Item:
    def __init__(self,symbol="A",x=None,y=None):
        self.symbol=symbol
        self.description=None
        self._x=x
        self._y=y
        self._holder=None

    def __str__(self):
        return "Item snas code pour print"

    def init_pos(self,_map,x=None,y=None,forced_mode=False): # force_mode spécifie si on veut écraser les coordonées existantes au cas ou il y en ait
        if True: # (not self.is_placed()) or forced_mode: # si l'objet n'a pas dja une position ou que l'on force à prendre la nouvelle position
            self._x=x # on change les coordonées
            self._y=y
        if not self.is_placed():
            self._x=0 # on met des coordonées 0,0 signe qu'il y a eu un pronleme sur l'init_pos
            self._y=0
        _map[self._y][self._x] = self.symbol

    
    def is_placed(self):
        return bool(self._x and self._y) # Si les deux sont déja définis c'est qu'on a déja fixé la position de l'objet

    def do_effect(self):
        """On définit la fonction à ce niveau pour qu'elle existe toujours, cependant on va la redéfinir pour chaque type d'item"""
        print("Pas d'effect")
        return False

    def do_grab_effect(self):
        """Effet qui s'effectue lorsqu'on arrappe l'objet (ce sera utile pour les armes/armures entre autres)"""
        print("Pas de grab_effect")
        return None
    
    def do_loot_effect(self):
        """Effet qui s'effectue lorsqu'on lache l'objet (ce sera utile pour les armes/armures entre autres)"""
        print("Pas de loot_effect")
        return None


class Potion(Item):
    def __init__(self,x_init=None,y_init=None,hp_effect=4,hp_max_effect=0,attack_effect=0,defence_effect=0,xp_effect=0,symbol="&"):
        super().__init__(symbol,x=x_init,y=y_init)
        self.hp_effect=hp_effect
        self.hp_max_effect=hp_max_effect
        self.attack_effect=attack_effect
        self.defence_effect=defence_effect
        self.xp_effect=xp_effect

    def __str__(self): # Permet de dire ce qu'on veut afficher si on fait print(Potion)
        return f"Potion hp {self.hp_effect} / hp_max {self.hp_max_effect} / att {self.attack_effect} / def {self.defence_effect}"
    
    def do_effect(self):
        self._holder.hp_change(self.hp_effect)
        self._holder.defence += self.defence_effect
        self._holder.attack += self.attack_effect
        self._holder.hp_max_change(self.hp_max_effect)
        self._holder.inventaire.remove(self) # la potion dispatait
        return True


class Equipement(Item): # Armes de poing et armures : changent les capacités du joueur tant que portées/possédées
    def __init__(self,x_init=None,y_init=None,attack_effect=1,defence_effect=0,symbol="!"):
        super().__init__(symbol,x=x_init,y=y_init)
        self.attack_effect=attack_effect
        self.defence_effect=defence_effect

    def do_grab_effect(self):
        self._holder.attack += self.attack_effect
        self._holder.defence += self.defence_effect

    def do_loot_effect(self):
        self._holder.attack -= self.attack_effect
        self._holder.defence -= self.defence_effect

class NextLevelDoor(Item):
    def __init__(self,x_init=None,y_init=None):
        super().__init__(symbol="L",x=x_init,y=y_init)

    def __str__(self):
        return "Porte pour régénérer la map"
    
    def do_grab_effect(self):
        print("Changement de monde")
        self._holder.game.new_level()
        
class NoneItem(Item):
    def __init__(self):
        super().__init__("°")
    
    def __str__(self):
        return "NoneItem"
    