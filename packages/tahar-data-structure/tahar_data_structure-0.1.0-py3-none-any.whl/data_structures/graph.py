class Graph:
    def __init__(self):
        self.adjacency_list = {}  # Stocke les connexions entre nœuds

    def add_node(self, node):
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []

    def add_edge(self, node1, node2):
        self.add_node(node1)
        self.add_node(node2)
        self.adjacency_list[node1].append(node2)
        self.adjacency_list[node2].append(node1)  # Graphe non orienté

    def bfs(self, start_node):
        visited = set()
        queue = [start_node]  # Utilisation d'une liste standard
        result = []
        
        while queue:
            current = queue.pop(0)  # Moins efficace que deque.popleft() pour les grandes listes
            if current not in visited:
                visited.add(current)
                result.append(current)
                queue.extend([n for n in self.adjacency_list[current] if n not in visited])
        return result

