import numpy as np
import random as rd




class monster :

    def __init__(self,monster_name,symbol,x_init,y_init,hp,attack,defence,move_frequency):
        """move_frequency : nombre de tour avant d'avancer. Ne peut pas être inferieur à 1.
            is_aggro : false si le monstre n'est pas aggressif envers le joueur, true si il va chercher à attaquer le joueur"""
        self.name = monster_name
        self.symbol = symbol
        self._x = x_init
        self._y = y_init
        self.hp = hp
        self.attack = attack
        self.defence = defence
        self.move_frequency = move_frequency
        self.compteur_move = 0
        self.is_alive = True
        self.is_aggro = False

    def init_pos(self,_map):
        _map[self._x][self._y] = self.symbol

    def move(self,map):

        self.compteur_move +=1

        if self.compteur_move%self.move_frequency == 0 :
            delta = np.random.randint(3,size=2)
            new_x = self._x + (delta[0]-1)
            new_y = self._y + (delta[1]-1)

            if map[new_y][new_x] == "." or map[new_y][new_x] == "x" :
                ret = True
                map[new_y][new_x] = self.symbol
                map[self._y][self._x] = "."
                data = [{"i": f"{self._y}", "j":f"{self._x}", "content":"."}, {"i": f"{new_y}", "j":f"{new_x}", "content":self.symbol}]
                self._x = new_x
                self._y = new_y
            elif map[new_y][new_x] == "G" :
                ret = True
                map[new_y][new_x] = self.symbol
                map[self._y][self._x] = "x"
                data = [{"i": f"{self._y}", "j":f"{self._x}", "content":"."}, {"i": f"{new_y}", "j":f"{new_x}", "content":self.symbol}]
                self._x = new_x
                self._y = new_y  
            elif map[new_y][new_x] == "&" :
                ret = True
                map[new_y][new_x] = self.symbol
                map[self._y][self._x] = "x"
                data = [{"i": f"{self._y}", "j":f"{self._x}", "content":"."}, {"i": f"{new_y}", "j":f"{new_x}", "content":self.symbol}]
                self._x = new_x
                self._y = new_y 
            elif map[new_y][new_x] == "#" :
                ret = False
                data = []
                return data,ret
            return data,ret
        else :
            ret = False
            data = []
            return data,ret

        


    



class bat(monster):

    def __init__(self,x_init,y_init):

        super().__init__("bat",'w',x_init,y_init,5,1,1,2)

    

    
    # def move(self,player_x, player_y,map):
    #     """ la fonction détermine dans quelle direction le monstre se déplace pour aggresser le joueur, et le fait bouger"""
    #     if abs(self._x - player_x) >= abs(self._y - player_y) :
    #         if self._x < player_x:
    #             new_x = self._x + 1
    #             new_y = self._y
    #         else:
    #             new_x = self._x - 1
    #             new_y = self._y
    #     else:
    #         if self._y < player_y:
    #             new_y = self._y + 1
    #             new_x = self._x
    #         else:
    #             new_y = self._y - 1
    #             new_x = self._x
        
    #     if map[new_y][new_x] == "." or map[new_y][new_x] == "x" :
    #         ret =True
    #         map[new_y][new_x] = self.symbol
    #         map[self._y][self._x] = "."
    #         data = [{"i": f"{new_y}", "j":f"{new_x}", "content":self.symbol},{"i": f"{self._y}", "j":f"{self._x}", "content":"."}]
    #         self._x = new_x
    #         self._y = new_y
    #     else:
    #         ret = False
    #         data = []
        
    #     return data, ret
    
    # def aggro_test(self,player_x,player_y):
    #     """ test pour savoir si l'ennemi est aggressif : moins de 5 unités de distance entre le joueur et lui , et il est aggressif"""
    #     if (self._x - player_x)**2 + (self._y - player_y)**2 < 30 :
    #         self.is_aggro = True
    #         return True
    #     else:
    #         return False

        
        
            
    





class gobelin(monster):

    def __ini_(self,x_init,y_init):

        super().__init__("gobelin",'e',5,2,1,1)
    

