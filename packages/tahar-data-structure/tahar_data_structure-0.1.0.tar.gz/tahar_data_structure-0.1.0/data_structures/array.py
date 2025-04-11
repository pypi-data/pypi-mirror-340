class Array:
    def __init__(self, taille):
# taille du tableau
      self.taille = taille
      self.item = []

    # Ajouter un élément au sommet de la pile
    def push(self, item):
        self.item.append(item)

    def get(self,index):
        if 0<= index<self.taille:
            return self.item[index]
        else:
            print("Error")
            return []
# modifier la valeur a un indice precis
    def set(self,index, valeur):
        print(self.item)
        if 0<= index <self.taille:
            self.item[index]=valeur
        else:
            print("Error")
# taille du tableau
    def len(self):
        return self.taille
# trouve une valeur et renvoi l'index
    def serach(self, index, valeur):
        for i in range(self.taille):
            if self.item[i] == valeur:
                return i
        return -1
# afficher le tableau
    def __str__(self):
        return str(self.item)

