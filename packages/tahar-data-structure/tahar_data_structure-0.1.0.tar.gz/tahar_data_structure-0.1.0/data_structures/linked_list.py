class Node:
    def __init__(self, data):
        self.data = data  # Stocke la donnée
        self.next = None   # Pointeur vers le prochain élément (None par défaut)

class LinkedList:
    def __init__(self):
        self.head = None  # La tête de liste est vide au départ

    def insertAtBeginning(self, item):
        new_node = Node(item)   # Crée un nouveau nœud
        new_node.next = self.head  # Le nouveau pointe vers l'ancienne tête
        self.head = new_node     # Met à jour la tête

    def insertAfter(self, item, index):
        new_node = Node(item)
        current = self.head
        count = 0
        
        # Trouver la position
        while current and count < index:
            current = current.next
            count += 1
        
        if not current:
            print("Index hors limites!")
            return
        
        # Insérer après
        new_node.next = current.next
        current.next = new_node

    def insertAtEnd(self, item):
        new_node = Node(item)
        
        if not self.head:  # Si liste vide
            self.head = new_node
            return
            
        last = self.head
        while last.next:   # Trouver le dernier élément
            last = last.next
        last.next = new_node

    def deleteItem(self, item):
        current = self.head
        prev = None
        
        while current:
            if current.data == item:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return
            prev = current
            current = current.next
        
        print(f"{item} non trouvé!")

    def display(self):
        node = self.head
        while node:
            print(node.data, end=" -> ")  # Correction : node.data au lieu de node.node
            node = node.next
        print("None")

    def search(self, item):
        current = self.head
        while current:
            if current.data == item:
                return True
            current = current.next
        return False

    def get_length(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def access(self, index):
        current = self.head
        count = 0
        while current:
            if count == index:
                return current.data
            count += 1
            current = current.next
        print("Index invalide!")
        return None

    def update(self, index, new_data):
        current = self.head
        count = 0
        while current:
            if count == index:
                current.data = new_data
                return
            count += 1
            current = current.next
        print("Index invalide!")
