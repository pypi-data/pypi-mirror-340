class Stack:
    def __init__(self):
        self.items = []  # Liste vide pour stocker les éléments
    
    # Ajouter un élément au sommet de la pile
    def push(self, item):
        self.items.append(item)
    
    # Retirer et renvoyer l'élément du sommet
    def pop(self):
        if self.is_empty():
            print("La pile est vide !")
            return None
        return self.items.pop()
    
    # Voir l'élément du sommet sans le retirer
    def peek(self):
        if self.is_empty():
            print("La pile est vide !")
            return None
        return self.items[-1]
    
    # Vérifier si la pile est vide
    def is_empty(self):
        return len(self.items) == 0
