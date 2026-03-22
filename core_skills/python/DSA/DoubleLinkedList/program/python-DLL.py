class Node():
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

class DoubleLinkedList():
    def __init__(self,value):
        new_node = Node(value)
        self.head = new_node
        self.tail = new_node
        self.length = 1

    def append(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.length += 1

    def print_list(self) :
        if self.head == None :
            return None
        else :
            temp = self.head
            while temp != None :
                print(temp.value)
                temp = temp.next

    def pop(self):
        if self.head is None:
            return None
        popped_node = self.tail

        if self.length == 1:
            self.head = None
            self.tail = None

        else:
            self.tail = self.tail.prev
            self.tail.next = None

        popped_node.prev = None
        popped_node.next = None
        self.length -= 1
        return popped_node
    
    def prepend(self,value):

        new_node = Node(value)
        if self.head == None :
            self.head = new_node
            self.tail = new_node
        else :

            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.length += 1

    def pop_first(self):
        if self.head == None :
            return None
        elif self.length == 1 :
            popped_node = self.head
            self.head = None
            self.tail = None
        else :
            popped_node = self.head
            self.head = self.head.next
            self.head.prev = None
            popped_node.next = None

        self.length -= 1
        return popped_node
    
    def get(self, index):
        if index <0 or index >= self.length :
            return None
        else :
            temp = self.head
            for _ in range(index):
                temp = temp.next

        return temp
    
    def set(self, index, value) :
        if index <0 or index >= self.length :
            return False
        else :
            temp = self.head
            for _ in range(index):
                temp = temp.next

            temp.value = value
            return True
        
    def insert(self, index,value):
        if index <0 or index > self.length :
            return False
        elif index == 0 :
            self.prepend(value)
            return True
        elif index == self.length :
            self.append(value)
            return True
        else :
            new_node = Node(value)

            prev_node = self.get(index-1)
            next_node = prev_node.next
            new_node.next = next_node
            new_node.prev = prev_node
            next_node.prev = new_node
            prev_node.next = new_node

            self.length += 1
            return True 
        
    def remove(self,index):
        if index <0 or index >= self.length :
            return False        
        elif index == 0 :
            popped_node = self.pop_first()
        elif index == self.length-1 :
            popped_node = self.pop()
        else :

            popped_node = self.get(index)

            prev_node  = popped_node.prev
            next_node = popped_node.next

            next_node.prev = prev_node
            prev_node.next = next_node

            popped_node.next = None
            popped_node.prev = None 

            self.length -= 1
        return popped_node





a = DoubleLinkedList(5)
a.append(20)
a.append(30)
a.append(40)
a.append(50)
a.print_list()
print('-----')
# print(a.pop_first().value)
print(a.remove(3).value)
print('-----')
a.print_list()
