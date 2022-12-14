import sys
import math

#복잡한 동작은 전부 Node class에 몰아넣자
class Node:
    def __init__(self, order):
        # each node can have |order - 1| keys
        self.keys = []
        
        # |order| / 2 <= # of subTree pointers <= |order|
        self.subTrees = []
        
        self.parent = None
        self.isLeaf = False
        
        # leaf node has next node pointer
        self.nextKey = None 
        self.prevNode = None  
        self.values = []

        #Set order level
        self.order = order
    

    # Insert at the leaf
    def insert_at_leaf(self, leaf, key):
        if (self.values):
            temp1 = self.values
            for i in range(len(temp1)):
                if (key == temp1[i]):
                    self.keys[i].append(key)
                    break
                elif (key < temp1[i]):
                    self.values = self.values[:i] + [key] + self.values[i:]
                    self.keys = self.keys[:i] + [[key]] + self.keys[i:]
                    break
                elif (i + 1 == len(temp1)):
                    self.values.append(key)
                    self.keys.append([key])
                    break
        else:
            self.values = [key]
            self.keys = [[key]]

    def split(self):                        # 자식 node들의 개수가 order보다 많아지게되면 split을 해줘야 한다
        left_child = Node(self.order)
        right_child = Node(self.order)
        middle = self.order // 2

        left_child.keys = self.keys[:middle]
        left_child.values = self.values[:middle]
        right_child.keys = self.keys[middle:]
        right_child.values = self.values[middle:]

        right_child.nextNode = self.nextNode
        left_child.nextNode = right_child
        right_child.prevNode = left_child
        left_child.prevNode = self.prevNode

        if self.prevNode != None:
            self.prevNode.nextNode = left_child
        self.keys = [right_child.keys[0]]
        self.values = [left_child, right_child]
        self.isLeaf = False

    def merge(self):                      # 노드를 삭제 한 후 자식의 개수가 order/2 보다 적을때 merge 해줘야 함 
        if self.prevNode != None:
            left_child = self.prevNode
            left_child.nextNode = self.nextNode
            if self.nextNode != None:
                self.nextNode.prevNode = left_child        

    def isfull(self):
        return len(self.keys) == self.order

    def isEmpty(self):
        return len(self.keys) == 0


