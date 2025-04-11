class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []  # Liste des enfants

class Tree:
    def __init__(self, root_value):
        self.root = TreeNode(root_value)  # Racine de l'arbre
    
    def add_child(self, parent_node, child_value):
        """Ajoute un enfant à un nœud parent."""
        child_node = TreeNode(child_value)
        parent_node.children.append(child_node)
        return child_node
    
    def pre_order(self, node=None, result=None):
        """Parcours pré-ordre (racine -> enfants)."""
        if result is None:
            result = []
        if node is None:
            node = self.root
        
        result.append(node.value)
        for child in node.children:
            self.pre_order(child, result)
        return result

