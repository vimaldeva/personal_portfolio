class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        

class LinkedList:
    def __init__(self, value):
        new_node = Node(value)
        self.head = new_node
        self.tail = new_node

        
    def append(self, value):
        new_node = Node(value)
        if self.head == None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        return True
    
    def has_loop(self):
        slow_node = self.head
        fast_node = self.head

        while fast_node != None and fast_node.next != None:

            slow_node = slow_node.next
            fast_node = fast_node.next.next
            if slow_node == fast_node :
                return True

        return False

        
a = LinkedList(10)

a.append(20)
a.append(30)
a.append(40)
a.append(50)
a.append(60)
a.append(70)
a.append(80)

a.has_loop()