class B_PLUS_TREE:
    def __init__(self, order):
        self.order = order
        self.root  = Node(order)
        self.parent = None     
        self.root.isLeaf = True

    def search(self, value):
        current_node = self.root
        while(current_node.isLeaf == False):
            temp2 = current_node.values
            for i in range(len(temp2)-1):
                if (value == temp2[i]):
                    current_node = current_node.keys[i + 1]
                    break
                elif (value < temp2[i]):
                    current_node = current_node.keys[i]
                    break
                elif (i + 1 == len(current_node.values)):
                    current_node = current_node.keys[i + 1]
                    break
        return current_node

     # Inserting at the parent
    def insert_in_parent(self, n, value, ndash):
        if (self.root == n):
            rootNode = Node(n.order)
            rootNode.values = [value]
            rootNode.keys = [n, ndash]
            self.root = rootNode
            n.parent = rootNode
            ndash.parent = rootNode
            return

        parentNode = n.parent
        temp3 = parentNode.keys
        for i in range(len(temp3)):
            if (temp3[i] == n):
                parentNode.values = parentNode.values[:i] + \
                    [value] + parentNode.values[i:]
                parentNode.keys = parentNode.keys[:i + 1] + [ndash] + parentNode.keys[i + 1:]
                if (len(parentNode.keys) > parentNode.order):
                    parentdash = Node(parentNode.order)
                    parentdash.parent = parentNode.parent
                    mid = int(math.ceil(parentNode.order / 2)) - 1
                    parentdash.values = parentNode.values[mid + 1:]
                    parentdash.keys = parentNode.keys[mid + 1:]
                    value_ = parentNode.values[mid]
                    if (mid == 0):
                        parentNode.values = parentNode.values[:mid + 1]
                    else:
                        parentNode.values = parentNode.values[:mid]
                    parentNode.keys = parentNode.keys[:mid + 1]
                    for j in parentNode.keys:
                        j.parent = parentNode
                    for j in parentdash.keys:
                        j.parent = parentdash
                    self.insert_in_parent(parentNode, value_, parentdash)       

    def find(self, key):
        l = self.search(key)
        for i, item in enumerate(l.values):
            if item == key:
                if key in l.keys[i]:
                    print(l.keys[i])
                else:
                    return False
        return False

    # Delete an entry
    def deleteEntry(self, node_, value, key):

        if not node_.isLeaf:
            for i, item in enumerate(node_.keys):
                if item == key:
                    node_.keys.pop(i)
                    break
            for i, item in enumerate(node_.values):
                if item == value:
                    node_.values.pop(i)
                    break

        if self.root == node_ and len(node_.keys) == 1:
            self.root = node_.keys[0]
            node_.keys[0].parent = None
            del node_
            return
        elif (len(node_.keys) < int(math.ceil(node_.order / 2)) and node_.isLeaf == False) or (len(node_.values) < int(math.ceil((node_.order - 1) / 2)) and node_.isLeaf == True):

            is_predecessor = 0
            parentNode = node_.parent
            PrevNode = -1
            NextNode = -1
            PrevK = -1
            PostK = -1
            for i, item in enumerate(parentNode.keys):

                if item == node_:
                    if i > 0:
                        PrevNode = parentNode.keys[i - 1]
                        PrevK = parentNode.values[i - 1]

                    if i < len(parentNode.keys) - 1:
                        NextNode = parentNode.keys[i + 1]
                        PostK = parentNode.values[i]

            if PrevNode == -1:
                ndash = NextNode
                value_ = PostK
            elif NextNode == -1:
                is_predecessor = 1
                ndash = PrevNode
                value_ = PrevK
            else:
                if len(node_.values) + len(NextNode.values) < node_.order:
                    ndash = NextNode
                    value_ = PostK
                else:
                    is_predecessor = 1
                    ndash = PrevNode
                    value_ = PrevK

            if len(node_.values) + len(ndash.values) < node_.order:
                if is_predecessor == 0:
                    node_, ndash = ndash, node_
                ndash.keys += node_.keys
                if not node_.isLeaf:
                    ndash.values.append(value_)
                else:
                    ndash.nextKey = node_.nextKey
                ndash.values += node_.values

                if not ndash.isLeaf:
                    for j in ndash.keys:
                        j.parent = ndash

                self.deleteEntry(node_.parent, value_, node_)
                del node_
            else:
                if is_predecessor == 1:
                    if not node_.isLeaf:
                        ndashpm = ndash.keys.pop(-1)
                        ndashkm_1 = ndash.values.pop(-1)
                        node_.keys = [ndashpm] + node_.keys
                        node_.values = [value_] + node_.values
                        parentNode = node_.parent
                        for i, item in enumerate(parentNode.values):
                            if item == value_:
                                p.values[i] = ndashkm_1
                                break
                    else:
                        ndashpm = ndash.keys.pop(-1)
                        ndashkm = ndash.values.pop(-1)
                        node_.keys = [ndashpm] + node_.keys
                        node_.values = [ndashkm] + node_.values
                        parentNode = node_.parent
                        for i, item in enumerate(p.values):
                            if item == value_:
                                parentNode.values[i] = ndashkm
                                break
                else:
                    if not node_.isLeaf:
                        ndashp0 = ndash.keys.pop(0)
                        ndashk0 = ndash.values.pop(0)
                        node_.keys = node_.keys + [ndashp0]
                        node_.values = node_.values + [value_]
                        parentNode = node_.parent
                        for i, item in enumerate(parentNode.values):
                            if item == value_:
                                parentNode.values[i] = ndashk0
                                break
                    else:
                        ndashp0 = ndash.keys.pop(0)
                        ndashk0 = ndash.values.pop(0)
                        node_.keys = node_.keys + [ndashp0]
                        node_.values = node_.values + [ndashk0]
                        parentNode = node_.parent
                        for i, item in enumerate(parentNode.values):
                            if item == value_:
                                parentNode.values[i] = ndash.values[0]
                                break

                if not ndash.isLeaf:
                    for j in ndash.keys:
                        j.parent = ndash
                if not node_.isLeaf:
                    for j in node_.keys:
                        j.parent = node_
                if not parentNode.isLeaf:
                    for j in parentNode.keys:
                        j.parent = parentNode
                        
    # insert의 과정
    # 1. 들어갈 위치를 찾기 위해 node들을 탐색한다
    # 2. 만약 childe node의 개수가 order보다 크다면 split 한다
    # 3. split한 right 노드의 첫번째 key는 parent에 저장한다.
    def insert(self, key):
        old_node = self.search(key)
        old_node.insert_at_leaf(old_node, key)

        if (len(old_node.values) == old_node.order):
            node1 = Node(old_node.order)
            node1.isLeaf = True
            node1.parent = old_node.parent
            mid = self.order // 2
            node1.values = old_node.values[mid+1:]
            node1.keys = old_node.keys[mid+1:]
            node1.nextKey = old_node.nextKey
            old_node.values = old_node.values[:mid+1]
            old_node.keys = old_node.keys[:mid+1]
            old_node.nextKey = node1
            self.insert_in_parent(old_node, node1.values[0], node1)

    #반복문으로 leaf의 위치를 찾는다
    #그 key를 삭제하고, order가 절반보다 작을시 merge해야한다.
    def delete(self, key):
        node_ = self.search(key)

        temp = 0
        for i, item in enumerate(node_.values):
            if item == key:
                temp = 1

                if key in node_.keys[i]:
                    if len(node_.keys[i]) > 1:
                        node_.keys[i].pop(node_.keys[i].index(key))
                    elif node_ == self.root:
                        node_.values.pop(i)
                        node_.keys.pop(i)
                    else:
                        node_.keys[i].pop(node_.keys[i].index(key))
                        del node_.keys[i]
                        node_.values.pop(node_.values.index(key))
                        self.deleteEntry(node_, key, key)
                else:
                    return
        if temp == 0:
            return
    
    def print_root(self):
        l = "["
        for k in self.root.keys:
            l += "{},".format(k)
        l = l[:-1] + "]"
        print(l)
    
    def print_tree(self):
        lst = [self.root]
        level = [0]
        leaf = None
        flag = 0
        lev_leaf = 0

        node1 = Node(str(level[0]) + str(self.root.values))

        while (len(lst) != 0):
            x = lst.pop(0)
            lev = level.pop(0)
            if (x.isLeaf == False):
                for i, item in enumerate(x.keys):
                    print(item.values)
            else:
                for i, item in enumerate(x.keys):
                    print(item.values)
                if (flag == 0):
                    lev_leaf = lev
                    leaf = x
                    flag = 1

        
    def find_range(self, k_from, k_to):
        child = self.root
        result = {}
        
        while child.isLeaf == False:
            child, index = self.search_key(child, k_from)
        if k_from not in child.keys:
            return
        
        node, i = self.find_pivot(child, k_from)
        for key, value in zip(child.keys[i:], child.values[i:]):
            if key > k_to:
                break
            else:
                result[key] = value
        keep = True
        child = child.next
        while child != None and k_to not in result.keys() and keep:
            for key, value in zip(child.keys, child.values):
                if key > k_to:
                    keep = False
                    break
                else:
                    result[key] = value
            child = child.next
        for key in result.keys():
            print(key,':',result[key])
        


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