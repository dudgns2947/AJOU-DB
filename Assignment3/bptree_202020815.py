import sys
import bisect
from math import floor

class Node:
    def __init__(self):
        # each node can have |order - 1| keys
        self.keys = []

        # |order| / 2 <= # of subTree pointers <= |order|
        self.isLeaf = True

        # leaf node has next node pointer
        self.child = []
        self.next = None

    def Split(self):
        newnode = Node()
        if self.isLeaf:
            newnode.isLeaf = True

            mid = int(len(self.keys) / 2)
            midKey = self.keys[mid]

            newnode.keys = self.keys[mid:]
            newnode.child = self.child[mid:]

            self.keys = self.keys[:mid]
            self.child = self.child[:mid]

            newnode.next = self.next
            self.next = newnode
        else:
            newnode.isLeaf = False
            mid = int(len(self.keys) / 2)
            midKey = self.keys[mid]

            newnode.keys = self.keys[mid+1:]
            newnode.child = self.child[mid+1:]
            
            self.keys = self.keys[:mid]
            self.child = self.child[:mid+1]

        return midKey, newnode

    def isRoot(self) -> bool:
        return self.next is None
    def isUnderflow(self) -> bool:  # Used to check on keys, not data!
        return len(self.keys) <= floor(self.order / 2) - 1

class B_PLUS_TREE:
    def __init__(self, order):
        self.order = order
        self.root = Node()
        self.root.isLeaf = True
        self.root.keys = []
        self.root.child = []
        self.root.next = None

    def search(self, key):
        current_node = self.root
        while(current_node.isLeaf == False):
            tmp = current_node.keys
            for i in range(len(tmp)-1):
                if (key == tmp[i]):
                    current_node = current_node.keys[i + 1]
                    break
                elif (key < tmp[i]):
                    current_node = current_node.keys[i]
                    break
                elif (i + 1 == len(current_node.keys)):
                    current_node = current_node.keys[i + 1]
                    break
        return current_node

    def print_tree(self):
        this_level = [self.root]
        while this_level:
            next_level = []
            output = ""
            for node in this_level:
                if node.child and node.isLeaf == False:
                    next_level.extend(node.child)
                    output += str(node.keys) + ""
            if(len(output) > 0):
                print(output)
            this_level = next_level
            output += "-"
            for node in this_level:
                    output += str(node.keys) + ","
            output = output[:-1]
            if(len(output) > 0):
                print(output)

    def print_root(self):
        l = "["
        for k in self.root.keys:
            l += "{},".format(k)
        l = l[:-1] + "]"
        print(l)

    def insert(self, key):
        key, node = self.insert_key(key, self.root)
        if key:
            new = Node()
            new.isLeaf = False
            new.keys = [key]
            new.child = [self.root, node]
            self.root = new

    def insert_key(self, key, node):
        if node.isLeaf: #Leaf노드일 경우
            idx = bisect.bisect(node.keys, key)
            node.keys[idx:idx] = [key]
            node.child[idx:idx] = [key]

            if len(node.keys) <= self.order - 1:
                return None, None
            else:
                mid, new = node.Split()
                return mid, new
        
        else: #새로 들어가야 할 key의 위치를 찾는 과정
            if key < node.keys[0]:
                new_key, new_node = self.insert_key(key, node.child[0])
                
            for i in range(len(node.keys) - 1):
                if key >= node.keys[i] and key < node.keys[i + 1]:
                    new_key, new_node = self.insert_key(key, node.child[i + 1])
            
            if key >= node.keys[-1]:
                new_key, new_node = self.insert_key(key, node.child[-1])
        
        if new_key:
            idx = bisect.bisect(node.keys, new_key)   # 들어갈 노드에 위치할 인덱스를 반환해줌
            node.keys[idx:idx] = [new_key]            # 사이에 idx를 넣음
            node.child[idx + 1:idx + 1] = [new_node]  # node는 자기자신이 포함되어야함
            if len(node.keys) <= self.order - 1:      # split할 필요 X
                return None, None
            else:
                mid, new = node.Split()            # order를 넘었으므로 split해야함
                return mid, new                    # 중간key값과, 노드를 반환함
        else:
            return None, None
            
