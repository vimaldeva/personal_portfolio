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
    
    def find_kth_node(self, k):
        if k <= 0 or self.head is None:
            return None

        slow = self.head
        fast = self.head

        # Move fast pointer k steps ahead
        for _ in range(k):
            if fast is None:       # k > length
                return None
            fast = fast.next

        # Move both until fast reaches end
        while fast is not None:
            slow = slow.next
            fast = fast.next

        return slow


        
        
a = LinkedList(10)

a.append(20)
a.append(30)
a.append(40)
a.append(50)
a.append(60)
a.append(70)
a.append(80)

print(a.find_kth_node(3).value)