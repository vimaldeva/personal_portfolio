class Node():
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList():
    def __init__(self, value):
        new_node = Node(value)
        self.head = new_node
        self.tail = new_node
        self.length = 1

    def print_list(self):
        if self.head == None :
            print("Empty List")
        else :
            current_node = self.head
            while current_node.next != None :
                print(current_node.value)
                current_node = current_node.next   
            print(current_node.value)         

    
    def append(self,value):
        new_node = Node(value)
        if self.head == None:
            self.head = new_node
            self.tail = new_node
        else :
            current_node = self.head
            while current_node.next != None :
                current_node = current_node.next
                
            self.tail = new_node
            current_node.next = new_node

a = LinkedList(2)
a.append(4)
a.append(10)
a.append(20)

# print(a.head.value)
a.print_list()
