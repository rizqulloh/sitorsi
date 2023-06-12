class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, data, identifier):
        new_node = Node(data)
        if self.root is None:
            self.root = new_node
            return True
        
        temp = self.root
        while True:
            if new_node.data[identifier] == temp.data[identifier]:
                return False
            
            if new_node.data[identifier] < temp.data[identifier]:
                if temp.left is None:
                    temp.left = new_node
                    return True
                temp = temp.left
            else:
                if temp.right is None:
                    temp.right = new_node
                    return True
                temp = temp.right

    def contains(self, value, identifier):
        temp = self.root
        while temp is not None:
            if value < temp.data[identifier]:
                temp = temp.left
            elif value > temp.data[identifier]:
                temp = temp.right
            else:
                return True
        
        return False
    
    def get(self, value, identifier):
        if self.root is None:
            return None
        return self.get_rec(value, self.root, identifier)

    def get_rec(self, value, current_node, identifier):
        if current_node is None:
            return None

        if value == current_node.data[identifier]:
            return current_node

        if value < current_node.data[identifier]:
            return self.get_rec(value, current_node.left, identifier)
        else:
            return self.get_rec(value, current_node.right, identifier)

    def fetch(self):
        if self.root is None:
            return []
        return self.fetch_rec(self.root)
    
    def fetch_rec(self, current_node: Node):
        result = []
        if current_node.left:
            result += self.fetch_rec(current_node.left)
        
        result.append(current_node.data)
        if current_node.right:
            result += self.fetch_rec(current_node.right)

        return result
    
    def blind_search(self, value, identifier):
        if self.root is None:
            return False
        return self.blind_search_rec(value, self.root, identifier)

    def blind_search_rec(self, value, current_node: Node, identifier):
        if current_node is None:
            return False
        if value == current_node.data[identifier]:
            return True
        if value < current_node.data[identifier]:
            return self.blind_search_rec(value, current_node.left, identifier)
        
        return self.blind_search_rec(value, current_node.right, identifier)
    
    def update(self, value, identifier, new_data):
        if self.root is None:
            return False
        return self.update_rec(value, self.root, identifier, new_data)

    def update_rec(self, value, current_node, identifier, new_data):
        if current_node is None:
            return False

        if value == current_node.data[identifier]:
            current_node.data = new_data
            return True

        if value < current_node.data[identifier]:
            return self.update_rec(value, current_node.left, identifier, new_data)
        else:
            return self.update_rec(value, current_node.right, identifier, new_data)
    
    def reconstruct(self, index, identifier):
        if self.root is None:
            return
        self.root = self.reconstruct_rec(index, self.root, identifier)

    def reconstruct_rec(self, index, current_node: Node, identifier):
        if current_node is None:
            return current_node
        
        if index < current_node.data[identifier]:
            current_node.left = self.reconstruct_rec(index, current_node.left, identifier)
        elif index > current_node.data[identifier]:
            current_node.right = self.reconstruct_rec(index, current_node.right, identifier)
        else:
            if current_node.left is None:
                return current_node.right
            elif current_node.right is None:
                return current_node.left
            
            temp = self.min(current_node.right)
            current_node.data = temp.data
            current_node.right = self.reconstruct_rec(temp.data[identifier], current_node.right, identifier)
        return current_node

    def min(self, current_node: Node):
        while current_node.left:
            current_node = current_node.left
        return current_node
    
