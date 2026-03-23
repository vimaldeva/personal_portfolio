
class Graph():
    def __init__(self):
        self.adj_list = {}

    def print_graph(self):
        for vertex in self.adj_list:
            print(vertex, ' : ', self.adj_list[vertex])

    def add_vertex(self, vertex):
        if vertex not in self.adj_list.keys():
            self.adj_list[vertex] = []
            return True
        return False
    
    def add_edge(self,v1, v2):
        if v1  in self.adj_list.keys() and v2 in self.adj_list.keys():
            self.adj_list[v1].append(v2)
            self.adj_list[v2].append(v1)
            return True
        return False
    
    def remove_edge(self, v1,v2):
        if v1 in self.adj_list.keys() and v2 in self.adj_list.keys():
            try :
                self.adj_list[v1].remove(v2)
                self.adj_list[v2].remove(v1)
            except ValueError :
                pass 
            return True
        return False
    
    def remove_vertex(self,v):
        if v in self.adj_list.keys() :
            for i in self.adj_list[v]:
                self.adj_list[i].remove(v)
            del self.adj_list[v]
            return True
        return False
    

    
a = Graph()

a.add_vertex('A')
a.add_vertex('B')
a.add_vertex('C')
a.add_vertex('D')
a.print_graph()
a.add_edge('A','B')
a.add_edge('A','C')
a.add_edge('A','D')
a.add_edge('B','D')
a.add_edge('C','D')
print("---------")
a.print_graph()
print("---------")
a.remove_vertex('B')
print("---------")

a.print_graph()
