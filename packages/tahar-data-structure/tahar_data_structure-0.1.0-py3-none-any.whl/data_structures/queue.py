class Queue:
    def __init__(self):
        self.items = []  # On renomme l'attribut pour éviter le conflit
    
    def enqueue(self, item):
        """Ajouter un élément à la fin de la file"""
        self.items.append(item)
    
    def dequeue(self):
        """Retirer le premier élément de la file"""
        if self.is_empty():
            print("La file est vide !")
            return None
        return self.items.pop(0)  # FIFO : premier entré, premier sorti
    
    def peek(self):
        """Voir le premier élément sans le retirer"""
        if self.is_empty():
            return None
        return self.items[0]
    
    def rear(self):
        """Voir le dernier élément ajouté"""
        if self.is_empty():
            return None
        return self.items[-1]
    
    def is_empty(self):
        """Vérifier si la file est vide"""
        return len(self.items) == 0
    
    def display_queue(self):
        """Afficher toute la file"""
        print("Début ->", " -> ".join(map(str, self.items)), "<- Fin")
