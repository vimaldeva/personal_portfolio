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
        self.length += 1

    def prepend(self, value):

        if self.head == None :
            new_node = Node(value)
            self.head = new_node
            self.tail = new_node
            return
        else :
            new_node = Node(value)
            new_node.next = self.head
            self.head = new_node
        self.length += 1

    def pop(self):
        if self.head == None :
            return
        else :
            current_node = self.head

            if current_node.next == None :
                popped_value = current_node.value
                self.head = None
                self.tail = None
                return popped_value

            else :
                while current_node.next.next != None :
                    current_node = current_node.next

                popped_value = current_node.next.value
                current_node.next = None
                self.tail = current_node
                return popped_value
        self.length -= 1

    def pop_first(self):
        if self.head == None :
            return
        
        popped_node = self.head
        if self.head.next == None:
            self.head = None
            self.tail = None
        else :
            self.head = self.head.next
            popped_node.next = None

        self.length -= 1
        

        return popped_node
    
    def get(self, index):
        if index < 0 or index >= self.length:
            return None

        temp_node = self.head
        for i in range(index):
            temp_node = temp_node.next

        return temp_node
     
    def set(self,index,value):
        temp = self.get(index)
        if temp :
            temp.value = value
            return True
        return False


a = LinkedList(2)
a.append(5)
a.append(15)
a.append(20)
a.append(35)
a.append(50)

a.print_list()
print("---------------")
a.set(3,200)
a.print_list()
