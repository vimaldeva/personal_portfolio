
class MaxHeap():
    def __init__(self):
        self.heap = []
    
    def _left_child(self,index):
        return 2*index + 1
    
    def _right_child(self,index):
        return 2*index + 2
    
    def _parent(self,index):
        return (index-1)//2
    
    def _swap(self, index1, index2):
        self.heap[index1], self.heap[index2] = self.heap[index2], self.heap[index1]

    def insert(self,value):
        self.heap.append(value)
        current = len(self.heap) -1

        while current > 0 and self.heap[current] > self.heap[self._parent(current)]:
            self._swap(current , self._parent(current))
            current = self._parent(current)

a= MaxHeap()
a.insert(99)
a.insert(72)
a.insert(61)
a.insert(58)

print(a.heap)

a.insert(110)
print('---------')
print(a.heap)


