class Node():
    def __init__(self,value):
        self.value = value
        self.next = None
    
class Queue():
    def __init__(self, value):
        new_node = Node(value)
        self.first = new_node
        self.last = new_node
        self.length = 1
    
    def print_queue(self):
        temp = self.first

        while temp is not None :
            print(temp.value)
            temp = temp.next
        
    def enqueue(self, value):
        new_node = Node(value)
        if self.first is None :
            self.first = new_node
            self.last = new_node
        
        else :
            self.last.next = new_node
            self.last = new_node
        self.length += 1

    def dequeue(self) :
        if self.first is None :
            return None
        
        dq_node = self.first
        if self.length == 1 :
            self.first = None
            self.last = None
        else :
            self.first = self.first.next
            dq_node.next = None

        return dq_node





a = Queue(5)
a.enqueue(10)
a.enqueue(20)
a.enqueue(30)
a.enqueue(40)

a.print_queue()

print('--------')
print(a.dequeue().value)
print('-------')
a.print_queue()
