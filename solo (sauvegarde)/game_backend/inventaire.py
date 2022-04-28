from .items import NoneItem

class Inventaire:
    def __init__(self,slots=8):
        self.Nslots=slots
        self.list=[NoneItem() for i in range(self.Nslots)]
    
    def __str__(self):
        return str(self.list)
    
    def add(self,item):
        for i in range(self.Nslots):
            if self.list[i].symbol=='°': # Moyen de trouver un NoneItem
                self.list[i]=item
                return True
        return False
    
    def remove(self,item):
        """enlève en selectionnant par l'item"""
        for i in range(self.Nslots):
            if self.list[i]==item: # le == se fait sur l'id de l'item (la methode == n'étant pas définie entre les items)
                self.list[i]=NoneItem()
                return True
        return False
    
    def pop(self,i):
        """Enleve l'item i et le renvoie"""
        if self.list[i].symbol=='°':
            return False,NoneItem()
        else :
            item=self.list[i]
            self.list[i]=NoneItem()
            return True,item

    def symbols(self):
        symbol_list=[]
        for i in range(self.Nslots):
            symbol_list.append(self.list[i].symbol)
        return symbol_list

    def __len__(self):
        S=0
        for i in range(self.Nslots):
            if self.list[i].symbol!='°':
                S+=1
        return S
    
    def __getitem__(self,i): # pour avoir un comportement de liste
        return self.list[i]