# deletion Algorithm concept
#1) Start at the root and go up to leaf node containing the key K
#2) Find the node n on the path from the root to the leaf node containing K
#    A. If n is root, remove K
#         a. if root has more than one key, done
#         b. if root has only K
#            i) if any of its child nodes can lend a node
#               Borrow key from the child and adjust child links
#            ii) Otherwise merge the children nodes. It will be a new root
#         c. If n is an internal node, remove K
#            i) If n has at least ceil(m/2) keys, done!
#            ii) If n has less than ceil(m/2) keys,
#                If a sibling can lend a key,
#                Borrow key from the sibling and adjust keys in n and the parent node
#                    Adjust child links
#                Else
#                    Merge n with its sibling
#                    Adjust child links
#         d. If n is a leaf node, remove K
#            i) If n has at least ceil(M/2) elements, done!
#                In case the smallest key is deleted, push up the next key
#            ii) If n has less than ceil(m/2) elements
#            If the sibling can lend a key
#                Borrow key from a sibling and adjust keys in n and its parent node
#            Else
#                Merge n and its sibling
#                Adjust keys in the parent node    

    def delete(self, key):
        node = self.root

        while not isinstance(node, Node):
            node, parentIndex = self._find(node, key)
                
        if key not in node.keys:
            return False

        index = node.keys.index(key)
        
        if B_PLUS_TREE.find_node(self, key, node) == key:
            node.keys.pop(index)  # Remove the list element.
                
        if node.isRoot() and not isinstance(node,Node) and len(node.keys) == 1:
            self.root = node.keys[0]
                

    @staticmethod
    def _find(self, key):
        for i, item in enumerate(self.keys):
            if key < item:
                return self.values[i], i
            elif i + 1 == len(self.keys):
                return self.values[i + 1], i + 1  

    def find_node(self, key, node):
        if node.isLeaf:
            return key

        else:
            if key <= node.keys[0]:
                return self.find_node(key, node.child[0])
            
            for i in range(len(node.keys) - 1):
                if key > node.keys[i] and key < node.keys[i + 1]:
                    return self.find_node(key, node.child[i])
                if key == node.keys[i + 1]:
                    return self.find_node(key, node.child[i + 1])

            if key > node.keys[-1]:
                return self.find_node(key, node.child[-1])

    def find(self, key):
        k = self.find_node(key, self.root)

        this_level = [self.root]
        while this_level:
            next_level = []
            output = ""
            for node in this_level:
                if node.child and node.isLeaf == False:
                    next_level.extend(node.child)
                    output += str(node.keys) + ""
            if(len(output) > 0):
                print(output)
            this_level = next_level
            output += "-"
            for node in this_level:
                if k in node.keys:
                    output += str(node.keys) + ","
            output = output[:-1]
            if(len(output) > 0):
                print(output)

    def find_range(self, k_from, k_to):
        this_level = [self.root]
        while this_level:
            next_level = []
            output = ""
            for node in this_level:
                if node.child and node.isLeaf == False:
                    next_level.extend(node.child)
            this_level = next_level
            for node in this_level:
                for i in range(len(node.keys)):
                    if int(node.keys[i]) >= k_from and int(node.keys[i]) <= k_to:
                        output += str(node.keys[i]) + ","
            output = output[:-1]
            if(len(output) > 0):
                print(output)




def main():
    myTree = None
    
    while (True):
        comm = sys.stdin.readline()
        comm = comm.replace("\n", "")
        params = comm.split()
        if len(params) < 1:
            continue
        
        print(comm)
        
        if params[0] == "INIT":
            order = int(params[1])
            myTree = B_PLUS_TREE(order)
            
        elif params[0] == "EXIT":
            return
            
        elif params[0] == "INSERT":
            k = int(params[1])
            myTree.insert(k)
            
        elif params[0] == "DELETE":
            k = int(params[1])
            myTree.delete(k)            
            
        elif params[0] == "ROOT":            
            myTree.print_root()            
            
        elif params[0] == "PRINT":            
            myTree.print_tree()            
                  
        elif params[0] == "FIND":            
            k = int(params[1])
            myTree.find(k)
            
        elif params[0] == "RANGE":            
            k_from = int(params[1])
            k_to = int(params[2])
            myTree.find_range(k_from, k_to)
        
        elif params[0] == "SEP":
            print("-------------------------")
    
if __name__ == "__main__":
    main()

